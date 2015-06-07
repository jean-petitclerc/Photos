__author__ = 'Jean'
# -*- coding: utf-8 -*-

import os, sys
import exifread

def get_exif_data(photo_dir, photo_file):
    print("Dossier de la photo: %s" % photo_dir)
    print("Nom de la photo....: %s" % photo_file)
    photo_path = os.path.join(photo_dir, photo_file)
    f = open(photo_path, 'rb')
    tags = exifread.process_file(f)
    print("Liste des tags")
    for (k,v) in tags.items():
        print("Got",k,"that maps to",v)
    print("*** fin de la liste")
    print()

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

