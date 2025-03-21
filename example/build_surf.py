from ase.build import surface
from ase.io import write

surf = surface("Au", (7, 5, 5), 20)
surf *= (10, 10, 1)

write("surface.xyz", surf)
