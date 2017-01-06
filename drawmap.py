from omg import *
import sys
from PIL import Image, ImageDraw

def drawmap(wad, name, width):
    xsize = width - 8

    edit = MapEditor(wad.maps[name])
    xmin = ymin = 32767
    xmax = ymax = -32768
    for v in edit.vertexes:
        xmin = min(xmin, v.x)
        xmax = max(xmax, v.x)
        ymin = min(ymin, -v.y)
        ymax = max(ymax, -v.y)

    scale = xsize / float(xmax - xmin)
    xmax = int(xmax * scale)
    xmin = int(xmin * scale)
    ymax = int(ymax * scale)
    ymin = int(ymin * scale)

    for v in edit.vertexes:
        v.x = v.x * scale
        v.y = -v.y * scale

    im = Image.new('RGB', ((xmax - xmin) + 8, (ymax - ymin) + 8), (255,255,255))
    draw = ImageDraw.Draw(im)

    edit.linedefs.sort(lambda a, b: cmp(not a.two_sided, not b.two_sided))

    for line in edit.linedefs:
         p1x = edit.vertexes[line.vx_a].x - xmin + 4
         p1y = edit.vertexes[line.vx_a].y - ymin + 4
         p2x = edit.vertexes[line.vx_b].x - xmin + 4
         p2y = edit.vertexes[line.vx_b].y - ymin + 4

         color = (0, 0, 0)
         if line.two_sided:
             color = (144, 144, 144)
         if line.action:
             color = (220, 130, 50)

         draw.line((p1x, p1y, p2x, p2y), fill=color)
         draw.line((p1x+1, p1y, p2x+1, p2y), fill=color)
         #draw.line((p1x-1, p1y, p2x-1, p2y), fill=color)
         #draw.line((p1x, p1y+1, p2x, p2y+1), fill=color)
         draw.line((p1x, p1y-1, p2x, p2y-1), fill=color)

    del draw

    return im
