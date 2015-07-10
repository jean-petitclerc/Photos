create table photo (
  photo_date date not null,
  photo_name text not null,
  file_name text not null,
  image_length int,
  image_width int,
  image_datetime text,
  gps_latitude real,
  gps_longitude real,
  camera_make text,
  camera_model text,
  orientation text)
;
create unique index photo_pk
  on photo(photo_date, photo_name)
;
create table photo_location (
  photo_date date not null,
  photo_name text not null,
  dir_name text not null)
;
create unique index photo_loc_pk
  on photo_location (photo_date, photo_name, dir_name)
;