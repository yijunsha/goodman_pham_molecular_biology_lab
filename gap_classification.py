import openpyxl
import os.path
import sys
import re

# strandFilename = input('\nEnter the filename for the strand: ')
strandFilename = "E-1_Bottom.xlsx_split.xlsx"

if os.path.isfile(strandFilename):
	strandWb = openpyxl.load_workbook(strandFilename)
	strSheet = strandWb.worksheets[0]
else:
	sys.exit("Please enter a valid filename.")

# rfFilename = input('\nEnter the filename for the reading frames to compare: ')
rfFilename = "Escherichia coli (K12_MG1655) _ncRNA_gene.xlsx_split.xlsx"
if os.path.isfile(rfFilename):
	rfWb = openpyxl.load_workbook(rfFilename)
	rfSheet = rfWb.worksheets[0]
else:
	sys.exit("Please enter a valid filename.")

output = open(strandFilename + "_summary_ncRNA_gene.txt", "w")

lowGapCount = 0
lowEndIntoCount = 0
lowGapIntoCount = 0
lowBetweenGapCount = 0
lowBetweenNoGapCount = 0
lowNoNotableCount = 0
lowEncompassCount = 0
lowUnsure = 0

highGapCount = 0
highEndIntoCount = 0
highGapIntoCount = 0
highBetweenGapCount = 0
highBetweenNoGapCount = 0
highNoNotableCount = 0
highEncompassCount = 0
highUnsure = 0

nameCol = 5
lowCover = "Low Coverage"
highCover = "High Coverage"

rfcurrentRow = 2
startCol = 3
endCol = 4
infoCol = 8
identity = ""

for row in range(2, strSheet.max_row + 1):

	startBP = strSheet.cell(row, startCol).value
	endBP = strSheet.cell(row, endCol).value

	if (endBP < rfSheet.cell(rfcurrentRow, startCol).value and
		type(rfSheet.cell(rfcurrentRow - 1, endCol).value) == str):
		strSheet.cell(row, infoCol, 'gap in reading frames')
		if (strSheet.cell(row, nameCol).value == lowCover):
			lowGapCount += 1
		else:
			highGapCount += 1
		continue

	if (rfcurrentRow >= rfSheet.max_row):
		strSheet.cell(row, infoCol, 'gap in reading frames')
		if (strSheet.cell(row, nameCol).value == lowCover):
			lowGapCount += 1
		else:
			highGapCount += 1
		continue

	# print(rfcurrentRow)
	# print(endCol)
	# print(rfSheet.cell(rfcurrentRow, endCol))
	# print(rfSheet.cell(rfcurrentRow, endCol).value)
	# print(row)
	# print(startBP)
	# print(endBP)
	# print('\n')
	# if (rfSheet.cell(rfcurrentRow, endCol).value is not None):
	while startBP > rfSheet.cell(rfcurrentRow, endCol).value:
		rfcurrentRow += 1
		if (rfcurrentRow >= rfSheet.max_row):
			strSheet.cell(row, infoCol, 'gap in reading frames')
		if (strSheet.cell(row, nameCol).value == lowCover):
			lowGapCount += 1
		else:
			highGapCount += 1
		break
	# else:
	# 	strSheet.cell(row, infoCol, 'gap in reading frames')
	# 	if (strSheet.cell(row, nameCol).value == lowCover):
	# 		lowGapCount += 1
	# 	else:
	# 		highGapCount += 1
	# 	continue

	# print(rfSheet.cell(rfcurrentRow, startCol).value, strSheet.cell(row, startCol).value)

	if (endBP < rfSheet.cell(rfcurrentRow, startCol).value and
		startBP > rfSheet.cell(rfcurrentRow - 1, endCol).value or rfcurrentRow >= rfSheet.max_row):

		identity = "gap in reading frames"

		if (strSheet.cell(row, nameCol).value == lowCover):
			lowGapCount += 1
		else:
			highGapCount += 1

	elif (startBP >= rfSheet.cell(rfcurrentRow, startCol).value and 
		startBP <= rfSheet.cell(rfcurrentRow, endCol).value and 
		endBP <= rfSheet.cell(rfcurrentRow + 1, startCol).value and
		endBP >= rfSheet.cell(rfcurrentRow, endCol).value):

		diff = rfSheet.cell(rfcurrentRow, endCol).value - startBP
		identity = "end into gap by " + str(diff) + "bp"

		if (strSheet.cell(row, nameCol).value == lowCover):
			lowEndIntoCount += 1
		else:
			highEndIntoCount += 1

	elif (endBP <= rfSheet.cell(rfcurrentRow, endCol).value and 
		endBP >= rfSheet.cell(rfcurrentRow, startCol).value and 
		startBP >= rfSheet.cell(rfcurrentRow - 1, endCol).value and
		startBP <= rfSheet.cell(rfcurrentRow, startCol).value):

		diff = endBP - rfSheet.cell(rfcurrentRow, startCol).value
		identity = "gap into start by " + str(diff) + "bp"

		if (strSheet.cell(row, nameCol).value == lowCover):
			lowGapIntoCount += 1
		else:
			highGapIntoCount += 1

	elif (startBP >= rfSheet.cell(rfcurrentRow, startCol).value and 
		startBP <= rfSheet.cell(rfcurrentRow, endCol).value and
		endBP <= rfSheet.cell(rfcurrentRow + 1, endCol).value and 
		endBP >= rfSheet.cell(rfcurrentRow + 1, startCol).value):

		if rfSheet.cell(rfcurrentRow, endCol).value > rfSheet.cell(rfcurrentRow + 1, startCol).value:
			identity = "between reading frames, no gap"

			if (strSheet.cell(row, nameCol).value == lowCover):
				lowBetweenNoGapCount += 1
			else:
				highBetweenNoGapCount += 1
		else:
			identity = "between reading frames, gap"
			if (strSheet.cell(row, nameCol).value == lowCover):
				lowBetweenGapCount += 1
			else:
				highBetweenGapCount += 1

	elif (startBP <= rfSheet.cell(rfcurrentRow, endCol).value and 
		startBP >= rfSheet.cell(rfcurrentRow, startCol).value and
		endBP <= rfSheet.cell(rfcurrentRow, endCol).value and 
		endBP >= rfSheet.cell(rfcurrentRow, startCol).value):

		identity = "no notable"

		if (strSheet.cell(row, nameCol).value == lowCover):
			lowNoNotableCount += 1
		else:
			highNoNotableCount += 1

	elif ((startBP <= rfSheet.cell(rfcurrentRow, startCol).value and 
		endBP >= rfSheet.cell(rfcurrentRow, endCol).value) or
		(startBP <= rfSheet.cell(rfcurrentRow + 1, startCol).value and 
		endBP >= rfSheet.cell(rfcurrentRow + 1, endCol).value)):

		identity = "encompassing reading frame"

		if (strSheet.cell(row, nameCol).value == lowCover):
			lowEncompassCount += 1
		else:
			highEncompassCount += 1

	else:
		identity = "unsure"

		if (strSheet.cell(row, nameCol).value == lowCover):
			lowUnsure += 1
		else:
			highUnsure += 1

	strSheet.cell(row, infoCol, identity)

output.write("Summary statistics:\n")
output.write("For Low Coverage Regions:\n")
output.write("	Gap in Reading frame: " + str(lowGapCount)  + "\n")
output.write("	End into Gap: " + str(lowEndIntoCount) + "\n")
output.write("	Gap into Start: " + str(lowGapIntoCount) + "\n")
output.write("	Between reading frames w Gap: " + str(lowBetweenGapCount) + "\n")
output.write("	Between reading frames w/o Gap: " + str(lowBetweenNoGapCount) + "\n")
output.write("	No Notable: " + str(lowNoNotableCount) + "\n")
output.write("	Encompassing reading frame: " + str(lowEncompassCount) + "\n")
output.write("	Unsure: " + str(lowUnsure) + "\n")
output.write("	Total Low Coverage: " + str(lowGapCount + lowEndIntoCount + lowGapIntoCount + 
	lowBetweenGapCount + lowBetweenNoGapCount + lowNoNotableCount + lowEncompassCount + lowUnsure) + "\n")


output.write("Summary statistics:\n")
output.write("For High Coverage Regions:\n")
output.write("	Gap in Reading frame: " + str(highGapCount)  + "\n")
output.write("	End into Gap: " + str(highEndIntoCount) + "\n")
output.write("	Gap into Start: " + str(highGapIntoCount) + "\n")
output.write("	Between reading frames w Gap: " + str(highBetweenGapCount) + "\n")
output.write("	Between reading frames w/o Gap: " + str(highBetweenNoGapCount) + "\n")
output.write("	No Notable: " + str(highNoNotableCount) + "\n")
output.write("	Encompassing reading frame: " + str(highEncompassCount) + "\n")
output.write("	Unsure: " + str(highUnsure) + "\n")
output.write("	Total High Coverage: " + str(highGapCount + highEndIntoCount + highGapIntoCount + 
	highBetweenGapCount + highBetweenNoGapCount + highNoNotableCount + highEncompassCount + highUnsure) + "\n")

strandWb.save(strandFilename + "_classified_ncRNA_gene.xlsx")