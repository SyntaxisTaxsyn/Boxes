# Todo list
# Functions to add

# Checkuser exists - done
# Add User - done
# Delete User
# Login User - done
# Logout User - done

## General

# Add table in boxes db for game data
# Add encode/decode methods for game data
# Add lookup for active users for game matching
# 


import mysql.connector
from datetime import datetime

def GetDBConnection(var):
    
    var = mysql.connector.connect(
    host="localhost",
    user="testuser",
    passwd="password",
    database="BoxesDB"
    )
    return var

# Returns the current time of day as a string formatted correctly for using with
# the MySQL DATETIME variable type
def GetDateTimeNOWasString():
    now = datetime.now()
    rightnow = now.strftime("%Y-%m-%d %H:%M:%S")
    return rightnow

# Query the connected database if the username exists
def CheckUserExists(UserName,DB):
    mycursor = DB.cursor()
    sql = "SELECT name FROM Users WHERE name = %s"
    name = (UserName,)
    mycursor.execute(sql,name)
    myresult = mycursor.fetchone()
    if myresult == None:
        return False
    else:
        return True

# Add a user entry to the database after checking they dont already exist
def AddUsertoDB(Username,Password,DB):
    if CheckUserExists(Username,DB) == False:
        mycursor = DB.cursor()
        sql = ("INSERT INTO Users (name,password,loggedin) VALUES (%s,%s,%s)")
        val = (Username,Password,0)
        mycursor.execute(sql,val)
        DB.commit()
        return True
    else:
        return False

# Log a user in to the database if they exist and the password is correct
def LoginUsertoDB(Username,Password,DB):
    if CheckUserExists(Username,DB) == True:
        mycursor = DB.cursor()
        sql = ("UPDATE Users SET loggedin = %s, lastlogintime = %s WHERE name = %s AND password = %s")
        val = (1,GetDateTimeNOWasString(),Username,Password)
        mycursor.execute(sql,val)
        DB.commit()
        if mycursor.rowcount == 0:
            return False # No user logged, login credentials wrong etc
        if mycursor.rowcount == 1:
            return True # User logged in sucessfully
        if mycursor.rowcount > 1:
            # Other error resulting in more than 1 row being updated
            #(possible duplicate users)
            return False

# Log a user out of the database if they exist
def LogoutUserfromDB(Username,DB):
    if CheckUserExists(Username,DB) == True:
        mycursor = DB.cursor()
        sql = ("UPDATE Users SET loggedin = %s, lastlogouttime = %s WHERE name = %s")
        val = (0,GetDateTimeNOWasString(),Username)
        mycursor.execute(sql,val)
        DB.commit()
        if mycursor.rowcount == 0:
            return False # No matching user name to log out
        if mycursor.rowcount == 1:
            return True # User logged out sucessfully
        if mycursor.rowcount > 1:
            # Other error resulting in more than 1 row being updated
            #(possible duplicate users)
            return False 

    

#mydb = mysql.connector.connect(
#  host="localhost",
#  user="testuser",
#  passwd="password",
#  database="BoxesDB"
#)

mydb = ""
mydb = GetDBConnection(mydb) #Get conection to DB

#mycursor = mydb.cursor()

#sql = "INSERT INTO Users (name,password,loggedin) VALUES (%s,%s,%s)"
#val = ("Paul","password",0)

#mycursor.execute(sql,val)
#mydb.commit()
#print(mycursor.rowcount, "record inserted.")


print(GetDateTimeNOWasString())
if CheckUserExists("Pal",mydb):
    print("TRUE")
else:
    print("FALSE")

if AddUsertoDB("Amy","amy280211",mydb):
    print("User added sucessfully")
else:
    print("User already exists")

if LoginUsertoDB("Amy","amy280211",mydb):
    print("User logged in sucessfully")
else:
    print("User not logged in")

if LogoutUserfromDB("Amys",mydb):
    print("User logged out sucessfully")
else:
    print("User not logged out")
