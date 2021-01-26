import xlwt
from xlwt import Workbook
import os.path
import sys
import re

# Read in file and check if it's valid, if not, then terminate the program
filename = input('\nEnter the filename: ')
if os.path.isfile(filename):
	f = open(filename)
else:
	sys.exit("Please enter a valid filename.")

wb = Workbook()

style = xlwt.easyxf('font: bold 1')

tSheet = wb.add_sheet('Top Strand ROI')
tSheet.write(0, 0, 'Start BP', style)
tSheet.write(0, 1, 'End BP', style)
tSheet.write(0, 2, 'Median BP', style)
tSheet.write(0, 3, 'Size of ROI', style)

bSheet = wb.add_sheet('Bottom Strand ROI')
bSheet.write(0, 0, 'Start BP', style)
bSheet.write(0, 1, 'End BP', style)
bSheet.write(0, 2, 'Median BP', style)
bSheet.write(0, 3, 'Size of ROI', style)

gSheet = wb.add_sheet('Gap ROI')
gSheet.write(0, 0, 'Start BP', style)
gSheet.write(0, 1, 'End BP', style)
gSheet.write(0, 2, 'Median BP', style)
gSheet.write(0, 3, 'Size of ROI', style)

tRow = 1
bRow = 1
gRow = 1


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

		if x[0] == 'g':
			gSheet.write(gRow, 0, coordA)
			gSheet.write(gRow, 1, coordB)
			gSheet.write(gRow, 2, ((coordB + coordA)/2))
			gSheet.write(gRow, 3, (coordB - coordA))
			gRow += 1
		elif x[0] == 'B':
			bSheet.write(bRow, 0, coordA)
			bSheet.write(bRow, 1, coordB)
			bSheet.write(bRow, 2, ((coordB + coordA)/2))
			bSheet.write(bRow, 3, (coordB - coordA))
			bRow += 1
		elif x[0] == 'T':
			tSheet.write(tRow, 0, coordA)
			tSheet.write(tRow, 1, coordB)
			tSheet.write(tRow, 2, ((coordB + coordA)/2))
			tSheet.write(tRow, 3, (coordB - coordA))
			tRow += 1

wb.save("ROI in the MG1655 E. coli Genome Track 2.xls")