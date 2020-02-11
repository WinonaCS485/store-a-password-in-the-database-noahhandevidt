import pymysql.cursors
import hashlib, uuid

# Connect to the database
connection = pymysql.connect(host='mrbartucz.com',
                             user='xw5214bs',
                             password='HarrisonSmith22',
                             db='xw5214bs_Login',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

usernameInput = input("Enter the username: ")
passwordInput = input("Enter the password: ")

salt = uuid.uuid4().hex 
print ("password + salt is: " + passwordInput + str(salt))


hashedPassword = hashlib.sha512((passwordInput + salt).encode('utf-8')).hexdigest()
print ("the hashed password is: ", hashedPassword)

passwordInput2 = input("Re-enter the password: ")

try:
    with connection.cursor() as cursor:
        # Insert values to User table
        sql = "INSERT INTO `User` (`Username`, `HashedPassword`, `Salt`) VALUES (%s, %s, %s);"
        to_sql = (usernameInput, hashedPassword, salt)
        
        # execute the SQL command
        cursor.execute(sql, to_sql)
        
        # get the results
        for result in cursor:
            print (result)
      
        # If you INSERT, UPDATE or CREATE, the connection is not autocommit by default.
        # So you must commit to save your changes. 
        connection.commit()
        
        
        
        # Get Salt for Username for checking password
        sql = "SELECT Salt FROM User WHERE Username LIKE %s"
        
        # execute the SQL command
        cursor.execute(sql, usernameInput)
        
        # get the results
        for result in cursor:
            returnSalt = result['Salt']
      
        # If you INSERT, UPDATE or CREATE, the connection is not autocommit by default.
        # So you must commit to save your changes. 
        # connection.commit()
        
        
        
        hashedPassword2 = hashlib.sha512((passwordInput2 + salt).encode('utf-8')).hexdigest()
        
        # Compare hashed re-entered password + salt to hashed password + salt
        sql = "SELECT HashedPassword FROM `User` WHERE Username LIKE %s;"
        
        # execute the SQL command
        cursor.execute(sql, usernameInput)
        
        # get the results
        for result in cursor:
            returnPassword = result['HashedPassword']
        
      
        # If you INSERT, UPDATE or CREATE, the connection is not autocommit by default.
        # So you must commit to save your changes. 
        # connection.commit()
        
        #tell user if correct password was entered
        if hashedPassword2 == returnPassword:
            print("Correct password")
        
        else:
            print("Incorrect password")
        
finally:
    connection.close()