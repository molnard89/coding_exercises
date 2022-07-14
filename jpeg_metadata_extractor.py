from argparse import ArgumentParser
import os
import sys

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

print('Input folder is: {}'.format(input_dir))
print('Output folder is {}'.format(output_dir))
