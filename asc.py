import sys
import os
import time
from pathlib import Path

# Build with pyinstaller:
# pyinstaller --onefile asc.py


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# You need a csv file that contains a header. E.g. something like:
# TIME, RENT, INCOME, FOOD
#
# The first position in the first line is linked to the x-axis
# The other positions in the first line are linked to the y-axis and it loops through
# Other lines below are ignored
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


version = '1.0'


# USER INPUTS
print('######## Autoscript for Plotly (JS-Version) v' + version + ' ########\n')

# set path and name
plot_name = input('Enter the plot name: ')
PATH = input("Enter the path to the csv-file. E.g. data/file.csv: ")
csv_header_file = input('Enter the path to the header.csv or your main csv file: ')

# check inputs
print('\nCheck if your inputs are correct. Type y or n:')
print('Plot name:            ' + plot_name)
print('Relative Path to CSV: ' + PATH)
print('Path to header file:  ' + csv_header_file)
check_input1 = input()

if check_input1 == 'y':
    pass
else:
    print('Exiting script...')
    time.sleep(3)
    sys.exit()


# set the plot range
try:
    plot_range_min = int(input('Set the MINIMUM plot range on the y axis. (Default: -10): '))
    plot_range_max = int(input('Set the MAXIMUM plot range on the y axis. (Default: 110): '))

    # check inputs
    print('\nCheck if your inputs are correct. Type y or n:')
    print('MIN plot range: ' + str(plot_range_min))
    print('MAX plot range: ' + str(plot_range_max))
    check_input2 = input()

    if check_input2 == 'y':
        pass
    else:
        print('Exiting script...')
        time.sleep(3)
        sys.exit()

except ValueError:
    print('[ERROR]: Please use only positive or negative integers.')
    print('Closing script in 5 seconds...')
    time.sleep(5)
    sys.exit()


# CONFIG
# layout
line_width = 1
main_font_color = 'white'
legend_font_color = 'white'

v_gridcolor = '#43454a'  # vertical gridlines
h_gridcolor = '#43454a'  # horizontal grid lines

x_axis_line_color = '#222326'
y_ticklabel_color = 'white'
x_ticklabel_color = 'white'

y_showticklabels = 'true'
x_showticklabels = 'true'

plot_bgcolor = '#181a1c'
paper_bgcolor = '#1b1c1f'


# GLOBAL VARS
y_names = []
mid1_loop1 = []
mid1_loop2 = []
mid1_loop3 = []
mid2_loop1 = []


# INIT
# import csv header
try:
    # x_axis
    with open(csv_header_file, 'r', encoding='utf8') as cr:
        x_axis = cr.readline()

    x_axis = x_axis.split(',')

    DATETIME = '"' + str(x_axis[0]) + '"'

    # y_axis
    y_axis = x_axis[1:]
    for i in range(len(y_axis)):
        y_names.append(y_axis[i])

except FileNotFoundError:
    print("[ERROR]: " + csv_header_file + " not found! Check if your csv-header file exists.")
    print('Closing script in 5 seconds...')
    time.sleep(5)
    sys.exit()


# count file
# check if file exists
try:
    Path('count.txt').touch(exist_ok=True)
except PermissionError:
    print('[ERROR]: Failed to create counter file. Check permissions!')
    time.sleep(3)
    sys.exit()

# write zeros if file is empty
csv_empty = os.stat('count.txt').st_size == 0

if csv_empty is True:
    with open('count.txt', 'w') as cvw:
        cvw.write('0')

# get count
with open('count.txt', 'r') as of:
    count = int(of.read())

print('COUNT: ' + str(count))


# get file name
path_list = list(PATH)
c = 0

# count all slash' and push to c
for i in range(len(path_list)):
    if "/" == path_list[i]:
        c = c + 1

# 1. split PATH object into c strings with / as delimiter
# 2. split temp_string again into 2 strings with . as delimiter
split_string = PATH.split("/", c)
temp_name = split_string[c]
temp_string = temp_name.split(".", 1)
file_name = temp_string[0]


print('######## BUILDING FILE ########')


# top
head = 'const CSV' + str(count) + ' =\n\t"' + PATH + '";\n\nfunction plotFromCSV' + str(count) + '() {' \
    '\n\tPlotly.d3.csv(CSV' + str(count) + ', function(err, rows) {\n\t\t' \
    'console.log(rows);\n\t\tprocessData' + str(count) + '(rows);\n\t});\n}\n'


# mid1 loop2
for x in range(len(y_names)):
    mid1_loop2.append('\t\ty' + str(x) + '.push(row["' + y_names[x].rstrip('\n') + '"]);')

mid1_loop2 = '\n'.join(mid1_loop2)

# mid1 loop1
for x in range(len(y_names)):
    mid1_loop1.append('\tlet y' + str(x) + ' = [];')

mid1_loop1 = '\n'.join(mid1_loop1)

# mid1 loop3
for x in range(len(y_names)):
    mid1_loop3.append('y' + str(x))

mid1_loop3 = ', '.join(mid1_loop3)


# mid1
mid1 = 'function processData' + str(count) + '(allRows) {\n\tlet x = [];\n' \
       + mid1_loop1 + '\n\tlet row;\n\n\tlet i = 0;\n\twhile (i < allRows.length) {\n\t\t' \
       + 'row = allRows[i];\n\t\tx.push(row[' + DATETIME + ']);\n' \
       + mid1_loop2 + '\n\t\ti += 1;\n\t}\n\n\tconsole.log("X", x);\n\tconsole.log("Y", y);\n\n\t' \
       + 'makePlotly' + str(count) + '(x, ' + mid1_loop3 + ');\n}\n'


# mid2 loop1
for x in range(len(y_names)):
    mid2_loop1.append(
        '\t\t{\n\t\t\tx: x, \n\t\t\ty: y' + str(x) + ', \n\t\t\tname: "' + y_names[x].rstrip('\n') + '",\n\t\t\tline: '
        '{\n\t\t\t\twidth: ' + str(line_width)
        + '\n\t\t\t}\n\t\t}'
    )

mid2_loop1 = ',\n'.join(mid2_loop1)

# mid2
mid2 = 'function makePlotly' + str(count) + '(x, ' + mid1_loop3 + ') {\n\t' \
       + 'let traces = [\n' + mid2_loop1 + '\n\t];'


# mid3
mid3 = '\n\tlet layout = {\n\t\ttitle: {\n\t\t\ttext: "' + plot_name + '",\n\t\t\t' + "font: { color: '" \
        + main_font_color + "' }" + "\n\t\t},\n\t\tlegend: { font: { color: '" + legend_font_color + "' } },\n\t\t" \
        + 'yaxis: {\n\t\t\trange: [' + str(plot_range_min) + ', ' + str(plot_range_max) + '],\n\t\t\t' \
        + "gridcolor: '" + h_gridcolor + "',\n\t\t\t" \
        + "color: '#222326',\n\t\t\tshowticklabels: " + y_showticklabels + ",\n\t\t\ttickfont: {\n\t\t\t\t" \
        "family: 'Helvetica, sans-serif',\n\t\t\t\tsize: 14,\n\t\t\t\tcolor: '" + y_ticklabel_color \
        + "'\n\t\t\t},\n\t\t},\n" \
        + "\t\txaxis: {\n\t\t\tgridcolor: '" + v_gridcolor + "',\n\t\t\tcolor: '" + x_axis_line_color + "',\n\t\t\t" \
        "showticklabels: " + x_showticklabels + ",\n\t\t\ttickfont: {\n\t\t\t\tfamily: 'Helvetica, sans-serif',\n" \
        "\t\t\t\tsize: 14,\n\t\t\t\tcolor: '" + x_ticklabel_color + "'\n\t\t\t},\n\t\t},\n\t\t" \
        'plot_bgcolor:"' + plot_bgcolor + '",\n\t\tpaper_bgcolor:"' + paper_bgcolor + '"\n\t};\n'


# bot
bot = '\tlet config = {\n\t\tresponsive: true\n\t};\n\n\tPlotly.newPlot("' + file_name + \
      '", traces, layout, config);\n' \
        '}\n\nplotFromCSV' + str(count) + '();\n'


output = head + '\n' + mid1 + '\n' + mid2 + '\n' + mid3 + '\n' + bot

# save output
with open(file_name + '.js', 'w', encoding='utf8') as f:
    f.write(output)

# save count
with open('count.txt', 'w') as cf:
    cf.write(str(count + 1))


print('\n[SUCCESS]: Saved your output as a js-file!')
time.sleep(3)
