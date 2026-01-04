import hashlib

def get_sbox(seed):
    s = list(range(256))
    r = hashlib.shake_256(seed).digest(1024)
    for i in range(256):
        j = (i + r[i] + r[i+256]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def expand_key(mk, salt, rounds, bits):
    sbox = get_sbox(mk + salt)
    state = int.from_bytes(hashlib.sha3_512(mk + salt).digest(), 'big')
    keys = []
    limit = 1 << (bits // 2)
    for r in range(rounds + 8):
        k = int.from_bytes(hashlib.blake2b(mk + bytes([r % 256]), digest_size=32).digest(), 'big')
        state = (state ^ k ^ r) % limit
        keys.append(state)
    return keys, sbox

