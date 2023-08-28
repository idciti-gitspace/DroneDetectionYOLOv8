from datetime import datetime

now = datetime.now()
td = 0
counter = 0

while True :
    wt = datetime.now()
    td = wt.second - now.second
    if td > 1 :
        now = datetime.now()
        print("counter : " + str(counter))
        counter = counter + 1