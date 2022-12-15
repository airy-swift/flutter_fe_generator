# flutter_fe_generator

### base yaml

```yaml
sign_in:
  description: ログインイベント
  version: 1.0,0
  enabled: True
  parameters:
    - required: True
      type: String
      parameter_name: provider
    - required: False
      type: String?
      parameter_name: user_id
logout: ログアウトイベント
  description:
  version: 1.0,0
  enabled: True
```

### result flutter

```dart

class FirebaseEventKind {
  FirebaseEventKind._(this._eventName, this._params);

  /// StartVersion: 1.0,0
  /// About: ログインイベント
  FirebaseEventKind.signIn({required String provider,String? userId}) //
    : this._('sign_in', <String, dynamic>{'provider': provider,'user_id': userId});

  /// StartVersion: 1.0,0
  /// About: ログアウトイベント
  FirebaseEventKind.buttonTap() //
    : this._('button_tap', <String, dynamic>{});


  final String _eventName;

  final Map<String, dynamic> _params;

  Future<void> sendEvent() async {
    logger.fine('SEND FIREBASE EVENT: _eventName (parameter: _params)');
    await FirebaseAnalytics.instance.logEvent(
      name: _eventName,
      parameters: _params,
    );
  }
}
```
