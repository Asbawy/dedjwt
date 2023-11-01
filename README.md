# DEDJWT : JWT Bruter
[![Photo](https://i.imgur.com/8U7Vjyb.png)](photo)
A script to brute force JWT tokens. It loads passwords from a list and attempts to decode the JWT token with each password. If the token is decoded successfully, the password is saved and the script exits.

## Feature

- Smart multi-threaded for faster brute force attempts.

## Requirements

- Python 3.x
- Python libraries: jwt, colorama, concurrent.futures, psutil

## Usage
1. Clone the repository or download the script.
2. Install the required Python libraries using `pip`:
```bash
pip install PyJWT pytz colorama psutil tqdm
```
3. Run the script:
```bash
python3 dedjwt.py
```
4. Follow the on-screen prompts:
   - Enter the JWT token you want to decode.
   - Provide a file containing a list of passwords.
   - Optionally, specify an output file to save found passwords.
5. The script will attempt to decode the token by testing passwords from the list against it.
6. If successful, it will display the decoded password.

## Contributing
Feel free to contribute to this project. You can fork the repository, make changes, and submit a pull request. Your contributions are welcome!
