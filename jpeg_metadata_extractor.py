from argparse import ArgumentParser
import os
import sys
from glob import glob
import PIL.Image
from PIL.ExifTags import TAGS
from datetime import datetime


def get_desc_str(fname):
    '''
    Extracting the "description" field of the jpeg for 
    further processing.
    '''
    
    img = PIL.Image.open(fname)
    exifdata = img.getexif()
    for tag_id in exifdata:
        # get the tag name
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        if 'description' in tag.casefold():
            desc = data.split(',')
            break
    return desc


def extract_datetime_info(file):
    '''
    Collecting the date and time information of a given jpeg
    from its "description" field. These are needed for calculating
    the corrected GPS time of the week in seconds. 
    Specific fields were selected according to the documentation.
    '''
    
    desc = get_desc_str(file)
    day, month, year = desc[9], desc[10], desc[11]
    hhmmss = desc[12]
    dt = datetime.strptime('{}/{}/{} {}'.format(
                    day, month, year[2:], 
                    hhmmss.split('.')[0]), '%d/%m/%y %H:%M:%S'
                    )
    day_of_week = dt.isoweekday()%7 #isoweekday() assigns 7 to Sunday
    hh, mm, ss = [float(elem) for elem in hhmmss.split(':')]
    hardware_clock = float(desc[27])/1000  # converting from ms to s
    last_pps_clock = float(desc[28])/1000  # converting from ms to s
    return day_of_week, hh, mm, ss, hardware_clock, last_pps_clock


def calc_corr_gpstime(
                day_of_week,
                hh, mm, ss,
                hardware_clock,
                last_pps_clock
                ):
    '''
    Calculate the corrected GPS time of the week in
    seconds according to
    CorrectedGPSTimeInSeconds = hardwareClock - lastPPSclock + GPSTimeInWeek,
    where
    GPSTimeInWeek = DayOfWeek*(60*60*24)+hh*(60*60)+mm*60+ss
    and DayOfWeek is 0 for Sunday, 1 for Mon, 2 for Tue, 3 for Wed, etc.
    '''
    
    gps_time_in_week_second = day_of_week*(60*60*24)+hh*(60*60)+mm*(60)+ss
    return hardware_clock - last_pps_clock + gps_time_in_week_second


parser = ArgumentParser(description=
                        """
                        Loop over subdirectories and jpeg files within 
                        to calculate their corrected GPS time of the 
                        week in seconds using metadata found attached to 
                        the jpegs. The values are written into txt files 
                        in the user-specified output folder for each 
                        subdirectory containing jpeg files.
                        """
                       )

parser.add_argument("-i", "--input", required = True,
                    help="Input directory to search for jpeg images."
                    )

parser.add_argument("-o", "--output", required = True,
                    help=
                    """
                    Output directory to store txt files with 
                    data extracted from the jpeg images.
                    """
                   )

args = parser.parse_args()
input_dir = args.input
output_dir = args.output

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    print('Created output directory {}'.format(output_dir))

print('The input folder is: \t{}'.format(input_dir))
print('The output folder is: \t{}'.format(output_dir))
print()

ext = 'jpeg'

cams = glob(os.path.join(input_dir,'*/'), recursive = True)
for cam in cams:
    for elem in cam.split('/'):
        if 'cam' in elem.casefold():
            camname = elem
            break

    subs = glob(os.path.join(cam,'*/'), recursive = True)
    for sub in subs:
        files = glob(os.path.join(sub,'*.{}'.format(ext)))
        print('*'*80)


        print('Currently working on {}'.format(sub.replace(input_dir,'')))
        print('This folder contains {} jpeg files.'.format(len(files)))
        print()
                        
        subname = sub.split('/')[-2]
        outname = '{}_{}_imageList.csv'.format(
                                   camname, subname
                                   )
        outfile = os.path.join(output_dir,outname)
        with open(outfile, 'w') as out:
            for i, file in enumerate(files):
                day_of_week, hh, mm, ss, hw_cl, pps_cl = extract_datetime_info(file)
                corr_gps_time = calc_corr_gpstime(day_of_week, hh, mm, ss, hw_cl, pps_cl)
                path_in_input = file.replace(input_dir,'')
                out.write('{};{}\n'.format(str(corr_gps_time),path_in_input))
                if i%11 == 0:
                    print('{:.1f} % done'.format(i/len(files)*100))
                    
        print('Finished working on {}'.format(sub.replace(input_dir,'')))
        print()
