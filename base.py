import re
import pyperclip

base_template = """
class FirebaseEventKind {{
  FirebaseEventKind._(this._eventName, this._params);
{0}

  final String _eventName;

  final Map<String, dynamic> _params;

  Future<void> sendEvent() async {{
    logger.fine('SEND FIREBASE EVENT: _eventName (parameter: _params)');
    await FirebaseAnalytics.instance.logEvent(
      name: _eventName,
      parameters: _params,
    );
  }}
}}
"""

each_template = """
  /// StartVersion: {version}
  /// About: {description}
  FirebaseEventKind.{camel}({params}) //
    : this._('{snake}', <String, dynamic>{{{map}}});
"""

param_template = "{required}{type} {param_name}"
map_template = "'{key}': {value}"


class FirebaseParameterRawData:
    required = True
    type = "String"
    parameter_name = ""


class FirebaseEventRawData:
    version = ""
    enabled = True
    description = ""
    event_name = ""
    parameters: list[FirebaseParameterRawData] = []

    def make_params_string(self):
        if len(self.parameters) == 0:
            return ''
        else:
            kakko = '{{{0}}}'
            parameter = ','.join(map(
                lambda param: param_template.format(
                    required='required ' if param.required else '',
                    type=param.type,
                    param_name=toCamel(param.parameter_name)
                ),
                self.parameters,
            ))
            return kakko.format(parameter)


def output(events: list[FirebaseEventRawData]):
    darts: list[str] = []
    for event in events:
        if not event.enabled:
            continue

        dart = each_template.format(
            version=event.version,
            description=event.description,
            camel=toCamel(event.event_name),
            snake=event.event_name,
            params=event.make_params_string(),
            map=','.join(map(
                lambda param: map_template.format(
                    key=param.parameter_name,
                    value=toCamel(param.parameter_name)
                ),
                event.parameters,
            )),
        )
        darts.append(dart)

    result = base_template.format(''.join(darts))
    return result


def toCamel(string):
    return re.sub("_(.)", lambda m: m.group(1).upper(), string)


def copy(string):
    pyperclip.copy(string)
