from urllib import request, parse
import json
import base64
from bs4 import BeautifulSoup
from lxml import html
import PyPDF2
import sys, time


# Slowly print a string
def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.005)



# Decode base64 image and save to storage
def decode_image(data, name):
    imgdata = base64.b64decode(data[23:])
    filename = './photos/'+name+'.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)


# Create students table
def create_table(c):
    c.execute('CREATE TABLE students(id int NOT NULL, name VARCHAR, program VARCHAR, intake int, guardian VARCHAR, gender CHAR, father VARCHAR, district VARCHAR, status CHAR, blood VARCHAR,phone VARCHAR, email VARCHAR, PRIMARY KEY (id))')



# Parse options for dropdown selector
def parseHTML(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find_all('option')

    result = [option.text.strip() for option in result]

    return result[1:]

# Fetch student data from API
def fetchStudent(id):
    data = {'id': id, 'type': 'stdVerify'}
    params = parse.urlencode(data)

    req = request.Request('https://bubt.edu.bd/global_file/getData.php?'+params)
    req.add_header('cookie', 'PHPSESSID=91fb31ccbe3b0a111bd56b9f8a062a6f')
    req = request.urlopen(req)
    return json.load(req)

# Get programs for a semester
def getPrograms(semester):
    data = {'semester': semester}
    params = parse.urlencode(data)
    res = request.urlopen('https://www.bubt.edu.bd/home/get_semester?'+params)
    return parseHTML(res.read())

# Get intakes for a program
def getIntakes(semester, program):

    url = ('https://www.bubt.edu.bd/home/get_program_dir?program_name=./result_files/'+semester+'/'+program).replace(' ', '+')
    res = request.urlopen(url)
    return [parseHTML(res.read())[-1]]

# Get sections for an intake
def getSections(semester, program, intake):
    
    url = ('https://www.bubt.edu.bd/home/get_intake_dir?int='+str(intake)+'&program_name=.%2Fresult_files%2F'+semester+'%2F'+program).replace(' ', '%20')
    res = request.urlopen(url)
    return parseHTML(res.read())

# Get result pdf file
def getResult(semester, program, intake, section):   
    url = ('https://www.bubt.edu.bd/result_files/'+semester+'/'+program+'/int_'+str(intake)+'_sec_'+str(section)+'.pdf').replace(' ', '%20')
    filename = "result.pdf"
    request.urlretrieve (url, filename)
    return filename

# Get first id from result pdf
def getFirstId(result_sheet):
    result = PyPDF2.PdfReader(result_sheet)
    text = result.pages[0].extract_text()
    import re

    search = re.findall("[0-9]{11}", text)

    if search:
        return search[0]
    else:
        return False

