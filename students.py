from Importer import Importer
from helpers import *
import toml
import os


# Read local `config.toml` file.
config = toml.load('config.toml')

# Check if file exist
if not os.path.isfile(config["sqlite_path"]):
    open(config["sqlite_path"], 'w+').close()

importer = Importer(config["sqlite_path"])


for semester in config["semesters"]:

    for program in getPrograms(semester):

        for intake in getIntakes(semester, program):

            if intake:
                
                sections = getSections(semester, program, intake)

                for section in sections:
                    result_sheet = getResult(semester, program, intake, section)

                    print([semester, program, intake, section])

                    firstId = getFirstId('result.pdf')

                    if firstId:
                        importer.start(int(firstId))



importer.close()