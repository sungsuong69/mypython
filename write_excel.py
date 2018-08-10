import xlsxwriter
from string import center
import re

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()
cell_format1 = workbook.add_format()       # Set properties later.
color_red_code = hex(218)
color_green_code = hex(238)
color_blue_code = hex(243)
bg_color = '#' + color_red_code + color_green_code + color_blue_code
bg_color = re.sub(r'0x', '', bg_color)
cell_format1.set_bg_color(bg_color)

cell_format1.set_bold()

cell_format = workbook.add_format()
cell_format.set_bold()
cell_format.set_align('center')
cell_format.set_font_color('red')
cell_format.set_bottom(2)

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', '2.5'],
    ['Gas',   'pk'],
    ['Food',  '34'],
    ['Gym',    '1.5'],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 1
col = 0

worksheet.set_column(0, 0, 8)
worksheet.set_column(1, 1, 8)
worksheet.set_column(2, 2, 8)
worksheet.set_column(3, 3, 3)
worksheet.set_column(4, 4, 30)
worksheet.set_column(5, 5, 3)
worksheet.set_column(6, 6, 8)
worksheet.set_column(7, 7, 8)
worksheet.set_column(8, 8, 8)
worksheet.set_column(9, 9, 8)
for i in range(9):
    worksheet.write_blank(row, col+i,'', cell_format1)
row = 2
# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    if re.search(r'\d',cost):
        cost = float(cost)
        
    worksheet.write(row, col,     item,cell_format)
    worksheet.write(row, col + 1, cost,cell_format)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()