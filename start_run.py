# *-utf8-*

import os
from os.path import join
import shutil
from comm_def import ASSET_DIR
from custom import imgs_dir
from image_checker import get_checker, NotImageFileException


def start_run():
    copy_images(ASSET_DIR)

def copy_images(asset_dir):
    for file_name in os.listdir(asset_dir):
        full_file_name = join(asset_dir, file_name)
        with open(full_file_name, 'rb') as f:
            try:
                checker = get_checker(f)
            except NotImageFileException:
                continue

            ext = checker.get_ext()
            height, width = checker.get_size(f)
            if not os.path.exists(imgs_dir):
                os.makedirs(imgs_dir)
            if width > height > 1000:
                shutil.copy(full_file_name, join(imgs_dir, "{}.{}".format(file_name, ext)))

