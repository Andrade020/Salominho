from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw

BASE_W = 320
BASE_H = 512
SCALE = 2
OUT_W = BASE_W * SCALE
OUT_H = BASE_H * SCALE

# Paleta
INK = (51, 45, 38)
PATH = (235, 209, 151)
PATH_EDGE = (122, 92, 58)
RED = (231, 55, 47)
RED_HI = (255, 159, 145)
BLUE = (37, 137, 235)
BLUE_HI = (168, 224, 255)
WHITE = (248, 245, 232)
WATER = (57, 151, 219)
WATER_LIGHT = (143, 218, 247)
SAND = (220, 188, 121)
ROCK = (127, 105, 80)
ROCK_DARK = (84, 70, 58)
GREEN = (91, 155, 77)
GREEN_DARK = (50, 106, 56)
LEAF = (52, 126, 66)
LEAF_LIGHT = (93, 169, 75)
WOOD = (115, 72, 42)
GOLD = (214, 164, 64)
PURPLE = (86, 55, 111)
CREAM = (239, 226, 192)


@dataclass(frozen=True)
class MapSpec:
    key: str
    folder: str
    chapters: int
    completed_default: int
    painter: Callable[[ImageDraw.ImageDraw, random.Random], None]


def pxpoly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width=1):
    draw.polygon(points, fill=fill)
    if outline:
        draw.line(points + [points[0]], fill=outline, width=width, joint="curve")


def draw_cloud(draw, x, y, s=1.0, color=(244, 242, 224)):
    r = max(2, int(7 * s))
    for dx, dy, rr in [(-8, 2, r), (0, -2, r + 2), (8, 2, r), (15, 4, r - 2)]:
        draw.ellipse((x + dx - rr, y + dy - rr, x + dx + rr, y + dy + rr), fill=color)


def draw_mountain(draw, x, base_y, w, h, fill=(150, 107, 77), shadow=(111, 78, 63)):
    pxpoly(draw, [(x - w // 2, base_y), (x, base_y - h), (x + w // 2, base_y)], fill, ROCK_DARK)
    pxpoly(draw, [(x, base_y - h), (x + w // 2, base_y), (x + w // 8, base_y)], shadow)


def draw_tree(draw, x, y, s=1.0, fruit=False, dead=False):
    tw = max(2, int(4 * s))
    th = max(6, int(18 * s))
    draw.rectangle((x - tw // 2, y, x + tw // 2, y + th), fill=WOOD)
    if dead:
        draw.line((x, y + 4, x - int(10*s), y - int(8*s)), fill=WOOD, width=max(1, int(2*s)))
        draw.line((x, y + 5, x + int(9*s), y - int(10*s)), fill=WOOD, width=max(1, int(2*s)))
        return
    r = max(5, int(11 * s))
    for cx, cy, rr, c in [
        (x, y - int(6*s), r, LEAF),
        (x - int(7*s), y - int(9*s), max(4, r-2), LEAF_LIGHT),
        (x + int(7*s), y - int(8*s), max(4, r-2), LEAF_LIGHT),
    ]:
        draw.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), fill=c)
    if fruit:
        for dx, dy in [(-8,-12),(4,-15),(9,-5),(-2,-2),(-12,-4)]:
            draw.rectangle((x+dx, y+dy, x+dx+2, y+dy+2), fill=(208, 55, 45))


def draw_palm(draw, x, y, s=1.0):
    h = int(20*s)
    draw.line((x, y, x-2, y-h), fill=WOOD, width=max(2, int(3*s)))
    top = (x-2, y-h)
    for ang in [-150,-115,-75,-35,0,35]:
        rad = math.radians(ang)
        ex = top[0] + int(math.cos(rad)*12*s)
        ey = top[1] + int(math.sin(rad)*7*s)
        draw.line((top[0], top[1], ex, ey), fill=LEAF, width=max(2, int(3*s)))


def draw_tent(draw, x, y, s=1.0, color=(210, 177, 125)):
    w = int(26*s)
    h = int(16*s)
    pxpoly(draw, [(x-w//2,y+h//2),(x,y-h),(x+w//2,y+h//2)], color, ROCK_DARK)
    draw.line((x,y-h,x,y+h//2), fill=ROCK_DARK, width=max(1,int(2*s)))
    draw.line((x-w//2,y+h//2,x+w//2,y+h//2), fill=ROCK_DARK, width=1)


def draw_waterfall(draw, x, y, w=24, h=30):
    draw.rectangle((x-w//2,y,x+w//2,y+h), fill=WATER)
    for dx in [-w//3,0,w//3]:
        draw.line((x+dx,y+2,x+dx-1,y+h-2), fill=WATER_LIGHT, width=2)
    draw.ellipse((x-w//2-4,y+h-4,x+w//2+4,y+h+5), fill=WATER_LIGHT)


def draw_ark(draw, x, y, s=1.0):
    w = int(42*s)
    h = int(16*s)
    draw.ellipse((x-w//2,y-h//2,x+w//2,y+h//2), fill=WOOD, outline=ROCK_DARK)
    draw.rectangle((x-int(16*s),y-int(16*s),x+int(16*s),y), fill=(139,88,45), outline=ROCK_DARK)
    pxpoly(draw, [(x-int(20*s),y-int(16*s)),(x,y-int(27*s)),(x+int(20*s),y-int(16*s))], (92,61,36), ROCK_DARK)


def draw_tower(draw, x, y, s=1.0):
    for i, (w,h) in enumerate([(38,10),(31,10),(25,10),(18,10),(12,9)]):
        w = int(w*s)
        h = int(h*s)
        yy = y - i*int(8*s)
        draw.rectangle((x-w//2,yy-h,x+w//2,yy), fill=(178,145,95), outline=ROCK_DARK)
    draw.line((x+int(21*s),y-int(35*s),x+int(27*s),y+3), fill=WOOD, width=2)


def draw_pyramid(draw, x, y, s=1.0):
    w = int(34*s)
    h = int(28*s)
    pxpoly(draw, [(x-w//2,y),(x,y-h),(x+w//2,y)], (196,150,69), ROCK_DARK)
    draw.line((x,y-h,x,y), fill=(236,203,127), width=2)


def draw_temple(draw, x, y, s=1.0):
    w = int(48*s)
    h = int(24*s)
    draw.rectangle((x-w//2,y-h,x+w//2,y), fill=(204,171,111), outline=ROCK_DARK)
    for dx in range(-w//2+6,w//2,8):
        draw.rectangle((x+dx-1,y-h+4,x+dx+1,y), fill=(122,95,67))
    pxpoly(draw, [(x-w//2-3,y-h),(x,y-h-int(10*s)),(x+w//2+3,y-h)], (182,139,82), ROCK_DARK)


def draw_fire(draw, x, y, s=1.0):
    r = max(2, int(5*s))
    pxpoly(draw, [(x-r,y+r),(x,y-int(2*r)),(x+r,y+r)], (239,92,34), (151,55,29))
    pxpoly(draw, [(x-r//2,y+r),(x,y-r),(x+r//2,y+r)], (255,207,66))


def draw_tabernacle(draw, x, y, s=1.0):
    w = int(92*s)
    h = int(56*s)
    draw.rectangle((x-w//2,y-h//2,x+w//2,y+h//2), fill=(238,230,202), outline=ROCK_DARK)
    for xx in range(x-w//2, x+w//2+1, max(6,int(10*s))):
        draw.line((xx,y-h//2,xx,y+h//2), fill=WOOD, width=1)
    tw = int(38*s)
    th = int(24*s)
    draw.rectangle((x-tw//2,y-th//2,x+tw//2,y+th//2), fill=PURPLE, outline=GOLD)
    pxpoly(draw, [(x-tw//2,y-th//2),(x,y-th),(x+tw//2,y-th//2)], (186,167,126), ROCK_DARK)
    draw.rectangle((x-int(25*s),y+int(10*s),x-int(11*s),y+int(22*s)), fill=(132,78,48), outline=ROCK_DARK)
    draw_fire(draw, x-int(18*s), y+int(8*s), s=.7*s)
    draw.ellipse((x+int(12*s),y+int(8*s),x+int(29*s),y+int(17*s)), fill=GOLD, outline=ROCK_DARK)
    draw.ellipse((x+int(15*s),y+int(10*s),x+int(26*s),y+int(14*s)), fill=WATER)


def draw_burning_bush(draw, x, y, s=1.0):
    for dx in [-7,0,7]:
        draw.line((x,y+8,x+dx,y), fill=WOOD, width=2)
    for dx,dy in [(-8,0),(-3,-7),(4,-5),(9,1),(0,3)]:
        draw_fire(draw,x+dx,y+dy,s=.8*s)


def draw_house(draw, x, y, s=1.0, red_door=False):
    w = int(24*s)
    h = int(16*s)
    draw.rectangle((x-w//2,y-h,x+w//2,y), fill=(186,145,91), outline=ROCK_DARK)
    pxpoly(draw, [(x-w//2-2,y-h),(x,y-h-int(8*s)),(x+w//2+2,y-h)], (141,97,60), ROCK_DARK)
    door = (154,45,35) if red_door else ROCK_DARK
    draw.rectangle((x-3,y-8,x+3,y), fill=door)


def draw_parted_sea(draw, top, bottom):
    mid = BASE_W//2
    draw.rectangle((0,top,BASE_W,bottom), fill=(206,183,126))
    draw.rectangle((0,top,mid-28,bottom), fill=WATER)
    draw.rectangle((mid+28,top,BASE_W,bottom), fill=WATER)
    for y in range(top+4,bottom,8):
        draw.line((mid-28,y,mid-42,y+3), fill=WATER_LIGHT, width=2)
        draw.line((mid+28,y,mid+42,y+3), fill=WATER_LIGHT, width=2)


def draw_grapes(draw, x, y, s=1.0):
    for row in range(4):
        for col in range(row+1):
            cx = x+(col-row/2)*5*s
            cy = y+row*4*s
            rr = max(1,int(2*s))
            draw.ellipse((cx-rr,cy-rr,cx+rr,cy+rr), fill=(97,55,127))
    draw.line((x,y-4*s,x+12*s,y-8*s), fill=WOOD, width=2)


def draw_bronze_serpent(draw,x,y,s=1.0):
    h = int(30*s)
    draw.line((x,y,x,y-h), fill=(106,71,39), width=max(2,int(3*s)))
    pts = []
    for i in range(14):
        yy = y-h+5+i*1.5*s
        xx = x+math.sin(i*.8)*6*s
        pts.append((int(xx),int(yy)))
    draw.line(pts, fill=(184,125,38), width=max(2,int(3*s)), joint="curve")


def draw_stones(draw,x,y,s=1.0,count=6):
    for i in range(count):
        w = int((8+i%2*2)*s)
        h = int(6*s)
        xx = x+(i%3-1)*int(10*s)
        yy = y-(i//3)*int(6*s)
        draw.rectangle((xx-w//2,yy-h,xx+w//2,yy), fill=(131,116,91), outline=ROCK_DARK)


def draw_river(draw, points, width=16):
    draw.line(points, fill=WATER, width=width, joint="curve")
    draw.line(points, fill=WATER_LIGHT, width=max(2,width//4), joint="curve")


def draw_path_and_nodes(draw, chapters, completed, top=34, bottom=486, columns=5):
    rows = math.ceil(chapters/columns)
    ys = [top + int(i*(bottom-top)/max(1,rows-1)) for i in range(rows)]
    left = 42
    right = 278
    xs = [left + int(i*(right-left)/(columns-1)) for i in range(columns)]
    nodes = []
    for idx in range(chapters):
        r = idx//columns
        c = idx%columns
        vc = c if r%2==0 else columns-1-c
        x = xs[vc] + int(5*math.sin(idx*1.7))
        y = ys[r] + int(3*math.sin(idx*1.13))
        nodes.append((idx+1,x,y))
    for (_,x1,y1),(_,x2,y2) in zip(nodes,nodes[1:]):
        draw.line((x1,y1,x2,y2), fill=PATH_EDGE, width=5)
        draw.line((x1,y1,x2,y2), fill=PATH, width=3)
    for chap,x,y in nodes:
        done = chap in completed
        fill = BLUE if done else RED
        hi = BLUE_HI if done else RED_HI
        r = 5
        draw.ellipse((x-r-1,y-r-1,x+r+1,y+r+1), fill=WHITE, outline=PATH_EDGE)
        draw.ellipse((x-r,y-r,x+r,y+r), fill=fill, outline=INK)
        draw.rectangle((x-2,y-3,x+1,y-1), fill=hi)
    return nodes


def scatter_rocks(draw, rng, y0, y1, n=45):
    for _ in range(n):
        x = rng.randrange(4,BASE_W-4)
        y = rng.randrange(y0,y1)
        rr = rng.choice([1,2,3])
        draw.ellipse((x-rr,y-rr,x+rr,y+rr), fill=rng.choice([ROCK,ROCK_DARK,(160,136,103)]))


def paint_genesis(draw, rng):
    draw.rectangle((0,0,BASE_W,128), fill=(118,191,95))
    draw.rectangle((0,128,BASE_W,252), fill=(121,127,104))
    draw.rectangle((0,252,BASE_W,386), fill=(214,181,117))
    draw.rectangle((0,386,BASE_W,BASE_H), fill=(196,173,93))
    for x in [30,68,128,220,284]:
        draw_tree(draw,x,52,rng.choice([.7,.9,1.1]),fruit=(x==128))
    draw_tree(draw,165,54,1.5,fruit=True)
    draw_river(draw,[(12,90),(55,84),(92,102),(138,94),(186,106),(230,92),(306,108)],12)
    draw_waterfall(draw,42,66,18,20)
    draw_waterfall(draw,257,60,16,19)
    for x in [18,54,97,145]:
        draw_tree(draw,x,170,.8,dead=True)
    draw.rectangle((174,145,319,222), fill=(71,132,159))
    for y in range(148,220,12):
        draw.line((175,y,319,y+4), fill=WATER_LIGHT, width=1)
    draw_ark(draw,246,188,1.4)
    draw_tower(draw,65,304,1.35)
    draw_tent(draw,184,316,1.1,(198,138,89))
    draw_tent(draw,222,326,1.0,(224,201,151))
    draw_tent(draw,255,304,.9,(187,118,79))
    draw.ellipse((196,338,210,345), fill=(95,87,70), outline=ROCK_DARK)
    for x in [170,235,285]:
        draw_palm(draw,x,350,.8)
    draw_river(draw,[(0,444),(65,434),(122,450),(180,436),(245,449),(320,440)],18)
    for x in [22,78,116,252,295]:
        draw_palm(draw,x,470,.9)
    draw_temple(draw,220,468,1.35)
    draw_pyramid(draw,270,424,1.2)
    draw_pyramid(draw,302,430,.9)
    scatter_rocks(draw,rng,252,386,28)


def paint_exodus(draw, rng):
    bands = [
        (0,82,(204,177,94)),
        (82,165,(211,184,125)),
        (165,245,(151,95,78)),
        (245,330,(181,164,118)),
        (330,425,(216,184,116)),
        (425,512,(194,149,85)),
    ]
    for a,b,c in bands:
        draw.rectangle((0,a,BASE_W,b),fill=c)
    draw_river(draw,[(0,54),(74,65),(142,53),(210,64),(320,50)],18)
    draw_temple(draw,246,72,1.35)
    draw_pyramid(draw,54,46,1.1)
    draw_pyramid(draw,92,42,.8)
    for x in [24,120,285]:
        draw_palm(draw,x,77,.8)
    draw_burning_bush(draw,72,122,1.3)
    for x in [190,226,260]:
        draw_tent(draw,x,151,.8)
    for x in [44,88,135,205,266]:
        draw_house(draw,x,214,.9,red_door=(x in [205,266]))
    draw.rectangle((0,181,112,223),fill=(128,51,49))
    draw_parted_sea(draw,245,330)
    for x in [32,72,112,168,225,282]:
        draw_tent(draw,x,378,.75)
    for x in range(20,300,19):
        draw.rectangle((x,344+(x%17),x+1,345+(x%17)),fill=WHITE)
    draw_mountain(draw,65,480,100,80,(117,78,66),(76,52,47))
    draw_cloud(draw,65,410,1.3,(230,226,218))
    draw_tabernacle(draw,234,468,.8)
    scatter_rocks(draw,rng,330,512,35)


def paint_leviticus(draw, rng):
    draw.rectangle((0,0,BASE_W,BASE_H),fill=(218,191,128))
    for x in [35,94,270]:
        draw_mountain(draw,x,92,70,50,(146,103,74),(107,77,62))
    draw_river(draw,[(0,155),(42,148),(84,163),(130,155)],12)
    for x in [18,52,286]:
        draw_palm(draw,x,190,.8)
    draw_tabernacle(draw,160,245,1.45)
    draw_cloud(draw,160,168,1.4,(236,232,213))
    for x,y in [(42,110),(84,120),(235,116),(278,132),(42,332),(82,350),(252,342),(286,365),(58,436),(250,446)]:
        draw_tent(draw,x,y,.85,rng.choice([(214,182,131),(233,211,168),(190,132,93)]))
    draw.rectangle((18,265,78,304),outline=WOOD,width=2)
    for x in [30,46,62]:
        draw.ellipse((x-4,284,x+4,290),fill=(243,237,218),outline=INK)
    draw.ellipse((246,222,268,232),fill=GOLD,outline=ROCK_DARK)
    draw.ellipse((250,224,264,228),fill=WATER)
    draw.rectangle((45,208,67,225),fill=(126,74,44),outline=ROCK_DARK)
    draw_fire(draw,56,204,1.1)
    draw.rectangle((226,295,295,329),outline=WOOD,width=2)
    for x in [238,256,276]:
        draw.ellipse((x-5,309,x+5,315),fill=(239,233,215),outline=INK)
    draw_stones(draw,82,408,1.0,6)
    scatter_rocks(draw,rng,0,512,25)


def paint_numbers(draw, rng):
    draw.rectangle((0,0,BASE_W,BASE_H),fill=(218,182,113))
    draw_tabernacle(draw,74,70,.7)
    for y in [28,55,95,120]:
        for x in range(20,165,28):
            if abs(x-74)<28 and y<95:
                continue
            draw_tent(draw,x,y,.55,rng.choice([(224,201,156),(191,127,83),(204,169,113)]))
    for x,b,w,h in [(235,105,110,70),(286,125,85,54),(52,226,90,66)]:
        draw_mountain(draw,x,b,w,h)
    scatter_rocks(draw,rng,110,420,75)
    draw_river(draw,[(0,240),(55,250),(110,242),(145,260)],13)
    draw_waterfall(draw,25,210,16,28)
    for x in [42,92,125]:
        draw_palm(draw,x,272,.8)
    draw_grapes(draw,75,173,1.3)
    draw_bronze_serpent(draw,260,315,1.5)
    for x,y in [(48,350),(91,372),(218,390),(268,404),(135,440)]:
        draw_tent(draw,x,y,.72)
    draw.rectangle((0,460,BASE_W,512),fill=(129,166,91))
    draw_river(draw,[(0,490),(75,477),(152,494),(230,478),(320,492)],12)


def paint_deuteronomy(draw, rng):
    draw.rectangle((0,0,BASE_W,310),fill=(204,179,112))
    draw.rectangle((0,310,BASE_W,512),fill=(144,177,95))
    draw_mountain(draw,65,116,120,88,(132,95,70),(94,68,57))
    draw_stones(draw,66,102,1.0,5)
    for x in [30,68,105,232,270]:
        draw_tent(draw,x,155,.75)
    for x in range(130,210,9):
        draw.ellipse((x-2,174,x+2,178),fill=rng.choice([(102,67,51),(76,81,98),(165,92,58)]))
    for i in range(6):
        x = 42+i*16
        h = 18+(i%3)*4
        draw.rectangle((x,225-h,x+6,225),fill=(127,113,91),outline=ROCK_DARK)
    draw_river(draw,[(0,302),(65,292),(120,316),(182,300),(242,319),(320,307)],22)
    for x in [28,72,128,210,280]:
        draw_tree(draw,x,380,.8,fruit=(x in [72,210]))
    for x in [42,108,250,294]:
        draw_palm(draw,x,426,.8)
    for y in [345,370,395,420]:
        draw.line((155,y,318,y-8),fill=(100,139,69),width=4)
    draw_temple(draw,250,444,1.0)
    draw.rectangle((205,430,302,466),outline=ROCK_DARK,width=2)
    draw.rectangle((0,475,BASE_W,512),fill=(104,177,196))
    for x in [45,145,290]:
        draw_palm(draw,x,495,.7)
    scatter_rocks(draw,rng,0,310,35)


SPECS = [
    MapSpec("genesis", "01_genesis", 50, 10, paint_genesis),
    MapSpec("exodo", "02_exodo", 40, 8, paint_exodus),
    MapSpec("levitico", "03_levitico", 27, 5, paint_leviticus),
    MapSpec("numeros", "04_numeros", 36, 7, paint_numbers),
    MapSpec("deuteronomio", "05_deuteronomio", 34, 6, paint_deuteronomy),
]


def parse_completed(items: list[str]) -> dict[str, set[int]]:
    out: dict[str, set[int]] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Use livro=1,2,3 ou livro=1-5: {item}")
        key, raw = item.split("=", 1)
        vals: set[int] = set()
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a,b = part.split("-",1)
                vals.update(range(int(a), int(b)+1))
            else:
                vals.add(int(part))
        out[key.strip()] = vals
    return out


def generate_map(spec: MapSpec, out_path: Path, completed: set[int] | None = None, seed: int = 2026):
    rng = random.Random(seed + spec.chapters)
    img = Image.new("RGB",(BASE_W,BASE_H),(202,190,160))
    draw = ImageDraw.Draw(img)
    spec.painter(draw,rng)
    if completed is None:
        completed = set(range(1,spec.completed_default+1))
    draw_path_and_nodes(draw,spec.chapters,completed)
    img = img.resize((OUT_W,OUT_H),Image.Resampling.NEAREST)
    out_path.parent.mkdir(parents=True,exist_ok=True)
    img.save(out_path,optimize=True)


def main():
    parser = argparse.ArgumentParser(description="Gera os cinco mapas temáticos do Pentateuco em pixel art.")
    parser.add_argument("--root",type=Path,default=Path.cwd(),help="Raiz do repositório Salominho.")
    parser.add_argument("--only",choices=[s.key for s in SPECS],help="Gera apenas um livro.")
    parser.add_argument("--completed",action="append",default=[],help="Ex.: --completed genesis=1-12 --completed exodo=1-4,8")
    args = parser.parse_args()

    custom = parse_completed(args.completed)
    selected = [s for s in SPECS if args.only is None or s.key==args.only]
    for spec in selected:
        out = args.root/"assets"/"worlds"/"old_testament"/spec.folder/"map_generated.png"
        generate_map(spec,out,custom.get(spec.key))
        print(f"OK {spec.key}: {out} ({spec.chapters} capítulos)")


if __name__ == "__main__":
    main()
