# Security Policy

## 1. Supported Versions

Security updates and bug fixes are currently provided only for the latest stable release of CTX-X Titanium.

| Version | Supported |
| :--- | :--- |
| v1.0.0 | ✅ Supported |
| < v 0 | ❌ No Longer Supported |

## 2. Reporting a Vulnerability

We take the security of user data seriously. If you discover a vulnerability, please follow these steps:

1.  **Do not open a public Issue** for security-related bugs.
2.  Submit a detailed report to [daviddaryanto2@gmail.com].
3.  Include technical details such as reproduction steps, proof-of-concept (PoC) code, and the potential impact.
4.  We aim to provide an initial response within 48-72 hours.

## 3. Threat Model & Technical Limitations

To ensure proper use of this tool, users and auditors must understand the following technical constraints:

### 3.1 Memory Safety
As this utility is implemented in **Python**, it does not have low-level control over memory management. Sensitive data (such as raw keys or plaintext) may reside in RAM longer than intended before being cleared by the Python Garbage Collector. This tool is not designed for environments highly susceptible to **Cold Boot attacks**.

### 3.2 Side-Channel Attacks
High-level implementations of cryptographic algorithms in Python are generally not resistant to **Timing Side-Channel attacks**. An adversary with microsecond-level timing capabilities may be able to extract information about the key or internal state.

### 3.3 Secure Shredding (SSDs/NVMe)
The `secure_shred` feature implements a 3-pass DoD 5220.22-M overwrite. However, on modern flash storage (**SSDs/NVMe**), its effectiveness is limited by the **Flash Translation Layer (FTL)** and wear-leveling algorithms, which may move data physically without actually overwriting the original blocks.

### 3.4 Hardware Binding (HWID)
The HWID binding relies on OS-level identifiers (Machine GUID/Machine-ID). While this prevents simple file movement between devices, it does not protect against an attacker with root/administrative access who can spoof hardware signatures.

## 4. Security Best Practices

* **Password Entropy**: The security of your data relies entirely on the strength of your master password. Use at least 12-16 random characters.
* **Decoy Password**: Use the `HONEY_PWD` feature cautiously. It is designed to mislead in duress scenarios but does not protect the actual data.
* **Trusted Environment**: Only run this software on a trusted Operating System. A compromised OS with a keylogger will bypass all cryptographic protections.

---
*Security is a process, not a product. Please use this tool responsibly.*
