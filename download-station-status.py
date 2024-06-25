import requests
import time
import json
import tarfile
import lzma
import os

def download_data(target_dir="station_status"):
    """Download station status data from the Toronto Bike Share API and compress it using LZMA."""
    # station status URL
    response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status')
    data = response.json()
    timestamp = int(time.time())
    json_file = f'{timestamp}.json'
    with open(json_file, 'w') as f:
        json.dump(data, f)

    tar_file = f'{timestamp}.tar'
    with tarfile.open(tar_file, 'w') as tar:
        tar.add(json_file)

    with open(tar_file, 'rb') as f_in, lzma.open(f'{target_dir}/{tar_file}.xz', 'w', preset=lzma.PRESET_EXTREME) as f_out:
        f_out.write(f_in.read())

    # cleanup files
    os.remove(tar_file)
    os.remove(json_file)

download_data()