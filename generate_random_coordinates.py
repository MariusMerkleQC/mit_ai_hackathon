import piexif
import random
from path_utils import get_normal_test_image_paths, get_abnormal_test_image_paths, get_training_image_paths

def generate_random_coordinates():
    # Generate random float coordinates for latitude and longitude
    latitude = random.uniform(47.5, 48.8)
    longitude = random.uniform(7.5, 8.5)

    return latitude, longitude


def convert_random_coodtinates(latitude, longitude):
    # Convert to deg, min, sec format
    latitude_in_dms = convert_to_deg_min_sec(latitude)
    longitude_in_dms = convert_to_deg_min_sec(longitude)

    return latitude_in_dms, longitude_in_dms

def convert_to_deg_min_sec(coord):
    """Convert decimal coordinates into degrees, minutes and seconds tuple"""
    _deg = abs(coord)
    _min = (_deg - int(_deg)) * 60
    _sec = (_min - int(_min)) * 60
    deg = int(_deg)
    minute = int(_min)
    second = round(_sec * 100)

    return deg, minute, second

def set_gps_location(image_path, lat, lng):
    exif_dict = piexif.load(image_path)

    gps_if = {
         piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
         piexif.GPSIFD.GPSLatitudeRef: 'N' if lat[0] >= 0 else 'S',
         piexif.GPSIFD.GPSLatitude: ((lat[0], 1), (lat[1], 1), (lat[2], 100)),
         piexif.GPSIFD.GPSLongitudeRef: 'E' if lng[0] >= 0 else 'W',
         piexif.GPSIFD.GPSLongitude: ((lng[0], 1), (lng[1], 1), (lng[2], 100)),
    }

    exif_dict["GPS"] = gps_if

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)


if __name__ == "__main__":
    paths = get_training_image_paths() + get_abnormal_test_image_paths() + get_normal_test_image_paths()
    for path in paths:
        latitude, longitude = generate_random_coordinates()
        latitude_in_dms, longitude_in_dms = convert_random_coodtinates(latitude, longitude)
        set_gps_location(str(path), latitude_in_dms, longitude_in_dms)