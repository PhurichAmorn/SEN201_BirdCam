set time = 6
set alarm_active = true
set energy_level = 50
set breakfast_done = false
set tasks_completed = 0

print "Good morning!"
do Check_Weather
print "Weather checked successfully."

if alarm_active equals true
    print "Alarm is ringing..."
    do Turn_Off_Alarm
else
    print "No alarm set."
endif

print "Starting morning routine..."

while time < 9
    print "Current time: {time} AM"

    if energy_level < 40
        print "Energy low — making coffee."
        do Make_Coffee
        set energy_level = energy_level + 30
    endif

    if time equals 7
        if breakfast_done equals false
            print "Preparing breakfast..."
            do Cook_Breakfast
            set breakfast_done = true
            print "Breakfast completed!"
        else
            print "Already had breakfast."
        endif
    endif

    if time equals 8
        print "Checking today's tasks..."
        for task in range 1 to 3
            print "Performing task {task}"
            do Complete_Task(task)
            set tasks_completed = tasks_completed + 1
        endfor
        print "All tasks done for the morning."
    endif

    set time = time + 1
    set energy_level = energy_level - 10
endwhile

print "Morning routine finished."
print "Summary:"
print "- Total tasks completed: {tasks_completed}"
print "- Energy level: {energy_level}"
print "- Breakfast done: {breakfast_done}"

if tasks_completed >= 3
    print "Great job! You had a productive morning."
else
    print "Try to complete more tasks tomorrow."
endif

do Prepare_For_Work
print "Leaving home. Have a nice day!"
