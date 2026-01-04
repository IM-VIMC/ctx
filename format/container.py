import struct, hashlib, hmac
from config import VERSION

def pack(data, mk, salt, nonce, iv, config):
    auth_k = hashlib.blake2b(mk + b"auth", digest_size=64).digest()
    h = struct.pack(">B32s24s32sIHHBH", VERSION, salt, nonce, iv, 
                    config["rounds"], config["scrypt_n"], 
                    config["pbkdf2_iter"]//1000, config["dklen"], config["bits"])
    mac = hmac.new(auth_k, h + data, hashlib.sha3_512).digest()
    return h + data + mac

def unpack(blob):
    v = blob[0]
    salt, nonce, iv = blob[1:33], blob[33:57], blob[57:89]
    r, sn, pi, dk, bits = struct.unpack(">IHHBH", blob[89:100])
    return v, salt, nonce, iv, r, sn, pi, dk, bits, blob[100:-64], blob[-64:]

