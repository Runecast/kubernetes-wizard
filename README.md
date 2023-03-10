# K8S Wizard

---

This application helps to create Kubernetes YAML manifests by automatically generating YAML from user input.

## Usage

In the application, you can choose your Kubernetes version and select a resource.
A form is created on the left panel, and the YAML will be generated on the right panel.
All data objects are collapsed by default but can be expanded to access their parameters.

You no longer need to go back and forth reading the API reference, the form contains all the needed information, e.g.:
- Descriptions
- Default values
- Possible values
- Parameter type
- Required

When filling the form, the YAML is automatically generated.
When you're done, you can click on the "Copy" button and paste the results in your YAML manifest.

If you already have a working YAML manifest and want to modify it, you can import it in the application using the "Import" button.
This must be the first step after choosing a resource, since this button will be disabled as soon as a field of the form if filled (to avoid silently overriding your inputs).

## For developers

### Set up

The project can be run using Docker with the command (use `sudo` if not in the Docker user group on Linux):
```bash
docker-compose -f ./docker-compose-[profile].yaml up -d
```
where `[profile]` can be:
- `dev`: the front-end is deployed on port 7901 and the back-end on port 5000.
- `prod`: the front-end is built, then served by the back-end on port 80.

To stop the application, run:
```bash
docker-compose -f ./docker-compose-[profile].yaml down
```

By default, there is only 1 worker in production and the port is 80. To change this behavior, create a `.env` file at the root of the project (next to `docker-compose-prod.yaml`) with the following content:
```env
WORKERS=[n_workers]
PORT=[port]
```
with `[n_workers]` and `[port]` integers.
The port can't be 7901 or 8080 (these values is reserved for development).

If you'd rather use Python and Node.js instead of Docker Compose to run the app locally, the back-end can be started using the script with:
```bash
cd backend
pip install -r requirements.txt  # Only the first time
python run_local.py
```
and the front-end can be started in another terminal session using:
```bash
cd frontend
npm install  # Only the first time
npm run serve
```

The app can then be found on port 8080.

### Data modifications

The JSON data files are obtained via the API reference scraping, but some information can be missing (e.g. default values, options...).
Some behaviors can also be added *a posteriori*, like the fact that we want to choose only one type of volume per volume in containers.
To easily add these changes to all the data files and avoid overwriting them if the data is scraped again, these changes are stored as a set of modifications added manually.

These modifications can be found in `./backend/src/modifications/modifications.yaml`.
Each one of them must have the following keys:
- `reference`
- `attribute`
- `action`
- `value` (except if the `action` is "drop attribute")

The references are the ones found in the JSON files.
The attribute can be `options` (possible values that are suggested), `required` (boolean), `predefined_value` (for each resource, this is the value automatically set for `apiVersion` and `kind`), `default` (used value if nothing is provided, usually appears as placeholder), `select_one` (when one object only must be filled).

To make it easier to write these modifications, an endpoint `/modify` has been created (only in development mode) to easily find references and ensure the chosen values are consistent.
