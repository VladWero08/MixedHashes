import glob
import json
import os

from dotenv import dotenv_values
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from ppm import read_ppm_header, display_ppm
from hash import sha_256_header

env_ = dotenv_values()
ppm_letter_file_paths = glob.glob(f"{env_['letters_dir_path']}/*.ppm")

def pad_ppm_file(ppm, block_size):
    """
    Given the `bytes` of a PPM file and a `block size`,
    append some bytes in order to be divisible with that block size.
    """

    padding_size = block_size - len(ppm) % block_size 
    padding_bytes = bytes([padding_size] * padding_size)
    return ppm + padding_bytes

def write_ppm_header_details(
    header,
    header_hash: str,
    header_details_path: str,
) -> None:
    """
    In a JSON file, write X, Y axis values and the
    associated hash of a PPM header.
    """

    if not os.path.isdir(env_["letter_header_details_dir_path"]):
        os.makedirs(env_["letter_header_details_dir_path"])

    with open(header_details_path, "w") as header_details_output:
        ppm_json = {
            "X": header[0],
            "Y": header[1],
            "hash": header_hash
        }
        json.dump(ppm_json, header_details_output, indent=2)

def encrypt_ppm_without_header(
    ppm_with_headers_path: str,
    ppm_without_header_path: str,
) -> None:
    """
    Encrypts a PPM file without its header using
    `AES`, with key size 128 bits, in ECB mode. 
    
    Writes the encrypted file to a different destination,
    provided in `ppm_without_header_path`.
    """

    if not os.path.isdir(env_["letters_encryption_dir_path"]):
        os.makedirs(env_["letters_encryption_dir_path"])

    with open(ppm_with_headers_path, "rb") as ppm_input:
        ppm_bytes = ppm_input.readlines()

    with open(ppm_without_header_path, "wb") as ppm_output:
        # remove the first 3 lines of the PPM file,
        # which contain the header
        ppm_bytes = b"".join(ppm_bytes[3:])

        # encrypt the PPM file with AES in ECB mode
        key = get_random_bytes(AES.key_size[0])
        cipher = AES.new(key, AES.MODE_ECB)
        # pad the PPM file if necessary
        ppm_bytes = pad_ppm_file(ppm_bytes, AES.block_size)
        cipher_text = cipher.encrypt(ppm_bytes)

        ppm_output.write(cipher_text)

def display_ppm_without_header(
    ppm_file_path: str,
    ppm_header: dict
) -> None:
    """
    Given a PPM file with its header removed, and
    the actual header, display that PPM image to showcase
    the vulnerability of the ECB mode.
    """

    with open(ppm_file_path, "rb") as ppm_input:
        ppm_bytes = ppm_input.read()

    ppm_header_ = f"P6\n{ppm_header['X']} {ppm_header['Y']}\n255\n"
    ppm = ppm_header_.encode("utf-8") + ppm_bytes
    
    display_ppm(ppm)


def encrypt_ppms() -> None:
    """
    It will read the PPM files, extract the header
    from them, hash it, and than delete the header.
    """

    for ppm_letter_file_path in ppm_letter_file_paths:
        letter = ppm_letter_file_path.replace(".ppm", "")[-1]
        # path to the file with header's details 
        ppm_letter_header_details_path = f"{env_['letter_header_details_dir_path']}{letter}.json"
        # path to the encrypted file
        ppm_letter_encrypt_path = f"{env_['letters_encryption_dir_path']}{letter}.ppm"
        
        (X, Y) = read_ppm_header(ppm_letter_file_path) 
        header_hash = sha_256_header(X, Y)

        write_ppm_header_details(
            header=(X, Y),
            header_hash=header_hash,
            header_details_path=ppm_letter_header_details_path
        )

        encrypt_ppm_without_header(
            ppm_with_headers_path=ppm_letter_file_path,
            ppm_without_header_path=ppm_letter_encrypt_path,
        )

def display_encrypted_ppm() -> None:
    # display the encrypted letters
    ppm_letters_encrypted = glob.glob(f"{env_['letters_encryption_dir_path']}*.ppm")

    for ppm_letter_encrypt_path in ppm_letters_encrypted:
        ppm_name = ppm_letter_encrypt_path.rsplit("/", maxsplit=1)[1]
        ppm_name_no_extension = ppm_name.split(".ppm")[0]
        ppm_header_path = f"{env_['letter_header_details_dir_path']}{ppm_name_no_extension}.json"

        with open(ppm_header_path, "r") as ppm_header_json:
            ppm_header = json.load(ppm_header_json)

        display_ppm_without_header(
            ppm_file_path=ppm_letter_encrypt_path,
            ppm_header=ppm_header
        )

if __name__ == "__main__":
    # encrypt all the letters
    encrypt_ppms()
    display_encrypted_ppm()


