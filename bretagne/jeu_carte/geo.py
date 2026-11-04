"""Projection Lambert-93 (RGF93, EPSG:2154) codée à la main + outils polygones."""
import math, json
A, F = 6378137.0, 1 / 298.257222101           # GRS80
E = math.sqrt(2 * F - F * F)
L0, P1, P2, P0 = math.radians(3), math.radians(44), math.radians(49), math.radians(46.5)
X0, Y0 = 700000.0, 6600000.0
def _m(p): return math.cos(p) / math.sqrt(1 - (E * math.sin(p)) ** 2)
def _t(p): return math.tan(math.pi / 4 - p / 2) / ((1 - E * math.sin(p)) / (1 + E * math.sin(p))) ** (E / 2)
N = (math.log(_m(P1)) - math.log(_m(P2))) / (math.log(_t(P1)) - math.log(_t(P2)))
FF = _m(P1) / (N * _t(P1) ** N)
R0 = A * FF * _t(P0) ** N
def l93(lon, lat):
    p, l = math.radians(lat), math.radians(lon)
    r = A * FF * _t(p) ** N; th = N * (l - L0)
    return X0 + r * math.sin(th), Y0 + R0 - r * math.cos(th)
def wgs(x, y):
    dx, dy = x - X0, R0 - (y - Y0)
    r = math.copysign(math.hypot(dx, dy), N); th = math.atan2(dx, dy)
    t = (r / (A * FF)) ** (1 / N); p = math.pi / 2 - 2 * math.atan(t)
    for _ in range(10):
        p = math.pi / 2 - 2 * math.atan(t * ((1 - E * math.sin(p)) / (1 + E * math.sin(p))) ** (E / 2))
    return math.degrees(th / N + L0), math.degrees(p)
def anneaux(geom):
    """Liste des polygones ; chaque polygone = liste d'anneaux [(lon,lat)...] (le 1er = extérieur)."""
    if geom['type'] == 'Polygon': return [geom['coordinates']]
    return geom['coordinates']
def aire_centroide(ring):
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        c = x1 * y2 - x2 * y1; a += c; cx += (x1 + x2) * c; cy += (y1 + y2) * c
    a /= 2
    return a, (cx / (6 * a), cy / (6 * a)) if a else ring[0]
def dans(pt, ring):
    x, y = pt; ins = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: ins = not ins
    return ins
