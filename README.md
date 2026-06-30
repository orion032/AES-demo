Python-AES
==========

A pure Python implementation of the Advanced Encryption Standard (AES) algorithm as defined in FIPS-197, with PKCS#7 padding support. This implementation is compatible with Python 2.7+ and Python 3.6+.

## ⚠️ Important Warning

**This code is for educational and recreational purposes ONLY.** It is **NOT recommended for secure systems**. For production encryption, use established cryptographic libraries like [`cryptography`](https://cryptography.io/) or [`PyCryptodome`](https://www.dlitz.net/software/pycryptodome/).

## Features

- Pure Python implementation with no external dependencies
- Supports AES-128, AES-192, and AES-256
- PKCS#7 padding support
- File-based encryption and decryption
- FIPS-197 test vectors included
- Python 2 and Python 3 compatible
- Educational focus with clear code structure

## Installation

### Option 1: Direct Usage
```bash
git clone https://github.com/orion032/AES-demo.git
cd AES-demo
python AES.py -demo
```

### Option 2: Install as Package
```bash
git clone https://github.com/orion032/AES-demo.git
cd AES-demo
pip install -e .
```

### Requirements
- Python 2.7+ or Python 3.6+
- No external dependencies (uses only standard library)

## Quick Start (Easiest for Beginners!)

### Interactive Wizard Mode 🧙

```bash
python AES.py --wizard
```

This launches a step-by-step guide that walks you through:
- Selecting files to encrypt/decrypt
- Choosing encryption strength
- Generating or entering keys
- Complete encryption/decryption

**Perfect if you're new to encryption!**

---

## Usage

### Standard Commands

#### Run Interactive Wizard (Beginner-Friendly)
```bash
python AES.py --wizard
# or
python AES.py -w
# or 
python wizard.py
```

### Run Demo (Test Vectors)
```bash
python AES.py -demo
```

### Encrypt a File (Command Line)
```bash
python AES.py -e <input_file> [-c (128|192|256)]
```

Example:
```bash
python AES.py -e document.txt -c 128
```

You will be prompted to enter a hexadecimal encryption key:
```
Enter encryption key (32 hex digits, or press Enter for zeros): 
```

The encrypted file will be saved as `document.txt.aes`

### Decrypt a File (Command Line)
```bash
python AES.py -d <input_file> [-c (128|192|256)]
```

Example:
```bash
python AES.py -d document.txt.aes -c 128
```

### Key Size Options

- `-c 128` - AES-128 (128-bit key = 32 hex digits) [default]
- `-c 192` - AES-192 (192-bit key = 48 hex digits)
- `-c 256` - AES-256 (256-bit key = 64 hex digits)

### Example Hexadecimal Keys

**128-bit (32 hex digits):**
```
000102030405060708090a0b0c0d0e0f
```

**256-bit (64 hex digits):**
```
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
```

### Get Help
```bash
python AES.py --help
python AES.py -h
```

## Module Structure

- `AES.py` - Main encryption/decryption implementation with CLI interface
- `AES_base.py` - S-Box tables and Galois Field lookup tables
- `ProgressBar.py` - Progress indicator for large file processing
- `wizard.py` - Interactive step-by-step guide (beginner-friendly)
- `TUTORIAL.md` - Comprehensive learning guide with examples

## Learning Resources

📚 **For complete beginners:** Start with [TUTORIAL.md](TUTORIAL.md)

📖 **Quick visual guide:**
```bash
python AES.py --wizard
```

🧪 **See it in action:**
```bash
python AES.py -demo
```

## How It Works

The implementation follows the FIPS-197 standard:

1. **SubBytes** - Non-linear byte substitution using S-box
2. **ShiftRows** - Shifting rows of the state array
3. **MixColumns** - Mixing data within each column
4. **AddRoundKey** - XOR operation with round key

For decryption, the inverse operations are applied in reverse order.

## Example Code

```python
from AES import Cipher, KeyExpansion, process_key, process_block, prepare_block

# Setup
plaintext = "Hello World!!!!!"
key_hex = "0f0e0d0c0b0a09080706050403020100"  # 128-bit key

Nb = 4
Nk = 4
Nr = 10

# Process key
key = process_key(key_hex, Nk)
expanded_key = KeyExpansion(key, Nb, Nk, Nr)

# Encrypt
block = process_block(plaintext.encode('utf-8')[:16], Nb)
ciphertext_block = Cipher(block, expanded_key, Nb, Nk, Nr)
ciphertext = prepare_block(ciphertext_block)

print("Ciphertext:", ciphertext.hex())
```

## References

- FIPS-197 (Federal Information Processing Standards Publication 197)
- [Python-AES-base](https://github.com/pcaro90/Python-AES-base/) - Table generation
- [Rijndael Cipher](https://en.wikipedia.org/wiki/Rijndael)

## License

See [LICENSE](LICENSE) file for details.

Original implementation by Pablo Caro
Improvements and updates maintained at https://github.com/orion032/AES-demo

