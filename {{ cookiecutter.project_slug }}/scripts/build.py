from frictionless import Package, Resource
from datetime import datetime
from dpm.utils import as_identifier
import json
from pathlib import Path


def build_package(descriptor: str = 'datapackage.yaml'):
    
    source = Package(descriptor)

    target_descriptor = {
        "profile": "tabular-data-package",
        "name": source.name,
        "resources": [
            {
            "profile": "tabular-data-resource",
            "name": resource_name,
            "path": f'data/{resource_name}.csv',
            "format": "csv",
            "encoding": "utf-8",
            "schema": {"fields": [
                {
                'name': field.custom['target'] if field.custom.get('target') else as_identifier(field.name),
                'type': field.type,
                'source': field.name,
                } for field in source.get_resource(resource_name).schema.fields                
            ]}
            } for resource_name in source.resource_names
        ]
    }

    target = Package.from_descriptor(target_descriptor)
    target.custom['updated_at'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    
    for resource in target.resources:
        resource.infer(stats=True)
        file_path = Path(f"logs/{resource.name}.json")
        if Path.exists(file_path):
            with open(file_path, 'r') as file:
                # Load existing content
                metadata = json.load(file)
            resource.custom.update({'metadata': metadata})

    target.to_json('datapackage.json')
