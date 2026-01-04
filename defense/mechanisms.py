import os, time, json, hashlib, hmac
from config import LOCKOUT_FILE, MAX_FATAL_ATTEMPTS

def check_lock(fail=False):
    k = hashlib.sha256(b"ctx_internal_state_v156").digest()
    if not os.path.exists(LOCKOUT_FILE): d = {"a": 0, "t": 0}
    else:
        try:
            with open(LOCKOUT_FILE, "rb") as f:
                r = f.read(); s, p = r[:32], r[32:]
                if hmac.new(k, p, hashlib.sha256).digest() != s: raise Exception()
                d = json.loads(p.decode())
        except: d = {"a": 0, "t": 0}

    if fail:
        d["a"] += 1; d["t"] = time.time()
        # Persistir el fallo antes de evaluar
        p_bytes = json.dumps(d).encode()
        s_bytes = hmac.new(k, p_bytes, hashlib.sha256).digest()
        with open(LOCKOUT_FILE, "wb") as f: f.write(s_bytes + p_bytes)
        
        if d["a"] >= MAX_FATAL_ATTEMPTS: return "FATAL", d["a"]
        return "FAIL", d["a"]
    else:
        if d["a"] >= 3:
            rem = int(300 - (time.time() - d["t"]))
            if rem > 0: return "LOCKED", rem
        if not fail and d["a"] > 0: 
            d = {"a": 0, "t": 0}
            p_bytes = json.dumps(d).encode()
            s_bytes = hmac.new(k, p_bytes, hashlib.sha256).digest()
            with open(LOCKOUT_FILE, "wb") as f: f.write(s_bytes + p_bytes)
    return "OK", d["a"]

