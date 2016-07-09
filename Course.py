class Course:
    def __init__(self):
        self.code = "Undefined!"
        self.name = "Undefined!"
        self.campus = "UTSC"
        self.link = "#"
        self.room = 'Undefined!'
        self.breadth_req = 'Undefined!'
        self.meeting_sections = []

        
class MeetingSection:
    def __init__(self):
        self.section = "Undefined!"
        self.day = "Undefined!"
        self.start = "Undefined!"
        self.end = "Undefined!"

def print_course(course):
    print(course.code, course.name)
    for session in course.meeting_sections:
        print(session.section, session.day, session.start, session.end)
        print('----------------------')

def write_to_file(course_list):
    # Write out everything except the meeting sections
    file = open('directory.txt', 'w')
    for course in course_list:
        file.write(course.code + '%' + course.breadth_req + '\n')
        file.write('--\n')
        for meeting in course.meeting_sections:
            file.write(str(meeting.day)  + '$' + str(meeting.start) + '\n')
        file.write('----\n')
    file.close()
            
def write_file_to_json(course_list):
    file = open("directory.json", "w")
    file_contents = ""
    file_contents += "{'UTSC_COURSES': ["
    for course in course_list:
        file_contents += "{"
        file_contents += "'code': '" + str(course.code) + "',"
        file_contents += "'breadth_req': '" + str(course.breadth_req) + "',"
        file_contents += "'meeting_sections': ["
        
        for meeting in course.meeting_sections:
            file_contents += "{"
            file_contents += "'day': '" + str(meeting.day) + "',"
            file_contents += "'start': '" + str(meeting.start) + "'"
            if meeting == course.meeting_sections[-1]:
                file_contents += "}]"
            else:
                file_contents += "},"
        
        file_contents += "},"
    # Remove the last comma
    print(file_contents[-1])
    file_contents = file_contents[:-1]
    file_contents += "]}"
    file.write(file_contents)
    
        
