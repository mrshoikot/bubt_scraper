from urllib import request
from bs4 import BeautifulSoup
import json, sys, time

def sprint(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.01)

id = 20
data = {}
data['ids'] = []

try:
    while True:
    
        req = request.urlopen('https://www.bubt.edu.bd/department/member_details/'+str(id))
        res = req.read()

        soup = BeautifulSoup(res, 'html.parser')
        isValid = not bool(soup.select('.panel-body>p.no_margin'))

        if isValid:
            data['ids'].append(id)
            sprint(str(id) + ' is valid\n')
        else:
            sprint(str(id) + ' is not valid\n')

        id += 1

except KeyboardInterrupt:

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
