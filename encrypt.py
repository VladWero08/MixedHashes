import typing as t
import glob
import os

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from solve import display_ppm
from hash import sha_256_header


ppm_letter_file_paths = glob.glob("letters/*.ppm")
ppm_header_hashes = []

def read_ppm_header(ppm_path: str):
    try:  
        with open(ppm_path, "rb") as ppm_input:
            # read the PPM file
            ppm_bytes = ppm_input.readlines()

            # extract the X, Y from the headers
            X, Y = ppm_bytes[1].decode("utf-8").split()    

            return (X, Y)
    except Exception as e:
        print(f"[ERROR] While reading PPM file {ppm_path}: {e}!")


def write_ppm_header_details(
    header,
    header_hash: str,
    header_details_path: str,
) -> None:
    if not os.path.isdir("letters/details/"):
        os.makedirs("letters/details/")

    with open(header_details_path, "w") as header_details_output:
        ppm_letter_details = f"""X: {header[0]} Y: {header[1]}\n"""
        ppm_letter_details += f"""hash: {header_hash}"""
        header_details_output.write(ppm_letter_details)


def pad_ppm_file(ppm, block_size):
    padding_size = block_size - len(ppm) % block_size 
    padding_bytes = bytes([padding_size] * padding_size)
    return ppm + padding_bytes


def encrypt_ppm_without_header(
    ppm_with_headers_path: str,
    ppm_without_header_path: str,
) -> None:
    if not os.path.isdir("letters/encrypt/"):
        os.makedirs("letters/encrypt/")

    with open(ppm_with_headers_path, "rb") as ppm_input:
        ppm_bytes = ppm_input.readlines()

    with open(ppm_without_header_path, "wb") as ppm_output:
        # remove the first 3 lines of the PPM file,
        # which contain the header
        ppm_bytes = b"".join(ppm_bytes[3:])

        # encrypt the PPM file with AES in ECB mode
        key = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_ECB)
        # pad the PPM file if necessary
        ppm_bytes = pad_ppm_file(ppm_bytes, DES.block_size)
        cipher_text = cipher.encrypt(ppm_bytes)

        ppm_output.write(cipher_text)

def format_ppm() -> None:
    """It will read the PPM files, extract the header
    from them, hash it, and than delete the header."""

    for ppm_letter_file_path in ppm_letter_file_paths:
        letter = ppm_letter_file_path.replace(".ppm", "")[-1]
        # path to the file with header's details 
        ppm_letter_header_details_path = f"letters/details/{letter}.txt"
        # path to the encrypted file
        ppm_letter_encrypt_path = f"letters/encrypt/{letter}.ppm"
        
        (X, Y) = read_ppm_header(ppm_letter_file_path) 
        header_hash = sha_256_header(X, Y)
        ppm_header_hashes.append(header_hash)

        write_ppm_header_details(
            header=(X, Y),
            header_hash=header_hash,
            header_details_path=ppm_letter_header_details_path
        )

        encrypt_ppm_without_header(
            ppm_with_headers_path=ppm_letter_file_path,
            ppm_without_header_path=ppm_letter_encrypt_path,
        )
            
# format_ppm()
display_ppm("letters/encrypt/L.ppm")