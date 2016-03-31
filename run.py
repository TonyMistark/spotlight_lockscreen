# *-utf8-*

from os import listdir
from os.path import join
import struct
import shutil

asset_dir = "C:\Users\meila-x\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
imgs_dir = "F:\imgs"

PNG_HEAD = '\x89PNG'
PNG_POSITION = 16
JPG_HEAD = '\xff\xd8\xff\xe1'

def main():
    for file_name in listdir(asset_dir):
        full_file_name = join(asset_dir, file_name)
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
            if width > height > 1000:
                shutil.copy(full_file_name, join(imgs_dir, "{}.{}".format(file_name, ext)))


if __name__ == "__main__":
    main()
