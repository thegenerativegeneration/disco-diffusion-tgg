import random
from PIL import Image
import numpy
from yaml import dump, full_load
from pydotted import pydot
import math


def voronoi(points, shape=None):
    depthmap = numpy.ones(shape, float) * 1e308
    colormap = numpy.zeros(shape, int)

    def hypot(X, Y):
        return (X - x) ** 2 + (Y - y) ** 2

    for i, (x, y) in enumerate(points):
        paraboloid = numpy.fromfunction(hypot, shape)
        colormap = numpy.where(paraboloid < depthmap, i + 1, colormap)
        depthmap = numpy.where(paraboloid < depthmap, paraboloid, depthmap)

    # Centroids for each region
    # for (x,y) in points:
    # colormap[x-1:x+2,y-1:y+2] = 0

    return colormap


def draw_map(colormap, palette, write_file=False):
    shape = colormap.shape

    colormap = numpy.transpose(colormap)
    pixels = numpy.empty(colormap.shape + (4,), numpy.int8)

    pixels[:, :, 0] = (palette[colormap] >> 24) & 0xFF  # Red
    pixels[:, :, 1] = (palette[colormap] >> 16) & 0xFF  # Green
    pixels[:, :, 2] = (palette[colormap] >> 8) & 0xFF  # Blue
    pixels[:, :, 3] = palette[colormap] & 0xFF  # Alpha

    image = Image.frombytes("RGBA", shape, pixels)
    if write_file:
        image.save("voronoi.png")
    return image


def render(width=1280, height=768, num_points=20, palette_config=None):
    points = []
    palette = numpy.array([0xFFFFFFFF])
    if palette_config is not None:
        with open(palette_config, "r") as conf:
            c = pydot(full_load(conf))
    else:
        c = pydot({"mode": "static", "palette": [0x00000000]})
    for i in range(num_points):
        random.seed()
        x = random.randint(1, 1280)
        y = random.randint(1, 768)
        points.append([x, y])
        if c.mode == "generated":
            r = random.randint(c.red.low, c.red.high)
            g = random.randint(c.green.low, c.green.high)
            b = random.randint(c.blue.low, c.blue.high)
            a = 255
            palette = numpy.append(
                palette,
                (g << 16) + (b << 8) + (a) + (r << 24),
            )

    if c.mode == "static":
        palette = numpy.array(c.palette)
        times = math.ceil(num_points / len(palette)) + 1  # stupid padding i dunno i'm off by 1 index
        palette = numpy.tile(palette, times)
    colormap = voronoi(points, shape=(width, height))
    return draw_map(colormap, palette)


def main():
    render(width=1280, height=768, num_points=20, palette_config="palettes/default.yaml")


if __name__ == "__main__":
    main()
