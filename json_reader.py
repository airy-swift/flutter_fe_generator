import json
from base import *


def read_json(file_name):
    json_open = open(file_name, 'r')
    json_data = json.load(json_open)
    return json_data


def from_json(json_data):
    events: list[FirebaseEventRawData] = []
    for index, raw in enumerate(json_data):
        event = FirebaseEventRawData()
        event.version = raw['version']
        event.enabled = raw['enabled']
        event.description = raw['description']
        event.event_name = raw['event_name']

        if (len(raw['parameters']) - 1) == index:
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
    data = read_json('example.json')
    event_datas = from_json(data)

    result = output(event_datas)
    print(result)
    copy(result)
