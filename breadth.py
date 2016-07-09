#!/usr/bin/python
from bs4 import BeautifulSoup
from Course import *
import traceback
import re

## Setup bs4 object 
try:
    soup = BeautifulSoup(open("UTSC Calendar 2016-2017.html", encoding="utf-8"), "html.parser")
except:
    trackback.print_exc()

"""
Overall goal: find all courses on page and all of their breadth requirements
"""
def find_course_anchors(tag):
    if tag.name == 'a':
        if tag.has_attr('name'):
            if re.match('[A-Z][A-Z][A-Z][A-Z][0-9][0-9][H][3]', tag['name']):
                #print(tag['name'])
                return True 
        return False
    
all_anchors = soup.findAll(find_course_anchors)
a_course_list = []
# Collect Breadth requirements for each course
for anchor in all_anchors:
    a_course = Course()
    a_course.code = anchor['name']
    str_version = str(anchor)
    try:
        while str_version.find('Breadth') == -1:
            anchor = anchor.next_sibling
            str_version = str(anchor)
        # Find first instance of 'Breadth Requirement'
        index_of_breadth = str_version.find('Breadth')
        first_letter_of_br = str_version[index_of_breadth+22]
        if first_letter_of_br == 'A':
            a_course.breadth_req = 'Arts, Literature, and Language'
        elif first_letter_of_br == 'H':
            a_course.breadth_req = 'History, Philosophy, and Cultural Studies'   
        elif first_letter_of_br == 'S':
            a_course.breadth_req = 'Social and Behavioural Sciences'
        elif first_letter_of_br == 'N':
            a_course.breadth_req = 'Natural Sciences'
        elif first_letter_of_br == 'Q':
            a_course.breadth_req = 'Quantitative Reasoning'
        else:
            print('NOPE: it was', str_version[index_of_breadth-15:index_of_breadth+15])
    except:
        a_course.breadth_req = 'N/A'    
    a_course_list.append(a_course)

def write_breadth_to_file(a_course_list):
    file = open('A_courses.txt', 'w')
    for course in a_course_list:
        file.write(course.code + '%' + course.breadth_req + '\n')
    print('Done')
    
    