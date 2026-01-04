import os

VERSION = 1
LOCKOUT_FILE = os.path.join(os.path.expanduser("~"), ".ctx_state.bin")
VESSEL_KEY = b"vessel"
MAX_FATAL_ATTEMPTS = 10
HONEY_PWD = "invitado_root"

PROFILES = {
    "bits": [128, 256, 512, 1024, 2048],
    "rounds": [128, 256, 512, 1024, 2048],
    "langs": ["Español", "English", "Indonesia"],
    "speeds": ["FAST (Max)", "MEDIUM (1 MB/s)", "SLOW (256 KB/s)"]
}

CONFIG = {
    "bits": 256,
    "rounds": 256,
    "lang": "Español",
    "speed_mode": "FAST (Max)",
    "hwid_bind": True,
    "shred": True,
    "scrypt_n": 2**14,
    "pbkdf2_iter": 600000,
    "dklen": 32
}

STRINGS = {
    "Español": {
        "menu": "PANEL DE CONTROL", "enc": "ENCRIPTAR ARCHIVO", "dec": "DESENCRIPTAR ARCHIVO", "set": "CONFIGURACIÓN DEL SISTEMA", "exit": "SALIR",
        "path": "RUTA OBJETIVO", "pwd": "LLAVE MAESTRA", "succ": "PROCESO FINALIZADO CON ÉXITO",
        "log_start": "Iniciando secuencia de arranque...",
        "log_mem": "Asignando memoria segura (Protected Memory)...",
        "log_salt": "Generando vectores de inicialización y Salt (CSPRNG)...",
        "log_hwid": "Escaneando firma de hardware única (Machine GUID)...",
        "log_kdf": "Derivando claves criptográficas (Scrypt + PBKDF2-HMAC)...",
        "log_auth": "Verificando integridad del contenedor (Blake2b)...",
        "log_shred": "Sobrescribiendo datos originales (DoD Standard)...",
        "log_lock": "Comprobando estado de bloqueo de seguridad...",
        "opt_hw": "Vincular HWID", "opt_shred": "Borrado Seguro", "on": "ACTIVADO", "off": "DESACTIVADO"
    },
    "English": {
        "menu": "CONTROL PANEL", "enc": "ENCRYPT FILE", "dec": "DECRYPT FILE", "set": "SYSTEM CONFIGURATION", "exit": "EXIT",
        "path": "TARGET PATH", "pwd": "MASTER KEY", "succ": "PROCESS COMPLETED SUCCESSFULLY",
        "log_start": "Initiating boot sequence...",
        "log_mem": "Allocating protected memory...",
        "log_salt": "Generating initialization vectors & Salt (CSPRNG)...",
        "log_hwid": "Scanning unique hardware signature (Machine GUID)...",
        "log_kdf": "Deriving cryptographic keys (Scrypt + PBKDF2-HMAC)...",
        "log_auth": "Verifying container integrity (Blake2b)...",
        "log_shred": "Overwriting original data (DoD Standard)...",
        "log_lock": "Checking security lockout status...",
        "opt_hw": "HWID Binding", "opt_shred": "Secure Shred", "on": "ENABLED", "off": "DISABLED"
    },
    "Indonesia": {
        "menu": "PANEL KONTROL", "enc": "ENKRIPSI BERKAS", "dec": "DEKRIPSI BERKAS", "set": "KONFIGURASI SISTEM", "exit": "KELUAR",
        "path": "JALUR TARGET", "pwd": "KUNCI UTAMA", "succ": "PROSES SELESAI DENGAN SUKSES",
        "log_start": "Memulai urutan boot...",
        "log_mem": "Mengalokasikan memori aman...",
        "log_salt": "Menghasilkan vektor inisialisasi & Salt...",
        "log_hwid": "Memindai tanda tangan perangkat keras unik...",
        "log_kdf": "Menurunkan kunci kriptografi...",
        "log_auth": "Memverifikasi integritas kontainer...",
        "log_shred": "Menimpa data asli...",
        "log_lock": "Memeriksa status penguncian keamanan...",
        "opt_hw": "Pengikatan HWID", "opt_shred": "Hapus Aman", "on": "AKTIF", "off": "NONAKTIF"
    }
}

PINK, CYAN, GREEN, YELLOW, WHITE, GRAY, RED, RESET, BOLD = (
    "\033[95m", "\033[96m", "\033[92m", "\033[93m", "\033[97m", "\033[90m", "\033[91m", "\033[0m", "\033[1m"
)

