from PIL import Image
import piexif

def _convert_to_degress(value):
        d, m, s = value
        degrees = d[0] / d[1]
        minutes = m[0] / m[1]
        seconds = s[0] / s[1]
        return degrees + (minutes / 60.0) + (seconds / 3600.0)

def get_gps_data(image_path: str):
    img = Image.open(image_path)
    exif_dict = piexif.load(img.info.get('exif', b''))
    
    gps_data = exif_dict.get('GPS', {})
    if not gps_data:
        print("No GPS data found.")
        return None

    latitude = _convert_to_degress(gps_data[piexif.GPSIFD.GPSLatitude])
    if gps_data[piexif.GPSIFD.GPSLatitudeRef] != b'N':
        latitude = -latitude

    longitude = _convert_to_degress(gps_data[piexif.GPSIFD.GPSLongitude])
    if gps_data[piexif.GPSIFD.GPSLongitudeRef] != b'E':
        longitude = -longitude

    return latitude, longitude


if __name__ == "__main__":
    # Example usage
    image_path = "data/training/DJI_M300_H20t_0001.jpg"
    gps_coords = get_gps_data(image_path)
    if gps_coords:
        print(f"Latitude: {gps_coords[0]}, Longitude: {gps_coords[1]}")
