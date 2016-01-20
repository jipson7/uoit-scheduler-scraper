from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime, date
from urllib import request
from sqlalchemy.orm import sessionmaker
from model import Course, Day, session

main_url = 'http://ssbp.mycampus.ca/prod/bwckschd.p_disp_dyn_sched?TRM=U'

def main(semester):
    class_options = []
    session.query(Course).filter_by(semester=semester).delete()
    driver = webdriver.Firefox()
    driver.get(main_url)
    driver.find_element_by_css_selector("option[value='" + semester + "']").click()
    driver.find_element_by_css_selector("input[value='Submit']").click()
    year_url = driver.current_url
    class_select = driver.find_element_by_id('subj_id')
    options_tags = class_select.find_elements_by_tag_name('option')
    for opt in options_tags:
        opt.click()
    driver.find_element_by_css_selector("input[value='Class Search']").click()
    raw_html = driver.page_source
    driver.quit()
    extract_data(raw_html, semester)

def extract_data(source, semester):
    soup = bs(source)
    headers = soup.find_all('th', {'class': 'ddheader', 'scope': 'col'})
    seat_tables = soup.find_all('table', {'summary': 'This layout table is used to present the seating numbers.'})
    data_tables = soup.find_all('table', {'summary': 'This table lists the scheduled meeting times and assigned instructors for this class.'})
    if len(headers) != len(seat_tables) or len(seat_tables) != len(data_tables):
        raise Exception('Length of datasets are offset, cant be parsed without error')
    x = len(headers)
    for i in range(x):
        course = Course()
        header_data = [x.strip() for x in headers[i].getText().split('-')]
        course.name = '-'.join(header_data[:-3])
        course_code = header_data[-2].split()
        course.department = course_code[0]
        course.code = course_code[1]
        course.section = header_data[-1]
        course.semester = semester

        seat_table = seat_tables[i]
        seat_cells = seat_table.find_all('td', {'class': 'dbdefault'})
        course.capacity_total = seat_cells[0].getText()
        course.capacity_taken = seat_cells[1].getText()
        course.capacity_remaining = seat_cells[2].getText()

        session.add(course)
        session.commit()

        course_id = course.id
        data_table = data_tables[i]
        data_rows = data_table.find_all('tr')[1:]
        for row in data_rows:
            day = Day()
            day.course_id = course_id
            cells = [x.getText() for x in row.find_all('td')]
            day.class_type = cells[1]
            try:
                time = cells[2].split('-')
                day.start_time = convertToTime(time[0].strip())
                day.end_time = convertToTime(time[1].strip())
            except Exception as e:
                day.start_time = None
                day.end_time = None
            day.day = cells[3]
            day.location = cells[4]
            try:
                date_cell = cells[5].split('-')
                day.start_date = convertToDate(date_cell[0].strip())
                day.end_date = convertToDate(date_cell[1].strip())
            except Exception as e:
                day.start_date = None
                day.end_Date = None
            day.section_type = cells[6]
            day.instructors = cells[7]
            session.add(day)
        session.commit()

def convertToTime(s):
    return datetime.strptime(s, '%I:%M %p').time()

def convertToDate(s):
    return datetime.strptime(s, '%b %d, %Y').date()

def getCurrentSemesterValue():
    t = date.today()
    if t.month < 5: m = '01'
    elif t.month < 9: m = '05'
    else: m = '09'
    return str(t.year) + m


if __name__ == '__main__':
    import sys
    try:
        semester = sys.argv[1]
    except IndexError:
        print('Must provide the first month of the request semester in the form YYYYMM')
        print('ex.  201601, 201505, 201409, etc')
        sys.exit()
    main(semester)

