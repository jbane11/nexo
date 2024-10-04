import numpy as np

#these two are in cm
height_LXe = 20

radius_cell = 4.995

#cubic cm & L
volume_LXe = height_LXe*(np.pi * (radius_cell**2))
Liter_volume_LXe = volume_LXe/1000
print("volume of LXe for max height of 20 cm:", round(volume_LXe, 3), "cubic cm, or", round(Liter_volume_LXe, 3), "L")

#cubic cm
max_balloonVol = (115*75*134)
Liter_max_balloonVol = max_balloonVol/1000
print("max wall-mounted balloon volume:", round(max_balloonVol, 3), "cubic cm, or", round(Liter_max_balloonVol, 3), "L"+"\n")

#average temp of liquid Xe in cell, at ~1.8 atm
xe_cell_top_K = [173.965, 173.492]
avg_xe_cell_top_K = np.mean(xe_cell_top_K)
print("average temp of top TC (in liquid, ~1.8 atm):", round(avg_xe_cell_top_K, 3), "K"+"\n")

#height of cell (cm)
volume_cell = 3998.5 #cubic cm or mL
height_cell = ((volume_cell) / (np.pi*(radius_cell**2)))
print("height of cell:", round(height_cell, 3), "cm"+"\n")

#vol of Lxe * maximum burst density (at cold temp [~162.5 K] and HIGH pressure [45 psi])
max_LXe_density = 2960 #g/L
max_density2 = 3000
max_mass = round((max_LXe_density * Liter_volume_LXe), 3)
max_mass2 = round((max_density2*Liter_volume_LXe), 3)
print("maximum mass of LXe at burst pressure:", max_mass, "g, or", round((max_mass/1000), 3), "kg")
print("maximum mass w/ density of 3000 g/L:", max_mass2, "g, or ", round((max_mass2/1000), 3), "kg"+"\n")

#volume of maximum density of 3000 g/L
n_max = max_mass2/131.293
R_constant = 0.082057 #L*atm*K-1*mol-1
roomtemp = 293 #K
maximum_volume = round((n_max*R_constant*roomtemp), 3)
print("maximum volume occupied by densest possible liquid (3000 g/L) at standard pressure:", maximum_volume, "L")
print("volume occupied by NIST table maximum: 849.923 L")

#mass required for 20 cm of liquid
#at 173.75, density is 2883.3 g/L
#p*V = m (in g)
twentycm_mass = 2883.3 * Liter_volume_LXe
print("mass required to make 20 cm of liquid at 173.75 K and 1.8 atm:", round(twentycm_mass, 3), "g, or", round((twentycm_mass/1000), 3), "kg"+"\n")

#total allowable length for tube in cm
small_strut_width = 13
med_strut_width = 16.5
large_strut_width = 20.9

total_length = round(((15*large_strut_width)+(med_strut_width)+(2*small_strut_width)), 3)
print("total allowable length occupied by tube on rack:", total_length, "cm, or", (total_length/100), "m")

#total volume for tube
total_diameter = 32
total_radius = 16
#height is total length
total_tube_vol = round((np.pi * (total_radius**2) * total_length), 2)
print("total allowable tube volume:", total_tube_vol, "cubic cm, or", (total_tube_vol/1000), "L")
