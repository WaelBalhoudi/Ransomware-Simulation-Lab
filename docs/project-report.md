# Project Report: Ransomware Simulation & Cryptographic Recovery

**Author:** Wael Balhoudi  
**Project:** Master's Cybersecurity Laboratory  
**Date:** November 2026

## 1. Executive Summary
This report details the development and execution of a ransomware simulation lab. The project successfully demonstrated the implementation of hybrid cryptography (AES-256-GCM and RSA-2048) to encrypt files, combined with a simulated social engineering delivery mechanism. The experiment concluded with the successful cryptographic recovery of all encrypted data using the corresponding RSA private key.

## 2. Technical Implementation

### 2.1 AES-256-GCM
AES in Galois/Counter Mode (GCM) was chosen for file encryption due to its speed and authenticated encryption properties. This ensures both the confidentiality of the file data and the integrity of the ciphertext, preventing tampering. A unique 12-byte nonce was generated for every file to prevent cryptographic reuse.

### 2.2 RSA-2048 Protection
To simulate the extortion mechanism (where a victim cannot recover files without paying), the AES key was encrypted using an RSA-2048 public key. Without the corresponding private key, the AES key (and therefore the files) cannot be recovered.

### 2.3 The GUI Interface
The Tkinter interface was designed to mimic known ransomware families (like WannaCry) to demonstrate the user-facing impact. It included a live countdown timer and a key-loading mechanism that was tested for usability (including clipboard integration and file-loading fallback).

## 3. Attack Lifecycle Demonstration
The lab demonstrated the full lifecycle:
1.  **Initial Access:** A simulated payload was downloaded and executed via social engineering.
2.  **Command & Control:** A Metasploit Meterpreter session was established.
3.  **Execution:** The encryption script was uploaded and executed silently in the background.
4.  **Impact:** Target files were overwritten with ciphertext and renamed.
5.  **Recovery:** The RSA private key was supplied, and all files were successfully restored.

## 4. Defensive Insights
Conducting this lab highlighted several critical defensive measures:
*   **Endpoint Protection:** Antivirus and SmartScreen were highly effective at blocking the initial payload download and execution, requiring deliberate bypasses in the lab.
*   **User Awareness:** The social engineering webpage demonstrated how easily users can be tricked into downloading malicious executables.
*   **Cryptographic Recovery:** Emphasized the absolute necessity of offline, immutable backups, as file recovery without the RSA private key is cryptographically impossible.

## 5. Future Work
Future iterations of this lab will integrate SIEM solutions (such as Wazuh) and EDR tools to analyze the behavioral footprint of the encryption process. Specifically, monitoring for rapid file modifications, extension changes, and unusual cryptographic API calls (e.g., Windows CryptoAPI) will be evaluated for detection efficacy.

---
*Disclaimer: This project was conducted strictly for educational purposes within an isolated virtual environment. No actual systems were harmed.*