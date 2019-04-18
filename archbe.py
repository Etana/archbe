#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import os
from PIL import Image
import re
import requests
import sys

if not len(sys.argv) > 1:
    print('USAGE: archbe.py [scale] <url>', file=sys.stderr)
    sys.exit(0)

source_url = sys.argv[-1]
scalefactor = int(sys.argv[1]) if len(sys.argv) > 2 else 2

BASE_URL = 'https://search.arch.be'
INFO_URL = BASE_URL + '/imageserver/topview.json.php?FIF='

match = list(re.search(r'((((\d{3})_\d{4}_\d{3})_\d{5}_\w{3})_\w{1}_\d{4}(?:_\w)?)', source_url).groups())
output = sys.stdout.buffer
if sys.stdout.isatty():
    output = '{}.jpg'.format(match[0])
    if os.path.exists(output):
        print('WARNING file {} already exists'.format(output), file=sys.stderr)
        sys.exit()

def put_in_image(url, img, x, y):
    img.paste(Image.open(s.get(url, stream=True).raw), (x, y))

s = requests.Session()
info = s.get(INFO_URL + '{3}/{2}/{1}/{0}.jp2'.format(*match)).json()
base_url = BASE_URL + info['config']['tileurl_v2'].format(file=info['topviews'][0]['filepath'], tile='{}')
tile_width, tile_height = info['topviews'][0]['tileWidth'], info['topviews'][0]['tileHeight']
layer = next(layer for layer in info['topviews'][0]['layers'] if layer['scalefactor'] == scalefactor)
img = Image.new('RGB', (layer['width'], layer['height']))
tile_num = layer['starttile']
with ThreadPoolExecutor(max_workers=6) as executor:
    for y in range(layer['rows']):
        for x in range(layer['cols']):
            executor.submit(put_in_image, base_url.format(tile_num), img, min(x * tile_width, layer['width']), min(y * tile_height, layer['height']))
            tile_num += 1

img.save(output, 'JPEG')
print('OK image (scale 1/{}) saved to {}'.format(scalefactor, output), file=sys.stderr)
