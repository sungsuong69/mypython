from collections import defaultdict
from bs4 import BeautifulSoup
import urllib
import re
import xlsxwriter

# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('nfl.xlsx')
worksheet = workbook.add_worksheet()

html_page = urllib.urlopen("http://www.python.org/index.html")

# Make soup
try:
    #resp = urllib.urlopen("http://www.donbest.com/ncaaf/odds/")
    resp = urllib.urlopen("http://www.donbest.com/nfl/odds/")
except URLError as e:
    print 'An error occured fetching %s \n %s' % (url, e.reason)   
soup = BeautifulSoup(resp.read(),features="html.parser")

def fix_odd(game_odd):
    """ fix odd """
    if re.search(r'\d',game_odd):
        return fload(game_odd)
    
def to_pacific_time_zone(game_time):
    """ convert estern time to pacific time zone """
    (time,ampm) = game_time.split()
    (hour,min) = time.split(':')
    hour = int(hour)
    if re.search(r'pm', game_time):
       print "hour = ", hour
       hour += 12

    hour -= 3
    if hour > 12:
        ampm = "am"
    return str(hour)+":"+min+" "+ampm            

def parse_rows(rows):
    """ Get data from rows """
    results = defaultdict(list)
    row_num = 0
    excel_row = 0
    for row in rows:
        if row_num == 0:
            h3_data = row.find('h3')
            if h3_data:
                print (h3_data.get_text())
                (title,date) = h3_data.get_text().split('-')
            
        if row_num > 1:
            table_headers = row.find_all('th')
            #if table_headers:
            #    results.append([headers.get_text() for headers in table_headers])

            table_data = row.find_all('td')
            if table_data:
                #print (table_data[0].get_text())
                #results.append([data.get_text() for data in table_data])
                col_num = 0
                for data in table_data:
                    if col_num == 0:
                        rot = data.get_text()
                        away_rot = data.get_text()[0:3]
                        home_rot = data.get_text()[3:6]
                    if col_num == 2:
                        span_tags = data.find_all('span')
                        if re.match("new york", span_tags[0].get_text().lower()):
                            away_team = re.sub(r'NEW YORK','NY',span_tags[0].get_text().upper())
                        else:
                            away_team = re.sub(r'\s+\w+$','',span_tags[0].get_text().upper())
                        if re.match("new york", span_tags[1].get_text().lower()):
                            home_team = re.sub(r'NEW YORK','NY',span_tags[1].get_text().upper())
                        else:
                            home_team = re.sub(r'\s+\w+$','',span_tags[1].get_text().upper())
 
                    if col_num > 2: 
                        time_tag  = data.find('div',id=re.compile("_Div_Time_1_"))
                        away_line_tags  = data.find_all('div',id=re.compile("_Div_Line_1_.*?_" + away_rot + ".*?119"))
                        home_line_tags  = data.find_all('div',id=re.compile("_Div_Line_1_.*?_" + home_rot + ".*?119"))
                        line_tags  = data.find_all('div',id=re.compile("_Div_Line_1_" + ".*?119"))
                        class_tags  = data.find_all('div',id=re.compile("_Div_Line_1_.*?119"))
                        if time_tag:
                            game_time = time_tag.get_text()
                        
                        if away_line_tags:
                            for away_line_tag in away_line_tags:
                                #print ("away line tags = ",away_line_tag.get_text())
                                away_odd = away_line_tag.get_text()
                        if home_line_tags:
                            for home_line_tag in home_line_tags:
                                #print ("home line tags = ",home_line_tag.get_text())
                                home_odd  = home_line_tag.get_text()
                    col_num += 1
                print (title)
                print (re.sub(r'^\s+','',date) + ' ' + game_time)
                print (away_rot + " | " + away_team + " | " + away_odd)
                print (home_rot + " | " + home_team + " | " + home_odd)
                game_date = re.sub(r'^\s+','',date) + ' ' + game_time
                results[game_date].append( {'game_id' : away_rot + '-' + home_rot,'title':title,'away_team' : away_team,'home_team' : home_team, 'away_odd' : away_odd, 'home_odd' : home_odd})
        row_num += 1;         
    return results

# Get table
try:
    tables = soup.find_all('table')
except AttributeError as e:
    print 'No tables found, exiting'

#print ("table size = ", len(tables))


excel_row = 0
cell_format1    = workbook.add_format()       # Set properties later.
color_red_code  = hex(218)
color_green_code= hex(238)
color_blue_code = hex(243)
bg_color        = '#' + color_red_code + color_green_code + color_blue_code
bg_color        = re.sub(r'0x', '', bg_color)
cell_format1.set_bg_color(bg_color)
#cell_format1.set_bold()
cell_format1.set_bottom(1)
cell_format1.set_top(1)

cell_format2 = workbook.add_format()
#cell_format2.set_bold()
cell_format2.set_align('center')
#cell_format2.set_font_color('red')

cell_format3 = workbook.add_format()
cell_format3.set_align('center')
cell_format3.set_font_color('#'+re.sub(r'0x','',hex(196))+re.sub(r'0x','',hex(215))+re.sub(r'0x','',hex(155)))

cell_format4 = workbook.add_format()
#cell_format4.set_bold()
cell_format4.set_align('center')
cell_format4.set_bottom(1)

col0_cell_format4 = workbook.add_format()
#cell_format4.set_bold()
col0_cell_format4.set_align('center')
col0_cell_format4.set_left(1)

col8_cell_format4 = workbook.add_format()
#cell_format4.set_bold()
col8_cell_format4.set_align('center')
col8_cell_format4.set_right(1)

cell_format5 = workbook.add_format()
cell_format5.set_align('left')

col0 = 0
col1 = 1
col2 = 2
col3 = 3
col4 = 4
col5 = 5
col6 = 6
col7 = 7
col8 = 8

# Get rows
for table in tables:
    table_data = defaultdict(list)
    try:
        rows = table.find_all('tr')
    except AttributeError as e:
        print 'No table rows found, exiting'
    
    # Get data
    table_data = parse_rows(rows)


    # Print data
    for game_date in sorted(table_data.iterkeys()):
        col = 0
        (dayofweek,month,dayofmonth,time,ampm) = game_date.split()
        game_time = time + " " + ampm
        game_time = to_pacific_time_zone(game_time)
        (time,ampm) = game_time.split()
        game_time = re.sub(r'\s+','',game_time)
        worksheet.set_column(col0,col0, 4)
        worksheet.set_column(col1,col1, 4)
        worksheet.set_column(col2, col2, 4)
        worksheet.set_column(col3, col3, 3)
        worksheet.set_column(col4, col4, 30)
        worksheet.set_column(col5, col5, 4)
        worksheet.set_column(col6, col6, 8)
        worksheet.set_column(col7, col7, 8)
        worksheet.set_column(col8, col8, 8)
        game_num = 0
        for n_col in range(9):
            worksheet.write_blank(excel_row, col+n_col,'', cell_format1)        
            #worksheet.set_column(col+1, col+1, 30)

        worksheet.write(excel_row+1,   col0,  time)
        for game in table_data[game_date]:
            #worksheet.set_column(col+1, col+1, 30)
            away_odd = game[game_num]['away_odd']
            home_odd = game[game_num]['home_odd']
            if(re.search(r'\d', away_odd)):
               away_odd = float(away_odd)
               
            if(re.search(r'\d',home_odd)):
                home_odd = float(home_odd)
            
            
            worksheet.write(excel_row+1,   col3,  game_num+1,cell_format3)
            worksheet.write(excel_row+1,   col4,  table_data[game_date][game_num]['away_team'],cell_format2)
            worksheet.write(excel_row+1,   col5,  fix_odd(game[game_num]['away_odd']),cell_format5)
            worksheet.write(excel_row+2,   col4,  table_data[game_date][game_num]['home_team'],cell_format2)
            worksheet.write(excel_row+2,   col5,  fix_odd(game[game_num]['home_odd']),cell_format5)
            worksheet.write(excel_row+3,   col4,  'OV',cell_format2)
            worksheet.write(excel_row+4,   col4,  'UN',cell_format4)

            worksheet.write_blank(excel_row+4,   col0,  ''  ,col0_cell_format4)
            worksheet.write_blank(excel_row+4,   col1,  ''  ,cell_format4)
            worksheet.write_blank(excel_row+4,   col2,  ''  ,cell_format4)
            worksheet.write_blank(excel_row+4,   col3,  ''  ,cell_format4)
            worksheet.write_blank(excel_row+4,   col5,  ''  ,cell_format4)
            worksheet.write_blank(excel_row+4,   col6,  ''  ,cell_format4)
            worksheet.write_blank(excel_row+4,   col7,  ''  ,cell_format4)
            worksheet.write_blank(excel_row+4,   col8,  ''  ,col8_cell_format4)
            game_num  += 1
            excel_row += 4
        excel_row += 1
workbook.close()
