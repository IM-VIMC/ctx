# Disclaimer

**Please read this disclaimer carefully before using CTX-X**

## 1. "As-Is" Basis
This software is provided "as is" and "with all faults." The author makes no representations or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracies, typographical errors, or other harmful components of this software. There are inherent dangers in the use of any software, and you are solely responsible for determining whether **CTX-X Titanium** is compatible with your equipment and other software installed on your equipment.

## 2. Experimental Cryptography
**CTX-X** utilizes a custom-designed Feistel Network and a proprietary container format. While it incorporates industry-standard primitives (such as Scrypt, PBKDF2, SHA-3, and Blake2b), the overall assembly has not undergone formal academic or professional third-party cryptanalysis. 
* This tool is intended for **educational, research, and personal utility purposes**.
* It should **not** be used to secure data of extreme sensitivity, high financial value, or in life-critical systems.

## 3. Risk of Data Loss
Encryption is a double-edged sword. You acknowledge that:
* **Forgotten Passwords**: If you forget your Master Password, your data is **permanently irretrievable**. There are no backdoors or recovery mechanisms.
* **Corrupted Files**: Any manual modification to the `.ctx` file (even a single bit change) will result in a failed HMAC verification, rendering the file undecryptable to prevent tampering.
* **Hardware Binding**: If the `hwid_bind` feature is enabled and your hardware fails or you reinstall your Operating System (changing the Machine GUID), you may lose access to your encrypted files.

## 4. Technical Limitations
* **Side-Channel Attacks**: Because this software is written in Python, it is not hardened against timing attacks or power analysis.
* **Secure Shredding**: The "Secure Shred" feature follows the DoD 5220.22-M standard; however, its effectiveness on modern SSDs and NVMe drives is not guaranteed due to hardware-level wear leveling.
* **Memory Safety**: Python’s garbage collection may leave traces of keys or plaintext in volatile memory (RAM) for a duration after the program has finished a task.

## 5. Legal Compliance
The use and export of encryption software are subject to various laws and regulations depending on your jurisdiction. It is your responsibility to ensure that your use of **CTX-X Titanium** complies with all local, state, and international laws.

---
**By using this software, you agree to assume all risks associated with its use and waive any claims against the developers for any damages, including data loss or security compromises.**

*This project is classified as toy-crypto and should not be compared to audited cryptographic standards such as AES, ChaCha20, or RSA*
