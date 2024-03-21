import json
from pathlib import Path


def add_metadata_to_json(resource_name, key, value, ):
    """
    Adds the pair key:value to the file logs/{resource_name}.json. Creates the file if it does not exist.

    Parameters
    ----------
    resource_name : str
        name of the file to be created or metadata appended.
    key : str
        Property key inserted in json.
    value : any
        Property value inserted into json.
    """
    file_path = Path(f'logs/{resource_name}.json')

    if Path.exists(file_path):
        with open(file_path, 'r') as file:
            # Load existing content
            metadata = json.load(file)
    else:
        metadata = {}

    metadata[key] = value

    with open(file_path, 'w') as file:
        json.dump(metadata, file, indent=2)


def write_dict_to_json(resource_name, data):
    """
    Saves the `data` dictionary as a JSON file `logs/{resource_name}.json. Replaces the file if it already exists.

    Parameters
    ----------
    resource_name : str
        The name of the resource to create a json metadata file.
    data : dict
        the dictionary that will be saved as JSON.
    """
    filepath = f'logs/{resource_name}.json'
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=2, sort_keys=False)

