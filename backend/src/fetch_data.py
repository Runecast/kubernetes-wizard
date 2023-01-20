import json
import logging
from pathlib import Path
from typing import Any, Union

import yaml

from config.k8s import cfg
from src.modifications.validation import validate_modification

from src.utils.cache import timed_lru_cache


logger = logging.getLogger(__name__)

CURRENT_FILE = Path(__file__).parent


def modify_dictionary_value(*, data: dict[str, Any], keys_list: list[str], value: str, **_kwargs) \
        -> Union[dict[str, Any], str]:
    """
    Set a scalar value in the dataset.

    :param data: Initial dataset from JSON.
    :param keys_list: List of successive keys to find the value to modify.
    :param value: New scalar value that must be set.
    :return: Modified dataset.
    """
    if keys_list:
        if keys_list[0] not in data:
            data[keys_list[0]] = ''

        data[keys_list[0]] = modify_dictionary_value(
            data=data[keys_list[0]], keys_list=keys_list[1:], value=value
        )
        return data
    else:
        return value


def set_dictionary_json(*, data: dict[str, Any], keys_list: list[str], value: str, **_kwargs) \
        -> Union[dict[str, Any], list[str], str]:
    """
    Set a structured value (list, hash map) in the dataset.

    :param data: Initial dataset from JSON.
    :param keys_list: List of successive keys to find the value to modify.
    :param value: New JSON value that must be set.
    :return: Modified dataset.
    """
    if keys_list and keys_list[0] in data.keys():
        data[keys_list[0]] = set_dictionary_json(
            data=data[keys_list[0]], keys_list=keys_list[1:], value=value
        )
        return data
    elif keys_list:
        data[keys_list[0]] = value
        return data
    else:
        return value


def append_scalar_to_dictionary(*, data: dict[str, Any], keys_list: list[str], value: str, **_kwargs) -> dict[str, Any]:
    """
    Add a scalar value to a list in the dataset.

    :param data: Initial dataset from JSON.
    :param keys_list: List of successive keys to find the value to modify.
    :param value: New scalar value that must be appending to the list.
    :return: Modified dataset.
    """
    if len(keys_list) > 1:
        data[keys_list[0]] = append_scalar_to_dictionary(
            data=data[keys_list[0]], keys_list=keys_list[1:], value=value
        )
        return data
    else:
        data[keys_list[0]].append(value)
        return data


def concatenate_lists(*, data: dict[str, Any], keys_list: list[str], value: str, **_kwargs) -> dict[str, Any]:
    """
    Concatenate a list to another list in the dataset.

    :param data: Initial dataset from JSON.
    :param keys_list: List of successive keys to find the value to modify.
    :param value: List of new elements that must be added to an existing list.
    :return: Modified dataset.
    """
    if len(keys_list) > 1:
        data[keys_list[0]] = concatenate_lists(
            data=data[keys_list[0]], keys_list=keys_list[1:], value=value
        )
        return data
    else:
        data[keys_list[0]] += value
        return data


def drop_value(*, data: dict[str, Any], keys_list: list[str], **_kwargs) -> dict[str, Any]:
    """
    Drop a value in the dataset.

    :param data: Initial dataset from JSON.
    :param keys_list: List of successive keys to find the value to drop.
    :return: Modified dataset.
    """
    if len(keys_list) > 1:
        data[keys_list[0]] = drop_value(
            data=data[keys_list[0]], keys_list=keys_list[1:]
        )
        return data
    else:
        del data[keys_list[0]]
        return data


def remove_item_from_list(*, data: dict[str, Any], keys_list: list[str], value: str, **_kwargs) -> \
        Union[dict[str, Any], list[str]]:
    """
    Remove an item from a list in the dataset.

    :param data: Initial dataset from JSON.
    :param keys_list: List of successive keys to find the value to modify.
    :param value: Value to remove from the list.
    :return: Modified dataset.
    """
    if keys_list and keys_list[0] in data.keys():
        data[keys_list[0]] = remove_item_from_list(
            data=data[keys_list[0]], keys_list=keys_list[1:], value=value
        )
        return data
    else:
        try:  # Try to parse as JSON to know if the value is a list
            value = value
        except json.decoder.JSONDecodeError:
            pass

        if isinstance(value, list):
            data = [item for item in data if item not in value]
        else:
            data = [item for item in data if item != value]
        return data


JSON_MODIFICATIONS = {
    cfg.action.set_scalar: modify_dictionary_value,
    cfg.action.append: append_scalar_to_dictionary,
    cfg.action.set_list: set_dictionary_json,
    cfg.action.concatenate: concatenate_lists,
    cfg.action.drop: drop_value,
    cfg.action.remove: remove_item_from_list,
}


def modify_json_with_yaml(data: dict[str, Any], modifications_df: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Modify the JSON dataset according to the modifications (extracted from the `src/modifications/modifications.yaml).

    :param data: Initial dataset from JSON.
    :param modifications_df: DataFrame containing the data of the spreadsheet describing the modifications that must be
    applied to the dataset.
    """
    for row in modifications_df:
        reference = row['reference']
        attribute = row['attribute']
        action = row['action']
        value = row['value'] if 'value' in row.keys() else None
        is_valid = validate_modification(reference, attribute, action, value)

        if is_valid:
            if isinstance(action, str):
                action = action.lower()

            if isinstance(reference, str):
                if value == 'FALSE':
                    value = False
                elif value == 'TRUE':
                    value = True

                path = reference.split('.')
                path.insert(-1, 'parameters')
                path.append(attribute)
                if action in JSON_MODIFICATIONS:
                    try:
                        data = JSON_MODIFICATIONS[action](data=data, keys_list=path, value=value)
                    except (KeyError, TypeError) as e:  # Some resources are not shared among all K8s versions
                        logger.warning(e)
                else:
                    logger.warning(f'Action "{action}" is unknown. Please check the spreadsheet is correct.')
    return data


@timed_lru_cache(seconds=cfg.api_modifications.cache_ttl)
def fetch_data(data_path: str) -> dict[str, Any]:
    """
    Fetch JSON data and modify it according to the content of the spreadsheet.

    :param data_path: Path where JSON data is located.
    :param modifications_url: URL of the spreadsheet containing the modifications that must be applied to the dataset.
    :return: Modified dataset.
    """
    with open(data_path, 'r') as k8s_data_file:
        data = json.loads(k8s_data_file.read())
        modifications_file = CURRENT_FILE / 'modifications' / 'modifications.yaml'
        data_modifications = yaml.safe_load(modifications_file.read_text())
        data = modify_json_with_yaml(data, data_modifications)
        return data
