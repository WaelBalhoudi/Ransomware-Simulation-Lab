# 🏗️ Secure File Simulation Lab — Architecture

## 1. Overview

This document describes the technical architecture of the Secure File Simulation Lab, an isolated cybersecurity laboratory designed to demonstrate file encryption, hybrid cryptography, controlled attack-lifecycle concepts, and defensive security analysis.

The environment uses VMware virtual machines connected through a Host-Only network. All experiments are intended for authorized educational testing within this isolated environment.

> ⚠️ **Educational use only:** This project is a controlled simulation. It is not intended for deployment against real systems or unauthorized targets.

---

## 2. Laboratory Environment

The laboratory consists of two primary virtual machines.

| Component | Attacker VM | Target VM |
|---|---|---|
| Operating system | Kali Linux | Windows 10 |
| Role | Testing and simulation | Test environment |
| Virtualization | VMware | VMware |
| Network interface | Host-Only | Host-Only |
| Main tools | Python, Metasploit | Python, Tkinter |

### Network configuration

| Parameter | Configuration |
|---|---|
| Network type | VMware Host-Only |
| Network address | `192.168.100.0/24` |
| Kali Linux IP | `192.168.100.10` |
| Windows 10 IP | `WINDOWS_VM_IP` |
| Network purpose | Isolated laboratory communication |

Replace `WINDOWS_VM_IP` with the actual address obtained using `ipconfig` inside the Windows VM.

---

## 3. Network Topology

The following diagram illustrates the laboratory architecture and the main stages of the simulation.

![Secure File Simulation Lab Network Topology](screenshots/architecture.png)

*Figure 1 — Network topology and simulation workflow.*

### Network communication

The two virtual machines communicate through the VMware Host-Only virtual network.

- **Kali Linux:** Hosts the laboratory scripts and testing tools.
- **Windows 10:** Provides the controlled target environment for file-encryption experiments.
- **VMware Virtual Switch:** Provides communication between the virtual machines.
- **Host-Only Network:** Isolates laboratory traffic from the external physical network.

The actual network isolation must be verified in VMware settings. A Host-Only adapter alone does not guarantee that every other network interface is disconnected.

---

## 4. System Components

### 4.1 Kali Linux — Testing Environment

Kali Linux is used as the laboratory testing platform.

Main components:

- Python 3 for simulation scripts.
- Cryptography library for cryptographic operations.
- Metasploit Framework for the authorized remote-session demonstration.
- Local web server for the controlled delivery experiment.

### 4.2 Windows 10 — Test Environment

Windows 10 acts as the laboratory endpoint.

Main components:

- Python runtime.
- Tkinter graphical interface.
- Test files used for encryption experiments.
- Encrypted files using the `.locked` extension.
- Laboratory monitoring and observation tools, where configured.

---

## 5. Cryptographic Architecture

The simulation demonstrates hybrid encryption by combining symmetric and asymmetric cryptography.

### 5.1 AES-256-GCM

AES-256-GCM is used for file encryption.

| Parameter | Value |
|---|---|
| Algorithm | AES |
| Key size | 256 bits |
| Mode | Galois/Counter Mode |
| Nonce size | 96 bits (12 bytes) |
| Authentication | Integrated authentication tag |

AES-GCM provides confidentiality and integrity verification. Decryption fails if the ciphertext, authentication tag, associated data, or required parameters are incorrect.

### 5.2 RSA-2048

RSA is used to protect the AES encryption key.

| Parameter | Value |
|---|---|
| Algorithm | RSA |
| Key size | 2048 bits |
| Public key | Used to protect the AES key |
| Private key | Used to recover the AES key |

The private key must remain confidential. For a secure implementation, RSA-OAEP with an appropriate hash function should be used for key wrapping.

### 5.3 Encryption workflow

1. Generate a cryptographically secure random AES-256 key.
2. Generate a unique 12-byte nonce for AES-GCM.
3. Encrypt the selected laboratory file.
4. Protect the AES key using the RSA public key.
5. Store the ciphertext, nonce, authentication tag, and protected AES key in the required format.

### 5.4 Recovery workflow

When implemented and validated, the recovery process consists of:

1. Load the corresponding RSA private key.
2. Recover the AES encryption key.
3. Retrieve the nonce and authentication tag.
4. Decrypt the encrypted file using AES-GCM.
5. Compare the recovered file's SHA-256 hash with the original file's hash.

**Important:** A recovery workflow should only be described as successfully implemented after an actual decryption test and integrity comparison have been completed.

---

## 6. Simulation Workflow

The laboratory experiment is organized into six phases.

| Phase | Description |
|---|---|
| 01 | Cryptographic key generation |
| 02 | Hybrid encryption implementation |
| 03 | Controlled delivery simulation |
| 04 | Authorized remote-session demonstration |
| 05 | File encryption and impact analysis |
| 06 | Cryptographic recovery and integrity validation |

The phases are intended to demonstrate the relationship between cryptographic mechanisms, endpoint activity, and security monitoring.

---

## 7. Security Considerations

The following precautions apply to the laboratory:

- Use dedicated virtual machines.
- Keep the experiment isolated from production networks.
- Use disposable test files rather than personal or important data.
- Keep private cryptographic keys protected.
- Use unique nonces for AES-GCM encryption.
- Preserve original test files and backups.
- Verify file integrity using SHA-256.
- Restore normal endpoint security settings after testing.
- Document any limitations or incomplete experiment phases.

---

## 8. Future Improvements

Potential extensions include:

- Integrating Sysmon for Windows endpoint telemetry.
- Integrating Wazuh for centralized security monitoring.
- Developing behavioral detection rules.
- Monitoring suspicious file modification patterns.
- Measuring encryption and recovery performance.
- Implementing and validating a complete recovery mechanism.
- Developing an incident response and backup strategy.

---

## 9. References

- [NIST — Advanced Encryption Standard (AES)](https://csrc.nist.gov/pubs/fips/197/final)
- [NIST — Galois/Counter Mode (GCM)](https://csrc.nist.gov/pubs/sp/800/38/d/final)
- [NIST — RSA Key Establishment](https://csrc.nist.gov/pubs/sp/800/56/b/r2/final)
- [Python Cryptography Documentation](https://cryptography.io/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Wazuh Documentation](https://documentation.wazuh.com/)

---

**Project:** Secure File Simulation Lab  
**Author:** Wael Balhoudi  
**Academic context:** Master's Cybersecurity Laboratory  
**Purpose:** Educational and Research Use Only