from PIL import Image
from io import BytesIO

def read_ppm_header(ppm_path: str):
    """Given a `PPM file (P6)`, return its header's X and Y
    axis values as a tuple."""
    try:  
        with open(ppm_path, "rb") as ppm_input:
            # read the PPM file
            ppm_bytes = ppm_input.readlines()

            # extract the X, Y from the headers
            X, Y = ppm_bytes[1].decode("utf-8").split()    

            return (X, Y)
    except Exception as e:
        print(f"[ERROR] While reading PPM file {ppm_path}: {e}!")

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

def display_from_file_ppm(ppm_file_path: str) -> None:
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

def display_ppm(ppm_bytes: bytes) -> None:
    ppm_bytes = BytesIO(ppm_bytes)
    ppm_image = Image.open(ppm_bytes)
    ppm_image.show()