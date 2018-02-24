# TBW
# This will read the config file and get the stuff

import calendar
import time
import requests
import jwt
import json

__pubkey = [""]
__prikey = [""]
__domain = [""]
__indrak = [""]
__stinfo = [{}]


def get_site_info():
    if __stinfo[0] != {}:
        return __stinfo[0]
    f = open('site_info.json', 'r')
    info = f.read()
    f.close()
    __stinfo[0] = json.loads(info)
    __domain[0] = __stinfo[0]['DOMAIN']

    return __stinfo[0]


def __get_pubkey():
    if __pubkey[0] != "":
        return __pubkey[0]

    f = open('token_key.pub', 'r')
    key = f.read()
    f.close()
    __pubkey[0] = key
    return __pubkey[0]


def __get_prikey():
    if __prikey[0] != "":
        return __pubkey[0]

    f = open('token_key.pem', 'r')
    key = f.read()
    f.close()
    __prikey[0] = key
    return __prikey[0]


def __get_indra_key():
    if __indrak[0] is not "":
        return __indrak[0]
    r = requests.get('https://secure.demilletech.net/api/key/')
    print(r.text)
    __indrak[0] = r.text
    return __indrak[0]


def get_domain():
    get_site_info()
    return __domain[0]


def get_epoch_time():
    return calendar.timegm(time.gmtime())


def verify_token(token):
    ret = decode_token(token)
    if isinstance(ret, dict):
        return True
    return False


def encode_token(payload):
    return jwt.encode(payload, __get_prikey(), algorithm='ES512').decode('UTF-8')


def generate_token(uniqueid, returl, userfed=False):
    payload = {
        "aud": "secure.demilletech.net",
        "jti": uniqueid,
        "returl": returl,
        "iat": get_epoch_time(),
        "ttl": 20,
        "iss": get_domain(),
        "userfed": userfed
    }
    return encode_token(payload)


def decode_token(encoded_token):
    try:
        decoded_token = jwt.decode(encoded_token, key=__get_indra_key(),
                                   algorithms='ES512', audience=get_domain())
    except jwt.exceptions.DecodeError:
        return "DECODE_ERROR"
    except jwt.exceptions.ExpiredSignatureError:
        return "EXPIRED_SIGNATURE"
    except jwt.exceptions.ImmatureSignatureError:
        return "IMMATURE_SIGNATURE"
    except jwt.exceptions.InvalidAlgorithmError:
        return "INVALID_ALGORITHM"
    except jwt.exceptions.InvalidAudienceError:
        return "INVALID_AUDIENCE"  # wut?
    except jwt.exceptions.InvalidIssuedAtError:
        return "INVALID_IAT"
    except jwt.exceptions.InvalidIssuerError:
        return "INVALID_ISSUER"
    except jwt.exceptions.InvalidKeyError:
        return "INVALID_KEY"
    except jwt.exceptions.InvalidTokenError:
        return "INVALID_TOKEN"
    return decoded_token
