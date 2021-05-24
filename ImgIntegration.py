# The purpose of this program is to determine the total number of red/green pixels within a certain range (range can be specified, preferably divisible into 35000)
# Integrates the number of colored pixels and outputs the values into a .xlsx file

from PIL import Image
import matplotlib.pyplot as plt
import xlwt
from xlwt import Workbook
import math
import sys
import os.path

# This function writes the start, end, and number of red/green pixels into a designated excel sheet
def WritetoFile(startPix, endPix):
	global bpStart
	global stpxC
	global greenPix
	global redPix
	global S1Row
	global S2Row

	 if BPList == Sheet1:
	 	BPList.write(S1Row, 0, (startPix - stpxC)*10.407 + bpStart)
	 	BPList.write(S1Row, 1, (endPix - stpxC)*10.407 + bpStart)
	 	BPList.write(S1Row, 2, redPix)
	 	BPList.write(S1Row, 3, greenPix)
	 	S1Row += 1
	
	 if BPList == Sheet2:
	 	BPList.write(S2Row, 0, (startPix - stpxC)*10.407 + bpStart)
	 	BPList.write(S2Row, 1, (endPix - stpxC)*10.407 + bpStart)
	 	BPList.write(S2Row, 2, redPix)
	 	BPList.write(S2Row, 3, greenPix)
	 	S2Row += 1
	
	return


# Because the .jpg file's graph is of varying different RGB colors, standardize the green and red pixels
# in the graph region to a specific RGB value so that it is easier to analyze later on
def color_correct():
	global pix

	for x in range(stpxC, enpxC):
		for y in range(stpxR - grHeight, stpxR):
			RGB = im.getpixel((x,y))
			R,G,B = RGB
			# Many of these RGB range values are very subjective and are meant to try to reach as many
			# pixels as possible without including unnecessary ones
			if R > 100 and R < 200 and G > 160 and G < 240 and B > -1 and B < 110:
				pix[x,y] = (144,209,57) # green pixels
			elif R > 150 and R < 256 and G > 30 and G < 110 and B > -1 and B < 80:
				pix[x,y] = (220,65,30) # red pixels
	return

# This function integrates the number of green and red pixels within a given range
def integrate_px():
	global bpStart
	global stpxC
	global greenPix
	global redPix

	# Make sure to start at the point that is divisible by the range designated
	 if bpStart % 8750 != 0:
	 	diff = bpStart % 8750
	 	bpDiff = 8750 - diff
	 	bpStart = bpStart + bpDiff
	 	stpxC = stpxC + math.floor(bpDiff / 10.407)

	 startPixel = stpxC
	 currentRange = 0

	 # Run through the graph to gather all pixels of red/green color
	 for x in range(stpxC, enpxC):
	 	for y in range (stpxR, stpxR - grHeight, -1):
	 		if pix[x,y] == (144,209,57):
	 			greenPix += 1
	 		elif pix[x,y] == (220,65,30):
	 			redPix += 1

	 	# If the number of pixels correlates to the range designated, send to WritetoFile
	 	if currentRange < 840:
	 		currentRange += 1
	 	elif currentRange == 840:
	 		WritetoFile(startPixel, x)
	 		startPixel = x
	 		currentRange = 0
	 		greenPix = 0
	 		redPix = 0
	 	if (currentRange > 825 and pix[x + 1, y] == (255,255,255)):
	 		WritetoFile(startPixel, x)
	 		startPixel = x
	 		currentRange = 0
	 		greenPix = 0
	 		redPix = 0

	WritetoFile(stpxC, x)
	greenPix = 0
	redPix = 0
	return

# Read in file and check if it's valid, if not, then terminate the program
filename = input('\nEnter the filename: ')
if os.path.isfile(filename):
	f = open(filename)
else:
	sys.exit("Please enter a valid filename.")

# hardset values for the starting column pixel, starting row pixel, end column pixel, height of the graph, start bp, and variables for the red/green pixels
stpxC = 615
stpxR = 418
enpxC = 4015
grHeight = 290
bpStart = -1
redPix = 0
greenPix = 0

# Set up an excel sheet
wb = Workbook()

style = xlwt.easyxf('font: bold 1')

Sheet1 = wb.add_sheet('E1 Track Integration')
Sheet1.write(0, 0, 'Start BP', style)
Sheet1.write(0, 1, 'End BP', style)
Sheet1.write(0, 2, 'Number of Red Pixels (Bottom)', style)
Sheet1.write(0, 3, 'Number of Green Pixels (Top)', style)

Sheet2 = wb.add_sheet('E2 Track Integration')
Sheet2.write(0, 0, 'Start BP', style)
Sheet2.write(0, 1, 'End BP', style)
Sheet2.write(0, 2, 'Number of Red Pixels (Bottom)', style)
Sheet2.write(0, 3, 'Number of Green Pixels (Top)', style)

S1Row = 1
S2Row = 1

for x in f:
	lineSplit = x.split(' ')
	IMG_PATH = "Images/" + lineSplit[0]
	print("\nAnalyzing file " + IMG_PATH + "...")

	if len(lineSplit) > 2:
		bpStart = int(lineSplit[1])
		stpxC = int(lineSplit[2])
		stpxR = int(lineSplit[3])
	else:
		stpxC = 615
		stpxR = 418
		bpStart = int(lineSplit[1])

	# Tries to open the image file and returns if invalid
	try:
		im = Image.open(IMG_PATH)
	except FileNotFoundError:
		sys.exit("Please enter a valid filename.")

	# Takes in the number of tracks you're trying to read
	numTracks = 2

	# Gets the pixel dimensions of the image and 
	# Converts the image into RGB values that can then be loaded into pix
	w, h = im.size
	im = im.convert('RGB')
	pix = im.load()
	param_enter = ''

	# For each track, write to a different file
	for x in range(1, numTracks + 1):
		# This is the file that the program writes into
		if x == 1:
			BPList = Sheet1

		else:
			BPList = Sheet2

		# For the first track, check if you want to enter parameters
		if x > 1:
			if len(lineSplit) > 2:
				stpxR = int(lineSplit[4])
			else:
				stpxR = 1232

		# Sends to color_correct function to standardize colors
		color_correct()

		redPix = 0
		greenPix = 0

		# integrates the pixels to generate how many red/green pixels
		integrate_px()

wb.save("Top and Bottom strand Pixel Integration 35000bp.xls")

print("\nFinished reading to files!")

