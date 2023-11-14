import glob

from PIL import Image
from io import BytesIO
from hash import sha_256_header_correspondence

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
ppm_files_paths = glob.glob("encrypted_files/*.ppm")

def write_header_to_ppm(
    ppm_input_file_path: str, 
    ppm_output_file_path: str,
    x: int, 
    y: int,
) -> None:
    """Given a path to a `.ppm`, write its header information: 
    `x` and `y` axis size, respectively its information in an output file."""
    try:
        with open(ppm_input_file_path, "rb") as ppm_input:
            ppm_input_bytes = ppm_input.read()

        with open(ppm_output_file_path, "w") as ppm_output:
            ppm_output.write("P6\n")
            ppm_output.write(f"{x} {y}\n")
            ppm_output.write("255\n")
        
        with open(ppm_output_file_path, "ab") as ppm_output:
            ppm_output.write(ppm_input_bytes)
    except Exception as e:
        print(f"[ERROR] While writing header from {ppm_input_file_path} to {ppm_output_file_path}: {e} !")


def display_ppm(ppm_file_path: str) -> None:
    """Given a path to a `.ppm` file, get the bytes data
    and trasnform it to a `PIL.Image`. Display the image."""

    try:
        with open(ppm_file_path, "rb") as ppm_input:
            ppm_bytes = ppm_input.read()
            ppm_bytes = BytesIO(ppm_bytes)

            ppm_image = Image.open(ppm_bytes)
            ppm_image.show()
    except Exception as e:
        print(f"[ERROR] While displaying {ppm_file_path}: {e}!")


def write_all_headers_to_all_pnm() -> None:
    """Generate all the combinaton of `headers` and `PPM files`:
    create copies of the PPM files and add every header possible
    to each one, saving each copy in a folder named after the hash of the header."""

    graphic_axis = sha_256_header_correspondence()
    ppm_file_paths = glob.glob("encrypted_files/*.ppm")

    for hash, axis in graphic_axis.items():
        # for every graphic axis found, 
        # try to compute the image 
        for ppm_input_file_path in ppm_file_paths:
            ppm_output_file_path = f"decrypted_files/{hash}/"
            ppm_output_file_path += ppm_input_file_path.split("\\")[1]
            
            write_header_to_ppm(
                ppm_input_file_path=ppm_input_file_path,
                ppm_output_file_path=ppm_output_file_path,
                x=axis["x"],
                y=axis["y"],
            )

def solve_ppm_header_association(hash: str):
    """Given one of the hashes, loop every PPM file
    and display the image `containing the header` associated with
    the `hash`, in order to interpret a possible message."""

    for ppm_file in ppm_files_paths:
        # get the name of the PPM file
        ppm_file_name = ppm_file.split("\\")[1]
        # display the PPM file that has the
        # header associated with the hash provided as parameter
        display_ppm(ppm_file_path=f"decrypted_files/{hash}/{ppm_file_name}")