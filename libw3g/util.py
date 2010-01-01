import os
from base64 import b32encode as b32e
from hashlib import sha256
from itertools import count

def get_replay_id(data):
    return b32e(sha256(data).digest())[:8].lower()

def get_timestamp(path):
    stat = os.stat(path)
    return int(stat.st_mtime)
