import os
import hashlib
import typing as t

ppm_hashes = [
    "602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d",
    "f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5",
    "aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5",
    "70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450",
    "77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6",
    "456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01",
    "bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d",
    "372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305"
]

def sha_256_header(
    x_pixels: str, 
    y_pixels: str
) -> str:
    """Returns the SHA-256 hash that corresponds to the
    header that has X pixels and Y pixels."""

    header = f"P6 {x_pixels} {y_pixels} 255"
    header_encryped = hashlib.sha256(header.encode()).hexdigest()

    return header_encryped

def sha_256_header_correspondence() -> dict:
    """Returns a dictionary in which each key corresponds to
    a hash transmitted to Alice, and the values are their `header's axis`."""
    hashes_correspondence = {}

    # for every possible combination of X and Y 
    # graphic file sizes, X in [0, 1999] and Y in [0, 1999],
    # brute force search for correspondence with the header hashes
    for i in range(1200):
        for j in range(1200):
            header = sha_256_header(i, j)

            if header in ppm_hashes:
                # find the position of the header in the list
                # of hashes and save it in the dictionary
                header_position = ppm_hashes.index(header)
                hashes_correspondence[header] = {"x": i, "y": j}

                # create a folder where images created with 
                # the current header will be stored
                hash_directory = f"decrypted_files/{ppm_hashes[header_position]}"
                # create a folder to hold information about the corresponding hash
                hash_information = f"{hash_directory}/information.txt"
                
                if not os.path.exists(hash_directory):
                    os.makedirs(hash_directory)
                if not os.path.exists(hash_information):
                    with open(hash_information, "w") as hash_output:
                        hash_output.write(f"Position: {header_position}\n")
                        hash_output.write(f"X: {i}, Y: {j}")

    # sort the dictionary by index key
    hashes_correspondence = dict(sorted(hashes_correspondence.items()))

    return hashes_correspondence