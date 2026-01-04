import os, secrets

def secure_shred(p, passes=3):
    if not os.path.exists(p): return
    sz = os.path.getsize(p)
    with open(p, "ba+", buffering=0) as f:
        for _ in range(passes):
            f.seek(0); f.write(secrets.token_bytes(sz))
            f.flush(); os.fsync(f.fileno())
    os.remove(p)
