#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------
# Copyright (c) 2013 Pablo Caro. All Rights Reserved.
# Pablo Caro <me@pcaro.es> - http://pcaro.es/
# AES.py
# ---------------------------------------------------

import sys
import os
import os.path
import argparse
from ProgressBar import ProgressBar
from AES_base import sbox, isbox, gfp2, gfp3, gfp9, gfp11, gfp13, gfp14, Rcon

if sys.version_info[0] == 3:
    raw_input = input


def RotWord(word):
    return word[1:] + word[0:1]


def SubWord(word):
    return [sbox[byte] for byte in word]


def SubBytes(state):
    """
    SubBytes transformation (step 1 of AES round).
    Substitutes each byte with its corresponding S-box value.
    """
    return [[sbox[byte] for byte in word] for word in state]


def InvSubBytes(state):
    """
    Inverse SubBytes transformation (step 1 of AES inverse round).
    Substitutes each byte with its corresponding inverse S-box value.
    """
    return [[isbox[byte] for byte in word] for word in state]


def ShiftRows(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        for j in range(4):
            n[i][j] = state[(i+j) % Nb][j]

    return n


def InvShiftRows(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        for j in range(4):
            n[i][j] = state[(i-j) % Nb][j]

    return n


def MixColumns(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        n[i][0] = (gfp2[state[i][0]] ^ gfp3[state[i][1]]
                   ^ state[i][2] ^ state[i][3])
        n[i][1] = (state[i][0] ^ gfp2[state[i][1]]
                   ^ gfp3[state[i][2]] ^ state[i][3])
        n[i][2] = (state[i][0] ^ state[i][1]
                   ^ gfp2[state[i][2]] ^ gfp3[state[i][3]])
        n[i][3] = (gfp3[state[i][0]] ^ state[i][1]
                   ^ state[i][2] ^ gfp2[state[i][3]])

    return n


def InvMixColumns(state):
    Nb = len(state)
    n = [word[:] for word in state]

    for i in range(Nb):
        n[i][0] = (gfp14[state[i][0]] ^ gfp11[state[i][1]]
                   ^ gfp13[state[i][2]] ^ gfp9[state[i][3]])
        n[i][1] = (gfp9[state[i][0]] ^ gfp14[state[i][1]]
                   ^ gfp11[state[i][2]] ^ gfp13[state[i][3]])
        n[i][2] = (gfp13[state[i][0]] ^ gfp9[state[i][1]]
                   ^ gfp14[state[i][2]] ^ gfp11[state[i][3]])
        n[i][3] = (gfp11[state[i][0]] ^ gfp13[state[i][1]]
                   ^ gfp9[state[i][2]] ^ gfp14[state[i][3]])

    return n


def AddRoundKey(state, key):
    Nb = len(state)
    new_state = [[None for j in range(4)] for i in range(Nb)]

    for i, word in enumerate(state):
        for j, byte in enumerate(word):
            new_state[i][j] = byte ^ key[i][j]

    return new_state


def Cipher(block, w, Nb=4, Nk=4, Nr=10):
    state = AddRoundKey(block, w[:Nb])

    for r in range(1, Nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, w[r*Nb:(r+1)*Nb])

    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, w[Nr*Nb:(Nr+1)*Nb])

    return state


def InvCipher(block, w, Nb=4, Nk=4, Nr=10):
    state = AddRoundKey(block, w[Nr*Nb:(Nr+1)*Nb])

    for r in range(Nr-1, 0, -1):
        state = InvShiftRows(state)
        state = InvSubBytes(state)
        state = AddRoundKey(state, w[r*Nb:(r+1)*Nb])
        state = InvMixColumns(state)

    state = InvShiftRows(state)
    state = InvSubBytes(state)
    state = AddRoundKey(state, w[:Nb])

    return state


def KeyExpansion(key, Nb=4, Nk=4, Nr=10):
    w = []
    for word in key:
        w.append(word[:])

    i = Nk

    while i < Nb * (Nr + 1):
        temp = w[i-1][:]
        if i % Nk == 0:
            temp = SubWord(RotWord(temp))
            temp[0] ^= Rcon[(i//Nk)]
        elif Nk > 6 and i % Nk == 4:
            temp = SubWord(temp)

        for j in range(len(temp)):
            temp[j] ^= w[i-Nk][j]

        w.append(temp[:])

        i += 1

    return w


def prepare_block(block):
    c = []
    for word in block:
        for byte in word:
            c.append(byte)

    s = None
    for byte in c:
        if sys.version_info[0] == 3:
            if not s:
                s = bytes([byte])
            else:
                s += bytes([byte])
        elif sys.version_info[0] == 2:
            if not s:
                s = chr(byte)
            else:
                s += chr(byte)

    return s


def get_block(inf, Nb=4):
    return process_block(inf[:Nb*4], Nb), inf[Nb*4:]


def padding(inf, Nb=4):
    ''' PKCS#7 padding '''

    # l = len(inf)  # Bytes
    # hl = [int((hex(l*8)[2:]).rjust(16, '0')[i:i+2], 16)
    #       for i in range(0, 16, 2)]

    # l0 = (8 - l) % 16
    # if not l0:
    #     l0 = 16

    # if isinstance(inf, str):  # Python 2
    #     inf += chr(0b10000000)
    #     inf += chr(0)*(l0-1)
    #     for a in hl:
    #         inf += chr(a)
    # elif isinstance(inf, bytes):  # Python 3
    #     inf += bytes([0b10000000])
    #     inf += bytes(l0-1)
    #     inf += bytes(hl)

    padding_length = (Nb*4) - (len(inf) % (Nb*4))

    if padding_length:
        if isinstance(inf, str):  # Python 2
            inf += chr(padding_length) * padding_length
        elif isinstance(inf, bytes):  # Python 3
            inf += bytes([padding_length] * padding_length)

    return inf


def unpadding(inf, Nb=4):
    ''' PKCS#7 padding '''

    padding_length = ord(inf[-1])

    if padding_length < (Nb*4):
        if len(set(inf[-padding_length:])) == 1:
            inf = inf[:-padding_length]

    return inf


def process_block(block, Nb=4):
    if sys.version_info[0] == 3:  # Python 3
        if type(block) == str:
            block = bytes(block, 'utf8')
        pass
    elif sys.version_info[0] == 2:  # Python 2
        block = map(ord, block)

    return [[block[i*4+j] for j in range(4)] for i in range(Nb)]


def process_key(key, Nk=4):
    try:
        key = key.replace(" ", "")
        return [[int(key[i*8+j*2:i*8+j*2+2], 16) for j in range(4)]
                for i in range(Nk)]
    except:
        print ("Password must be hexadecimal.")
        sys.exit()


def print_block(block):
    s = ''

    for i in range(len(block[0])):
        for j in range(len(block)):
            h = hex(block[j][i])[2:]
            if len(h) == 1:
                h = '0'+h
            s += h + ' '
        s += '\n'
    print (s)


def str_block_line(block):
    s = ''

    for i in range(len(block)):
        for j in range(len(block[0])):
            h = hex(block[i][j])[2:]
            if len(h) == 1:
                h = '0'+h
            s += h
    return (s)


def help():
    print ("Help:")
    print("python AES.py -demo")
    print("python AES.py (-e | -d) <file> [-c (128|192|256)]")
    print("    -e: Encrypt")
    print("    -d: Decrypt")
    print("    -c <n>: <n> bits key (default 128)")
    print("Note: a function mode (-e/-d) has to be specified.")
    sys.exit()


def validate_hex_key(key_str, expected_length):
    """
    Validate and normalize a hexadecimal key string.
    
    Args:
        key_str: The hex key string (may contain spaces)
        expected_length: Expected number of hex digits (e.g., 32 for 128-bit)
    
    Returns:
        Validated and padded/truncated hex key string
    
    Raises:
        ValueError: If the key contains invalid hex characters
    """
    key_str = key_str.replace(' ', '').replace(':', '').replace('-', '')
    
    # Validate hex format
    try:
        int(key_str, 16)
    except ValueError:
        raise ValueError("Key must contain only hexadecimal digits (0-9, a-f, A-F)")
    
    if len(key_str) < expected_length:
        print("⚠ Warning: Key too short. Padding with zeros to {0} digits.".format(expected_length))
        key_str += "0" * (expected_length - len(key_str))
    elif len(key_str) > expected_length:
        print("⚠ Warning: Key too long. Using only first {0} digits.".format(expected_length))
        key_str = key_str[:expected_length]
    
    return key_str


def get_hex_key_input(expected_length):
    """
    Interactively prompt the user for a hexadecimal key.
    
    Args:
        expected_length: Expected number of hex digits
    
    Returns:
        Validated hex key string
    """
    while True:
        try:
            key = raw_input(
                "Enter encryption key ({0} hex digits, or press Enter for zeros): ".format(expected_length))
            
            if not key.strip():
                return "0" * expected_length
            
            return validate_hex_key(key, expected_length)
        except ValueError as e:
            print("✗ Invalid key: {0}".format(str(e)))
            print("  Please try again with valid hexadecimal characters.\n")
            continue


def demo():
    plaintext = "00112233445566778899aabbccddeeff"
    Nb = 4

    # AES-128
    print("\n")
    print("*"*40)
    print("*" + "AES-128 (Nk=4, Nr=10)".center(38) + "*")
    print("*"*40)
    Nk = 4
    Nr = 10

    key = "000102030405060708090a0b0c0d0e0f"
    print("KEY:\t\t{0}".format(key))
    key = process_key(key, Nk)
    expanded_key = KeyExpansion(key, Nb, Nk, Nr)

    print("PLAINTEXT:\t{0}".format(plaintext))

    block = process_key(plaintext)
    block = Cipher(block, expanded_key, Nb, Nk, Nr)
    print("ENCRYPT:\t{0}".format(str_block_line(block)))

    block = InvCipher(block, expanded_key, Nb, Nk, Nr)
    print("DECRYPT:\t{0}".format(str_block_line(block)))
    print("\n")

    # AES-192
    print("*"*40)
    print("*" + "AES-192 (Nk=6, Nr=12)".center(38) + "*")
    print("*"*40)
    Nk = 6
    Nr = 12

    key = "000102030405060708090a0b0c0d0e0f1011121314151617"
    print("KEY:\t\t{0}".format(key))
    key = process_key(key, Nk)
    expanded_key = KeyExpansion(key, Nb, Nk, Nr)

    print("PLAINTEXT:\t{0}".format(plaintext))

    block = process_key(plaintext)
    block = Cipher(block, expanded_key, Nb, Nk, Nr)
    print("ENCRYPT:\t{0}".format(str_block_line(block)))

    block = InvCipher(block, expanded_key, Nb, Nk, Nr)
    print("DECRYPT:\t{0}".format(str_block_line(block)))
    print("\n")

    # AES-256
    print("*"*40)
    print("*" + "AES-256 (Nk=8, Nr=14)".center(38) + "*")
    print("*"*40)
    Nk = 8
    Nr = 14

    key = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
    print("KEY:\t\t{0}".format(key))
    key = process_key(key, Nk)
    expanded_key = KeyExpansion(key, Nb, Nk, Nr)

    print("PLAINTEXT:\t{0}".format(plaintext))

    block = process_key(plaintext)
    block = Cipher(block, expanded_key, Nb, Nk, Nr)
    print("ENCRYPT:\t{0}".format(str_block_line(block)))

    block = InvCipher(block, expanded_key, Nb, Nk, Nr)
    print("DECRYPT:\t{0}".format(str_block_line(block)))
    print("\n")


def main():
    """Main entry point with improved argument parsing and error handling."""
    
    # Handle wizard mode (beginner-friendly interface)
    if len(sys.argv) > 1 and sys.argv[1] in ['--wizard', '-w', 'wizard']:
        try:
            from wizard import main_wizard
            main_wizard()
        except ImportError:
            print("Error: Wizard module not found. Make sure wizard.py is in the same directory.")
            sys.exit(1)
        return
    
    # Handle legacy arguments first for backward compatibility
    if len(sys.argv) > 1 and sys.argv[1] == '-demo':
        demo()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-e', '-d']:
        if len(sys.argv) < 3:
            print("Error: Input file required")
            print("Usage: python AES.py (-e | -d) <file> [-c (128|192|256)]")
            sys.exit(1)
        
        mode = sys.argv[1]
        ifile = sys.argv[2]
        
        if not os.path.exists(ifile):
            print("Error: Input file '{0}' not found.".format(ifile))
            sys.exit(1)
        
        key_size = 128
        for i, arg in enumerate(sys.argv[3:]):
            if arg == '-c' and i+1 < len(sys.argv[3:]):
                try:
                    key_size = int(sys.argv[4+i])
                    if key_size not in [128, 192, 256]:
                        raise ValueError()
                except (ValueError, IndexError):
                    print("Error: Invalid key size. Use 128, 192, or 256.")
                    sys.exit(1)
        
        # Process encryption/decryption
        process_file(mode, ifile, key_size)
        return
    
    # If no arguments or only -h/--help, show help
    if len(sys.argv) == 1:
        demo()
        return
    
    # Setup argparse for new-style commands
    parser = argparse.ArgumentParser(
        prog='AES.py',
        description='AES Encryption/Decryption - Educational Implementation',
        epilog='WARNING: This is for educational purposes only. Do not use in production!'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run FIPS-197 demo with test vectors')
    
    # Encrypt/Decrypt command
    crypto_parser = subparsers.add_parser('crypto', help='Encrypt or decrypt a file')
    crypto_parser.add_argument(
        'mode',
        choices=['encrypt', 'decrypt'],
        help='Operation mode'
    )
    crypto_parser.add_argument(
        'file',
        help='Input file path'
    )
    crypto_parser.add_argument(
        '-c', '--key-size',
        type=int,
        choices=[128, 192, 256],
        default=128,
        help='Key size in bits (default: 128)'
    )
    crypto_parser.add_argument(
        '-k', '--key',
        help='Encryption key (hex). If not provided, will prompt interactively.'
    )
    crypto_parser.add_argument(
        '-o', '--output',
        help='Output file path (optional, auto-generated by default)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'demo':
        demo()
    elif args.command == 'crypto':
        mode = '-e' if args.mode == 'encrypt' else '-d'
        ifile = args.file
        key_size = args.key_size
        
        if not os.path.exists(ifile):
            print("Error: Input file '{0}' not found.".format(ifile))
            sys.exit(1)
        
        # Use provided key or prompt for it
        if args.key:
            try:
                key_str = validate_hex_key(args.key, key_size // 8 * 2)
            except ValueError as e:
                print("Error: Invalid key format - {0}".format(str(e)))
                sys.exit(1)
        else:
            key_str = None
        
        # Process encryption/decryption
        process_file(mode, ifile, key_size, key_str, args.output)
    else:
        parser.print_help()


def process_file(mode, ifile, key_size, key_str=None, output_file=None):
    """
    Process file encryption or decryption.
    
    Args:
        mode: Operation mode ('-e'/'encrypt' or '-d'/'decrypt')
        ifile: Input file path
        key_size: Key size in bits (128, 192, or 256)
        key_str: Hex key string (optional, will prompt if not provided)
        output_file: Output file path (optional, auto-generated by default)
    """
    # Normalize mode
    if mode in ['-e', 'encrypt']:
        mode = '-e'
    elif mode in ['-d', 'decrypt']:
        mode = '-d'
    else:
        print("Error: Invalid mode. Use -e/encrypt or -d/decrypt")
        sys.exit(1)
    
    # Read input file
    try:
        with open(ifile, 'rb') as f:
            inf = f.read()
    except IOError as e:
        print("Error reading input file: {0}".format(str(e)))
        sys.exit(1)
    
    # Setup AES parameters
    Nb = 4
    Nk = key_size // 32
    Nr = Nk + 6
    
    # Get or prompt for key
    if key_str is None:
        key_str = get_hex_key_input(Nk * 8)
    
    try:
        key = process_key(key_str, Nk)
    except Exception as e:
        print("Error processing key: {0}".format(str(e)))
        sys.exit(1)
    
    expanded_key = KeyExpansion(key, Nb, Nk, Nr)
    
    # Determine output file
    if output_file is None:
        if mode == '-e':
            ofile = ifile + '.aes'
        elif mode == '-d' and (ifile.endswith('.aes') or ifile.endswith('.cif')):
            ofile = ifile[:-4]
        else:
            ofile = raw_input('Enter output filename: ')
    else:
        ofile = output_file
    
    # Check if output file exists
    if os.path.exists(ofile) and output_file is None:
        response = raw_input('The file "{0}" already exists. Overwrite? [y/N]: '.format(ofile))
        if response.upper() != 'Y':
            ofile = raw_input('Enter new filename: ')
    
    # Process the file
    pb = ProgressBar(len(inf), 0)
    output = None
    
    if mode == '-e':
        inf = padding(inf, Nb)
    
    print('')
    while inf:
        block, inf = get_block(inf, Nb)
        
        c = pb.update(len(inf))
        if c:
            pb.show()
        
        if mode == '-e':
            block = Cipher(block, expanded_key, Nb, Nk, Nr)
        elif mode == '-d':
            block = InvCipher(block, expanded_key, Nb, Nk, Nr)
        
        block = prepare_block(block)
        if output:
            output += block
        else:
            output = block
    
    if mode == '-d':
        output = unpadding(output, Nb)
    
    # Write output file
    try:
        with open(ofile, 'wb') as f:
            f.write(output)
        print('\n✓ File saved to: {0}'.format(ofile))
    except IOError as e:
        print("Error writing output file: {0}".format(str(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()
