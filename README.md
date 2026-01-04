CTX-X TITANIUM (v160) - Experimental Block Cipher Utility
CTX-X Titanium is a Python-based experimental cryptographic implementation (toy-crypto) using a custom Feistel Network architecture. This project explores the combination of memory-hard functions, advanced bit-permutation techniques, and hardware-binding-based defense mechanisms.
> [!CAUTION]
> EXPERIMENTAL STATUS: This software is not intended for use in production environments or for securing classified data. This implementation has not undergone formal cryptanalysis audits (such as differential or linear analysis). Use for educational and research purposes only.
>
🏗️ Core Architecture Specifications
This system operates at a dynamic block level, supporting configurations from 128-bit to 2048-bit.
 1. Feistel Network & F-Function
This algorithm uses the classic Feistel structure but with modifications to its internal functions:
* Dynamic S-Box: Instead of a static S-Box like AES, this project generates a unique 256-byte substitution table per session using SHAKE_256 of the master key and salt.
* MDS (Maximum Distance Separable) Matrix: Implements linear transformations _mc2 and _mc3 to ensure optimal bit diffusion within the f-function, inspired by the MixColumns structure.
* Bitwise Rotation (ROL): Uses a circular bit shift that varies based on the round index to break the data's symmetry pattern.
2. Key Schedule & Derivation
Key management is performed through a computationally intensive process to mitigate offline brute-force attacks:
* Starting Material: A combination of password, HWID (Hardware ID), and static VESSEL_KEY.
* Phase I (Pre-Hash): Hashing using Blake2b (64-byte digest).
 * Phase II (Memory-Hard): Processing via Scrypt with parameters N=2^{14}, r=8, p=1 for resistance to ASIC/FPGA acceleration.
* Phase III (Stretching): Final iteration using PBKDF2-HMAC-SHA512 for 600,000 rounds.
🛡️ Defense Mechanisms & Integrity
This system goes beyond standard encryption by including layers of active defense logic:
* Hardware-Binding (HWID): Use wmic csproduct get uuid on Windows or machine-id on Linux to bind decryption only to a specific machine.
* Encryp-then-MAC (EtM): Data integrity is verified using HMAC-SHA3-512 covering the entire encrypted header and payload before the decryption process begins.
 * Stateful Lockout: Failed decryption 10 times (defined in MAX_FATAL_ATTEMPTS) will trigger a permanent lockout via an HMAC-encrypted state file in the user directory.
* Honeypot Logic: There is a hardcoded password (invitado_root) that, if entered, will cause the system to pretend to encrypt but only generate decoy data without touching the original data.
📦 Binary Container Structure (.ctx)
The encrypted file has a non-standard structure packaged using the following Python struct:
| Offset | Size (Bytes) | Description |
|---|---|---|
| 0 | 1 | Protocol Version (v160) |
| 1 | 32 | Salt (CSPRNG) |
| 33 | 24 | Nonce |
| 57 | 32 |  IV (Initialization Vector) |
| 89 | 4 | Number of Rounds (Big-endian) |
| 93 | 2 | Scrypt N (Log2) |
| 95 | 2 | PBKDF2 Iterations (/1000) |
| 97 | 1 | Key Length (dklen) |
| 98 | 2 | Block Size (bits) |
| 100 | Variables | Ciphertext (Payload) |
| -64 | 64 | HMAC-SHA3-512 (Integrity Tag) |
🛠️ Code Modules
* core/engine.py: Contains the main mathematical logic including block XOR functions, bit rotations, and engine transforms.
 * kdf/derive.py: Manages hardware identity extraction and key derivation chains.
* defense/mechanisms.py: Manages anti-tampering logic and authentication attempt management.
* tools/utils.py: Secure Shredding implementation using DoD 5220.22-M standard (3-pass overwrite with secrets.token_bytes).
🚀 Installation & Usage
* Ensure Python 3.8+ is installed.
* Clone the repository and run main.py.
* Adjust the security profile in the Settings menu:
* Bit Depth: 128 - 2048 bits.
* Rounds: Up to 2048 rounds (Higher numbers are slower).
* Shredding: Enable to permanently delete the original file after encryption.
 <!-- end list -->
python main.py

📝 Security Analysis (Self-Assessment)
* Strengths: Very robust against dictionary attacks due to the slow KDF and HWID binding.
* Weaknesses: As a custom block cipher, there may be gaps in bit diffusion if the number of rounds is set too low. No formally proven guarantee of Indistinguishability under Chosen Ciphertext Attack (IND-CCA2).
#cryptography #encryption #python #security #experimental #toy-crypto #infosec #ctf #coding
