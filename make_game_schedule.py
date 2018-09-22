from collections import defaultdict
from bs4 import BeautifulSoup
import urllib
import re
import xlsxwriter


#league = 'ncaaf'
league = 'nfl'

if league == 'nfl':
   url = 'http://www.donbest.com/nfl/odds/'
else:
   url = 'http://www.donbest.com/ncaaf/odds/'
   #url = 'http://www.donbest.com/ncaaf/odds/20180913.html'
    
# Make soup
try:
    #resp = urllib.urlopen("http://www.donbest.com/nfl/odds/")
    resp = urllib.urlopen(url)
except URLError as e:
    print 'An error occured fetching %s \n %s' % (url, e.reason)   

soup = BeautifulSoup(resp.read(),features="html.parser")

# Get table
try:
    tables = soup.find_all('table')
except AttributeError as e:
    print 'No tables found, exiting'


#----------------------------------------------------------------------
def mysortbytime(elem,other):
#----------------------------------------------------------------------
    """taking elem as datetime as (dayofweek,month,dayofmonth,time,ampm) = elem.split() """
    (e_dayofweek,e_month,e_dayofmonth,e_time,e_ampm) = elem.split()
    (o_dayofweek,o_month,o_dayofmonth,o_time,o_ampm) = other.split()
    e_civilian_time = e_time + " " + e_ampm
    o_civilian_time = o_time + " " + o_ampm
    (e_hour,e_min) = to_military_time(e_civilian_time).split(':')
    (o_hour,o_min) = to_military_time(o_civilian_time).split(':')
    if int(e_hour) == int(o_hour):
        return int(e_min) - int(o_min)
    return int(e_hour) -  int(o_hour)

#----------------------------------------------------------------------
def to_military_time(civilian_time):
#----------------------------------------------------------------------
    (time,ampm) = civilian_time.split()
    (hour,min) = time.split(':')
    hour = int(hour)
    if re.findall(r'PM',civilian_time) and hour < 12:
       hour += 12 
    return str(hour) + ":" + min 

#----------------------------------------------------------------------
def fix_odd(game_odd):
#----------------------------------------------------------------------
    """ fix odd """
    if re.search(r'\d',game_odd):
        return float(game_odd)
    return game_odd 

#----------------------------------------------------------------------
def to_pacific_time_zone(game_time):
#----------------------------------------------------------------------
    """ convert estern time to pacific time zone """
    (time,ampm) = game_time.split()
    (hour,min) = time.split(':')
    hour = int(hour)
    print game_time
    if re.search(r'PM', game_time):
       print "hour = ", hour
       hour += 12

    hour -= 3
    if hour < 12:
        ampm = "AM"
    elif hour == 12:
        ampm = "PM"
    else:
        hour -= 12
        ampm = "PM"
    return str(hour)+":"+min+" "+ampm            

#----------------------------------------------------------------------
def fix_team_name(team_name,league='nfl'):
#----------------------------------------------------------------------
    if(league == 'nfl'):
        if re.match("new york", team_name.lower()):
            return re.sub(r'NEW YORK','NY',team_name.upper())
        elif re.match("los angeles", team_name.lower()):
            return re.sub(r'LOS ANGELES','LA',team_name.upper())
        else:
            return re.sub(r'\s+\w+$','',team_name.upper())
    else :    
        #return re.sub(r'\s+\w+$','',team_name.upper())
        return team_name.upper()

#----------------------------------------------------------------------
def parse_rows(rows,league='nfl'):
#----------------------------------------------------------------------
    """ Get data from rows """
    results = defaultdict(list)
    row_num = 0
    excel_row = 0
    game_type = ''
    for row in rows:
        if row_num == 0:
            h3_data = row.find('h3')
            if h3_data:
                print (h3_data.get_text())
                if re.findall(r'FCS', h3_data.get_text()) or re.findall(r'EXTRA', h3_data.get_text()):
                   (title,date,junk0,junk1) = h3_data.get_text().split('-')
                else:
                   (title,date) = h3_data.get_text().split('-')
                    
        if row_num > 1:
            table_headers = row.find('h3')
            if table_headers:
                print ("//////",table_headers.get_text())
                if re.findall(r'[-]',table_headers.get_text()):
                   print ("//////",table_headers.get_text())
                   game_type = table_headers.get_text()

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
                        #if re.match("new york", span_tags[0].get_text().lower()):
                        #    away_team = re.sub(r'NEW YORK','NY',span_tags[0].get_text().upper())
                        #else:
                        #    away_team = re.sub(r'\s+\w+$','',span_tags[0].get_text().upper())
                        #if re.match("new york", span_tags[1].get_text().lower()):
                        #    home_team = re.sub(r'NEW YORK','NY',span_tags[1].get_text().upper())
                        #else:
                        #    home_team = re.sub(r'\s+\w+$','',span_tags[1].get_text().upper())
                        away_team = fix_team_name(span_tags[0].get_text().lower(), league)
                        home_team = fix_team_name(span_tags[1].get_text().lower(), league)
 
                    if col_num > 2: 
                        time_tag  = data.find('div',id=re.compile("_Div_Time_\d+_"))
                        away_line_tags  = data.find_all('div',id=re.compile("_Div_Line_\d+_.*?_" + away_rot + ".*?37"))
                        home_line_tags  = data.find_all('div',id=re.compile("_Div_Line_\d+_.*?_" + home_rot + ".*?37"))
                        line_tags  = data.find_all('div',id=re.compile("_Div_Line_\d+_" + ".*?37"))
                        class_tags  = data.find_all('div',id=re.compile("_Div_Line_\d+_.*?37"))
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
                print ("game_type = ",game_type)
                game_date = re.sub(r'^\s+','',date) + ' ' + game_time
                results[game_date].append( {'game_type':game_type,'game_id' : away_rot + '-' + home_rot,'title':title,'away_team' : away_team,'home_team' : home_team, 'away_odd' : away_odd, 'home_odd' : home_odd})
        row_num += 1;         
    return results

def output_header(worksheet,workbook,row_num=0,text=''):
    col0 = 0
    col1 = 1
    col2 = 2
    col3 = 3
    col4 = 4
    col5 = 5
    col6 = 6
    col7 = 7
    col8 = 8
    col9 = 9


    cell_format1 = workbook.add_format();
    color_red_code  = hex(218)
    color_green_code= hex(238)
    color_blue_code = hex(243)
    bg_color        = '#' + color_red_code + color_green_code + color_blue_code
    bg_color        = re.sub(r'0x', '', bg_color)
    cell_format1.set_bg_color(bg_color)
    cell_format1.set_bottom(2)
    cell_format1.set_top(1)
    cell_format1.set_align('center')
    cell_format1.set_font_size(14)


    col0_cell_format1    = workbook.add_format()       # Set properties later.
    col0_cell_format1.set_bg_color(bg_color)
    #cell_format1.set_bold()
    col0_cell_format1.set_bottom(2)
    col0_cell_format1.set_top(1)
    col0_cell_format1.set_left(1)

    col8_cell_format1    = workbook.add_format()       # Set properties later.
    col8_cell_format1.set_bg_color(bg_color)
    #cell_format1.set_bold()
    col8_cell_format1.set_bottom(2)
    col8_cell_format1.set_top(1)
    col8_cell_format1.set_right(1)
   
    worksheet.write_blank(row_num, col0,'', col0_cell_format1)        

    for n_col in range(1,9):
        worksheet.write_blank(row_num, col0+n_col,'', cell_format1)        
    worksheet.write(row_num, col4,text, cell_format1)        
    worksheet.write_blank(row_num, col9,'', col8_cell_format1)        
 
def output_row(worksheet,workbook,cell_format_bottom=1,row_num=0,game_num=None,time=None,text=''):
    col0 = 0
    col1 = 1
    col2 = 2
    col3 = 3
    col4 = 4
    col5 = 5
    col6 = 6
    col7 = 7
    col8 = 8
    col9 = 9
    cell_format2 = workbook.add_format()
    #cell_format2.set_bold()
    cell_format2.set_align('center')
    cell_format2.set_bottom(cell_format_bottom)
    cell_format2.set_top(1)
    cell_format2.set_right(1)
    cell_format2.set_left(1)
    cell_format2.set_font_size(14)

    cell_format3 = workbook.add_format()
    cell_format3.set_align('center')
    cell_format3.set_font_color('#'+re.sub(r'0x','',hex(196))+re.sub(r'0x','',hex(215))+re.sub(r'0x','',hex(155)))


    cell_format5 = workbook.add_format()
    cell_format5.set_align('left')
    cell_format5.set_top(1)
    cell_format5.set_bottom(cell_format_bottom)
    cell_format5.set_right(1)
    cell_format5.set_left(1)
    cell_format4 = workbook.add_format()


    if game_num > 0:
        worksheet.write_blank(row_num,   col0,'',cell_format5)
    else:
        worksheet.write(row_num,   col0,  time,cell_format5)

    worksheet.write_blank(row_num,   col1,  '',cell_format5)
    worksheet.write_blank(row_num,   col2,  '',cell_format5)
    if game_num != None:
       worksheet.write      (row_num,   col3,  game_num+1,cell_format3)
    else:    
       worksheet.write_blank(row_num,   col3,  '',cell_format5)
    worksheet.write      (row_num,   col4, text,cell_format2)
    #worksheet.write(excel_row+1,   col5,  fix_odd(table_data[game_datetime][game_num]['away_odd']),cell_format5)
    worksheet.write_blank(row_num,   col5,  '',cell_format5)
    worksheet.write_blank(row_num,   col6,  '',cell_format5)
    worksheet.write      (row_num,   col7,  '',cell_format5)
    worksheet.write      (row_num,   col8,  '',cell_format5)
    worksheet.write_blank(row_num,   col9,  ''  ,cell_format5)

      
def init_column_excel(worksheet):
    col0 = 0
    col1 = 1
    col2 = 2
    col3 = 3
    col4 = 4
    col5 = 5
    col6 = 6
    col7 = 7
    col8 = 8
    col9 = 9

    worksheet.set_column(col0,col0, 4)
    worksheet.set_column(col1,col1, 4)
    worksheet.set_column(col2, col2, 4)
    worksheet.set_column(col3, col3, 3)
    worksheet.set_column(col4, col4, 30)
    worksheet.set_column(col5, col5, 4)
    worksheet.set_column(col6, col6, 8)
    worksheet.set_column(col7, col7, 8)
    worksheet.set_column(col8, col8, 8)
    worksheet.set_column(col9, col9, 8)
     
def output_gameschedule():
    # Create a workbook and add a worksheet
    workbook = xlsxwriter.Workbook('game_schedule.xlsx')
    worksheet = workbook.add_worksheet()

    excel_row = 0

    init_column_excel(worksheet)
    # Get rows
    for table in tables:
        table_data = defaultdict(list)
        try:
            rows = table.find_all('tr')
        except AttributeError as e:
            print 'No table rows found, exiting'
        
        # Get data
        table_data = parse_rows(rows,league)

        # Print data
        for game_datetime in sorted(table_data, cmp=mysortbytime):
            print game_datetime
            (dayofweek,month,dayofmonth,time,ampm) = game_datetime.split()
            game_time = time + " " + ampm
            game_time = to_pacific_time_zone(game_time)
            (time,ampm) = game_time.split()
            game_time = re.sub(r'\s+','',game_time)
            dayofweek = re.sub(r'\W','',dayofweek)
            game_num = 0

           
            output_header(worksheet, workbook,excel_row, dayofweek.upper())

            for game in table_data[game_datetime]:
                print "output ====> game_type = ",table_data[game_datetime][game_num]['game_type']
                if re.findall(r'EXTRA GAMES', table_data[game_datetime][game_num]['game_type']):
                    continue
                if re.findall(r'FCS', table_data[game_datetime][game_num]['game_type']):
                    continue
                               
                output_row(worksheet, workbook,1, excel_row+1, game_num,time,table_data[game_datetime][game_num]['away_team'])
                output_row(worksheet, workbook,1, excel_row+2, None,None,table_data[game_datetime][game_num]['home_team'])
                output_row(worksheet, workbook,1, excel_row+3, None,None,'OV')
                output_row(worksheet, workbook,2, excel_row+4, None,None,'UN')

                game_num  += 1
                excel_row += 4
            excel_row += 1
    workbook.close()

def main():
    output_gameschedule()

if __name__ == '__main__':
    main() 