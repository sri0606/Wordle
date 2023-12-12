import mysql.connector
import csv
from io import StringIO
import hashlib
from cryptography.fernet import Fernet
from math import pow
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['feedback', 'scoreboard','users']
        
        reversible_key = os.environ.get("REVERSIBLE_ENCRYPT_KEY")
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : reversible_key}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):

        #Internal function to handle dates and convert the string dates to datetime objects when necessary
        def handle_dates(param):
            dates = param[-2:]
            start_date = datetime.strptime(dates[0], '%Y-%m-%d')

            if dates[1] is None or dates[1] == "NULL":
                end_date = None
            else:
                end_date = datetime.strptime(dates[1], '%Y-%m-%d')
            param_edited = param[:-2]+[start_date, end_date]
            return param_edited

        # Construct the INSERT query dynamically
        query = f"INSERT IGNORE INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])})"

        for param in parameters:
            if param:
                #convert the keys from strings to integers
                param = self.convert_id_to_integers(param)
                #primary id's are ignored as they are auto-incremented
                val = tuple(param)
                # Execute the INSERT query with parameters as a list
                self.query(query,val)
        
        return 

    def convert_id_to_integers(self,string_list):
        '''
        Converts a list (data row from csv) of strings to integers if valid
        '''
        result = []
        for s in string_list:
            try:
                s = s.strip()  # Remove leading and trailing spaces
                s = s.strip('"')  # Remove double quotes if they exist
                integer_value = int(s.strip())
                result.append(integer_value)
            except ValueError:
                # If the conversion fails, keep it as string
                result.append(s)
        return result
    
    def addFeedbackData(self,feedback_data):
        feedback_data=feedback_data.to_dict(flat=True)
        insert_query = f"INSERT INTO feedback (name,email,comment) VALUES (%s, %s, %s)"
        parameters = (feedback_data["name"],feedback_data["email"],feedback_data["comment"])
        self.query(insert_query,parameters=parameters)
        return
    
    def getFeedbackData(self):
        
        feedback_data = {}
        # Fetch data from the institutions table
        feedbacks_list = self.query("SELECT * FROM feedback")

        print(feedbacks_list)
        for feedback in feedbacks_list:
            feedback_data[feedback["comment_id"]] = {
                "name": feedback["name"],
                "email": feedback["email"],
                "comment": feedback["comment"]
            }
        return feedback_data

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='guest'):
        # Check email already exists
        existing_user = self.query("SELECT * FROM users WHERE email=%s",(email,))

        if existing_user:
           #email already exists
            return {'success': 0, 'message': 'User with this email already exists.'}
        else:
            encrypted_password = self.onewayEncrypt(password)
            
            # Insert the new user into the user table
            self.query("INSERT INTO users (role,email, password) VALUES (%s, %s, %s)",
                       (role,email, encrypted_password,))

            return {'success': 1, 'message': 'User created successfully.'}

    def authenticate(self, email='me@email.com', password='password'):
        # Retrieve user information
        user = self.query("SELECT * FROM users WHERE email=%s", (email,))

        if user:
            # User with the given email exists, now check the password
            stored_password = user[0]['password']

            # Apply the same one-way encryption to the provided password
            encrypted_password = self.onewayEncrypt(password)

            # Check if the encrypted password matches the stored password
            if encrypted_password == stored_password:
                # Authentication successful
                return {'success': 1, 'message': 'Authentication successful.'}
            else:
                # Incorrect password
                return {'success': 0, 'message': 'Authentication failed. Incorrect password.'}
        else:
            # User does not exist
            return {'success': 0, 'message': 'Authentication failed. User not found.'}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message

    def check_user_is_owner(self,email):

        user = self.query("SELECT * FROM users WHERE email=%s",(email,))

        if user[0]["role"]=="owner":
            return True
        
        return False

    def get_top_five(self):
        """
        Get top five users to finish wordle quickly
        """
        query = """
            SELECT email, COALESCE(time_taken, 999999) AS time_taken
            FROM scoreboard
            ORDER BY time_taken ASC
            LIMIT 5;
        """
        top_five = self.query(query)
        for entry in top_five:
            if entry['time_taken']=="999999":
                entry['time_taken']="None"
            entry['time_taken'] = str(entry['time_taken'])

        return top_five
    
    def update_time_taken(self, current_user_email,time_elapsed):
        """
        Update users time taken to finish game
        """
        if time_elapsed==0:
            time_elapsed=1
         # Create a timedelta object
        time_delta = timedelta(seconds=time_elapsed)

        # Extract hours, minutes, and seconds from timedelta
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_datetime = f"{hours}:{minutes}:{seconds}"

        # Check email already exists
        existing_user = self.query("SELECT * FROM scoreboard WHERE email=%s",(current_user_email,))

        if existing_user:
           #email already exists
           query = "UPDATE scoreboard SET time_taken=%s WHERE email=%s"
        else:
            query = "INSERT INTO scoreboard (time_taken, email) VALUES (%s,%s)"
        parameters = (formatted_datetime,current_user_email,)

        self.query(query, parameters)

        return