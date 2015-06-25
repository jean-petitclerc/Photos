__author__ = 'Jean'
# -*- coding: utf-8 -*-

import os, sys
import exifread

class Photo(object):
    def __init__(self, photo_date, photo_name, dir_name, file_name):
        self.photo_date = photo_date
        self.photo_name = photo_name
        self.dir_name   = dir_name
        self.file_name  = file_name
        self.exif_datetime_original = None
        self.exif_image_length      = None
        self.exif_image_width       = None
        self.exif_exposure_time     = None
        self.exif_f_number          = None
        self.exif_focal_length      = None
        self.exif_iso_speed         = None
        self.exif_unique_id         = None
        self.gps_latitude           = None
        self.gps_latitude_ref       = None
        self.gps_longitude          = None
        self.gps_longitude_ref      = None
        self.image_datetime         = None
        self.camera_make            = None
        self.camera_model           = None
        self.orientation            = None

    def set_exif_data(self, key, value):
        if key == "EXIF DateTimeOriginal":
            self.exif_datetime_original = value
        elif key == "EXIF ExifImageLength":
            self.exif_image_length = value
        elif key == "EXIF ExifImageWidth":
            self.exif_image_width = value
        elif key == "EXIF ExposureTime":
            self.exif_exposure_time = value
        elif key == "EXIF FNumber":
            self.exif_f_number = value
        elif key == "EXIF FocalLength":
            self.exif_focal_length = value
        elif key == "EXIF ISOSpeedRatings":
            self.exif_iso_speed = value
        elif key == "EXIF ImageUniqueID":
            self.exif_unique_id = value
        elif key == "GPS GPSLatitude":
            self.gps_latitude = value
        elif key == "GPS GPSLatitudeRef":
            self.gps_latitude_ref = value
        elif key == "GPSLongitude":
            self.gps_longitude = value
        elif key == "GPSLongitudeRef":
            self.gps_longitude_ref = value
        elif key == "Image DateTime":
            self.image_datetime  = value
        elif key == "Image Make":
            self.camera_make = value
        elif key == "Image Model":
            self.camera_model = value
        elif key == "Image Orientation":
            self.orientation = value
        else:
            pass

    def __str__(self):
        l_exif_datetime_original = self.exif_datetime_original or "Not defined"
        l_exif_image_length      = self.exif_image_length      or "Not defined"
        l_exif_image_width       = self.exif_image_width       or "Not defined"
        l_exif_exposure_time     = self.exif_exposure_time     or "Not defined"
        l_exif_f_number          = self.exif_f_number          or "Not defined"
        l_exif_focal_length      = self.exif_focal_length      or "Not defined"
        l_exif_iso_speed         = self.exif_iso_speed         or "Not defined"
        l_exif_unique_id         = self.exif_unique_id         or "Not defined"
        l_gps_latitude           = self.gps_latitude           or "Not defined"
        l_gps_latitude_ref       = self.gps_latitude_ref       or "Not defined"
        l_gps_longitude          = self.gps_longitude          or "Not defined"
        l_gps_longitude_ref      = self.gps_longitude_ref      or "Not defined"
        l_image_datetime         = self.image_datetime         or "Not defined"
        l_camera_make            = self.camera_make            or "Not defined"
        l_camera_model           = self.camera_model           or "Not defined"
        l_orientation            = self.orientation            or "Not defined"
        return "Photo:\n" + \
               "  Name................: " + self.photo_name + "\n"   + \
               "  Date................: " + self.photo_date + "\n"   + \
               "  Path................: " + self.dir_name   + "\n"   + \
               "  File................: " + self.file_name  + "\n"   + \
               "  EXIF DateTime.......: " + l_exif_datetime_original + "\n" + \
               "  EXIF Image Length...: " + l_exif_image_length      + "\n" + \
               "  EXIF Image Width....: " + l_exif_image_width       + "\n" + \
               "  EXIF Exposure Time..: " + l_exif_exposure_time     + "\n" + \
               "  EXIF F Number.......: " + l_exif_f_number          + "\n" + \
               "  EXIF Focal Length...: " + l_exif_focal_length      + "\n" + \
               "  EXIF ISO Speed......: " + l_exif_iso_speed         + "\n" + \
               "  EXIF Unique ID......: " + l_exif_unique_id         + "\n" + \
               "  GPS Latitude........: " + l_gps_latitude           + "\n" + \
               "  GPS Latitude Ref....: " + l_gps_latitude_ref       + "\n" + \
               "  GPS Longitude.......: " + l_gps_longitude          + "\n" + \
               "  GPS Longitude Ref...: " + l_gps_longitude_ref      + "\n" + \
               "  Image DateTime......: " + l_image_datetime         + "\n" + \
               "  Camera Make.........: " + l_camera_make            + "\n" + \
               "  Camera Model........: " + l_camera_model           + "\n" + \
               "  Image Orientation...: " + l_orientation            + "\n"
    def consolidate_properties(self):
        pass

    def save(self):
        pass

def get_exif_data(photo_dir, photo_file):
    print("Dossier de la photo: %s" % photo_dir)
    print("Nom de la photo....: %s" % photo_file)
    photo_date = get_date_from_dir(photo_dir)
    photo_temp = os.path.basename(photo_file)
    photo_name, photo_ext = os.path.splitext(photo_temp)
    photo = Photo(photo_date, photo_name, photo_dir, photo_file)
    photo_path = os.path.join(photo_dir, photo_file)
    f = open(photo_path, 'rb')
    tags = exifread.process_file(f, details=False)
    print("Liste des tags")
    for key in sorted(tags.keys()):
        val = str(tags[key])
        #print("Got>",key,"< : >",val,"<")
        photo.set_exif_data(key, val)
    print("*** fin de la liste")
    print(photo)
    photo.consolidate_properties()
    db_record_photo(photo)
    print()

def get_date_from_dir(path):
    import re
    dirs = path.split(os.sep)
    last_dir = dirs[-1]
    p = re.compile('^[12][0-9]{3}-[01][0-9]-[0123][0-9]$')
    if p.match(last_dir):
        return last_dir
    else:
        return '0001-01-01'

def filter_exif_data(key, value, photo):
    if key == "EXIF DateTimeOriginal ":
        photo.exif_datetime_original = value
    elif key == "EXIF ExifImageLength ":
        photo.exif_image_length = value
    elif key == "EXIF ExifImageWidth ":
        photo.exif_image_width = value
    elif key == "EXIF ExposureTime":
        photo.exif_exposure_time = value
    elif key == "EXIF FNumber":
        photo.exif_f_number = value
    elif key == "EXIF FocalLength":
        photo.exif_focal_length = value
    elif key == "EXIF ISOSpeedRatings":
        photo.exif_iso_speed = value
    elif key == "EXIF ImageUniqueID":
        photo.exif_unique_id = value
    elif key == "GPS GPSLatitude":
        photo.gps_latitude = value
    elif key == "GPS GPSLatitudeRef":
        photo.gps_latitude_ref = value
    elif key == "GPSLongitude":
        photo.gps_longitude = value
    elif key == "GPSLongitudeRef":
        photo.gps_longitude_ref = value
    elif key == "Image DateTime":
        photo.image_datetime  = value
    elif key == "Image Make":
        photo.camera_make = value
    elif key == "Image Model":
        photo.camera_model = value
    elif key == "Image Orientation":
        photo.orientation = value
    else:
        pass

def finalize_photo(photo):
    pass

def db_record_photo(photo):
    pass

def scan_dir(start_dir):
    count_jpeg = 0
    count_others = 0
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if (file.endswith(".jpg") or file.endswith(".jpeg") or
                file.endswith(".JPG") or file.endswith(".JPEG")):
                count_jpeg += 1
                #print(os.path.join(root, file))
                get_exif_data(root, file)
            else:
                print(os.path.join(root, file))
                count_others += 1
    print("Fichiers jpeg trouvés..: %i" % count_jpeg)
    print("Fichiers autres trouvés: %i" % count_others)

def main():
    if (len(sys.argv) - 1) < 1:
        print("Ce programme a besoin d'un argument, le dossier de départ.")
        return 8
    start_dir = sys.argv[1]
    print("Dossier de départ: %s" % start_dir)
    scan_dir(start_dir)
    return 0

if __name__ == "__main__":
    sys.exit(main())

