set motion_detected = true
set light_level = "low"

if motion_detected equals true
    if light_level equals "low"
        print "Turn on infrared camera"
    else
        print "Use normal camera mode"
    endif
else
    print "No motion detected"
endif
