'''
Dux-Soup remote control API wrapper

versions:
    V0.6 [25.10.2019]
        - cleanup
        - moved exception text to global
        - added examples
    V0.1 [19.10.2019]
        - first working version
'''

__author__ = "Bojan"
__license__ = "GPL"
__version__ = "0.6"
__maintainer__ = "Bojan"
__status__ = "Production"

import hashlib
import hmac
import base64
import time
import json
import requests

class DuxWrap:
    '''Dux-Soup remote control wrapper'''
    version = "0.6"

    #mockup requests
    #used for format check and request generate
    dsrsw_request_mockups_data = {
        "visit": {
            "targeturl": "{}/{}/queue",
            "params": {
                "profile": "",
            },
        },
        "connect": {
            "targeturl": "{}/{}/queue",
            "params": {
                "profile":"",
                "messagetext":""
            },
        },
        "message": {
            "targeturl": "{}/{}/queue",
            "params": {
                "profile":"",
                "messagetext":""
            },
        },
        "wait": {
            "targeturl": "{}/{}/queue",
            "params": {
                "duration": 0,
            },
        },
        "reset": {
            "targeturl": "{}/{}/queue",
        },

        "size": {
            "targeturl": "{}/{}/queue/size",
        },
        "profile": {
            "targeturl":"{}/{}/profile",
        },
        "items": {
            "targeturl": "{}/{}/queue/items",
        }
    }

    #exception messages text
    exception_messages = [
        'Required key [{}] for command [{}] missing',
        'Required params key [{}] for command [{}] missing',
        'API key or user ID missing',
        'Unknown command [{}]',
        'Unable to generate request data',
    ]

    #list of get method requests
    get_method_requests = ['items', 'profile', 'size']

    # Dux Soup remote control API endpoint
    endpoint = 'https://app.dux-soup.com/xapi/remote/control'

    def __init__(self, api_key, user_id):
        '''init'''
        self.api_key = api_key
        self.user_id = user_id

    def _create_signature(self, data):
        '''create signature

        :param dict data: Data to create signature for
        :return str: Return signature
        '''
        mac = hmac.new(bytes(self.api_key, 'ascii'), digestmod=hashlib.sha1)
        message = bytes(data, 'ascii')
        mac.update(message)
        sig = mac.digest()
        return str(base64.b64encode(sig), 'ascii')

    def _create_signature_type(self, request_type, data):
        '''create signature based on type of request

        :param str request_type: Request type
        :param dict data: Data to insert in request
        :return str: Return signature
        '''
        if request_type in self.get_method_requests:
            signature_data = data["targeturl"]
        else:
            signature_data = json.dumps(data)
        return self._create_signature(signature_data)

    def _check_required_params(self, request_type, data):
        '''check required params for request

        :param str request_type: Request type
        :param dict data: Data to insert in request
        :return bool: Returns True if all is OK
        '''
        req = self.dsrsw_request_mockups_data[request_type]
        for key in req:
            #exclude target URL
            if key == "targeturl":
                continue
            #check if data contain required params
            if key not in data:
                raise Exception(
                        self.exception_messages[0].format(key, request_type))
            #check valid param structure
            if key == "params":
                for p_key in req[key]:
                    if p_key not in data[key]:
                        raise Exception(self.exception_messages[1].format(
                                p_key, request_type))
        return True

    def _create_request_data(self, request_type, data):
        '''create request data from mocukps

        :param str request_type: Request type
        :param dict data: Data to insert in request
        :return dict: Returns request data seti or none on issue
        '''
        if request_type not in self.dsrsw_request_mockups_data:
            return None
        req = dict(self.dsrsw_request_mockups_data[request_type])
        #required fields
        req["command"] = request_type
        req["timestamp"] = int(time.time() * 1000)
        req["targeturl"] = req["targeturl"].format(self.endpoint, self.user_id)
        req["userid"] = self.user_id
        #required per endpoint
        self._check_required_params(request_type, data)
        #add params
        req["params"] = {}
        if "params" in data:
            req["params"] = data["params"]
        return req

    def _request_send(self, command, request):
        '''execute request

        :param str command: Command to execute
        :param dict request: Request data set
        :return dict: Dict with result data
        '''
        sig = self._create_signature_type(command, request)
        headers={
            "X-Dux-Signature": sig,
            "Content-Type": "application/json"
        }
        if command in self.get_method_requests:
            res = requests.get(
                request["targeturl"],
                headers=headers
            )
        else:
            res = requests.post(
                request["targeturl"],
                json=request,
                headers=headers
            )
        try:
            return json.loads(res.text)
        except Exception as err:
            raise Exception(err)

    def update_creds(self, api_key, user_id):
        '''update creds

        :param str api_key: API key
        :param str user_id: User ID
        :return bool: Returns True idf all is OK
        '''
        if not api_key or not user_id:
            raise Exception(self.exception_messages[2])
        self.api_key = api_key
        self.user_id = user_id
        return True

    def call(self, command, data):
        '''call command on endpoint

        :param str command: Command to execute
        :param dict data: Request data
        :return dict: Dict with result data
        '''
        #check creds
        if not self.api_key or not self.user_id:
            raise Exception(self.exception_messages[2])
        #check if command existing
        if command not in self.dsrsw_request_mockups_data:
            raise Exception(self.exception_messages[3].format(command))
        #execute command
        request_data = self._create_request_data(command, data)
        if not request_data:
            raise Exception(self.exception_messages[4])
        return self._request_send(command, request_data)
