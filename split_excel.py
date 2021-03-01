import openpyxl
import os.path
import sys
import re

# Read in file and check if it's valid, if not, then terminate the program
filename = input('\nEnter the filename: ')
if os.path.isfile(filename):
	wb = openpyxl.load_workbook(filename)
	sheet = wb.worksheets[0]
else:
	sys.exit("Please enter a valid filename.")

sheet.insert_cols(2)
sheet.insert_cols(4)

sheet.cell(1, 2, 'read direction')
sheet.cell(1, 3, 'start bp')
sheet.cell(1, 4, 'end bp')


currentCol = 3

for row in range(1, sheet.max_row + 1):
	cellValue = sheet.cell(row, currentCol).value
	if cellValue[0] == 'c' or cellValue[0] == 'j':
		split = cellValue.split('(')
		sheet.cell(row, currentCol - 1, split[0])
		split[1] = split[1].replace(')','')
		sheet.cell(row, currentCol, split[1])
	cellValue = sheet.cell(row, currentCol).value
	ellipseSplit = cellValue.split('..')
	if (len(ellipseSplit) > 1):
		startBP = int(ellipseSplit[0])
		endBP = int(ellipseSplit[1])
		sheet.cell(row, currentCol, startBP)
		sheet.cell(row, currentCol + 1, endBP)


wb.save(filename + "_split.xlsx")