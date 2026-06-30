#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example usage of the Python-AES library.

This demonstrates basic encryption and decryption operations.
For production use, use established cryptographic libraries like `cryptography` or `PyCryptodome`.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AES import Cipher, InvCipher, KeyExpansion, process_key, process_block, padding, unpadding, prepare_block, get_block

def simple_example():
    """Simple example of AES encryption/decryption with a known test vector."""
    
    print("=" * 60)
    print("Python-AES Simple Example")
    print("=" * 60)
    
    # Test data (plaintext)
    plaintext = "Hello World!!!!!"  # 16 bytes exactly
    
    # Encryption key (128-bit = 16 bytes = 32 hex digits)
    key_hex = "0f0e0d0c0b0a09080706050403020100"
    
    print("\nOriginal plaintext: {0}".format(plaintext))
    print("Encryption key (hex): {0}".format(key_hex))
    
    # Setup AES-128
    Nb = 4
    Nk = 4
    Nr = 10
    
    # Process key
    key = process_key(key_hex, Nk)
    expanded_key = KeyExpansion(key, Nb, Nk, Nr)
    
    # Process plaintext block
    plaintext_bytes = plaintext.encode('utf-8') if isinstance(plaintext, str) else plaintext
    block = process_block(plaintext_bytes[:16], Nb)
    
    # Encrypt
    ciphertext_block = Cipher(block, expanded_key, Nb, Nk, Nr)
    ciphertext = prepare_block(ciphertext_block)
    
    print("\nEncrypted (hex): {0}".format(ciphertext.hex() if hasattr(ciphertext, 'hex') else ciphertext.encode('hex')))
    
    # Decrypt
    ciphertext_block = process_block(ciphertext, Nb)
    plaintext_block = InvCipher(ciphertext_block, expanded_key, Nb, Nk, Nr)
    decrypted = prepare_block(plaintext_block)
    
    print("Decrypted: {0}".format(decrypted.decode('utf-8') if isinstance(decrypted, bytes) else decrypted))
    
    # Verify
    if plaintext_bytes[:16] == decrypted:
        print("\n✓ Encryption/Decryption successful!")
    else:
        print("\n✗ Encryption/Decryption failed!")

if __name__ == '__main__':
    simple_example()
