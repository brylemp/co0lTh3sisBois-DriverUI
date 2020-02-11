import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
import pandas
import csv
import sqlite3
import datetime
import time

#initialization
GPIO.setwarnings(False)
# reader = SimpleMFRC522()
# temp_DRIVERID='13'
# shuttlePrice='5'
# buzzer=31
def buzzSuccessful(buzzer):
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        
def buzzNoBalance():
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        
def buzzNotInDB():
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer,GPIO.LOW)
        
        
def checkUID(UID):
        #read sqlite
        data=None
        try:
                conn=sqlite3.connect('shuttle1.db')
                cursor=conn.cursor()
                sqlite_select_query = """SELECT * from accountBalance where UID = ?"""
                cursor.execute(sqlite_select_query, (UID, ))
                print("Reading single row \n")
                record = cursor.fetchone()
                print(record)
                if(record!=None):
                        data=[record[1],0]
                        if(record[2]>=25):
                                data=[record[1],1]
                                cursor.close()
                                conn.close()
                        return data
                else:
                        return None
                cursor.close()
                conn.close()
        except sqlite3.Error as error:
                print("Failed to read single row from sqlite table", error)
        # finally:
                # cursor.close()
                # conn.close()
                

def inputTransactiontoDB(transactionRecord):
        #Writing CSV to SQLITE
        conn=sqlite3.connect('shuttle1.db')
        cursor=conn.cursor()

        sqlite_insert_query = """INSERT INTO transactions(uid,Date_Time,Passenger_ID,Amount,Driver_ID)
                                VALUES (?, ?, ?, ?, ?);"""

        cursor.executemany(sqlite_insert_query, transactionRecord)
        conn.commit()
        cursor.close()
        conn.close()
        print(transactionRecord)
        print('Added to transactionDB')


# def readUID():
#         #reading
#         while True:
#                 try:
#                         GPIO.setmode(GPIO.BOARD) 
#                         GPIO.setup(buzzer,GPIO.OUT)
#                         id, text = reader.read()
#                         print(id)
#                         print(text)
#                         IDnum=checkUID(id)
#                         print(IDnum)
#                         if(IDnum!=None):
#                                 if(IDnum[1]==1):
#                                         transactionRecord= [(str(id),str(datetime.datetime.now()),str(IDnum[0]),int(shuttlePrice),str(temp_DRIVERID))]
#                                         inputTransactiontoDB(transactionRecord)
#                                         buzzSuccessful()
#                                 else:
#                                         buzzNoBalance()
#                         else:
#                                 print('UID not in database')
#                                 buzzNotInDB()
#                 finally:
#                         GPIO.cleanup()
    

# if __name__ == "__main__":
        # while True:
                # try:
                        # readUID()
                # except:
                        # print('Shuttle Function Error ... running again ... \n')
                        # input("Press Enter to run again...")
                

        
        







