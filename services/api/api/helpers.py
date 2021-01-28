import hashlib

from fastapi import Request

def get_fingerprint(request: Request):
    data = ':'.join([v for k, v in request.headers.items() if k in ('sec-ch-ua', 'sec-ch-ua-mobile', 'user-agent')])
    return hashlib.md5(data.encode()).hexdigest()