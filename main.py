import os, sys, shutil, tempfile, hashlib, hmac, time, random
from config import *
from core.engine import transform
from core.keyschedule import expand_key
from kdf.derive import get_hwid, derive_master
from defense.mechanisms import check_lock
from format.container import pack, unpack
from tools.utils import secure_shred

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print(f"{CYAN}{BOLD}")
    print(f" CTX-X v{VERSION}")
    print(f" ──────────────────────────────────────────────────────────────")
    print(f" {GRAY}CORE:{RESET} {CONFIG['bits']}BIT  {GRAY}::{RESET}  {GRAY}ROUNDS:{RESET} {CONFIG['rounds']}  {GRAY}::{RESET}  {GRAY}MODE:{RESET} {CONFIG['speed_mode']}")
    print(f" ──────────────────────────────────────────────────────────────{RESET}\n")

def print_line(title=None):
    if title:
        print(f"\n {CYAN}┌── {BOLD}{title} {RESET}{CYAN}{'─'*(50-len(title))}{RESET}")
    else:
        print(f" {CYAN}└{'─'*53}{RESET}")

def log_step(text, level="INFO", delay=0.15):
    icon = f"{GREEN}✔{RESET}" if level == "INFO" else f"{RED}✖{RESET}" if level == "ERR" else f"{YELLOW}⚠{RESET}"
    color = WHITE if level == "INFO" else RED if level == "ERR" else YELLOW
    print(f"   {icon}  {color}{text}{RESET}")
    time.sleep(delay)

def get_status_str(val):
    return f"{GREEN}{STRINGS[CONFIG['lang']]['on']}{RESET}" if val else f"{RED}{STRINGS[CONFIG['lang']]['off']}{RESET}"

def draw_progress(current, total):
    width = 40
    pct = (current / total) * 100
    fill = int(width * current // total)
    bar = f"{CYAN}━{RESET}" * fill + f"{GRAY}─{RESET}" * (width - fill)
    sys.stdout.write(f"\r   {CYAN}⟪{RESET} {bar} {CYAN}⟫{RESET} {WHITE}{pct:>5.1f}%{RESET}")
    sys.stdout.flush()

def settings_menu():
    while True:
        print_header()
        t = STRINGS[CONFIG["lang"]]
        print_line(t['set'])
        
        print(f"   {CYAN}01.{RESET} Bits             {GRAY}::{RESET} {WHITE}{CONFIG['bits']}{RESET}")
        print(f"   {CYAN}02.{RESET} Rounds           {GRAY}::{RESET} {WHITE}{CONFIG['rounds']}{RESET}")
        print(f"   {CYAN}03.{RESET} Language         {GRAY}::{RESET} {WHITE}{CONFIG['lang']}{RESET}")
        print(f"   {CYAN}04.{RESET} Speed            {GRAY}::{RESET} {WHITE}{CONFIG['speed_mode']}{RESET}")
        print(f"   {CYAN}05.{RESET} {t['opt_hw']:<15}  {GRAY}::{RESET} {get_status_str(CONFIG['hwid_bind'])}")
        print(f"   {CYAN}06.{RESET} {t['opt_shred']:<15}  {GRAY}::{RESET} {get_status_str(CONFIG['shred'])}")
        print(f"\n   {GRAY}00. {t['exit']}{RESET}")
        
        print_line()
        c = input(f"\n   {CYAN}❯{RESET} ")
        
        if c == '1':
            v = get_selection(PROFILES['bits'], "BITS")
            if v: CONFIG['bits'] = v
        elif c == '2':
            v = get_selection(PROFILES['rounds'], "ROUNDS")
            if v: CONFIG['rounds'] = v
        elif c == '3':
            v = get_selection(PROFILES['langs'], "LANG")
            if v: CONFIG['lang'] = v
        elif c == '4':
            v = get_selection(PROFILES['speeds'], "SPEED")
            if v: CONFIG['speed_mode'] = v
        elif c == '5': CONFIG['hwid_bind'] = not CONFIG['hwid_bind']
        elif c == '6': CONFIG['shred'] = not CONFIG['shred']
        elif c == '0': break

def get_selection(opts, label):
    print(f"\n   {YELLOW}>> {label}{RESET}")
    for i, o in enumerate(opts, 1): print(f"     {CYAN}{i}.{RESET} {o}")
    try:
        x = int(input(f"\n     {CYAN}#{RESET} "))
        if 1 <= x <= len(opts): return opts[x-1]
    except: pass
    return None

def process_file(mode):
    print_header()
    t = STRINGS[CONFIG["lang"]]
    
    path = input(f"\n   {CYAN}1.{RESET} {t['path']} {GRAY}::{RESET} ").strip().strip('"')
    if not os.path.exists(path):
        log_step("Target not found", "ERR"); time.sleep(1); return

    pwd = input(f"   {CYAN}2.{RESET} {t['pwd']}  {GRAY}::{RESET} ").strip()
    
    print(f"\n {GRAY}{'─'*60}{RESET}\n")
    
    try:
        start_t = time.time()
        log_step(t['log_start'], delay=0.2)
        log_step(t['log_mem'], delay=0.2)
        
        if mode == 'e':
            log_step(t['log_salt'], delay=0.3)
            salt, nonce, iv = os.urandom(32), os.urandom(24), os.urandom(32)
            
            log_step(t['log_hwid'], delay=0.3)
            hwid = get_hwid() if CONFIG['hwid_bind'] else b"STATIC_NULL_BIND"
            
            base, ext = os.path.splitext(path)
            if os.path.isdir(path):
                tmp = tempfile.mktemp()
                shutil.make_archive(tmp, 'zip', path)
                with open(tmp+".zip", "rb") as f: data = f.read()
                ext_str = ".folder"
                os.remove(tmp+".zip")
            else:
                with open(path, "rb") as f: data = f.read()
                ext_str = ext

            meta_flag = b'\x01' if CONFIG['hwid_bind'] else b'\x00'
            meta = meta_flag + len(ext_str).to_bytes(1, 'big') + ext_str.encode().ljust(15, b'\x00') + data
            
            log_step(t['log_kdf'], delay=0.4)
            mk = derive_master(pwd, salt, CONFIG, hwid)
            ks, sb = expand_key(mk, salt + nonce, CONFIG["rounds"], CONFIG["bits"])
            
            print(f"\n   {YELLOW}[ EXECUTION ]{RESET}")
            ct = transform(meta, ks, sb, salt + nonce, CONFIG["rounds"], CONFIG["bits"], True, draw_progress, CONFIG["speed_mode"])
            
            final_blob = pack(ct, mk, salt, nonce, iv, CONFIG)
            with open(base + ".ctx", "wb") as f: f.write(final_blob)
            
            if CONFIG['shred']:
                print(); log_step(t['log_shred'], "WARN", 0.5)
                secure_shred(path)
                
        else:
            log_step(t['log_lock'], delay=0.2)
            status, info = check_lock()
            if status == "LOCKED":
                log_step(f"LOCKOUT: {info}s", "ERR"); time.sleep(2); return

            if pwd == HONEY_PWD:
                log_step("HONEYPOT DETECTED", "WARN", 1.0)
                with open(os.path.splitext(path)[0]+"_decoy.txt", "w") as f: f.write("DECOY")
                return

            with open(path, "rb") as f: blob = f.read()
            v, s, n, iv, r, sn, pi, dk, bits, ct, mac = unpack(blob)
            
            log_step(t['log_kdf'], delay=0.3)
            
            mk = None
            candidates = [b"STATIC_NULL_BIND", get_hwid()]
            
            for try_hwid in candidates:
                try_mk = derive_master(pwd, s, {"scrypt_n":sn, "pbkdf2_iter":pi*1000, "dklen":dk}, try_hwid)
                try_ak = hashlib.blake2b(try_mk + b"auth", digest_size=64).digest()
                
                if hmac.compare_digest(mac, hmac.new(try_ak, blob[:-64], hashlib.sha3_512).digest()):
                    mk = try_mk
                    break
            
            log_step(t['log_auth'], delay=0.3)
            
            if mk is None:
                st, count = check_lock(fail=True)
                if st == "FATAL":
                    if CONFIG['shred']: secure_shred(path)
                    secure_shred(LOCKOUT_FILE)
                    log_step("FATAL INTEGRITY FAILURE", "ERR"); return
                log_step(f"AUTH FAIL ({count}/{MAX_FATAL_ATTEMPTS})", "ERR"); return
            
            check_lock(False)
            ks, sb = expand_key(mk, s + n, r, bits)
            
            print(f"\n   {YELLOW}[ EXECUTION ]{RESET}")
            pt = transform(ct, ks, sb, s + n, r, bits, False, draw_progress, CONFIG["speed_mode"])
            
            ext_len = pt[1]
            ext_r = pt[2:2+ext_len].decode()
            actual = pt[17:]
            out_base = os.path.splitext(path)[0]
            
            if ext_r == ".folder":
                t_tmp = tempfile.mktemp() + ".zip"
                with open(t_tmp, "wb") as f: f.write(actual)
                shutil.unpack_archive(t_tmp, out_base, 'zip')
                os.remove(t_tmp)
            else:
                with open(out_base + ext_r, "wb") as f: f.write(actual)
            
            if CONFIG['shred']:
                print(); log_step(t['log_shred'], "WARN", 0.5)
                secure_shred(path)

        print(f"\n\n {GRAY}{'─'*60}{RESET}")
        log_step(f"{t['succ']} [{time.time()-start_t:.2f}s]", "INFO", 1.0)
        
    except Exception as e:
        print(f"\n {RED}SYSTEM ERROR: {e}{RESET}")
    
    input(f"\n   {GRAY}[ ENTER ]{RESET}")

def main_menu():
    while True:
        print_header()
        t = STRINGS[CONFIG["lang"]]
        print_line(t['menu'])
        
        print(f"   {CYAN}01.{RESET} {WHITE}{t['enc']}{RESET}")
        print(f"   {CYAN}02.{RESET} {WHITE}{t['dec']}{RESET}")
        print(f"   {CYAN}03.{RESET} {WHITE}{t['set']}{RESET}")
        print(f"\n   {GRAY}00. {t['exit']}{RESET}")
        
        print_line()
        c = input(f"\n   {CYAN}❯{RESET} ")
        if c == '1': process_file('e')
        elif c == '2': process_file('d')
        elif c == '3': settings_menu()
        elif c == '0': sys.exit()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n   {YELLOW}>>...{RESET}")
        sys.exit()
