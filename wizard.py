#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactive wizard mode for AES encryption - beginner-friendly interface.
Guides users through encryption/decryption step-by-step.
"""

import sys
import os

try:
    from AES import (
        demo, process_file, validate_hex_key, 
        get_hex_key_input, KeyExpansion, Cipher, InvCipher,
        process_key, process_block, padding, unpadding, 
        get_block, prepare_block, ProgressBar
    )
except ImportError:
    print("Error: Could not import AES module. Make sure you're in the correct directory.")
    sys.exit(1)


def clear_screen():
    """Clear terminal screen (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a formatted header."""
    width = 40
    print("\n" + "╔" + "═" * (width - 2) + "╗")
    print("║" + title.center(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝\n")


def print_success(message):
    """Print a success message."""
    print("✓ " + message)


def print_error(message):
    """Print an error message."""
    print("✗ " + message)


def print_warning(message):
    """Print a warning message."""
    print("⚠ " + message)


def print_info(message):
    """Print an info message."""
    print("ℹ " + message)


def prompt_choice(options, prompt="Your choice: "):
    """Get user choice from a list of options."""
    while True:
        try:
            choice = input(prompt).strip()
            if choice in options:
                return choice
            print_error("Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def prompt_file(mode="read"):
    """Prompt for a file path and verify it exists."""
    while True:
        try:
            filepath = input("Enter file path: ").strip()
            
            if not filepath:
                print_error("File path cannot be empty.")
                continue
            
            if mode == "read" and not os.path.exists(filepath):
                print_error("File not found: {0}".format(filepath))
                continue
            
            if mode == "write" and os.path.exists(filepath):
                response = input("File exists. Overwrite? (y/n): ").strip().lower()
                if response != 'y':
                    continue
            
            return filepath
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def show_menu():
    """Show main menu and return user's choice."""
    print_header("AES Encryption Tool - Wizard")
    
    print("What would you like to do?\n")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. View demo (test vectors)")
    print("4. View tutorial")
    print("5. Exit\n")
    
    return prompt_choice(['1', '2', '3', '4', '5'])


def show_key_size_menu():
    """Show key size selection and return choice."""
    print("\nChoose encryption key size:\n")
    print("1. 128-bit  (32 hex digits) - Fast, good security")
    print("2. 192-bit  (48 hex digits) - Balanced")
    print("3. 256-bit  (64 hex digits) - Strongest\n")
    
    choice = prompt_choice(['1', '2', '3'])
    return {
        '1': 128,
        '2': 192,
        '3': 256
    }[choice]


def get_or_generate_key(key_size_bits):
    """Get key from user or generate a random one."""
    key_hex_length = (key_size_bits // 32) * 8
    
    print("\nEncryption Key Options:\n")
    print("1. Enter your own key (hexadecimal)")
    print("2. Generate a random key (secure)\n")
    
    choice = prompt_choice(['1', '2'])
    
    if choice == '2':
        import random
        key_hex = ''.join(random.choice('0123456789abcdef') for _ in range(key_hex_length))
        print_success("Generated random key!")
    else:
        print("\nKey must be {0} hexadecimal characters (0-9, a-f)".format(key_hex_length))
        print("Examples: a1b2c3d4e5f6... or just press Enter for zeros\n")
        
        while True:
            try:
                key_hex = input("Enter key (or press Enter for zeros): ").strip()
                
                if not key_hex:
                    key_hex = "0" * key_hex_length
                    print_warning("Using all zeros as key (not secure!)")
                    break
                
                key_hex = validate_hex_key(key_hex, key_hex_length)
                break
            except ValueError as e:
                print_error(str(e))
    
    return key_hex


def encrypt_wizard():
    """Interactive encryption wizard."""
    print_header("Encrypt a File")
    
    # Get input file
    print("Step 1 of 4: Select file to encrypt")
    infile = prompt_file("read")
    
    try:
        file_size = os.path.getsize(infile)
        print_success("Found: {0} ({1} bytes)".format(infile, file_size))
    except OSError:
        print_error("Could not read file.")
        return
    
    # Get key size
    print("\nStep 2 of 4: Choose key size")
    key_size = show_key_size_menu()
    print_success("Selected: {0}-bit key".format(key_size))
    
    # Get or generate key
    print("\nStep 3 of 4: Encryption key")
    key_hex = get_or_generate_key(key_size)
    
    # Show key to user
    print("\n" + "─" * 40)
    print("IMPORTANT: Save this key in a safe place!")
    print("─" * 40)
    print("\nYour encryption key:")
    print("  " + key_hex)
    print("\n" + "─" * 40)
    
    input("\nPress Enter to continue with encryption...")
    
    # Perform encryption
    print("\nStep 4 of 4: Encrypting...")
    try:
        process_file('-e', infile, key_size, key_hex)
        print_success("Encryption complete!")
        print("\nEncrypted file: {0}.aes".format(infile))
        print_info("Keep the key safe! You'll need it to decrypt.")
    except Exception as e:
        print_error("Encryption failed: {0}".format(str(e)))


def decrypt_wizard():
    """Interactive decryption wizard."""
    print_header("Decrypt a File")
    
    # Get input file
    print("Step 1 of 3: Select file to decrypt")
    print("(Should be a .aes or .cif file)")
    infile = prompt_file("read")
    
    try:
        file_size = os.path.getsize(infile)
        print_success("Found: {0} ({1} bytes)".format(infile, file_size))
    except OSError:
        print_error("Could not read file.")
        return
    
    # Get key size
    print("\nStep 2 of 3: Choose key size used for encryption")
    key_size = show_key_size_menu()
    print_success("Selected: {0}-bit".format(key_size))
    
    # Get key
    print("\nStep 3 of 3: Enter encryption key")
    key_hex_length = (key_size // 32) * 8
    print("Key must be {0} hexadecimal characters\n".format(key_hex_length))
    
    key_hex = get_hex_key_input(key_hex_length)
    
    # Perform decryption
    print("\nDecrypting...")
    try:
        process_file('-d', infile, key_size, key_hex)
        
        if infile.endswith('.aes'):
            outfile = infile[:-4]
        elif infile.endswith('.cif'):
            outfile = infile[:-4]
        else:
            outfile = infile + ".decrypted"
        
        print_success("Decryption complete!")
        print("Decrypted file: {0}".format(outfile))
    except Exception as e:
        print_error("Decryption failed: {0}".format(str(e)))
        print_error("Check that you used the correct key.")


def show_tutorial():
    """Show tutorial file."""
    try:
        # Use absolute path based on script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tutorial_path = os.path.join(script_dir, 'TUTORIAL.md')
        
        with open(tutorial_path, 'r') as f:
            tutorial = f.read()
        
        # Show tutorial in chunks (handle large files)
        lines = tutorial.split('\n')
        chunk_size = 20
        
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            print(chunk)
            
            if i + chunk_size < len(lines):
                input("\n[Press Enter to continue...]")
    
    except FileNotFoundError:
        print_error("TUTORIAL.md not found. Make sure it's in the same directory as wizard.py.")


def main_wizard():
    """Main wizard loop."""
    while True:
        choice = show_menu()
        
        if choice == '1':
            encrypt_wizard()
        elif choice == '2':
            decrypt_wizard()
        elif choice == '3':
            clear_screen()
            print_header("FIPS-197 Test Vectors Demo")
            demo()
        elif choice == '4':
            clear_screen()
            show_tutorial()
        elif choice == '5':
            print("\nGoodbye!\n")
            sys.exit(0)
        
        input("\nPress Enter to return to menu...")
        clear_screen()


if __name__ == '__main__':
    try:
        main_wizard()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
