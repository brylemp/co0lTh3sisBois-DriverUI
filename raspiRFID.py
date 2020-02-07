import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pandas
import csv
import sqlite3
import datetime
import time

#initialization
# GPIO.setwarnings(False)
reader = SimpleMFRC522()
temp_DRIVERID='13'
shuttlePrice='5'
buzzer1=31
def buzzSuccessful():
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer1,GPIO.LOW)
        
def buzzNoBalance():
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        
def buzzNotInDB():
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(buzzer1,GPIO.LOW)
        
        
def checkUID(UID):
        #read sqlite
        data=0
        try:
                conn=sqlite3.connect('shuttle1.db')
                cursor=conn.cursor()
                sqlite_select_query = """SELECT * from accountBalance where UID = ?"""
                cursor.execute(sqlite_select_query, (UID, ))
                print("Reading single row \n")
                record = cursor.fetchone()
                if(record[2]>=25):
                        data=record[1]
                        cursor.close()
                        conn.close()
                        return data
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


def readUID():
        #reading
        while True:
                try:
                        GPIO.setmode(GPIO.BOARD) 
                        GPIO.setup(buzzer1,GPIO.OUT)
                        id, text = reader.read_no_block()
                        print(id)
                        print(text)
                        IDnum=checkUID(id)
                        print(IDnum)
                        if(IDnum!=None):
                                transactionRecord= [(str(id),str(datetime.datetime.now()),str(IDnum),int(shuttlePrice),str(temp_DRIVERID))]
                                inputTransactiontoDB(transactionRecord)
                                buzzSuccessful()
                        else:
                                print('UID not in database')
                                buzzNoBalance()
                finally:
                        GPIO.cleanup()
    
def main():
        while True:
                try:
                        readUID()
                except:
                        print('Shuttle Function Error ... running again ... \n')
                        input("Press Enter to run again...")
                

        
        







