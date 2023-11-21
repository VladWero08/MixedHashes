import glob

from dotenv import dotenv_values

from ppm import write_header_to_ppm, display_from_file_ppm
from hash import sha_256_header_correspondence

env_ = dotenv_values()
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
ppm_files_paths = glob.glob(f"{env_['solution_encrypted_dir_path']}/*.ppm")


def write_all_headers_to_all_pnm() -> None:
    """Generate all the combinaton of `headers` and `PPM files`:
    create copies of the PPM files and add every header possible
    to each one, saving each copy in a folder named after the hash of the header."""

    graphic_axis = sha_256_header_correspondence()

    for hash, axis in graphic_axis.items():
        # for every graphic axis found, 
        # try to compute the image 
        for ppm_input_file_path in ppm_files_paths:
            ppm_output_file_path = f"{env_['solution_decrypted_dir_path']}{hash}/"
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
        display_from_file_ppm(ppm_file_path=f"{env_['solution_decrypted_dir_path']}{hash}/{ppm_file_name}")