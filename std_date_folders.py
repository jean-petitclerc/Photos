__author__ = 'jean'
# -*- coding: utf-8 -*-

import sys, os

def scan_dir(start_dir, cur_dt_fmt):
    try:
        for root, dirs, files in os.walk(start_dir):
            for dir in dirs:
                print("Found this directory: %s" % dir, end='')
                if cur_dt_fmt == 'MDY':
                    mm, dd, yyyy = dir.split('-')
                else:
                    dd, mm, yyyy = dir.split('-')
                new_dir = yyyy + '-' + mm + '-' + dd
                print(" New name: %s" % new_dir)
                os.rename(os.path.join(root, dir), os.path.join(root, new_dir))
    except OSError as e:
        print("OS error: {0}".format(e))


def main():
    if (len(sys.argv) - 1) < 2:
        print("Ce programme a besoin de deux arguments, "
              "le dossier de depart et le format de date MDY ou DMY.")
        return 8
    start_dir = sys.argv[1]
    cur_dt_fmt = sys.argv[2]
    cur_dt_fmt = cur_dt_fmt.upper()
    if cur_dt_fmt not in ['DMY', 'MDY']:
        print("Le format doit etre MDY ou DMY")
        return 8
    print("Dossier de depart: %s" % start_dir)
    print("Format initial...: %s" % cur_dt_fmt)
    scan_dir(start_dir, cur_dt_fmt)
    return 0

if __name__ == "__main__":
    sys.exit(main())