#!/usr/bin/env python
from os.path import basename, splitext
from math import sqrt
import argparse

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def distance(self, other):
        return sqrt(
            (self.x - other.x)**2 +
            (self.y - other.y)**2 +
            (self.z - other.z)**2
        )
    
    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __str__(self):
        return f"{self.x},{self.y},{self.z}"

class Atom:
    def __init__(self, name, idnum, char, tp, att1, att2, x, y, z, av, bv, n, line):
        self.name = name
        self.idnum = idnum
        self.Element = char
        self.res = tp
        self.chain = att1
        self.resnum = att2
        self.point = Point(float(x), float(y), float(z))
        self.AValue = av
        self.BValue = bv
        self.AtomN = n
        self.line = line
    
    def getPoint(self):
        return self.point
    
    def getLine(self):
        return self.line
    
    def __str__(self):
        return self.line

def parse_data(line):
    if line.startswith("CRYST1") or line.startswith("REMARK") or line.startswith("END"):
        return
    
    if line.startswith("ATOM  ") or line.startswith("HETATM"):
        name = line[0:6].strip()
        idnum = line[6:11].strip()
        char = line[11:16].strip()
        tp = line[16:20].strip()
        att1 = line[20:23].strip()
        att2 = line[23:26].strip()
        x = line[26:38].strip()
        y = line[38:46].strip()
        z = line[46:54].strip()
        av = line[55:61].strip()
        bv = line[60:66].strip()
        n = line[67:79].strip()
        
        ATOM.append(Atom(name, idnum, char, tp, att1, att2, x, y, z, av, bv, n, line))

def print_centroid():
    if not ATOM:
        print("No atoms found in the structure")
        return
    
    x = y = z = 0.0
    maxx = maxy = maxz = -float('inf')
    minx = miny = minz = float('inf')
    
    for atom in ATOM:
        pt = atom.point
        x += pt.x
        y += pt.y
        z += pt.z
        maxx = max(maxx, pt.x)
        minx = min(minx, pt.x)
        maxy = max(maxy, pt.y)
        miny = min(miny, pt.y)
        maxz = max(maxz, pt.z)
        minz = min(minz, pt.z)
    
    count = len(ATOM)
    x /= count
    y /= count
    z /= count
    
    print("Centroid is:")
    print(f"{x:.3f}, {y:.3f}, {z:.3f}")
    
    print("\nCoordinate ranges:")
    print(f"X: {minx:.3f} to {maxx:.3f}")
    print(f"Y: {miny:.3f} to {maxy:.3f}")
    print(f"Z: {minz:.3f} to {maxz:.3f}")
    
    rangex = (maxx - minx) * 5
    rangey = (maxy - miny) * 5
    rangez = (maxz - minz) * 5
    
    rangex = round(rangex)
    rangey = round(rangey)
    rangez = round(rangez)
    
    if args.Even:
        if rangex % 2:
            rangex += 1
        if rangey % 2:
            rangey += 1
        if rangez % 2:
            rangez += 1
    
    print("\nRecommended gist input command:")
    print(f"gist gridspacn 0.5 gridcntr {x:.3f} {y:.3f} {z:.3f} griddim {int(rangex)} {int(rangey)} {int(rangez)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument("-i", dest='structure', help="Input file in .pdb format", type=str, required=True)
    parser.add_argument("-e", dest='Even', help="Make grid dimensions even", action='store_true')
    args = parser.parse_args()

    filename = splitext(basename(args.structure))[0]
    print(f"Processing file: {filename}")

    ATOM = []
    
    with open(args.structure, "r") as f:
        for line in f:
            parse_data(line)
    
    print_centroid()
