# Methodology: Ransomware Simulation Lab

## 1. Introduction
This document outlines the step-by-step methodology used to simulate a ransomware attack in an isolated laboratory environment. The primary goal was to understand the lifecycle of a modern cyberattack, specifically focusing on the implementation of hybrid cryptography and the mechanics of file encryption and recovery.

## 2. Phase 1: Cryptographic Architecture
The simulation utilizes **Hybrid Encryption**, which is the standard for modern ransomware. Symmetric encryption (AES) is fast and used for file data, while asymmetric encryption (RSA) is used to securely protect the AES key.

### 2.1 Key Generation
*   A 2048-bit RSA key pair was generated.
*   The **Public Key** (`rsa_public.pem`) was designated for the victim environment (used to encrypt the AES key).
*   The **Private Key** (`rsa_private.pem`) was kept secure in the attacker environment (used to decrypt the AES key).

### 2.2 The Encryption Engine
The Python script (`encryption_engine.py`) executes the following sequence:
1.  Generates a random 256-bit AES session key.
2.  Encrypts the AES key using the RSA Public Key (with OAEP padding) and saves it to disk as `key.bin`.
3.  Iterates through designated test files.
4.  Encrypts each file using AES-256-GCM. A new 12-byte nonce is generated for every file.
5.  Overwrites the original file with the nonce and ciphertext, appending the `.locked` extension.

### 2.3 The Recovery Engine
The recovery process demonstrates cryptographic reversibility:
1.  The user provides the RSA Private Key via the GUI or CLI.
2.  The script decrypts `key.bin` to recover the original AES session key.
3.  The script iterates through all `.locked` files, extracts the nonce, decrypts the ciphertext using the AES key, and restores the original file extension.

## 3. Phase 2: Delivery and Execution Simulation
To demonstrate the broader attack lifecycle, a controlled delivery mechanism was simulated.
*   A benign Metasploit payload was generated to simulate initial access.
*   The payload was hosted on a local web server disguised as a legitimate software download (Social Engineering).
*   Upon execution in the Windows 10 VM, a reverse shell was established, allowing the attacker (Kali Linux) to upload the encryption engine and execute it remotely.

## 4. Phase 3: User Interface (Impact Simulation)
A Tkinter-based GUI (`impact_simulator_gui.py`) was developed to simulate the psychological impact of a ransomware attack. 
*   Features include a countdown timer, a simulated Bitcoin address (clearly marked as a lab), and a decryption input field.
*   The GUI handles error states (e.g., invalid key provided) and successful recovery states.

## 5. Safety Controls
*   The encryption engine explicitly ignores its own source code, the public key, and the GUI script to prevent self-corruption.
*   The script operates only within its current working directory, preventing accidental encryption of system files outside the lab scope.
*   All testing was conducted in Host-Only VMware network environments.