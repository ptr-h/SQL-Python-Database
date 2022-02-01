import sqlite3
import random

class DBOperations():

    sql_create_table_first_time = "CREATE TABLE EmployeeUoB (employee_id integer NOT NULL PRIMARY KEY AUTOINCREMENT, title VARCHAR(5) NOT NULL,forename VARCHAR(20) NOT NULL,surname VARCHAR(20) NOT NULL,email VARCHAR(40) NOT NULL UNIQUE,salary REAL NOT NULL)"

    sql_for_show_all_table = "SELECT * FROM sqlite_master WHERE type='table' and name='EmployeeUoB';"
    
    sql_create_table = "CREATE TABLE IF NOT EXISTS EmployeeUoB (employee_id integer NOT NULL PRIMARY KEY AUTOINCREMENT , title VARCHAR(5) NOT NULL, forename VARCHAR(20) NOT NULL, surname VARCHAR(20) NOT NULL, email VARCHAR(40) NOT NULL UNIQUE, salary REAL NOT NULL);"

    sql_insert = "INSERT INTO EmployeeUoB (title,forename,surname,email,salary) VALUES (?,?,?,?,?)"

    sql_select_all = "SELECT * FROM EmployeeUoB"

    sql_search = "SELECT * FROM EmployeeUoB where employee_id = ?"

    sql_update_data = "UPDATE EmployeeUoB SET title=?, forename=?, surname=?, email=?, salary=? WHERE employee_id=?"

    sql_delete_data = "DELETE FROM EmployeeUoB WHERE employee_id = ?"

    sql_drop_table = "DROP TABLE IF EXISTS EmployeeUoB"

    sql_presentation = ".headers on.mode column"

#Initalisation of necessary commands
    def __init__(self):
        try:
            self.conn = sqlite3.connect("EmployeeDB.db")
            self.cur = self.conn.cursor()
            #self.cur.execute(self.sql_create_table_first_time)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

#Establish a connection to the database
    def get_connection(self):
        self.conn = sqlite3.connect("EmployeeDB.db")
        self.cur = self.conn.cursor()


#Create an employee table in the database
    def create_table(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_create_table_first_time)
            self.conn.commit()
            print("Table created successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

#Insert new employees into the database
    def insert_data(self):
        try:
            self.get_connection()

            emp = Employee()
            emp.set_title(str(input("Enter Employee Title: ")))
            emp.set_forename(str(input("Enter Employee Forename: ")))
            emp.set_surname(str(input("Enter Employee Surname: ")))
            emp.set_email(str(input("Enter Employee Email: ")))
            emp.set_salary(float(input("Enter Employee Salary: ")))
            all_data = str(emp).split("\n")
            self.cur.execute(self.sql_insert, tuple(all_data[1:]))
            self.conn.commit()
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

#Neatly output all employees in the database 
    def select_all (self):
            try:
                self.get_connection()
                self.cur.execute(self.sql_select_all)
                results = self.cur.fetchall()
                formatted_row = '{:<5} {:<5} {:<20} {:<20} {:<20} {:<15}'

                
                if len(results)>0:

                  print(formatted_row.format("ID", "Title", "Forename", "Surname", "Email", "Salary (£)"))


                  for row in results:
                      print(formatted_row.format(*row))
                      
                else: 
                  print('No data in table')

            except Exception as e:
                print(e)
            finally:
              self.conn.close()


#Search for an Employee based on Employee ID
    def search_data(self):
        try:
            self.get_connection()
            employee_id = int(input("Enter Employee ID: "))
            self.cur.execute(self.sql_search, tuple(str(employee_id)))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                for index, detail in enumerate(result):
                    if index == 0:
                        print("Employee ID: " + str(detail))
                    elif index == 1:
                        print("Employee Title: " + detail)
                    elif index == 2:
                        print("Employee Name: " + detail)
                    elif index == 3:
                        print("Employee Surname: " + detail)
                    elif index == 4:
                        print("Employee Email: " + detail)
                    else:
                        print("Salary: £" + str(detail))
            else:
                print("No Record")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

#Updating all employee information based on Employee ID 
    def update_data(self):
        try:
            self.get_connection()
            employee_id = (int(input("UPDATE: Employee ID of Employee: ")))
            title = (str(input("Enter Employee Title: ")))
            forename = (str(input("Enter Employee Forename: ")))
            surname = (str(input("Enter Employee Surname: ")))
            email = (str(input("Enter Employee Email: ")))
            salary = str(input("Enter Employee Salary: "))
            
            self.cur.execute(self.sql_update_data,
                             (title, forename, surname, email, salary,
                              employee_id))
            result = self.cur
            self.conn.commit()
            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()


#Deleting an employee from the database based on Employee ID
    def delete_data(self):
        try:
            self.get_connection()
            employee_id = (int(input("DELETE: Employee ID of Employee: ")))
            self.cur.execute(self.sql_delete_data, tuple(str(employee_id)))
            result = self.cur
            self.conn.commit()
            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            

#Extra function of my choice to return an employee at random (Useful for competitions/raffles or involuntary tasks)
    def return_random_emp(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)
            results = self.cur.fetchall()
            formatted_row = '{:<5} {:<5} {:<20} {:<20} {:<20} {:<15}'
            if len(results) > 0:
                print(formatted_row.format("ID", "Title", "Forename", "Surname", "Email", "Salary (£)"))
                print(formatted_row.format(*results[random.randint(0,len(results)-1)]))
 
            else:
                print("No Employees found in the database! ")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

            

#Employee Class used whenever inserting a new employee to the database
class Employee():
    def __init__(self):
        #self.employee_id = 0
        self.title = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def set_title(self, title):
        self.title = title

    def set_forename(self, forename):
        self.forename = forename

    def set_surname(self, surname):
        self.surname = surname

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary

    def __str__(self):
        return "\n" + self.title + "\n" + self.forename + "\n" + self.surname + "\n" + self.email + "\n" + str(
            self.salary)



# Menu of options to choose from
while True:
    print("\n Menu:")
    print("**********")
    print(" 1. Create table EmployeeUoB")
    print(" 2. Insert data into EmployeeUoB")
    print(" 3. Select all data into EmployeeUoB")
    print(" 4. Search an employee")
    print(" 5. Update data some records")
    print(" 6. Delete data some records")
    print(" 7. Pick a random employee")
    print(" 8. Exit\n")

    __choose_menu = input("Enter your choice: ")
    db_ops = DBOperations()
    if __choose_menu == '1':
        db_ops.create_table()
    elif __choose_menu == '2':
        db_ops.insert_data()
    elif __choose_menu == '3':
        db_ops.select_all()
    elif __choose_menu == '4':
        db_ops.search_data()
    elif __choose_menu == '5':
        db_ops.update_data()
    elif __choose_menu == '6':
        db_ops.delete_data()
    elif __choose_menu == '7':
        db_ops.return_random_emp()
    elif __choose_menu == '8':
        exit(0)
    else:
        print("Invalid Choice")