import numpy as np
import uncertainties as unc

bottlemass = unc.ufloat(4.84, 0.09) #kg
bottleheight = unc.ufloat(42, 0.5) #cm
bottleradius = 5.1 #cm 

bottlevol = np.pi*(bottleradius**2)*bottleheight
density = 0.48282 #g/ml or kg/L

temp = 294.4 #K

pressure = 52.3954 #atm or 770 psig

#rho = m/v > v*rho = m > v = m/rho

bottlevol_2 = bottlemass/density

bottlevoltrue = 2.25
print("Bottle vol. determined by height calculations:", bottlevol,"cubic cm or", bottlevol/1000, "L")
print("Bottle vol. determined by density calculations:", bottlevol_2, "L")
print("Actual vol.:", bottlevoltrue, "L\n")

lengths_froms2 = [10.5, 29.3, 14.5, 51.0, 9.5, 11.5,
                  32.0, 10.5, 11.5, 17.0, 10.5, 52.3,
                  9.5, 24.45, 9.5, 46.1, 19.2, 119.2, 
                  13.1, 16.0, 49.0, 24.1, 7.5, 35.5,
                  160, 12.8, 6.35, 22.6, 22.6, 44, 186.75, 206, 38, 128.2]

lengthsum_s2 = np.sum(lengths_froms2)
print(lengthsum_s2, "cm total")

innerradius = 0.4138 #cm

pipevolume = np.pi*(innerradius**2)*lengthsum_s2
print("total volume of piping, NO recovery volume =", round(pipevolume, 3), "cubic cm/", round((pipevolume/1000), 3), "L\n")

cellvol = 3.9998 #L

totalvol = cellvol + (pipevolume/1000)

print("ROUGH total volume filled by xenon gas:", round(totalvol, 3), "L")

densityavgrun = unc.ufloat(17.014, 1.1) #m^3/kg, density at 45 psi & ~293 K
massavgrun = 1.2918 #kg
volavgrun = massavgrun/densityavgrun
print("vol of 1.2918 kg Xe at 45 psi, room temp:", volavgrun, "m^3 or", volavgrun*1000, "L")
print("flow rate:", volavgrun/150, "L/s")

deltaP = 30.3 #psi

visc_Xe = (deltaP*np.pi*(innerradius**4))/(8*lengthsum_s2*(volavgrun/150))
#PSI * cm^4/cm*L/s > psi*cm^3*s/L
print("viscosity:", visc_Xe)
print("velocity:", lengthsum_s2/150, "cm/s")

