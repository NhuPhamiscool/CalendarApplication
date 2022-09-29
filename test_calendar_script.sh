#!/bin/bash

python3 daemon.py empty.csv &


#TEST 1 ADD
~/cald/calendar.py ADD "27-10-2021" "do homwork" "due on tuesday"
~/cald/calendar.py ADD "19-11-2021" "my birthday"
~/cald/calendar.py ADD "02-12-2021" "party" 
~/cald/calendar.py ADD "05-12-2021" "party at home"
~/cald/calendar.py ADD "10-12-2021" "christmas party with Alia"
~/cald/calendar.py ADD "12-12-2021" "christmas" "no more school days"

# TEST CALENDAR 
~/cald/calendar.py GET INTERVAL 05-12-2021 12-12-2021 | diff -  ~/cald/test_calendar/get_interval.out

# TEST GET MULTIPLE DATE
~/cald/calendar.py GET DATE 05-12-2021 12-12-2021 27-10-2021 | diff -  ~/cald/test_calendar/get_multiple_date.out

# TEST GET NAME PARTIAL
~/cald/calendar.py GET NAME "party" | diff -  ~/cald/test_calendar/get_name_partial.out

# TEST CALENDAR ERROR
~/cald/calendar.py GET NAME 2>&1 | diff -  ~/cald/test_calendar/get_name_no_args.out
~/cald/calendar.py GET NAME "basketball" 2>&1 | diff -  ~/cald/test_calendar/get_name_no_event.out
~/cald/calendar.py GET INTERVAL 12-12-2021 05-12-2021 2>&1 | diff -  ~/cald/test_calendar/interval_start_after_end.out

