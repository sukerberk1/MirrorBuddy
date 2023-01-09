import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def gather_schedule(param):
    # Any exceptions return none, function currently unsafe to use
    try:
        url = f'http://planlekcji.staff.edu.pl/plany/{param}.html'
        # open the website with URL and convert it into dataframe
        html = requests.get(url).content  
        df_list = pd.read_html(html)
        # get needed info from the dataframe
        df_head = df_list[0]
        heading = df_head.at[0, 0]
        df_schedule = df_list[2] 
        # we could return a schedule as a dataframe, but to make it more universal we convert it into 2d list
        list_schedule = df_schedule.values.tolist()
        return heading, list_schedule
    except Exception as e: 
        print(e)
        print("Wystąpił błąd")
        return 0,0


"""Slow-working function returning such list: [(heading, link_character, link_number),(..),(..)]"""
def get_headings():
    chars = ['o','s','n']
    heading_list = [] # define empty space for headings
    for c in chars:
        for n in range(0,100):
            url = f'http://planlekcji.staff.edu.pl/plany/{c}{n}.html'
            html = requests.get(url).content
            df_list = pd.read_html(html)
            try:
                df_head = df_list[0]
                heading = df_head.at[0, 0]
                # append heading, so it can be displayed, but also the link parameters so we can get the schedule later
                info = heading, c , n
                heading_list.append(info)
            except IndexError:
                heading_list.append(None)
    return heading_list


"""Function returns list with heading and link parameter as string: [(heading,'o1'),(..)]"""
def get_headings_fast():
    url = 'http://planlekcji.staff.edu.pl/lista.html'
    html = requests.get(url).content  
    soup = BeautifulSoup(html, features="lxml")
    links = soup.find_all('a')
    # get needed data from links list (it consist of bs4 tag objects)
    data = []
    for link in links:
        # fetching link parameter f.e. 'o2' or 's15' uses primitive handling - string slicing. Error-prone solution !!!
        link_parameter = str(link)[15:18].replace('.','')
        heading = link.get_text()
        # formatting output data
        if heading[0].isnumeric() and not heading[1].isnumeric():
            info = (heading[0]+' '+heading[1:], link_parameter)
        else:
            info = link.get_text(), link_parameter
        data.append(info)
    return data


"""Function reformats the schedule from gather_schedule()"""
def reformat_schedule(plan):
    max_len = 0
    weekdays = ['','Poniedziałek','Wtorek', 'Środa','Czwartek','Piątek']
    schedule_done = []
    for row in plan:
        if len(row) >= max_len:
            max_len = len(row)
    for i in range(1,max_len):
        new_row = []
        for item in plan:
            new_row.append(item[i])
        schedule_done.append(new_row)
    # now insert weekdays at the begining of every column:
    for i in range(len(schedule_done)):
        schedule_done[i].insert(0,weekdays[i])
    return schedule_done


"""Function removes nan values from the plan"""
def validate_schedule(plan):
    validated = []
    for row in plan:
        new_row = []
        for field in row:
            if type(field) != str:
                new_row.append('')
            else: new_row.append(field)
        validated.append(new_row)

    return validated 


"""News functions down here"""
def gather_List(strona):
    list = [[None for x in range(3)] for x in range(12)]
    url = f"https://tm1.edu.pl/page/{strona}"
    page = requests.get(url)
    # print(page.text)
    soup = BeautifulSoup(page.content.decode('utf-8'), "html.parser")
    results = soup.find(id="posts")
    # print(results.prettify())
    elements = results.find_all("a", class_="tile article-tile")
    i = 0
    for element in elements:
        title_element = element.find('h3')
        post_date = element.find(class_="post-date")
        description_element = element.find(class_="post-content")
        # try:
        #     title_element = title_element.strip('<strong>/')
        # except AttributeError:
        #     title_element = "BRAK"
        # try:
        #     description_element = description_element.text.strip('<p>/')
        # except AttributeError:
        #     description_element = "BRAK"
        list[i][0] = cut_special_signs(title_element.get_text())
        list[i][1] = cut_special_signs(post_date.get_text())
        list[i][2] = cut_special_signs(description_element.get_text())
        i += 1
    return list


# to cut backslash signs from news list
def cut_special_signs(string):
    return string.replace('\xa0',' ').replace('\n',' ')


import datetime as dt


"""Function gives list that stores time as [[hour, minute], [hour, minute]] from plan"""
def get_time(time):
    hour_min = []
   
    time = time.replace(" ", "")
    time = time.replace("-", " ")
    time = time.split()
    time = list(time)
    for i in time:
        i = i.replace(":"," ")
        i = i.split()
        i = [int(n) for n in i]
        hour_min.append(i)
    return hour_min

"""Function to compare if the time from plan have place in actuall time"""
def compare_time(hour_min):
    time = dt.datetime.now()
    #h_actuall = int(time.strftime("%H"))
    #min_actuall = int(time.strftime("%M"))
    h_actuall = 11
    min_actuall = 36
    
    print(hour_min)
    print(hour_min[1][1])
    if h_actuall >= hour_min[0][0] and h_actuall <= hour_min[1][0]:
        if (h_actuall == hour_min[1][0] and  min_actuall <= hour_min[1][1]) or (h_actuall == hour_min[0][0] and min_actuall >= hour_min[0][1]):
            return True
        
    else:
        return False




school_hours = [[[8,0],[8,45]],
                [[8,50],[9,35]],
                [[9,40],[10,25]],
                [[10,30],[11,15]],
                [[11,35],[12,20]],
                [[12,40],[13,25]],
                [[13,30],[14,15]],
                [[14,20],[15,5]]]

"""Function to find where is the classroom"""
def find_where_i_have_lesson(class_name):
    data = get_headings_fast()
    for i in range(len(data)):
        if class_name == data[i][0]:
            class_name, schedule = gather_schedule(data[i][1])
            
            date = dt.datetime.now()
            day = int(date.strftime("%w"))
            
            for i in school_hours:
                hour = compare_time(i)
                time = dt.datetime.now()
                h_actuall = int(time.strftime("%H"))
                try:
                    if hour == True:
                        nth_lesson = school_hours.index(i) + 1
                        for i in schedule:
                            if nth_lesson == i[0]:
                                return nth_lesson, i[2:][day]
                    elif i == school_hours[-1]:
                        return 0, "Nie masz lekcji"
                        
                except TypeError:
                    return 0, "Nie masz lekcji"



"""Returns index and schedule for teacher"""
def find_teacher(t):
    names = get_headings_fast()
    for i in names:
        if t.lower() in i[0].lower():
            return i[0], i[1]

    return 0, "Nie ma takiego nauczyciela"
    

"""Returns actuall index of lesson and number of classroom"""
def schedule_of_teacher(name):
    name, index = find_teacher(name)

    if name == 0:
        return "Nie ma takiego nauczyciela"
    
    elif name != 0:
        name, schedule = gather_schedule(index)
        
        index_of_lesson, where = find_where_i_have_lesson(name)
        return index_of_lesson, where
        


def clean_up_string_and_get_num_of_classroom(txt):
    try:
        x = re.findall("\d\d\d",txt)
        num_of_classroom = int(x[0])
        return num_of_classroom
    except IndexError as e:
        print(e)
        return "Nie ma takiej klasy"


