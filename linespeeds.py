import math
from PIL import Image, ImageDraw, ImageFont
import csv
import numpy as np


def main():
    se = (deg2num(61.5376, 23.626, 13), deg2num(61.4269, 23.964, 13))
    img = openImage("tampere.png")
    data = read_data("busdata.csv")
    # data = organize_data(data)
    draw_busses(img, data, se)
    img.save('result.png')
    img.show()


def openImage(img_name):
    return Image.open(img_name)


def read_data(data_file):
    data = []
    with open(data_file, mode='r') as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        for row in csv_reader:
            data.append(row)
    return data


def organize_data(data):
    new_data = []

    for d in data:
        if d not in new_data:
            new_data.append({d["Line"], list()})
        new_data[new_data.index(d["Line"])].append(
            d["Line"].append(((d["Latitude"], d["Longitude"]), d["Speed"])))
    return new_data


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def draw_busses(img, data, se):
    for d in data:
        draw_one_buss(img, d, se)


def draw_one_buss(img, buss, se):
    lat = float(buss["Latitude"])
    lon = float(buss["Longitude"])
    draw(img, deg2num(lat, lon, 13), buss["Speed"], se)


def draw(img, coords, speed, se):
    if draw_not_overlapping():
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', size=16)
        color = "rgb(0,0,0)"
        draw.text((se[0][0] - coords[0], se[0][1] - coords[1]),
                  speed, fill=color, font=font)


def draw_not_overlapping():
    return True


main()
