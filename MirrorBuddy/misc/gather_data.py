import pandas as pd
import requests
from bs4 import BeautifulSoup

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
    except:
        return None


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
    soup = BeautifulSoup(html)
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