import email
from http.client import HTTPException
import time
from typing import Dict
from fastapi import Depends, status
import jwt
from decouple import config
from pydantic import EmailStr


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(email : "email") -> Dict[str, str]:
    payload = {
        "email": email,
        # "role": User.role.value,
        # "active": User.is_active,
        "expires": time.time() + 60000
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        # import pdb 
        # pdb.set_trace()
    return token_response(token)




def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}



    
    
    
    
