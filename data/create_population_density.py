import rasterio
import math
from datetime import datetime

print("Opening file...")
data = rasterio.open('./irl_ppp_2020_UNadj.tif')
band = data.read(1)

EARTH_RADIUS = 6371
MICROCELL_SIZE = 1/120

## Returns the width of a 1/120 degree microcell in metres at the given latitude
def get_microcell_width(latitude):
	lat_rads = latitude * math.pi/180
	cell_width_rads = MICROCELL_SIZE * math.pi/180
	
	x = math.asin(
			math.sqrt( (math.cos(lat_rads) ** 2) * (math.sin(cell_width_rads) ** 2) )
			)
	
	return 2000 * EARTH_RADIUS * x


with open("./populations/Ireland.txt", "w") as output_file:
	print("Files opened successfully, reading values...")
	
	# Initial coordinates set around bottom left of the map
	lat, long = 51.43, -10.66 
	
	start = datetime.now()
	
	while (long < -6.01):
		lat = 51.43
		while(lat < 55.43):
			## Work out all 'pixels' which either contain the stating coords or are COMPLETELY within this cell 
			## Then sum their poulations and write info to file
			mcell_pop = 0
	
			x, y = data.index(long, lat)
			x1, y1 = data.index(long + MICROCELL_SIZE, lat + MICROCELL_SIZE)
			
			for i in range(x1, x):
				for j in range(y, y1):
					if band[x][y] > 0:
						mcell_pop += band[x][y]
			
			if mcell_pop > 0:
				## Longitude	Latitude	population of cell	country code	admin code
				output_file.write(str(round(long, 5)) + "	" + str(round(lat, 5)) + "	" + str(int(round(mcell_pop))) + "	" + "21" + "	" + "210100\n")
				# LOOK INTO ROUNDING OF POPULATION
			
			lat += MICROCELL_SIZE
		long += MICROCELL_SIZE

	print("Completed.\nExecution took ", datetime.now() - start)
	