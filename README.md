# Dux Soup remote control wrapper
Wrapper around Dux Soup remote control API

## Documentation
[Remote Control by Example](https://support.dux-soup.com/article/115-remote-control-by-example)

[API test environment](https://app.dux-soup.com/web/rc/test)

___
## Install
```pip install duxwrap```
___


### Commands list
Commands alowed bu Dux Soup remote contol:
- visit (**visit profile**)
- connect (**send connection request**)
- message (**send message**)
- wait (**pause the robot**)
- reset (**clear the queue**)
- size (**size of the queue**)
- profile (**account information**)
- items (**list items in queue**)

___


### Required params for certain commands
#### visit
```
"params": {
    "profile": "PROFILE_URL",
}
```
___
#### connect
```
"params": {
    "profile": "PROFILE_URL",
    "messagetext": "MESSAGE TEXT"
}
```
Please check documentation above for more info on **messagetext** format and additional options
___
#### message
```
"params": {
    "messagetext": "MESSAGE TEXT"
}
```
Please check documentation above for more info on **messagetext** format and additional options
___
#### wait
```
"params": {
    "duration": DURATION_IN_SECONDS,
}
```
___

### How to use
```python
import json
from duxwrap import DuxWrap

"""create wrapper"""
dux = DuxWrap('API_KEY', 'USER_ID')
print('DuxSoup version:', dux.version)

"""get acount info"""
profile_data = dux.call("profile", {})
print('PROFILE DATA SET')
print(json.dumps(profile_data, indent=4, sort_keys=True))
print('-----------------------------\n\n')

"""pause the robot"""
print('PAUSE RESPONSE')
params = {
    "params": {
        "duration": 0
    }
}
pause_data = dux.call("wait", params)
print(json.dumps(pause_data, indent=4, sort_keys=True))
```
