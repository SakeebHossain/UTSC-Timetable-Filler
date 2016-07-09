from bs4 import BeautifulSoup
from Course import *
import traceback

## Setup bs4 object 
try:
    soup = BeautifulSoup(open("Office of the Registrar.html", encoding="utf-8"), "html.parser")
except:
    trackback.print_exc()

## Get anchor tags that contains course names and codes
#A function that finds all anchors containing course names
def target_blank_href(tag):
    counter = 0    
    if tag.has_attr('target') and tag.has_attr('href'):
        if tag['target'] == '_blank':
            if 'http://www.utsc.utoronto.ca/~registrar/calendars/calendar' in tag['href']:
                counter += 1
                if counter == 5:
                    return
                return True
    return False  

courses = soup.find_all(target_blank_href)

## Parse anchor tags to get course name and code, put them in Course object
course_list = []
for course in courses:
    try:
        name = course.find_parent('b').getText().split(' - ')[1]
        link = course['href']
        code = course.getText()
        if code != 'alendar/':
            c = Course()
            c.code = code
            c.link = link
            c.name = name
            course_list.append(c)
    except:
        traceback.print_exc()


## Collect tables containing course session info, put them in Course object
def find_hours(tag):
    if tag.name == 'tr':
        if 'style' in tag.attrs:
            if tag['style'] == "font-size:10px;font-weight:bold":
                return True
    return False

raw_hours = soup.find_all(find_hours)

## Parse tables to get course info
hours = []
i=0
for hour in raw_hours:
    row = hour.next_sibling
    try:
        while row['style'] == 'background-color: rgb(231, 234, 239);':
            m = MeetingSection()
            m.section = row.td.string
            m.day = row.td.next_sibling.string
            m.start = row.td.next_sibling.next_sibling.string
            m.end = row.td.next_sibling.next_sibling.next_sibling.string
            course_list[i].meeting_sections.append(m)
            row = row.next_sibling
        i+=1
    except:
        i+=1

file0 = open('breadth_reqs.txt', 'r')
breadth_file = file0.readlines()
course_info = []
for line in breadth_file:
    c_i = line.strip('\n').split('%')
    course_info.append(c_i)
    
## Create a dictionary that maps day to course
day_to_course_dict = {}
mylist = ['MO', 'TU', 'WE', 'TH', 'FR']
for val in mylist:
    day_to_course_dict[val] = []
    
for course in course_list:
    for session in course.meeting_sections:
        #Pick the day
        if not(session.section == None) and ('TUT' in session.section):
            continue
        elif session.day == 'MO':
            day_to_course_dict['MO'].append(course)
        elif session.day == 'TU':
            day_to_course_dict['TU'].append(course)           
        elif session.day == 'WE':
            day_to_course_dict['WE'].append(course)
        elif session.day == 'TH':
            day_to_course_dict['TH'].append(course)
        elif session.day == 'FR':
            day_to_course_dict['FR'].append(course)
        
    #Add breadth requirement
    for cs_info in course_info:
        if cs_info[0] in course.code:
            course.breadth_req = cs_info[1]
            break


    


def find_courses(days, st, breadth, semester, year):
    """
    days -> list of str
    start -> str
    breadth -> str
    semester -> str
    year -> str
    """
    if days == ['*']:
        days = ['MO', 'TU', 'WE', 'TH', 'FR']
    for day in days:
        for course in day_to_course_dict[day]:
            for meeting_section in course.meeting_sections:
                if meeting_section.start == st or st == '*':
                    if meeting_section.end == ed or ed == '*':
                        if(meeting_section.section == None) or (not('TUT' in meeting_section.section) and not('PRA' in meeting_section.section)):
                            if meeting_section.day == day:
                                if course.code[-1] == semester:
                                    if course.breadth_req in breadth or breadth == '*':
                                        if course.code[3] == year or year == '*':
                                            print(course.code, course.name, meeting_section.section)
    

