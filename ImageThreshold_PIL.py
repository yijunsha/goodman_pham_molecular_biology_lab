# The purpose of this program is to take a .jpg image extracted from CLC Workbench and count the
# number of red/green pixels in each image to determine whether or not a gap, bottom strand, or
# top strand ROI exists in that region based on the proportion of the red:green.
# The program takes in .jpg and outputs a .txt for each ROI and the bp range of each.

from PIL import Image
import matplotlib.pyplot as plt
import sys

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

# Function to display the pixel values of the image
def displayImg(yes_no):
	if yes_no == 'y':
		plt.imshow(im)
		plt.show()
		return
	
	elif yes_no == 'n':
		return
	
	else:
		check = input("Please enter y for yes or n for no: ")
		displayImg(check)
		return
	return

# This function checks to see whether or not the user wants to enter their own parameters or just use
# existing default parameters.
def Param_select(par_enter, x):
	global stpxC
	global stpxR
	global enpxC
	global grHeight
	global minLength
	global bpStart
	global gapThres
	global strandThres
	global param_enter

	# If you choose to use your own parameters:
	if par_enter == 'own':
		# For the first track, enter all the parameters
		if (x == 1): 
			# Sends to the enterParam function to enter parameters
			enterParam('y')
		else:
			# The second has all the same parameters except start row pixel
			check = input("\nWould you like to look at the image to determine pixel values? (y/n): ")
			displayImg(check)
			stpxR = int(input('	Enter which row the start pixel is located at: '))
			if stpxR < 0 or stpxR > h:
				stpxR = int(input("Please enter a valid row value: "))
		return

	# If you choose to use the default values
	elif par_enter == 'default':
		if (x == 1):
			bpStart = int(input('Enter the beginning base pair value of the cropped image: '))
		stpxC = 615
		enpxC = 4015
		grHeight = 290
		minLength = 10
		gapThres = 20
		strandThres = 90
		if (x == 1):
			stpxR = 418
		else:
			stpxR = 1232
		return

	# If you want to know what the default values are
	elif par_enter == 'display defaults':
		print("The following values are used as a default:")
		print("Start pixel column: 615px")
		print("End pixel column: 4015px")
		print("Start pixel row for Track 1: 418px")
		print("Start pixel row for Track 2: 1232px")
		print("Graph pixel height: 290px")
		print("Minimum pixel length of ROI: 10px")
		print("Threshold for gap: 20px")
		print("Percentage threshold for a strand to be considered ROI: 90%")
		param_enter = input('\nEnter "own", "default", or "display defaults" to check the default values: ')
		Param_select(par_enter = param_enter, x = x)
		return

	# If you input something that isn't one of the known option
	else:
		param_enter = input(' Please enter "own", "default", or "display defaults": ')
		Param_select(par_enter = param_enter, x = x)
		return

# Function designed to enter in parameters and asks the user if they would like to re-enter
def enterParam(y_n):
	global stpxC
	global stpxR
	global enpxC
	global grHeight
	global minLength
	global bpStart
	global gapThres
	global strandThres

	# If you do want to enter parameter values
	if y_n == 'y':

		print("\nPlease enter integer values for the following parameters:")

		stpxC = int(input('	Enter which column the start pixel is located at: '))
		if stpxC < 0 or stpxC > w:
			stpxC = int(input("Please enter a valid column value: "))
		
		stpxR = int(input('	Enter which row the start pixel is located at: '))
		if stpxR < 0 or stpxR > h:
			stpxR = int(input("Please enter a valid row value: "))

		enpxC = int(input('	Enter which column the end pixel is located at: '))
		if enpxC < 0 or enpxC > w:
			enpxC = int(input("Please enter a valid column value:"))
		
		grHeight = int(input('	Enter the pixel height of the graph: '))
		if grHeight < 0 or grHeight > h:
			grHeight = int(input("Please enter a valid height: "))
		
		minLength = int(input('	Enter the minimum pixel length of the ROI you are looking for: '))
		if minLength < 0 or minLength > w:
			minLength = int(input("Please enter a valid length: "))
		
		bpStart = int(input('	Enter the beginning base pair value of the cropped image: '))

		gapThres = int(input('	Enter the threshold for a gap: '))
		if gapThres < 0 or gapThres > grHeight:
			gapThres = int(input("Please enter a valid gap threshold: "))
		
		strandThres = int(input('	Enter the percent (0-100) red or green to be considered significant for ROI: '))
		if strandThres < 0 or strandThres > 100:
			strandThres = int(input("Please enter a valid percentage: "))
		
		parameter_check = input("Would you like to re-enter the values (y/n): ")
		if parameter_check == 'y':
			check = input("\nWould you like to look at the image to determine pixel values? (y/n): ")
			displayImg(check)
		enterParam(parameter_check)
		return
	
	elif y_n == 'n':
		return
	
	else:
		parameter_check = input("Please enter y for yes or n for no: ")
		enterParam(parameter_check)
		return
	
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

# User input parameters:
IMG_PATH = input('\nEnter the filename: ')

# Tries to open the image file and returns if invalid
try:
	im = Image.open(IMG_PATH)
except FileNotFoundError:
	sys.exit("Please enter a valid filename.")

# Takes in the number of tracks you're trying to read
numTracks = int(input('How many tracks are you reading?: '))

# Gets the pixel dimensions of the image and 
# Converts the image into RGB values that can then be loaded into pix
w, h = im.size
im = im.convert('RGB')
pix = im.load()
param_enter = ''

# For each track, write to a different file
for x in range(1, numTracks + 1):
	# This is the file that the program writes into
	output = "BPPairs_90_Track" + str(x)+ ".txt"
	BPList = open(output, "a")
	
	print("\nAnalyzing Track " + str(x) + "...")

	# For the first track, check if you want to enter parameters
	if (x == 1): 
		check = input("\nWould you like to look at the image to determine pixel values? (y/n): ")
		displayImg(check)
		print("Would you like to enter your own parameters or use the default?")
		param_enter = input('	Enter "own", "default", or "display defaults" to check the default values: ')
	# Send to the Param_select function to see whether or not you want to input parameters
	Param_select(par_enter = param_enter, x = x)		

	# Sends to color_correct function to standardize colors
	color_correct()

	# Shows the graph after being edited, uncomment to display
	# plt.imshow(im)
	# plt.show()

	# Sends to find_ROI function to find regions of interest in the strand
	find_ROI()

	BPList.write("	End of " + IMG_PATH + " with start BP of " + str(bpStart) + "\n\n")
	# Close the file we're writing to
	BPList.close()

print("\nFinished reading to files!")

