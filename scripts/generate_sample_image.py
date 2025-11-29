from PIL import Image, ImageDraw
import os

out_dir = os.path.join('pipeline', 'examples')
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, 'sample_satellite.jpg')

w, h = 640, 640
img = Image.new('RGB', (w, h))
d = ImageDraw.Draw(img)

# draw simple patchwork to mimic roofs/roads/vegetation
colors = [(34,139,34),(205,133,63),(169,169,169),(218,165,32),(70,130,180)]
step = 64
for y in range(0, h, step):
    for x in range(0, w, step):
        c = colors[((x//step) + (y//step)) % len(colors)]
        d.rectangle([x, y, x+step-2, y+step-2], fill=c)

# draw some small white rectangles to simulate panels
for i in range(30):
    rx = (i*17) % (w-40) + 10
    ry = (i*31) % (h-20) + 10
    d.rectangle([rx, ry, rx+30, ry+12], fill=(20,20,80))

img.save(path)
print('Wrote sample image to', path)
