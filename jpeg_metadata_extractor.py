from argparse import ArgumentParser
import os
import sys
import glob
import PIL.Image
from PIL.ExifTags import TAGS

def get_exif(fname):
    img = PIL.Image.open(fname)
    exifdata = img.getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        if 'description' in tag.casefold():
            print(tag)
            print(data)
        # print(f"{tag:25}: {data}")
    return exifdata


def corrected_gps_time_in_week_second(
                           day_of_week,
                           h, m, s,
                           hardware_clock,
                           last_pps_clock
                           ):
    gps_time_in_week_second = day_of_week*(60*60*24)+h*(60*60)+m*(60)+s
    return hardware_clock - last_pps_clock + gps_time_in_week_second


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
cam_nr = 6

file_list = []
for i in range(cam_nr):
    file_list_cam = []
    for root, directories, files in os.walk(os.path.join(input_dir,'CAM{}'.format(i+1))):
        for name in files:
            full_name = os.path.join(root, name)
            if ext in full_name:
                file_list_cam.append(full_name)
    file_list.append(file_list_cam)

for files_per_cam in file_list:
    for i, im in enumerate(files_per_cam):
        if i == 10:
            break
        print(im)
        print('*'*80)
        exif = get_exif(im)

        print('*'*80)
    break
'''
for full_path in file_list:
    path_elements = full_path.split('/')
'''

    
