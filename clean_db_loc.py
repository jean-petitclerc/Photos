__author__ = 'Jean'
import sys
import os
import sqlite3
from optparse import OptionParser
import configparser


# Global variable
config = {}
conn = None  # DB handle
counts = {"nb_photos": 0, "nb_locations": 0, "found": 0, "not_found": 0}


# Global constant
CONFIG_FILE = 'config' + os.sep + 'photos.cfg'


# parms
parm = {'clean':False}


def parse_options():
    # Use optparse to get parms
    usage = "usage: %prog [options] starting_directory"
    parser = OptionParser(usage=usage)
    parser.add_option("-k", "--clean", dest="clean", action="store_true", default=False,
                      help="Clean the location if the photo is not found in it.")
    (options, args) = parser.parse_args()
    return options, args  # options: copy, rejects; args: starting_directory


def parse_configs():
    global config
    try:
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(CONFIG_FILE)
        config['master_location'] = cfg_parser['default']['MASTER_LOCATION']
        config['db_file'] = cfg_parser['database']['DB_FILE']
    except Exception as x:
        print("Error: Could not read the configuration file: " + CONFIG_FILE)
        print(x)
    return config


def inspect_locations():
    global conn, parm, counts
    select = \
        '''
        select p.photo_name, p.photo_date, l.dir_name, p.file_name
          from photo_location l, photo p
         where l.photo_name = p.photo_name
           and l.photo_date = p.photo_date
         order by p.photo_date, p.photo_name, l.dir_name
        '''
    delete = \
        '''
        delete from photo_location
         where dir_name = ?
           and photo_name = ?
           and photo_date = ?
        '''

    try:
        print("Checking if the locations are all valid...")
        cur = conn.cursor()
        cur.execute(select, [])
        delete_handle = conn.cursor()
        last_photo_name = None
        last_photo_date = None
        row = cur.fetchone()
        while row is not None:
            photo_name = row[0]
            photo_date = row[1]
            dir_name = row[2]
            file_name = row[3]
            counts["nb_locations"] += 1
            if (photo_name != last_photo_name) or (photo_date != last_photo_date):
                print("\nPhoto Name: " + photo_name)
                print("Photo Date: " + photo_date)
                counts["nb_photos"] += 1
                last_photo_name = photo_name
                last_photo_date = photo_date
            complete_file_name = dir_name + os.sep + file_name
            print("    Location: %80s : " % complete_file_name, end='')
            if os.path.isfile(complete_file_name):
                print("Found")
                counts["found"] += 1
            else:
                print("Not Found")
                counts["not_found"] += 1
                if parm["clean"]:
                   delete_handle.execute(delete, [dir_name, photo_name, photo_date])
            row = cur.fetchone()
        print()

    except sqlite3.Error as x:
        print("SQL Error: \n" + str(x))


def main():
    global parm, conn, config
    print("Starting " + sys.argv[0] + "\n")

    # Get parameters and validate them
    (options, args) = parse_options()
    parm["clean"] = options.clean

    print("Paramètres:")
    print("    Option de nettoyage des locations............: ", end='')
    print("On" if parm["clean"] else "Off")
    print()

    config = parse_configs()
    print("Configurations:")
    if config['master_location'] is None:
        print("Error: The MASTER_LOCATION is missing from the [default] section in " + CONFIG_FILE)
        return 8
    if config['db_file'] is None:
        print("Error: The DB_FILE is missing from the [database] section in " + CONFIG_FILE)
        return 8
    print("    Fichier de configuration.....................: " + CONFIG_FILE)
    print("    Master Location..............................: " + config['master_location'])
    print("    Database file................................: " + config['db_file'])
    print()

    conn = sqlite3.connect(config['db_file'])
    inspect_locations()
    conn.commit()
    conn.close()

    print("Counters:")
    print("    Nb de Photos.................................: " + str(counts["nb_photos"]))
    print("    Nb de locations..............................: " + str(counts["nb_locations"]))
    print("        Nb de bonnes locations...................: " + str(counts["found"]))
    print("        Nb de locations invalides................: " + str(counts["not_found"]))


if __name__ == "__main__":
    sys.exit(main())