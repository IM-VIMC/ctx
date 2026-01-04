# 🛡️ CTX  (v1)
### *Experimental Block Cipher Utility & Cryptographic Playground*

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-experimental-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**CTX-X** is a Python-based experimental cryptographic utility (toy-crypto) designed around a custom **Feistel Network** architecture. This project serves as a research platform for exploring memory-hard key derivation, hardware-bound security, and active anti-tamper mechanisms.

> [!CAUTION]
> **EXPERIMENTAL STATUS:** This software is not intended for production use or securing sensitive data. It has not undergone formal cryptanalysis (differential/linear analysis). Use strictly for educational and research purposes.

---

## 🏗️ Core Architecture Specifications

The system operates on a **dynamic block level**, allowing flexible configurations from **128-bit to 2048-bit** block sizes.

### 1. Feistel Network & F-Function
The cipher utilizes a classic Feistel structure with a heavily modified internal F-Function to maximize diffusion and confusion:

| Component | Technical Implementation |
| :--- | :--- |
| **Dynamic S-Box** | Unlike static AES tables, this project generates a unique 256-byte substitution table per session using `SHAKE_256` of the master key and salt. |
| **MDS Matrix** | Implements linear transformations (`_mc2` and `_mc3`) to ensure optimal bit diffusion within the f-function, inspired by the *MixColumns* structure. |
| **Bitwise Rotation (ROL)** | A circular bit shift that varies dynamically based on the round index to disrupt data symmetry. |

### 2. Advanced Key Derivation Function (KDF)
To mitigate offline brute-force and ASIC/FPGA acceleration, the key schedule follows a multi-phase, computationally expensive chain:

* **Entropy Input:** Password + HWID (Hardware ID) + Static `VESSEL_KEY`.
* **Phase I (Pre-Hash):** **Blake2b** hashing (64-byte digest).
* **Phase II (Memory-Hard):** **Scrypt** processing with parameters $N=2^{14}, r=8, p=1$.
* **Phase III (Stretching):** **PBKDF2-HMAC-SHA512** for **600,000 rounds**.

---

## 🛡️ Integrated Defense Mechanisms

CTX-X Titanium goes beyond standard encryption by implementing active layers of security:

* **Hardware-Binding (HWID):** Uses `wmic` (Windows) or `machine-id` (Linux) to bind the decryption capability to a specific machine.
* **Encrypt-then-MAC (EtM):** Full-payload integrity verification using **HMAC-SHA3-512** before decryption begins.
* **Stateful Lockout:** Tracks failed attempts. Exceeding `MAX_FATAL_ATTEMPTS` (10) triggers a permanent lockout via an HMAC-encrypted state file.
* **Honeypot Logic:** Using the master password `invitado_root` triggers "Decoy Mode"—the system pretends to encrypt/decrypt but only generates junk data, leaving original files untouched.

---

## 📦 Binary Container Structure (`.ctx`)

The encrypted output is packaged into a custom binary format using Python's `struct` module:

| Offset | Size (Bytes) | Field Description |
| :--- | :--- | :--- |
| 0 | 1 | Protocol Version (v160) |
| 1 | 32 | Salt (CSPRNG generated) |
| 33 | 24 | Nonce |
| 57 | 32 | IV (Initialization Vector) |
| 89 | 4 | Number of Rounds (Big-endian) |
| 93 | 2 | Scrypt N (Log2) |
| 95 | 2 | PBKDF2 Iterations (/1000) |
| 97 | 1 | Key Length (dklen) |
| 98 | 2 | Block Size (bits) |
| 100 | Variable | **Ciphertext (Payload)** |
| -64 | 64 | **HMAC-SHA3-512 (Integrity Tag)** |

---

## 🛠️ Project Structure

* 📂 `core/engine.py`: Core mathematical logic, block XOR, and bitwise transformations.
* 📂 `kdf/derive.py`: HWID extraction and the multi-stage key derivation chain.
* 📂 `defense/mechanisms.py`: Anti-tampering logic, lockout states, and honeypot triggers.
* 📂 `tools/utils.py`: Secure file shredding (DoD 5220.22-M standard: 3-pass overwrite).

---

## 🚀 Installation & Usage

1.  **Prerequisites:** Python 3.8+
2.  **Clone & Run:**
    ```bash
    git clone [https://github.com/IM-VIMC/ctx.git](https://github.com/IM-VIMC/ctx)
    cd ctx
    python main.py
    ```
3.  **Security Profile Setup:**
    * **Bit Depth:** Choose between 128 and 2048 bits.
    * **Rounds:** Configure up to 2048 rounds (Warning: High round counts impact performance).
    * **Shredding:** Toggle to permanently delete source files after processing.

---

## 📝 Security Self-Assessment

| Strengths | Weaknesses |
| :--- | :--- |
| **KDF Hardness:** Extremely resistant to dictionary attacks due to Scrypt + high PBKDF2 iterations. | **No Formal Proof:** Not proven to be IND-CCA2 secure. |
| **Portability Protection:** HWID binding prevents decryption on unauthorized devices. | **Side-Channels:** Python implementation is not constant-time; vulnerable to timing attacks. |
| **Integrity First:** EtM prevents "padding oracle" style attacks on the ciphertext. | **Diffusion Risk:** Custom MDS matrix has not been mathematically verified for all block sizes. |

---

### 🏷️ Keywords
`#cryptography` `#encryption` `#python` `#security` `#experimental` `#toy-crypto` `#infosec` `#feistel-cipher`
