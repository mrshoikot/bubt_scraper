import sqlite3
from helpers import fetchStudent, create_table

class Importer:
    def __init__(self, sqlitepath):
        self.count = 1
        self.conn = sqlite3.connect(sqlitepath)
        self.c = self.conn.cursor()

        self.fail = 0

        self.keys = (
            'sis_std_id',
            'sis_std_name',
            'sis_std_prgrm_sn',
            'sis_std_intk',
            'sis_std_LocGuardian',
            'sis_std_gender',
            'sis_std_father',
            'sis_std_district',
            'sis_std_Status',
            'sis_std_blood',
            'sis_std_email',
        )
        
    # Check if the student already exists
    def doesExist(self, id):
        try:
            self.c.execute("SELECT id, email FROM students WHERE id = ?", (id,))
        except sqlite3.OperationalError:
            create_table(self.c)
        return self.c.fetchall()

    # Update student email that already exist
    def updateEmail(self, id, email):
        self.c.execute("UPDATE students SET email='"+email+"' WHERE id="+str(id))
        self.conn.commit()

    # Insert new student to database
    def insertStudent(self, data, intake=None):
        values = []

        if intake:
            data['sis_std_intk'] = intake

        # If key doesn't exist fill it with None
        for key in self.keys - data.keys():
            data[key] = None

        for x in self.keys:
            values.append(data[x])
        values = tuple(values)


        print(values)

        self.c.execute('INSERT INTO students (id, name, program, intake, guardian, gender, father, district, status, blood, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
        self.conn.commit()


    def start(self, id, intake=None):

        self.fail = 0

        while self.fail < 5:

            print("Count: "+str(self.count))
            self.count += 1

            response = fetchStudent(id)

            # If the student exist try to update the email or continue
            exists = self.doesExist(id)
            if exists:

                if not response:
                    print("ID not found")
                    self.fail += 1
                    continue


                
                print(str(id) + " Already Exists!")
                
                if 'sis_std_email' in response:
                    print(response['sis_std_email'])
                    
                if response['sis_std_email'] and exists[0][1] != response['sis_std_email']:
                    self.updateEmail(id, response['sis_std_email'])

                id += 1
                continue


            try:
                self.insertStudent(response, intake)
            except Exception as e:
                if response:
                    print(e)
                else:
                    print("ID not found")
                    self.fail += 1
                print(id)
                print(' ')
                id += 1
                continue

            print(' ')

            id += 1

    def close(self):
        self.conn.close()