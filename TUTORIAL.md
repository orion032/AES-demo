# AES Encryption Tool - Quick Start Tutorial

Welcome! This guide teaches you how to use the AES encryption tool step by step.

## What is AES?

AES (Advanced Encryption Standard) is a widely-used encryption method that scrambles your files so only someone with the correct key can read them.

**Think of it like a safe:**
- Your file is the valuables
- Your key is the combination
- Encryption locks the safe
- Decryption opens it (if you have the key)

## Installation

### Step 1: Get the code
```bash
git clone https://github.com/orion032/AES-demo.git
cd AES-demo
```

### Step 2: Verify it works
```bash
python AES.py -demo
```

You should see test results with ✓ marks showing the encryption works correctly.

---

## Basic Usage: Encrypt Your First File

### Interactive Wizard Mode (Easiest!)

```bash
python AES.py --wizard
```

This will guide you through every step with prompts.

**Example session:**
```
╔════════════════════════════════════╗
║   AES Encryption Tool - Wizard     ║
╚════════════════════════════════════╝

What would you like to do?
1. Encrypt a file
2. Decrypt a file
3. View demo
4. Exit

Your choice: 1

File to encrypt: myfile.txt
✓ Found: myfile.txt

Choose key size:
1. 128-bit (faster, adequate)
2. 192-bit 
3. 256-bit (most secure)

Your choice: 1

Enter encryption key (or press Enter for random key):
[Generating secure random key...]
✓ Key: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

Processing...
[████████████████████] 100%

✓ Success! Encrypted file: myfile.txt.aes

Your key (save this in a safe place!):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Common Tasks

### Task 1: Encrypt a Document

**Scenario:** You want to encrypt `secret.docx` with a 256-bit key

```bash
python AES.py --wizard
# Follow prompts → choose "Encrypt" → select file → choose 256-bit → enter key
```

**Or use command line:**
```bash
python AES.py -e secret.docx -c 256
# Then type your key when prompted
```

### Task 2: Share an Encrypted File

1. **Encrypt the file:**
```bash
python AES.py -e report.xlsx -c 128
```

2. **Send these two things to recipient:**
   - The `.aes` file (the encrypted data)
   - The key separately (via secure channel like Signal/Telegram)

3. **Recipient decrypts:**
```bash
python AES.py -d report.xlsx.aes -c 128
# Then paste in the key they received
```

### Task 3: Create a Backup

```bash
# Encrypt with a strong key you'll remember
python AES.py -e backup_data.tar.gz -c 256

# Save the key somewhere safe (password manager, paper, etc.)
# Store the .aes file anywhere (cloud, external drive, etc.)

# To restore later:
python AES.py -d backup_data.tar.gz.aes -c 256
```

---

## Understanding Keys

### What's a Key?

A key is a long string of random characters (hexadecimal digits: 0-9, a-f).

### Key Sizes

| Size | Hex Digits | Security | Speed | Use Case |
|------|-----------|----------|-------|----------|
| 128-bit | 32 | Good | Fast | Personal files, everyday use |
| 192-bit | 48 | Better | Medium | Sensitive documents |
| 256-bit | 64 | Excellent | Slower | Highly confidential data |

### Example Keys

**128-bit (32 hex chars):**
```
0f0e0d0c0b0a09080706050403020100
```

**256-bit (64 hex chars):**
```
0f0e0d0c0b0a09080706050403020100101112131415161718191a1b1c1d1e1f
```

### Choosing a Good Key

❌ **DON'T:**
- Use simple patterns: `aaaaaaaa...` or `12345678...`
- Use dictionary words
- Reuse passwords

✓ **DO:**
- Use random characters: `7f3a9e2c1b4d8e5f6a3c2b1e9d7c4a2f`
- Generate with online tools (offline!) or use `/dev/urandom`
- Store securely (password manager, encrypted file, etc.)
- Use a new key for each file (optional but safer)

---

## Workflow Examples

### Example 1: Personal Use
```bash
# Create a text file
echo "My secret diary entry" > diary.txt

# Encrypt it
python AES.py -e diary.txt -c 128

# Save key in password manager
# Delete original file:
del diary.txt

# Later, to read it:
python AES.py -d diary.txt.aes -c 128
# [paste key from password manager]
```

### Example 2: Team Collaboration
```bash
# Alice encrypts a report
python AES.py -e quarterly_report.pdf -c 256

# Alice sends:
# 1. quarterly_report.pdf.aes via email
# 2. Key via separate secure message (Signal/Phone)

# Bob decrypts it
python AES.py -d quarterly_report.pdf.aes -c 256
# [pastes key]
```

### Example 3: Cloud Backup
```bash
# Encrypt before uploading to cloud
python AES.py -e family_photos.zip -c 256

# Upload family_photos.zip.aes to Google Drive/OneDrive/etc
# Keep key in local password manager

# If you lose your computer:
# 1. Download family_photos.zip.aes from cloud
# 2. Get key from password manager backup
# 3. Decrypt it
python AES.py -d family_photos.zip.aes -c 256
```

---

## Troubleshooting

### "File not found"
- Check the file name spelling
- Make sure you're in the right directory
- Use full path: `python AES.py -e /full/path/to/file.txt -c 128`

### "Invalid key" or "Key must be hexadecimal"
- Keys only use 0-9 and a-f characters
- Don't include spaces or special characters
- Check you copied the key correctly

### "Wrong key" during decryption
- Make sure it's the EXACT same key used to encrypt
- Keys are case-insensitive (A=a) but hex characters matter
- Decrypted file will be corrupted if key is wrong

### File seems corrupted after decryption
- You used the wrong key
- The .aes file was corrupted during transfer
- Decryption failed (error should show above)

---

## Security Tips

1. **Keep keys safe**
   - Use a password manager (Bitwarden, 1Password, etc.)
   - Never share keys via email unencrypted
   - Don't store key in same location as encrypted file

2. **For highly sensitive data**
   - Use 256-bit keys
   - Use different key for each file
   - Store backup keys offline (paper, in safe, etc.)

3. **Before sharing encrypted file**
   - Test decryption yourself first
   - Send key through different channel than file
   - Tell recipient which key size you used

4. **Long-term storage**
   - Keep copies of keys (redundancy)
   - Test decryption every few years (just to be sure)
   - Don't rely on memory - write it down!

---

## Advanced: Batch Operations

**Encrypt multiple files:**
```bash
# PowerShell
Get-ChildItem *.txt | ForEach-Object { python AES.py -e $_.Name -c 128 }

# Bash
for file in *.txt; do python AES.py -e "$file" -c 128; done
```

**Decrypt multiple files:**
```bash
# PowerShell
Get-ChildItem *.aes | ForEach-Object { python AES.py -d $_.Name -c 128 }

# Bash
for file in *.aes; do python AES.py -d "$file" -c 128; done
```

---

## Command Reference

```bash
# Run interactive wizard (easiest for beginners!)
python AES.py --wizard

# Run test/demo
python AES.py -demo

# Encrypt (legacy)
python AES.py -e <file> -c <128|192|256>

# Decrypt (legacy)
python AES.py -d <file> -c <128|192|256>

# Show help
python AES.py --help
python AES.py -h
```

---

## Key Takeaways

✓ Use `--wizard` mode if you're new
✓ Choose 128-bit for everyday, 256-bit for sensitive data
✓ Never lose your key!
✓ Store key separately from encrypted file
✓ Test decryption after encryption (to confirm it works)

---

**Need help?** Check the README.md or view the demo: `python AES.py -demo`

**⚠️ Remember:** This is educational software. For production use, use professional cryptographic libraries.
