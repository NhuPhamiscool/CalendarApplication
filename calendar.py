#!/usr/bin/python3

import sys
import os
import time
import datetime


path = "/tmp/cald_pipe"
def run():
    if os.path.exists(path):
        fifo = open(path, "w")
        try:
            i = 1
            while i < len(sys.argv):
                if i >=3 and " " in sys.argv[i]:
                    fifo.write('"'+sys.argv[i]+'"'+" ")
                else:
                    fifo.write(sys.argv[i]+" ")
                i+=1

        except OSError:
            print ("pipe has been closed")
        fifo.close()            
    else:
        print("pipe doesn't exist",file = sys.stderr)


if __name__ == '__main__':

    def date_check(date):
        if len(date) != 10:
            print("Unable to parse date", file = sys.stderr)
            return True
        try:
            day,mon,year = date.split('-')
            datetime.datetime(int(year),int(mon),int(day))

        except ValueError:
            print("Unable to parse date", file = sys.stderr)
            return True

        return False


    def output(calendardata):
        output=[]
        # start after the date argument
        i = 3
        with open(calendardata,"r") as get_date:
            while i < len(sys.argv):
                if sys.argv[2] == "NAME":
                    for line in get_date:
                        line_splitted = line.strip("\n").split(",")
                        if line_splitted[1].startswith(sys.argv[i]):
                            output.append(line)

                    i+= 1
                    get_date.seek(0)

                # when sys.argv[2] == "DATE"
                else: 
                    for line in get_date:
                        linebroken = line.split(",")
                        
                        if sys.argv[i] == linebroken[0]:
                            output.append(line)

                    i+= 1
                    get_date.seek(0)

        return output


    def display(result):
        for line in result:
            splitted = line.strip("\n").split(",")
            # without description
            if len(splitted) == 2:
                print(splitted[0]+" "+":"+" "+splitted[1])
            # with description
            else:
                print(splitted[0]+" "+":"+" "+splitted[1]+" "+":"+" "+splitted[2])


    cmls = ["DEL","ADD","UPD"]
    # interacting with daemon 
    if sys.argv[1] in cmls:
        run()

    # not interacting with daemon
    else:
        calendardata = ""
        with open("/tmp/calendar_link","r") as path_db:
            for line in path_db:
                calendardata = line
        
        if calendardata == "":
            print("Unable to process calendar database", file = sys.stderr)
            sys.exit()

        if sys.argv[1] == "GET" and sys.argv[2] == "DATE":
            # missing date args
            if len(sys.argv) <= 3:
                print("Unable to parse date", file = sys.stderr)
                sys.exit()

            # checking all date args
            i = 3
            while i < len(sys.argv):
                datecheckin = date_check(sys.argv[i])
                if datecheckin == True:
                    sys.exit()
                i+=1

            result = output(calendardata)
            display(result)

        elif sys.argv[1] == "GET" and sys.argv[2] == "NAME":
            # missing args
            if len(sys.argv) <= 3:
                print("Please specify an argument", file = sys.stderr)
                sys.exit()

            result = output(calendardata)
            display(result)

        elif sys.argv[1] == "GET" and sys.argv[2] == "INTERVAL":
            i = 3
            while i < len(sys.argv):
                datecheckin = date_check(sys.argv[i])
                if datecheckin == True:
                    sys.exit()
                i+=1
            
            day1,mon1,year1 = sys.argv[3].split('-')
            start_date = datetime.datetime(int(year1),int(mon1),int(day1))

            day2,mon2,year2 = sys.argv[4].split('-')
            end_date = datetime.datetime(int(year2),int(mon2),int(day2))
            
            if start_date > end_date:
                print("Unable to Process, Start date is after End date", file = sys.stderr)
                sys.exit()

            start=0
            end=0
            f = open(calendardata,"r")
            dataa = f.readlines()
            
            for i in dataa:
                databroken1 = i.split(",")
                if sys.argv[3] == databroken1[0]:
                    # first line to match with start date
                    start=dataa.index(i)
                    break
                    
            for i in dataa:
                databroken2 = i.split(",")
                if sys.argv[4] == databroken2[0]:
                    # last line to match with end date 
                    end = dataa.index(i)
                    
            ls = []
            i=start 
            # getting the list of event within the interval
            while i < end+1:
                ls.append(dataa[i])
                i+=1

            display(ls)