import json
import yaml


input_file_name = "schedule"
output_file_name = "schedule_converted"

with open(input_file_name + ".json", 'r', encoding='utf-8') as input_file:
    with open(output_file_name + ".yaml", 'w', encoding='utf-8') as output_file:
        json_data = json.loads(input_file.read())
        converted_json_data = json.dumps(json_data)

        yaml_data = yaml.safe_load(converted_json_data)
        converted_yaml_data = yaml.dump(yaml_data, allow_unicode=True)

        output_file.write(converted_yaml_data)
