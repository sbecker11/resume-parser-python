import json
import sys
import jsonschema
from jsonschema import validate

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_data_object.py <data_object>.json")

        sys.exit(1)

    data_file = sys.argv[1]

    # Read the JSON data from the input file
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    schema_file = "./inputs/resume-schema.json"
    # load the schema from the schema json file
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    # Validate the data against the schema
    try:
        validate(instance=data, schema=schema)
        print(f"data object {data_file} is valid against schema {schema_file}")
    except jsonschema.exceptions.ValidationError as err:
        print("Validation error: {err.message}")

if __name__ == "__main__":
    main()