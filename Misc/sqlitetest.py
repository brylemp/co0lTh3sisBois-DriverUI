import sqlite3
Driver_ID = 13

conn = sqlite3.connect('shuttle1.db')

cursor = conn.execute("SELECT Date, Total_Amount from driverSummary where Driver_id = %s" % (Driver_ID))
rowexists = cursor.fetchone()
if rowexists == None:
    print("None")

else:
    cursor = conn.execute("SELECT Date, Total_Amount from driverSummary where Driver_id = %s" % (Driver_ID))
    histrecord = []
    for row in cursor:
        driverquery = {
            'Date':row[0],
            'Total_Amount':row[1]
        }
        histrecord.append(driverquery)

    while (1):
        if len(histrecord)%3 == 0:
            break
        else:
            driverquery = {
                'Date':' ',
                'Total_Amount':0
            }
            histrecord.append(driverquery)
            break
        
    history_page = []
    for x in range(int(len(histrecord)/3)):
        history_page.append(histrecord[x*3:(x*3)+3])

    # print(history_page)



