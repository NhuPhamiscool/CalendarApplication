#!/bin/bash

python3 daemon.py empty.csv &

#TEST 1 ADD
~/cald/calendar.py ADD "12-12-2021" "SCHOOL" "monday"
~/cald/calendar.py ADD "27-10-2021" "do homwork" "due on tuesday"
~/cald/calendar.py ADD "02-12-2021" "party" 
~/cald/calendar.py ADD "29-01-2022" "my birthday" "party at home"

diff empty.csv ~/cald/test_daemon/add_event.out

# TEST 2 DEL
~/cald/calendar.py DEL "27-10-2021" "do homwork"

diff empty.csv ~/cald/test_daemon/del_event.out

# TEST 3 UPD
~/cald/calendar.py UPD "12-12-2021" "SCHOOL" "christmas" "no more school days"
~/cald/calendar.py UPD "29-01-2022" "my birthday" "new year party" "wine needed"

diff empty.csv ~/cald/test_daemon/upd_event.out

# ---------------------------------------------------------------

#TEST 3 INVALID DATE

~/cald/calendar.py ADD 12-12/2021 "SUMMER TIME" "YO"
~/cald/calendar.py ADD 12-12/2021 "buying milk" "full cream"

#TEST 4 UPDATE NON-EXIST EVENT

~/cald/calendar.py UPD 12-12-2021 "SUMMER TIME" "SCHOOL TIME"

#TEST 5 MISSING EVENT NAME
~/cald/calendar.py ADD
~/cald/calendar.py DEL
~/cald/calendar.py UPD

diff /tmp/cald_err.log ~/cald/test_daemon/test_error_log.out




