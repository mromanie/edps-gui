#!/usr/bin/env python3

import argparse
import subprocess
import os
from urllib.parse import urlparse
import requests
import tarfile
from tqdm import tqdm

import utilities


instruments = {
    'amber': ['amber'],
    'cr2re': ['cr2re', 'crires+', 'crires2'],
    'crires': ['crires'],
    'efosc': ['efosc', 'efosc2'],
    'eris': ['eris'],
    'esotk': ['esotk'],
    'espda': ['espda', 'espresso_da'],
    'espdr': ['espdr', 'espresso_dr', 'espresso'],
    'fors': ['fors', 'fors1', 'fors2'],
    'giraf': ['giraf', 'giraffe'],
    'gravity': ['gravity'],
    'harps': ['harps'],
    'hawki': ['hawki'],
    'iiinstrument': ['iiinstrument'],
    'isaac': ['isaac'],
    'kmos': ['kmos'],
    'matisse': ['matisse'],
    'midi': ['midi'],
    'molecfit': ['molecfit'],
    'muse': ['muse'],
    'naco': ['naco'],
    'nirps': ['nirps'],
    'sinfo': ['sinfo', 'sinfoni'],
    'sofi': ['sofi'],
    'spher': ['spher', 'sphere'],
    'uves': ['uves'],
    'vcam': ['vcam', 'vircam'],
    'vimos': ['vimos'],
    'visir': ['visir'],
    'xshoo': ['xshoo', 'xshooter']
}


def get_key_by_list_value(d, target_list):
    for key, value in d.items():
        if target_list in value:
            return key
    return None



def install_esopipe(pipe):
    package1 = f"esopipe-{pipe}-wkf"
    package2 = f"esopipe-{pipe}-datastatic"
    command = ["sudo", "dnf", "install", "-y", package1, package2]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully installed packages for {pipe}")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")


#_____________________________________________________________________________

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('instrument_in', type=str)
    parser.add_argument('-d', '--download_demodata', action='store_true', help='Download demo data')
    parser.add_argument('-w', '--demodata_dir', type=str, help='Root directory to write the demo data in',
                        default='/home/user/EDPS_data')
    args = parser.parse_args()
    
    instrument_in = args.instrument_in.lower()
    instrument = get_key_by_list_value(instruments, instrument_in)
    if instrument is None:
        print('Instrument unknown, exiting ...')
        exit(1)

    # Install the requested pipeline ...
    ###install_esopipe(instrument)

    # ... and, if so whished, the demo data ...
    if args.download_demodata:
        extractor = utilities.DemoDataExtractor('https://www.eso.org/sci/software/pipe_aem_table.html')
        link = extractor.get_demo_data_link(instrument)
        print(f"The Demo Data link for {instrument.upper()} is: {link}")

        # Extract the filename from the URL
        filename = os.path.basename(urlparse(link).path)

        # Download the file with a progress indicator
        response = requests.get(link, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        with open(filename, 'wb') as f, tqdm(total=total_size, unit='iB', unit_scale=True) as progress_bar:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))

        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall(path=args.demodata_dir, filter=utilities.safe_extract_filter)

        os.remove(filename)

    print('All done!')
