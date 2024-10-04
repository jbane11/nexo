import numpy as np

def convert(atm):
    psi = atm*14.6959
    print(psi, "psi")

convert(0.01)
convert(0.1)
convert(1)
convert(10)
convert(100)
