import logging
from pathlib import Path
from typing import Union

import yaml


logger = logging.getLogger(__name__)


CURRENT_FILE = Path(__file__).parent
MODIFICATIONS_FILE = CURRENT_FILE / 'modifications.yaml'
REFERENCES_FILE = CURRENT_FILE / 'data' / 'references.yaml'
ACTIONS_FILE = CURRENT_FILE / 'data' / 'actions.yaml'
ATTRIBUTES_FILE = CURRENT_FILE / 'data' / 'attributes.yaml'

REFERENCES = yaml.safe_load(REFERENCES_FILE.read_text())
ACTIONS = yaml.safe_load(ACTIONS_FILE.read_text())
ATTRIBUTES = yaml.safe_load(ATTRIBUTES_FILE.read_text())

modifications_data = {
    'references': REFERENCES,
    'actions': ACTIONS,
    'attributes': ATTRIBUTES,
}


def validate_modification(reference: str, attribute: str, action: str, value: Union[str, list[Union[str, int]]]) \
        -> bool:
    """
    Check modification consistency.
    """
    is_valid = True

    if reference not in REFERENCES:
        logger.warning(
            f'Reference "{reference}" is unknown. Please check the modifications are correct.\n'
            f'Possible values can be found in "src/modifications/data/references.yaml".'
        )
        is_valid = False

    if attribute not in ATTRIBUTES:
        logger.warning(
            f'Attribute "{attribute}" is unknown. Please check the modifications are correct.\n'
            f'Possible values can be found in "src/modifications/data/attribute.yaml".'
        )
        is_valid = False

    if action not in ACTIONS:
        logger.warning(
            f'Action "{action}" is unknown. Please check the modifications are correct.\n'
            f'Possible values can be found in "src/modifications/data/attributes.yaml".'
        )
        is_valid = False

    if attribute in ['set list', 'concatenate list'] and not isinstance(value, list):
        logger.warning(
            f'The value associated with the attribute "{attribute}" must be a list when the chosen action is '
            f'"{action}".'
        )
        is_valid = False

    if attribute in ['append scalar', 'set scalar'] and isinstance(value, list) or isinstance(value, dict):
        logger.warning(
            f'The value associated with the attribute "{attribute}" must be a scalar when the chosen action is '
            f'"{action}".'
        )
        is_valid = False

    return is_valid
