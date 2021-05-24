# This program is identical to ImageThreshold_PIL.py except that it takes in a .txt of all of the images at once and their respective values
# This program allows for all the images to be analyzed in one go.

from PIL import Image
import matplotlib.pyplot as plt
import sys
import os.path

# This function writes the (start, end) pair into a .txt file and labels it with an identifier
def WritetoFile(mode, startPix, endPix):
	if mode == 0:
		BPList.write("gap: ")
	elif mode == 1:
		BPList.write("Top strand: ")
	else:
		BPList.write("Bottom strand: ")
	# Each pixel is approximately 10.41 base pairs, therefore I am multiplying it by 10.41
	BPList.write("(" + str((startPix-stpxC)*10.41 + bpStart) + "," + str((endPix-stpxC)*10.41 + bpStart) + ") \n")
	return

# This function checks to see if the pixel after the 10th+ pixel is still of interest in the same category
# as before.
def checkNext(checkMode, currentRange, start, end):
	tempgPix = 0
	temprPix = 0

	# The for loop runs through the next pixel to generate new greenPixel and redPixel amounts
	for y in range(stpxR, stpxR - grHeight, -1):
		if pix[end + 1,y] == (144,209,57):
			tempgPix += 1
		elif pix[end + 1,y] == (220,65,30):
			temprPix += 1

	# CheckMode 0 is for gaps
	if checkMode == 0:
		if tempgPix + temprPix < gapThres:
			currentRange += 1
			return currentRange

	# Check if there are no pixels, if there are no colored pixels and checkMode is not 0, 
	# this signifies the end of a region of interest
	elif tempgPix + temprPix == 0:
		WritetoFile(mode = checkMode, startPix = start, endPix = end)
		start = 0
		currentRange = 0
		return currentRange

	# CheckMode 1 is for >85% green pixels (top strand majority)
	elif checkMode == 1:
		if (tempgPix/(tempgPix + temprPix))*100 > strandThres:
			currentRange += 1
			return currentRange

	# CheckMode 2 is for >85% red pixels (bottom strand majority)
	else:
		if (temprPix/(tempgPix + temprPix))*100 > strandThres:
			currentRange += 1
			return currentRange

	# If any of the previous parameters failed, then that means this is the end of the region of interest
	# Calls the WritetoFile function and resets the start and currentRange
	WritetoFile(mode = checkMode, startPix = start, endPix = end)
	start = 0
	currentRange = 0
	
	return currentRange

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

def find_ROI():
	# Some beginning values to work with, start pixel means the "start" in (start, end) pairs
	# gap = a gap ROI, Bot = a bottom strand ROI, and Top = a top strand ROI
	# current Range signifies the current range of pixels that are being labeled as ROI
	startgapPixel = 0
	startBotPixel = 0
	startTopPixel = 0
	currentgapRange = 0
	currentBotRange = 0
	currentTopRange = 0

	# Main body of the program that runs through each pixel and counts up the number of red and green pixels
	for x in range(stpxC, enpxC):
		greenPix = 0
		redPix = 0
		for y in range(stpxR, stpxR - grHeight, -1):
			if pix[x,y] == (144,209,57):
				greenPix += 1
			elif pix[x,y] == (220,65,30):
				redPix += 1

		# If the total number of pixels is less than the threshold, then it constitutes as a gap ROI
		if greenPix + redPix < gapThres:
			# If there have been over 10 consecutive pixels matching this ROI, send it to the checkNext fxn
			if startgapPixel != 0 and currentgapRange >= minLength:
				currentgapRange = checkNext(checkMode = 0, currentRange = currentgapRange, start = startgapPixel, end = x)
			
			# If this is the first seen ROI of its type, mark this as the starting pixel in the (start,end) and
			# increase the current range of the ROI
			elif startgapPixel == 0:
				startgapPixel = x
				currentgapRange +=1
			
			# If this is the not the first seen ROI of its type, just increase the current range of the ROI
			else:
				currentgapRange += 1
		
		# If the total number of green pixels is >85% of the total, then it constitutes a Top strand ROI
		elif (greenPix/(greenPix + redPix))*100 > strandThres:
			if startTopPixel != 0 and currentTopRange >= minLength:
				currentTopRange = checkNext(checkMode = 1, currentRange = currentTopRange, start = startTopPixel, end = x)
			
			elif startTopPixel == 0:
				startTopPixel = x
				currentTopRange +=1
			
			else:
				currentTopRange += 1
		
		# If the total number of red pixels is >85% of the total, then it constitutes a Bottom strand ROI
		elif (redPix/(greenPix + redPix))*100 > strandThres:
			if startBotPixel != 0 and currentBotRange >= minLength:
				currentBotRange = checkNext(checkMode = 2, currentRange = currentBotRange, start = startBotPixel, end = x)

			elif startBotPixel == 0:
				startBotPixel = x
				currentBotRange +=1
			
			else:
				currentBotRange += 1
		
		# If none of the above apply, reset all parameters
		else:
			startgapPixel = 0
			startBotPixel = 0
			startTopPixel = 0
			currentgapRange = 0
			currentBotRange = 0
			currentTopRange = 0
	return

# Brief summary of the program
print("The purpose of this program is to determine the base pairs of the regions of interest "),
print("located in the tracks of Bisulfide-treated aligned sequencing reads. "),
print("\nSuch regions of interest include:")
print("	Reads concentrated in the Top Strand (Green)")
print("	Reads concentrated in the Bottom Strand (Red)")
print("	Gaps in the reads\n")
print("In order to determine these factors, the program will ask you to input several parameters. "),
print("These parameters are based primarily on the pixel value of the .jpg image that it draws from "),
print("so please make sure to zoom in on the displayed image to get a good sense of where each graph "),
print("ends and begins as well as how many base pairs equate to one pixel.")

# Read in file and check if it's valid, if not, then terminate the program
filename = input('\nEnter the filename: ')
if os.path.isfile(filename):
	f = open(filename)
else:
	sys.exit("Please enter a valid filename.")

stpxC = 615
stpxR = 418
enpxC = 4015
grHeight = 290
minLength = 10
bpStart = -1
gapThres = 20
strandThres = 95

for x in f:
	lineSplit = x.split(' ')
	IMG_PATH = "Images/" + lineSplit[0]
	print("\nAnalyzing file " + IMG_PATH + "...")

	if (len(lineSplit) > 2):
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
		output = "BPPairs_95_Track" + str(x)+ ".txt"
		BPList = open(output, "a")

		# For the first track, check if you want to enter parameters
		if x > 1:
			if len(lineSplit) > 2:
				stpxR = int(lineSplit[4])
			else:
				stpxR = 1232

		# Sends to color_correct function to standardize colors
		color_correct()

		# Sends to find_ROI function to find regions of interest in the strand
		find_ROI()

		kbRegion = IMG_PATH.split('/')

		BPList.write("	End of " + kbRegion[1] + " with start BP of " + str(bpStart) + "\n\n")
		# Close the file we're writing to
		BPList.close()

print("\nFinished reading to files!")

