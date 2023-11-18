import typing as t
import glob
import os

from solve import display_ppm
from hash import sha_256_header


ppm_letter_file_paths = glob.glob("letters/*.ppm")
ppm_header_hashes = []

def read_ppm_header(
    ppm_path: str, 
) -> t.Optional[tuple[int]]:
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
    header: tuple[int],
    header_hash: str,
    header_details_path: str,
) -> None:
    if not os.path.isdir("letters/details/"):
        os.makedirs("letters/details/")

    with open(header_details_path, "w") as header_details_output:
        ppm_letter_details = f"""X: {header[0]} Y: {header[1]}\n"""
        ppm_letter_details += f"""hash: {header_hash}"""
        header_details_output.write(ppm_letter_details)


def write_ppm_without_header(
    ppm_with_headers_path: str,
    ppm_without_header_path: str,
) -> None:
    if not os.path.isdir("letters/encrypt/"):
        os.makedirs("letters/encrypt/")

    with open(ppm_with_headers_path, "rb") as ppm_input:
        ppm_bytes = ppm_input.readlines()

    with open(ppm_without_header_path, "wb") as ppm_output:
        ppm_bytes = b"".join(ppm_bytes[3:])
        ppm_output.write(ppm_bytes)

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

        write_ppm_without_header(
            ppm_with_headers_path=ppm_letter_file_path,
            ppm_without_header_path=ppm_letter_encrypt_path,
        )
            
format_ppm()