# Project Report: Secure File Simulation & Cryptographic Recovery

**Author:** Wael Balhoudi  
**Project:** Master's Cybersecurity Laboratory  
**Environment:** VMware (Kali Linux & Windows 10)  
**Date:** November 2026

---

## 1. Executive Summary
This report documents the development and execution of an isolated ransomware simulation laboratory. The primary objective was to understand the mechanics of modern ransomware by engineering a custom encryption engine utilizing hybrid cryptography (AES-256-GCM and RSA-2048). 

The project successfully demonstrated the complete attack lifecycle: from cryptographic key generation and social engineering delivery to remote code execution (via Metasploit) and endpoint encryption. Finally, the laboratory proved the cryptographic reversibility of the attack by successfully restoring all encrypted data using the corresponding RSA private key. 

---

## 2. Technical Implementation & Architecture

### 2.1 Hybrid Cryptographic Architecture
Modern ransomware rarely relies on a single encryption algorithm. To balance speed and secure key distribution, a hybrid architecture was implemented:
*   **AES-256-GCM (Symmetric):** Used for bulk file encryption. Galois/Counter Mode was selected because it provides both confidentiality and data authenticity (preventing tampering), operating at high speeds. A unique 12-byte nonce was generated for each file.
*   **RSA-2048 (Asymmetric):** Used to protect the AES session key. The AES key was encrypted using the RSA Public Key (with OAEP padding) and saved as `key.bin`. Without the RSA Private Key, the AES key cannot be recovered.

### 2.2 The Encryption Engine (`encryption_engine.py`)
The Python-based engine is designed to safely traverse a target directory. It explicitly ignores its own source code, the GUI script, and the public key to prevent self-corruption. It overwrites target files in place with the AES ciphertext and appends a `.locked` extension to signify impact.

### 2.3 The Impact Simulator GUI (`impact_simulator_gui.py`)
To simulate the user-facing psychological impact, a Tkinter graphical interface was developed. It mimics known ransomware families (like WannaCry) by displaying a prominent warning, a simulated Bitcoin payment address (clearly marked as a lab), and a live countdown timer. The GUI includes a decryption module that accepts the RSA Private Key via clipboard paste or a file-selection dialog.

---

## 3. Step-by-Step Laboratory Execution

The following steps detail the complete end-to-end execution of the laboratory.

### Phase 1: Cryptographic Key Generation
1.  Executed `gen_keys.py` on the Kali Linux attacker machine.
2.  The script generated a 2048-bit RSA key pair.
3.  The `rsa_public.pem` was prepared for deployment to the victim, while `rsa_private.pem` was securely moved to an `~/attacker` directory to simulate the attacker holding the decryption key.

### Phase 2: Social Engineering & Payload Delivery
1.  A Metasploit reverse TCP payload was generated using `msfvenom` and disguised as a legitimate software installer (`SuperGame_Setup.exe`).
2.  A fake website offering a "Super Game 2026" download was hosted via Python HTTP server on Kali (`python3 -m http.server 8000`).
3.  On the Windows 10 target, Windows Defender real-time protection and SmartScreen were deliberately disabled to simulate a vulnerable endpoint.
4.  The payload was downloaded and executed on the Windows VM.

### Phase 3: Command & Control (C2) & Remote Execution
1.  A Metasploit `multi/handler` listener was established on Kali (LHOST: 192.168.100.10, LPORT: 4444).
2.  Upon execution of the payload, a successful Meterpreter reverse shell session was established with `NT AUTHORITY\SYSTEM` privileges.
3.  Using the Meterpreter `upload` command, the `encryption_engine.py`, `impact_simulator_gui.py`, and `rsa_public.pem` were transferred directly to the victim's `C:\Users\waelb\Desktop\victim data` folder.

### Phase 4: Encryption & Impact
1.  Through the Meterpreter shell, the Python engine was executed: `python encryption_engine.py`.
2.  The engine generated a random AES session key, encrypted it with the RSA public key, and saved it as `key.bin`.
3.  All target files (`.txt`, `.pdf`, `.pptx`) were encrypted using AES-256-GCM and overwritten.
4.  The Tkinter GUI automatically triggered on the Windows desktop, displaying the simulated ransom note and countdown.

### Phase 5: Cryptographic Recovery
1.  On the GUI, the "Decrypt" button was selected.
2.  The `rsa_private.pem` file (held on Kali) was loaded into the interface.
3.  The GUI passed the key to the engine, which decrypted `key.bin` to recover the AES key.
4.  The AES key was used to decrypt all `.locked` files, restoring them to their original state, and the GUI displayed a success message.

---

## 4. Laboratory Challenges & Resolutions

During the lab, several technical hurdles were encountered and resolved:
*   **Windows Defender Interference:** The target OS actively blocked the payload and attempted to quarantine the encryption engine. This was resolved by configuring Defender exclusions and disabling SmartScreen, highlighting the importance of endpoint security.
*   **GUI Clipboard Limitations:** Tkinter does not natively support `Ctrl+V` for clipboard paste in all Linux/Windows environments. This was resolved by implementing a right-click context menu and a "Load from File" button.
*   **Windows Path Constraints:** Initial testing revealed that Windows does not permit filenames ending with a period (e.g., `key.`). The architecture was adjusted to use `key.bin`.

## 5. Defensive Insights
Conducting this simulation provided critical insights into defensive strategies:
*   **User Awareness:** Social engineering remains the most effective initial access vector. Training users to recognize fake download pages is critical.
*   **EDR/AV Efficacy:** Windows Defender successfully blocked the initial payload until manually bypassed, proving the value of real-time protection.
*   **Backup Strategy:** Because the encryption is cryptographically sound, data recovery without the RSA private key is impossible. Offline, immutable backups are the only reliable defense against data loss.

## 6. Future Work
Future iterations of this project will focus on detection engineering. Specifically:
*   Integrating Sysmon for Windows to monitor file creation and modification events.
*   Deploying Wazuh SIEM to ingest Sysmon logs and trigger alerts on rapid `.locked` file extensions.
*   Evaluating the encryption and recovery performance on larger datasets.

---
*Disclaimer: This project was conducted strictly for educational and research purposes within an isolated virtual environment. No real systems were harmed, and no actual ransom was requested.*
