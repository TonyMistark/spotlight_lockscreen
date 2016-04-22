#!/usr/bin/env python
# -*- coding:utf-8 -*-

import struct

class NotImageFileException(Exception):
	pass

class ImageFileTypeChecker(object):
    @classmethod
    def check(cls, img_file):
        img_file.seek(0)
        return img_file.read(4) == cls.HEAD

    @classmethod
    def get_size(cls, img_file):
        raise NotImplementedError()

    @classmethod
    def get_ext(cls):
        return cls.EXT


class JPGChecker(ImageFileTypeChecker):
    HEAD = '\xff\xd8\xff\xe1'
    EXT = 'jpg'

    @staticmethod
    def get_size(jpg_file):
        jpg_file.seek(0)
        size = 2
        ftype = 0
        while not 0xc0 <= ftype <= 0xcf:
            jpg_file.seek(size, 1)
            byte = jpg_file.read(1)
            while ord(byte) == 0xff:
                byte = jpg_file.read(1)
            ftype = ord(byte)
            size = struct.unpack('>H', jpg_file.read(2))[0] - 2
        jpg_file.seek(1, 1)
        height, width = struct.unpack('>HH', jpg_file.read(4))
        return height, width


class PNGChecker(ImageFileTypeChecker):
    HEAD = '\x89PNG'
    EXT = 'png'

    @staticmethod
    def get_size(png_file):
        png_file.seek(16)
        width, height = struct.unpack('>ii', png_file.read(8))
        return height, width


def get_checker(image_file):
    for checker in (PNGChecker, JPGChecker):
        if checker.check(image_file):
            return checker
    else:
        raise NotImageFileException

