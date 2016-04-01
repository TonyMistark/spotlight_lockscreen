# *-utf8-*

import os
from os.path import join
import struct
import shutil
from comm_def import (
ASSET_DIR, PNG_HEAD, PNG_POSITION,
JPG_HEAD,
)
from custom import imgs_dir


def start_run():
    for file_name in os.listdir(ASSET_DIR):
        full_file_name = join(ASSET_DIR, file_name)
        with open(full_file_name, 'rb') as f:
            file_head = f.read(len(PNG_HEAD))
            print file_name, repr(file_head),
            if file_head == PNG_HEAD:
                f.seek(16)
                width, height = struct.unpack('>ii', f.read(8))
                ext = 'png'
                print width, height
            elif file_head == JPG_HEAD:
                ext = 'jpg'
                f.seek(0)
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    f.seek(size, 1)
                    byte = f.read(1)
                    while ord(byte) == 0xff:
                        byte = f.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', f.read(2))[0] - 2
                f.seek(1, 1)
                height, width = struct.unpack('>HH', f.read(4))
                print width, height
            else:
                width, height = 0, 0
                print ''
            if not os.path.exists(imgs_dir):
                os.makedirs(imgs_dir)
            if width > height > 1000:
                shutil.copy(full_file_name, join(imgs_dir, "{}.{}".format(file_name, ext)))