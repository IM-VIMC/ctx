import hashlib, time, sys

def b2i(b): return int.from_bytes(b, 'big')
def i2b(v, l): return v.to_bytes(l, 'big')
def rol(v, n, bits): return ((v << n) & ((1 << bits) - 1)) | (v >> (bits - n))

def _mc2(x): return ((x << 1) ^ 0x1B) & 0xFF if x & 0x80 else (x << 1) & 0xFF
def _mc3(x): return _mc2(x) ^ x

def _mds(data, size):
    res = bytearray(size)
    for c in range(0, size, 8):
        d = data[c:c+8]
        res[c]   = _mc2(d[0]) ^ _mc3(d[1]) ^ d[2] ^ d[3] ^ d[4] ^ d[5] ^ d[6] ^ _mc3(d[7])
        res[c+1] = _mc3(d[0]) ^ _mc2(d[1]) ^ _mc3(d[2]) ^ d[3] ^ d[4] ^ d[5] ^ d[6] ^ d[7]
        res[c+2] = d[0] ^ _mc3(d[1]) ^ _mc2(d[2]) ^ _mc3(d[3]) ^ d[4] ^ d[5] ^ d[6] ^ d[7]
        res[c+3] = d[0] ^ d[1] ^ _mc3(d[2]) ^ _mc2(d[3]) ^ _mc3(d[4]) ^ d[5] ^ d[6] ^ d[7]
        res[c+4] = d[0] ^ d[1] ^ d[2] ^ _mc3(d[3]) ^ _mc2(d[4]) ^ _mc3(d[5]) ^ d[6] ^ d[7]
        res[c+5] = d[0] ^ d[1] ^ d[2] ^ d[3] ^ _mc3(d[4]) ^ _mc2(d[5]) ^ _mc3(d[6]) ^ d[7]
        res[c+6] = d[0] ^ d[1] ^ d[2] ^ d[3] ^ d[4] ^ _mc3(d[5]) ^ _mc2(d[6]) ^ _mc3(d[7])
        res[c+7] = _mc3(d[0]) ^ d[1] ^ d[2] ^ d[3] ^ d[4] ^ d[5] ^ _mc3(d[6]) ^ _mc2(d[7])
    return bytes(res)

def f_func(x, k, rc, sbox, tweak, r_idx, bits):
    hb, size = bits // 2, bits // 8
    m_bytes = i2b(x ^ k ^ tweak, size // 2).ljust(size, b'\x00')
    sub = bytearray(size)
    for i in range(size):
        sub[i] = sbox[m_bytes[i] ^ (rc & 0xFF)]
    return rol(b2i(_mds(sub, size)), (13 + r_idx) % hb, hb) ^ rc

def transform(data, keys, sbox, salt, rounds, bits, encrypt=True, callback=None, speed_mode="FAST (Max)"):
    size, hb = bits // 8, bits // 16
    limit = 1 << (bits // 2)
    if encrypt:
        p = size - (len(data) % size)
        data += bytes([p]) * p
    
    total = len(data) // size
    out = bytearray()
    prev = b2i(salt[:size].ljust(size, b'\x00'))
    t = b2i(salt[::-1][:hb].ljust(hb, b'\x00'))
    
    delay = 0
    if "MEDIUM" in speed_mode: delay = size / (1024 * 1024)
    elif "SLOW" in speed_mode: delay = size / (256 * 1024)

    for i in range(total):
        if delay > 0: time.sleep(delay)
        blk = data[i*size:(i+1)*size]
        if encrypt:
            ch = i2b(b2i(blk) ^ prev, size)
            L, R = b2i(ch[:hb]) ^ keys[-1], b2i(ch[hb:]) ^ keys[-2]
            for r in range(rounds):
                f = f_func(R, keys[r], r, sbox, t, r, bits)
                L, R = R, (L ^ f) % limit
            c_b = i2b(L ^ keys[-3], hb) + i2b(R ^ keys[-4], hb)
            out.extend(c_b); prev = b2i(c_b)
        else:
            L, R = b2i(blk[:hb]) ^ keys[-3], b2i(blk[hb:]) ^ keys[-4]
            for r in range(rounds - 1, -1, -1):
                f = f_func(L, keys[r], r, sbox, t, r, bits)
                L, R = (R ^ f) % limit, L
            un = i2b(L ^ keys[-1], hb) + i2b(R ^ keys[-2], hb)
            pl = i2b(b2i(un) ^ prev, size)
            out.extend(pl); prev = b2i(blk)
        if callback: callback(i + 1, total)
            
    if not encrypt:
        p = out[-1]
        return out[:-p] if 0 < p <= size else out
    return out
