from statistics import mean
from statistics import stdev
import os.path
import sys
import re
import matplotlib.pyplot as plt
import numpy as np

# Read in file and check if it's valid, if not, then terminate the program
filename = input('\nEnter the filename: ')
if os.path.isfile(filename):
	f = open(filename)
else:
	sys.exit("Please enter a valid filename.")

output = open(filename + "_stats.txt", "w")

# Variables to keep track of for left side and right side of plasmid
gapCountLeft = 0
bottomCountLeft = 0
topCountLeft = 0

gapListLeft = []
bottomListLeft = []
topListLeft = []

gCountTempLeft = 0
bCountTempLeft = 0
tCountTempLeft = 0

gListTempLeft = []
bListTempLeft = []
tListTempLeft = []

gapCountRight = 0
bottomCountRight = 0
topCountRight = 0

gapListRight = []
bottomListRight = []
topListRight = []

gCountTempRight = 0
bCountTempRight = 0
tCountTempRight = 0

gListTempRight = []
bListTempRight = []
tListTempRight = []

gMeanList = []
bMeanList = []
tMeanList = []

coordList = []

# Mode for determining which side of the plasmid it's on
mode = -1

# Run through the lines in the file
for x in f:
	# Clean up the line to read in coordinates (A, B)
	x = x.replace('\t','')
	if not(x.startswith('E')) and not(x.startswith('\n')):
		x = x.replace(' ','')
		x = x.replace('(','')
		x = x.replace(')','')
		split = x.split(':')
		coord = split[1]
		coordSplit = coord.split(',')
		coordA = float(coordSplit[0]) 
		coordB = float(coordSplit[1])
		
		# Various if/elif to determine which side of the oriC/terminal site the ROI are located
		if coordA < 1684259.0 and coordB < 1684259.0:
			mode = 0
			diff = coordB - coordA
		elif coordA > 3925975.0 and coordB > 3925975.0:
			mode = 1
			diff = coordB - coordA
		elif coordA < 3925744.0 and coordA > 1685188.0 and coordB < 3925744.0 and coordB > 1685188.0:
			mode = 1
			diff = coordB - coordA
		elif coordA < 1685188.0 and coordA > 1684259.0 and coordB > 1685188.0:
			coordA = 1685188.0
			mode = 1
			diff = coordB - coordA
		elif coordA < 1684259.0 and coordB > 1684259.0 and coordB < 1685188.0:
			coordB = 1684259.0
			mode = 0
			diff = coordB - coordA
		elif (coordA < 3925744.0 and coordB > 3925744.0 and coordB < 3925975.0):
			coordB = 3925744.0
			mode = 1
			diff = coordB - coordA
		elif coordA < 3925975.0 and coordA > 3925744.0 and coordB > 3925975.0:
			coordA = 3925975.0
			mode = 0
			diff = coordB - coordA
		elif coordA < 3925744.0 and coordB > 3925975.0:
			tempB = 3925744.0
			tempA = 3925975.0
			diff1 = tempB - coordA
			diff2 = coordB - tempA
			mode = 2
		elif coordA < 1684259.0 and coordB > 1685188.0:
			tempB = 1684259.0
			tempA = 1685188.0
			diff2 = tempB - coordA
			diff1 = coordB - tempA
			mode = 2
		else:
			mode = 3
		
		# If mode 0, it's on the left side, add to the correct list (gap, bottom, top)
		if mode == 0:
			if x[0] == 'g':
				gapCountLeft += 1
				gCountTempLeft += 1
				gapListLeft.append(diff)
				gListTempLeft.append(diff)
			elif x[0] == 'B':
				bottomCountLeft += 1
				bCountTempLeft += 1
				bottomListLeft.append(diff)
				bListTempLeft.append(diff)
			elif x[0] == 'T':
				topCountLeft += 1
				tCountTempLeft += 1
				topListLeft.append(diff)
				tListTempLeft.append(diff)
		# If mode 1, it's on the right side, add to the correct list (gap, bottom, top)
		elif mode == 1:
			if x[0] == 'g':
				gapCountRight += 1
				gCountTempRight += 1
				gapListRight.append(diff)
				gListTempRight.append(diff)
			elif x[0] == 'B':
				bottomCountRight += 1
				bCountTempRight += 1
				bottomListRight.append(diff)
				bListTempRight.append(diff)
			elif x[0] == 'T':
				topCountRight += 1
				tCountTempRight += 1
				topListRight.append(diff)
				tListTempRight.append(diff)
		# If mode 2, it's on both sides, add to the correct list (gap, bottom, top)
		elif mode == 2:
			if x[0] == 'g':
				gapCountRight += 1
				gCountTempRight += 1
				gapListRight.append(diff1)
				gListTempRight.append(diff1)
				gapCountLeft += 1
				gCountTempLeft += 1
				gapListLeft.append(diff2)
				gListTempLeft.append(diff2)
			elif x[0] == 'B':
				bottomCountRight += 1
				bCountTempRight += 1
				bottomListRight.append(diff1)
				bListTempRight.append(diff1)
				bottomCountLeft += 1
				bCountTempLeft += 1
				bottomListLeft.append(diff2)
				bListTempLeft.append(diff2)
			elif x[0] == 'T':
				topCountRight += 1
				tCountTempRight += 1
				topListRight.append(diff1)
				tListTempRight.append(diff1)
				topCountLeft += 1
				tCountTempLeft += 1
				topListLeft.append(diff2)
				tListTempLeft.append(diff2)
	
	# If it's the end of a region, write to the output file
	elif x.startswith('E'):
		split = x.split(' ')
		split[2] = split[2].replace('\n','')
		split = split[2].split('.')
		output.write("For " + split[0] + ":\n")
		split = split[0].split('-')
		coA = split[0].replace('+','')
		coordList.append(int(coA))
		
		# Write down average sizes and stdevs for regions
		output.write("Number of gaps: " + str(gCountTempRight + gCountTempLeft) +"\n")
		if gCountTempRight + gCountTempLeft != 0:
			gMeanList.append(mean(gListTempRight + gListTempLeft))
			output.write("Average size of gaps: " + str(mean(gListTempRight + gListTempLeft)))
			if gCountTempRight + gCountTempLeft >= 2:
				output.write(" ± " + str(stdev(gListTempRight + gListTempLeft)) + "\n")
			else:
				output.write("\n")
		else:
			gMeanList.append(0)
		
		output.write("Number of bottom strand ROIs: " + str(bCountTempRight + bCountTempLeft) + "\n")
		if bCountTempRight + bCountTempLeft != 0:
			bMeanList.append(mean(bListTempRight + bListTempLeft))
			output.write("Average size of bottom strand ROIs: " + str(mean(bListTempRight + bListTempLeft)))
			if bCountTempRight + bCountTempLeft >= 2:
				output.write(" ± " + str(stdev(bListTempRight + bListTempLeft)) + "\n")
			else:
				output.write("\n")
		else:
			bMeanList.append(0)
		
		output.write("Number of top strand ROIs: " + str(tCountTempRight + tCountTempLeft) +"\n")
		if tCountTempRight + tCountTempLeft != 0:
			tMeanList.append(mean(tListTempRight + tListTempLeft))
			output.write("Average size of top strand ROIs: " + str(mean(tListTempRight + tListTempLeft)))
			if tCountTempRight + tCountTempLeft >= 2:
				output.write(" ± " + str(stdev(tListTempRight + tListTempLeft)) + "\n")
			else:
				output.write("\n")
		else:
			tMeanList.append(0)

		output.write('\n')
		gCountTempRight = 0
		bCountTempRight = 0
		tCountTempRight = 0
		gCountTempLeft = 0
		bCountTempLeft = 0
		tCountTempLeft = 0
		gListTempRight.clear()
		bListTempRight.clear()
		tListTempRight.clear()
		gListTempLeft.clear()
		bListTempLeft.clear()
		tListTempLeft.clear()

output.write("Summary statistics:\n")
output.write("For the right side of the plasmid:\n")
output.write("	Average size for gap: " + str(mean(gapListRight)) + " ± " + str(stdev(gapListRight)) + "\n")
output.write("	Number of gaps: " + str(gapCountRight) + "\n")
output.write("	Average size for bottom strand: " + str(mean(bottomListRight))  + " ± " + str(stdev(bottomListRight)) + "\n")
output.write("	Number of bottom strand ROIs: " + str(bottomCountRight) + "\n")
output.write("	Average size for top strand: " + str(mean(topListRight))  + " ± " + str(stdev(topListRight)) + "\n")
output.write("	Number of top strand ROIs: " + str(topCountRight) + "\n")

output.write("\nFor the left side of the plasmid:\n")
output.write("	Average size for gap: " + str(mean(gapListLeft)) + " ± " + str(stdev(gapListLeft)) + "\n")
output.write("	Number of gaps: " + str(gapCountLeft) + "\n")
output.write("	Average size for bottom strand: " + str(mean(bottomListLeft))  + " ± " + str(stdev(bottomListLeft)) + "\n")
output.write("	Number of bottom strand ROIs: " + str(bottomCountLeft) + "\n")
output.write("	Average size for top strand: " + str(mean(topListLeft))  + " ± " + str(stdev(topListLeft)) + "\n")
output.write("	Number of top strand ROIs: " + str(topCountLeft) + "\n")

plt.plot(coordList, gMeanList, label = "Gap")
# plt.plot(coordList, bMeanList, label = "Bottom Strand ROI")
# plt.plot(coordList, tMeanList, label = "Top Strand ROI")
plt.title('Average size of Gap in the MG1655 E. coli Genome')
plt.ylabel('Average Size (bp)')
plt.xlabel('Region in Genome (bp)')
plt.xticks(np.arange(0, 4700, 100))
plt.axis([0, 4700, 0, 1600])
plt.xticks(rotation=60)
plt.legend()
plt.savefig(filename + 'gap.png')
plt.show()

fig, axs = plt.subplots(2, sharex = True, sharey = True)
axs[0].plot(coordList, tMeanList, 'tab:green')
axs[0].set_title('Top Strand ROI')
axs[1].plot(coordList, bMeanList, 'tab:red')
axs[1].set_title('Bottom Strand ROI')
plt.setp(axs, xticks=np.arange(0, 4700, 100))
plt.axis([0, 4700, 0, 750])
plt.xticks(rotation=60)
fig.suptitle('Average size of ROI in the MG1655 E. coli Genome')
for ax in axs:
	ax.set(xlabel='Region in Genome (kb)', ylabel='Average Size (bp)')
	ax.label_outer()
plt.savefig(filename + '.png')
plt.show()

f.close()