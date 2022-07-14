from argparse import ArgumentParser
import os
import sys
import glob

parser = ArgumentParser(description="""Loop over subdirectories and 
                        jpeg files within to extract metadata and 
                        do stuff with it.""")

parser.add_argument("-i", "--input", required = True,
                        help="Input directory to search for jpeg images.")

parser.add_argument("-o", "--output", required = True,
                        help="""Output directory to store csv files with
                        data extracted from the jpeg images.""")

args = parser.parse_args()
input_dir = args.input
output_dir = args.output

print('The input folder is: \t{}'.format(input_dir))
print('The output folder is: \t{}'.format(output_dir))
print()

ext = 'jpeg'

file_list = []
for root, directories, files in os.walk(input_dir):
    for name in files:
        full_name = os.path.join(root, name)
        if ext in full_name:
            file_list.append(full_name)
print(file_list) 
