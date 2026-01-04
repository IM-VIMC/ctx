import hashlib, os, subprocess, sys
from config import VESSEL_KEY

def get_hwid():
    try:
        if sys.platform == 'win32':
            id = subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split('\n')[1].strip()
        else:
            paths = ['/etc/machine-id', '/var/lib/dbus/machine-id']
            id = next((open(p).read().strip() for p in paths if os.path.exists(p)), os.uname().nodename)
        return hashlib.sha3_256(id.encode()).digest()
    except: return hashlib.sha3_256(b"static_fallback").digest()

def derive_master(pwd, salt, config, hwid):
    material = pwd.encode() + hwid + VESSEL_KEY
    b = hashlib.blake2b(material + salt, digest_size=64).digest()
    s = hashlib.scrypt(b, salt=salt, n=config["scrypt_n"], r=8, p=1, dklen=128, maxmem=134217728)
    return hashlib.pbkdf2_hmac('sha512', s, salt + VESSEL_KEY, config["pbkdf2_iter"], dklen=config["dklen"])

