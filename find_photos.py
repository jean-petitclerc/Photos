__author__ = 'Jean'
# -*- coding: utf-8 -*-
#TODO : Implement configuration file

import os, sys, shutil
from optparse import OptionParser
import exifread
import sqlite3

# Global variable
# parms
parm_copy = False
conn = None  # DB handle

# Global constant
MASTER_LOCATION = "c:\\backup\\Photos\\"


class Photo(object):
    def __init__(self, photo_date, photo_name, dir_name, file_name):
        self.photo_date = photo_date
        self.photo_name = photo_name
        self.dir_name = dir_name
        self.file_name = file_name
        self.exif_datetime_original = None
        self.exif_image_length = None
        self.exif_image_width = None
        self.exif_exposure_time = None
        self.exif_f_number = None
        self.exif_focal_length = None
        self.exif_iso_speed = None
        self.exif_unique_id = None
        self.gps_latitude = None
        self.gps_latitude_ref = None
        self.gps_lat = None
        self.gps_longitude = None
        self.gps_longitude_ref = None
        self.gps_lon = None
        self.image_datetime = None
        self.camera_make = None
        self.camera_model = None
        self.orientation = None

    def set_exif_data(self, key, value):
        if key == "EXIF DateTimeOriginal":
            self.exif_datetime_original = str(value)
        elif key == "EXIF ExifImageLength":
            self.exif_image_length = value.values[0]
        elif key == "EXIF ExifImageWidth":
            self.exif_image_width = value.values[0]
        elif key == "EXIF ExposureTime":
            self.exif_exposure_time = str(value)
        elif key == "EXIF FNumber":
            self.exif_f_number = str(value)
        elif key == "EXIF FocalLength":
            self.exif_focal_length = str(value)
        elif key == "EXIF ISOSpeedRatings":
            self.exif_iso_speed = str(value)
        elif key == "EXIF ImageUniqueID":
            self.exif_unique_id = str(value)
        elif key == "GPS GPSLatitude":
            self.gps_latitude = value.values
        elif key == "GPS GPSLatitudeRef":
            self.gps_latitude_ref = str(value)
        elif key == "GPS GPSLongitude":
            self.gps_longitude = value.values
        elif key == "GPS GPSLongitudeRef":
            self.gps_longitude_ref = str(value)
        elif key == "Image DateTime":
            self.image_datetime = str(value)
        elif key == "Image Make":
            self.camera_make = str(value)
        elif key == "Image Model":
            self.camera_model = str(value)
        elif key == "Image Orientation":
            self.orientation = str(value)
        else:
            pass

    def __str__(self):
        l_exif_datetime_original = self.exif_datetime_original or "Not defined"
        l_exif_image_length = self.exif_image_length or "Not defined"
        l_exif_image_width = self.exif_image_width or "Not defined"
        l_exif_exposure_time = self.exif_exposure_time or "Not defined"
        l_exif_f_number = self.exif_f_number or "Not defined"
        l_exif_focal_length = self.exif_focal_length or "Not defined"
        l_exif_iso_speed = self.exif_iso_speed or "Not defined"
        l_exif_unique_id = self.exif_unique_id or "Not defined"
        l_gps_latitude = str(self.gps_latitude) or "Not defined"
        l_gps_lat = self.gps_lat or "Not defined"
        l_gps_latitude_ref = self.gps_latitude_ref or "Not defined"
        l_gps_longitude = str(self.gps_longitude) or "Not defined"
        l_gps_longitude_ref = self.gps_longitude_ref or "Not defined"
        l_gps_lon = self.gps_lon or "Not defined"
        l_image_datetime = self.image_datetime or "Not defined"
        l_camera_make = self.camera_make or "Not defined"
        l_camera_model = self.camera_model or "Not defined"
        l_orientation = self.orientation or "Not defined"
        return "Photo:\n" + \
               "  Name................: " + self.photo_name + "\n" + \
               "  Date................: " + self.photo_date + "\n" + \
               "  Path................: " + self.dir_name + "\n" + \
               "  File................: " + self.file_name + "\n" + \
               "  EXIF DateTime.......: " + l_exif_datetime_original + "\n" + \
               "  EXIF Image Length...: " + str(l_exif_image_length) + "\n" + \
               "  EXIF Image Width....: " + str(l_exif_image_width) + "\n" + \
               "  EXIF Exposure Time..: " + l_exif_exposure_time + "\n" + \
               "  EXIF F Number.......: " + l_exif_f_number + "\n" + \
               "  EXIF Focal Length...: " + l_exif_focal_length + "\n" + \
               "  EXIF ISO Speed......: " + l_exif_iso_speed + "\n" + \
               "  EXIF Unique ID......: " + l_exif_unique_id + "\n" + \
               "  GPS Latitude........: " + l_gps_latitude + "\n" + \
               "  GPS Latitude Ref....: " + l_gps_latitude_ref + "\n" + \
               "  GPS Latitude (fixed): " + l_gps_lat + "\n" + \
               "  GPS Longitude.......: " + l_gps_longitude + "\n" + \
               "  GPS Longitude Ref...: " + l_gps_longitude_ref + "\n" + \
               "  GPS Longitude(fixed): " + l_gps_lon + "\n" + \
               "  Image DateTime......: " + l_image_datetime + "\n" + \
               "  Camera Make.........: " + l_camera_make + "\n" + \
               "  Camera Model........: " + l_camera_model + "\n" + \
               "  Image Orientation...: " + l_orientation + "\n"

    def consolidate_properties(self):
        # Fix timestamp format
        if self.exif_datetime_original is not None:
            (temp_date, temp_time) = self.exif_datetime_original.split()
            temp_date = temp_date.replace(':', '-')
            self.exif_datetime_original = temp_date + ' ' + temp_time

        # Fix timestamp format
        if self.image_datetime is not None:
            (temp_date, temp_time) = self.image_datetime.split()
            temp_date = temp_date.replace(':', '-')
            self.image_datetime = temp_date + ' ' + temp_time

        # Reformat GPS Lat/Lon
        if self.gps_latitude is not None:
            self.gps_lat = str(self.gps_latitude[0]) + '.'
            if self.gps_latitude[1].den == 1:
                self.gps_lat += str(self.gps_latitude[1])
                self.gps_lat += '.'
                min_sec = float(self.gps_latitude[2].num) / float(self.gps_latitude[2].den)
            else:
                min_sec = float(self.gps_latitude[1].num) / float(self.gps_latitude[1].den)
            self.gps_lat += str(min_sec)
            self.gps_lat += self.gps_latitude_ref
        if self.gps_longitude is not None:
            self.gps_lon = str(self.gps_longitude[0]) + '.'
            if self.gps_longitude[1].den == 1:
                self.gps_lon += str(self.gps_longitude[1])
                self.gps_lon += '.'
                min_sec = float(self.gps_longitude[2].num) / float(self.gps_longitude[2].den)
            else:
                min_sec = float(self.gps_longitude[1].num) / float(self.gps_longitude[1].den)
            self.gps_lon += str(min_sec)
            self.gps_lon += self.gps_longitude_ref

        # Try hard to find a date
        if self.photo_date == '0001-01-01':
            if self.image_datetime is not None:
                self.photo_date = self.image_datetime[0:10]
            elif self.exif_datetime_original is not None:
                self.photo_date = self.exif_datetime_original[0:10]
            else:
                print("No date found for this photo: " + self.photo_name)


def get_exif_data(photo_dir, photo_file):
    global parm_copy
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
        val = tags[key]
        # print("Got>",key,"< : >",val,"<")
        photo.set_exif_data(key, val)
    print("*** fin de la liste")
    # print(photo)
    photo.consolidate_properties()
    print(photo)
    db_record_photo(photo)
    copy_to_master_location(photo)
    print()


def db_record_photo(photo):
    global conn
    insert = \
        '''
        insert into photo(photo_date, photo_name, file_name, image_length, image_width, image_datetime,
                          gps_latitude, gps_longitude, camera_make, camera_model, orientation)
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

    select = \
        '''
        select image_length, image_width
          from photo
         where photo_date = ?
           and photo_name = ?
        '''

    try:
        cur = conn.cursor()
        cur.execute(select, [photo.photo_date, photo.photo_name])
        row = cur.fetchone()
        if row is None:
            ins = conn.cursor()
            ins.execute(insert, [photo.photo_date, photo.photo_name, photo.file_name, photo.exif_image_length,
                                 photo.exif_image_width, photo.image_datetime, photo.gps_lat, photo.gps_lon,
                                 photo.camera_make, photo.camera_model, photo.orientation])
            db_record_location(photo)
        else:
            if (row[0] == photo.exif_image_length) and (row[1] == photo.exif_image_width):
                print("Photo is already in the database")
                db_record_location(photo)
            else:
                print("Error: Same photo but different size")
                print("Photo date...: " + photo.photo_date)
                print("Photo name...: " + photo.photo_name)
                print("In DB, length: " + str(row[0]))
                print("        width: " + str(row[1]))
                print("New, length..: " + str(photo.exif_image_length))
                print("     width...: " + str(photo.exif_image_width))
    except sqlite3.Error as x:
        print("SQL Error: \n" + str(x))


def db_record_location(photo):
    select = \
        '''
        select count(*)
          from photo_location
         where photo_date = ?
           and photo_name = ?
           and dir_name   = ?
        '''
    insert = \
        '''
        insert into photo_location(photo_date, photo_name, dir_name)
            values(?, ?, ?)
        '''

    try:
        cur = conn.cursor()
        cur.execute(select, [photo.photo_date, photo.photo_name, photo.dir_name])
        row = cur.fetchone()
        if row[0] == 0:
            print("New location for photo: " + photo.dir_name)
            ins = conn.cursor()
            ins.execute(insert, [photo.photo_date, photo.photo_name, photo.dir_name])
        else:
            print("Location already in the DB: " + photo.dir_name)

    except sqlite3.Error as x:
        print("SQL Error: \n" + str(x))


def copy_to_master_location(photo):
    global MASTER_LOCATION, parm_copy
    master_dir_name = MASTER_LOCATION + photo.photo_date
    if master_dir_name != photo.dir_name:
        print("Photo not found in master location")
        print("Photo Date..........: " + photo.photo_date)
        print("Photo Name..........: " + photo.photo_name)
        print("Current location....: " + photo.dir_name)
        print("Expected location...: " + master_dir_name)
        if parm_copy:
            src_file = photo.dir_name + os.sep + photo.file_name
            dst_file = master_dir_name + os.sep + photo.file_name
            if not os.path.isdir(master_dir_name):
                os.mkdir(master_dir_name)
            if not os.path.isfile(master_dir_name + os.sep + photo.file_name):
                print("Copying from: " + src_file)
                print("          to: " + dst_file)
                shutil.copy2(src_file, dst_file)
                photo.dir_name = master_dir_name
                db_record_location(photo)


def get_date_from_dir(path):
    import re

    dirs = path.split(os.sep)
    last_dir = dirs[-1]
    p = re.compile('^[12][0-9]{3}-[01][0-9]-[0123][0-9]$')
    if p.match(last_dir):
        return last_dir
    else:
        return '0001-01-01'


def scan_dir(start_dir):
    count_jpeg = 0
    count_others = 0
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if (file.endswith(".jpg") or file.endswith(".jpeg") or
                    file.endswith(".JPG") or file.endswith(".JPEG")):
                count_jpeg += 1
                # print(os.path.join(root, file))
                get_exif_data(root, file)
            else:
                print(os.path.join(root, file))
                count_others += 1
    print("Fichiers jpeg trouvés..: %i" % count_jpeg)
    print("Fichiers autres trouvés: %i" % count_others)


def parse_options():
    # Use optparse to get parms
    usage = "usage: %prog [options] starting_directory"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--copy", dest="copy", action="store_true", default=False,
                      help="Copy the photo to the expected location if needed.")
    (options, args) = parser.parse_args()
    return (options, args) # options: copy; args: starting_directory


def main():
    global parm_copy, conn
    print("Starting " + sys.argv[0] + "\n")
    # Get parameters and validate them
    (options, args) = parse_options()
    parm_copy = options.copy
    if len(args) < 1:
        print("Ce programme a besoin d'un argument, le dossier de départ.")
        return 8
    start_dir = args[0]
    print("Paramètres:")
    print("    Dossier de départ.........: %s" % start_dir)
    print("    Option de copie...........: ", end='')
    print("On" if parm_copy else "Off")
    print()

    conn = sqlite3.connect('data/photos.db')
    scan_dir(start_dir)
    conn.commit()
    conn.close()
    print("\nEnding " + sys.argv[0] + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
