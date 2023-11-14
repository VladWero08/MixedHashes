# MixedHashes

MixedHashes NSUCRYPTO'2023: https://nsucrypto.nsu.ru/archive/2023/round/1/section/2/task/3/#data

## Headers

To find the headers, the main idea was to compute every possible combination of the X and Y axis,
in the range of [0, 1199]. If any _SHA-256 hash_ would have corresponded with one of the provided hashes,
it means we found a valid _header_ for that hash.

## PPM files

Ignoring the fact that the PRESENT cipher was used, the main focus was on the fact that is written in ECB mode. 
Because we have graphic files, it means that the relation between the encrypted blocks will be kept like in the plain blocks. 
I have computed every combination between headers and PPM files, displayed each one, and found an association between them:

# Header - PPM association

| file | hash | letter |
| ---- | ---- | ------ |
| 1 | 3 | ♡ |
| 2 | 7 | L |
| 3 | 5 | o |
| 4 | 4 | v |
| 5 | 1 | e |
| 6 | 6 | y |
| 7 | 8 | o |
| 8 | 2 | u |

#### Solution: ♡Loveyou
