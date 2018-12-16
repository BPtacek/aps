import requests

url = "http://statsapi.web.nhl.com/api/v1/"

def prepare_url(call_type):
    path = url + call_type
    return path.rstrip()

def check_params(params):
    return isinstance(params, dict)

def make_call(call_type, payload):
    address = prepare_url(call_type)
    if check_params(payload):
        r = requests.get(address, params = payload)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError("api_calls module: Response status code not 200")
    else:
        raise TypeError('GET call parameters are not entered as key:value pairs')

if __name__ == "__main__":
    pass
