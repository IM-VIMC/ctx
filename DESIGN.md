# CTX-X: Design Specification

This document outlines the technical architecture and cryptographic implementation of **CTX-X Titanium**, a file encryption utility built with Python. It utilizes a custom Feistel Network structure and a multi-layered key derivation scheme.

---

## 1. Cryptographic Architecture

### 1.1 Key Derivation Function (KDF)
To mitigate brute-force and dictionary attacks, CTX-X employs a three-stage pipeline to derive the master key:

1.  **Pre-Hashing**: Combines the user password, Hardware ID (if enabled), a static `VESSEL_KEY`, and a 32-bit CSPRNG `salt` using **Blake2b**.
2.  **Memory-Hard Stretching**: The initial hash is processed via **Scrypt** ($N=2^{14}, r=8, p=1$) to provide resistance against hardware acceleration (ASIC/GPU).
3.  **Final Extraction**: The Scrypt output is passed through **PBKDF2-HMAC-SHA512** with a high iteration count (default: 600,000) to generate the final symmetric keys.

### 1.2 The Encryption Engine
The core engine utilizes a configurable **Feistel Network** construction:

* **Block Size**: Variable/Configurable (ranging from 128-bit to 2048-bit).
* **Round Function ($F$):**
    * **Dynamic S-Box**: Generated uniquely for every session using the master key and salt via the **SHAKE-256** XOF (Extendable-Output Function).
    * **MDS Matrix Diffusion**: Implements a linear transformation (similar to the AES MixColumns step) to ensure rapid bit diffusion within a block.
    * **Bitwise Rotation**: Dynamic left-rotation based on the round index to break linearity.
* **Mode of Operation**: A custom implementation resembling **Cipher Block Chaining (CBC)**, where each block is XORed with the previous ciphertext block to prevent pattern leakage.

### 1.3 Integrity and Authentication
The system follows the **Encrypt-then-MAC (EtM)** paradigm:
* After encryption, the entire container (header + ciphertext) is hashed using **HMAC-SHA3-512**.
* The authentication key is logically separated from the encryption key using a dedicated **Blake2b** derivation.
* Integrity is verified *before* decryption to prevent padding oracle attacks or unauthorized data manipulation.

---

## 2. Defense Mechanisms

### 2.1 Hardware Binding (HWID)
When `hwid_bind` is enabled, the encryption key is cryptographically tied to the device's hardware signature (Machine GUID on Windows or Machine-ID on Linux). This ensures that files cannot be decrypted on a different machine, even with the correct password.

### 2.2 Anti-Tamper & Security Lockout
* **State Tracking**: Login failure counts are stored in a hidden state file protected by an HMAC tag to prevent manual tampering.
* **Exponential Delay**: After 3 failed attempts, a 300-second lockout timer is enforced.
* **Fatal Shredding**: Upon reaching the maximum failure threshold (`MAX_FATAL_ATTEMPTS`), the system can be configured to delete the target file or clear security states to protect data from physical brute-force.

### 2.3 Honeypot Password
The system includes a decoy password mechanism. If the decoy password is used, the system simulates a successful decryption process but produces randomized "decoy" data, intended to mislead an adversary in duress scenarios.

---

## 3. Container Format (Binary Structure)

The `.ctx` file is structured as follows:

| Offset | Size | Description |
| :--- | :--- | :--- |
| 0 | 1 Byte | Protocol Version (e.g., v160) |
| 1 | 32 Bytes | Salt (CSPRNG) |
| 33 | 24 Bytes | Nonce |
| 57 | 32 Bytes | IV (Initialization Vector) |
| 89 | 4 Bytes | Round Count (Big-Endian) |
| 93 | 2 Bytes | Scrypt N Parameter |
| 95 | 2 Bytes | PBKDF2 Iterations / 1000 |
| 97 | 1 Byte | DKLen (Derived Key Length) |
| 98 | 2 Bytes | Bit Size (Block Width) |
| 100 | Variable | Ciphertext (Encrypted Data) |
| -64 | 64 Bytes | HMAC-SHA3-512 Tag (Integrity) |

---

## 4. Technical Limitations & Security Notes

* **Implementation Language**: As this is implemented in high-level Python, it is not hardened against advanced CPU-level side-channel timing attacks.
* **Secure Shredding**: The 3-pass DoD-standard shredding overwrites data with random bits. However, its effectiveness on SSDs and NVMe drives is limited by modern Flash Translation Layer (FTL) wear-leveling algorithms.
* **Cryptographic Status**: The custom Feistel construction is designed for educational and personal utility; it has not undergone formal third-party cryptanalysis.

---
*This document is provided for transparency and auditing purposes.*

---

## Threat Model (Non-Exhaustive)

CTX-X is designed to resist:
- Offline brute-force attacks
- Casual data tampering
- Unauthorized decryption on foreign devices

CTX-X does NOT claim resistance against:
- Adaptive chosen-ciphertext attacks (CCA2)
- Side-channel attacks
- Nation-state adversaries
