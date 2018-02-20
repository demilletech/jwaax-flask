# TBW
# This will read the config file and get the stuff

import calendar
import time
import requests
import jwt

__secret = [""]
__domain = [""]
__indrak = [""]


def __get_secret():
    f = open('dt_auth/site_secret.txt', 'r')
    key = f.read()
    f.close()
    __domain[0] = key[:key.index(":")]
    __secret[0] = key[key.index(":") + 1:]
    return __secret[0]


def __get_indra_key():
    if __indrak[0] is not "":
        return __indrak[0]
    r = requests.get('https://secure.demilletech.net/api/key/')
    print(r.text)
    __indrak[0] = r.text
    return __indrak[0]


def get_domain():
    __get_secret()
    return __domain[0]


def get_epoch_time():
    return calendar.timegm(time.gmtime())


def verify_token(token):
    ret = decode_token(token)
    if isinstance(ret, dict):
        return True
    return False


def encode_token(payload):
    return jwt.encode(payload, __get_secret(), algorithm='HS256').decode('UTF-8')


def generate_token(uniqueid, returl):
    payload = {
        "aud": "secure.demilletech.net",
        "domain": get_domain(),
        "uniqueid": uniqueid,
        "returl": returl,
        "iat": get_epoch_time(),
        "exp": get_epoch_time() + 120,
        "iss": get_domain()
    }
    return encode_token(payload)


def decode_token(encoded_token):
    try:
        decoded_token = jwt.decode(encoded_token, key=__get_indra_key(),
                                   algorithms='PS256', audience=get_domain())
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
