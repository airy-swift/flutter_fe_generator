import yaml
from base import *


def read_yaml(file_name):
    with open(file_name) as file:
        obj = yaml.load(file, Loader=yaml.Loader)
        return obj


def from_yaml(yaml_data):
    events: list[FirebaseEventRawData] = []
    for index, event_name in enumerate(yaml_data):
        raw = yaml_data[event_name]
        event = FirebaseEventRawData()
        event.version = raw['version']
        event.enabled = raw['enabled']
        event.description = raw['description']
        event.event_name = event_name

        if 'parameters' in raw:
            params: list[FirebaseParameterRawData] = []
            for raw_p in raw['parameters']:
                param = FirebaseParameterRawData()
                param.required = raw_p['required']
                param.type = raw_p['type']
                param.parameter_name = raw_p['parameter_name']
                params.append(param)
            event.parameters = params
        events.append(event)
    return events


if __name__ == '__main__':
    data = read_yaml('example.yaml')
    event_datas = from_yaml(data)

    result = output(event_datas)
    print(result)
    copy(result)
