import sys 


metallicity = float(sys.argv[1])
hden = float(sys.argv[2])
turbulence = float(sys.argv[3])
isrf = float(sys.argv[4])
radius = float(sys.argv[5])

fdir = f"hden{hden:.5f}_metallicity{metallicity:.5f}_turbulence{turbulence:.5f}_isrf{isrf:.5f}_radius{radius:.5f}"

print(fdir)
