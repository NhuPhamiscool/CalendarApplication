#!/usr/bin/python3

import signal
import os
import sys
import datetime

path = "/tmp/cald_pipe"
calendar_db = "/tmp/calendar_link"
error_log = "/tmp/cald_err.log"
database_name="cald_db.csv"
db_file=""

if len(sys.argv)==1:
    # finding the path of where this program executed
    path_db = os.path.dirname(os.path.abspath(sys.argv[0]))
    # joining the path above with the database file
    db_file = os.path.join(path_db,database_name)
    # create the database file
    with open(db_file, "a") as fi:
        pass

else:
    db_file = sys.argv[1]
    with open(db_file, "a") as fi:
        pass


# saving the calendar database path to the temporary file
with open(calendar_db,"w") as f:  
    f.write(db_file)

with open(error_log,"w") as f:
    pass

def errorlog(errortowrite):
    saveerror = open(error_log,"a")
    saveerror.write(errortowrite+"\n")
    saveerror.close()


def date_check(date):
    if len(date) != 10:
        mess = "Unable to parse date"
        errorlog(mess)
        return True
    try:
        day,mon,year = date.split('-')
        datetime.datetime(int(year),int(mon),int(day))

    except ValueError:
        mess = "Unable to parse date"
        errorlog(mess)
        return True
    
    return False

def read_data (string_command):
    description = ""
    event = ""
    date = ""
    command = []

    # case where string has white space (eg: "my birthday")
    if '"' in string_command:
        ls=[]
        # strip command by white space but omitting the white space inside the quotation marks
        command_ls = [co.strip() for co in string_command.split('"')]
        
        for i in command_ls:
            if i == '':
                command_ls.remove(i)

        # splitting ("ADD date" => "ADD","date")
        splitted = command_ls[0].split()
        # replace it in the list
        command_ls[0] = splitted
        # merge ls
        for i in command_ls:
            if type(i) == list:
                ls+=i
            else:
                ls.append(i)

        # missing event name
        if len(ls) <= 2:
            errorlog("Missing event name")
            return []

        command = ls
        date = ls[1]
        event = ls[2]

    # case where string has no white space (eg: "birthday")
    else:
        command = string_command.split()
        if len(command) <= 2:
            errorlog("Missing event name")
            return []
            
        date = command [1]
        event = command [2]

    if command[0] == "UPD" and len(command) <4:
        errorlog("Not enough arguments given")
        return []

    date_valid = date_check(date)
    if date_valid == True:
        # passing value of -1 dedicating date is invalid
        date = -1
    
    if command[0] == "ADD":
        # meaning it has description
        if len(command) >3:
            description = command[3]

        return [date,event,description]

    elif command[0] == "DEL":
        return [date,event]

    elif command[0] == "UPD":
        new_e = command[3]
        # meaning it has description
        if len(command) > 4:
            description = command[4]

        return [date,event,new_e,description]


def add_database(dates,event,des):
    db_add = open(db_file,"a")
    if des != "":
        db_add.write(dates+","+event+","+des+ "\n")
    else:
        db_add.write(dates+","+event+"\n")
    
    db_add.close()


def remove_database(dates,event):
    db_rev = open(db_file,"r") 
    db = db_rev.readlines()
    db_rev.close()

    # write data into database without the removed event
    new_db = open(db_file,"w")
    for line in db:
        splitted = line.split(",")
        if dates == splitted[0] and event == splitted[1]:
            continue
        else:
            new_db.write(line)
    
    new_db.close()


def update_database(dates,old,new,des):
    db_up = open(db_file,"r")
    line = db_up.readlines()
    count = 0

    for i in line:
        if dates in i and old in i:
            count+=1
            splitted = i.split(",")
            splitted[1] = new
            # means if theres a description
            if len(splitted) > 2: 
                splitted[2] = des 
            else:
                splitted.append(des)
            new_ = ",".join(splitted)
            line[line.index(i)] = new_+"\n"
    
    db_up.close()

    if count == 0 :
        errorlog("Unable to update, event does not exist")
        return -1

    db_up1 = open(db_file,"w")
    for i in line:
        db_up1.write(i)
    
    db_up1.close()


#Use this variable for your loop
daemon_quit = False

#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True


def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    if os.path.exists(path):
        os.remove(path)

    os.mkfifo(path)
    
    while not daemon_quit:
        fifo = open(path, "r")
        command = fifo.readline()

        if "ADD" in command:
            return_list = read_data(command)
            # empty list means there's an error
            if len(return_list) == 0:
                continue
            # return_list[0] is date
            if return_list[0] == -1:
                continue
            date,event,description = return_list[0],return_list[1],return_list[2]
            add_database(date,event,description)
                
        elif "DEL" in command:
            return_list = read_data(command)
            if len(return_list) == 0:
                continue
            if return_list[0] == -1:
                continue
            date,event_toremove = return_list[0],return_list[1]
            remove_database(date,event_toremove)

        elif "UPD" in command:
            return_list = read_data(command)
            if len(return_list) == 0:
                continue
            if return_list[0] == -1:
                continue
            date,old_event,new_event,description = return_list[0],return_list[1],return_list[2],return_list[3]
            # when error_ch = -1 means error happens 
            error_ch = update_database(date,old_event,new_event,description)
            if error_ch == -1:
                continue

    fifo.close()


if __name__ == '__main__':
    run()