# Julie Walin
# December, 2020

# This module holds all of the time calculations.

# Takes hours in decimal form and converts to seconds.  --->> O(1)
def hours_decimal_to_seconds(hours_dec):
    return(hours_dec * 3600)

# converts time in HH:MM:SS and converts to seconds.    --->> O(1)
def hours_HHMMSS_to_seconds(hours_HHMMSS):
    h, m, s = hours_HHMMSS.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# Converts seconds to HH:MM:SS assuming seconds is time from midnight. --->> O(1)
def seconds_to_HHMMSS(seconds):
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

# Validates input, allowing 00:00:00 - 23:59:59     --->> O(1)
# Ensures that the digits are integers and the numbers are in range.
def valid_HHMMSS_input(hours_HHMMSS):
    try:
        h, m, s = hours_HHMMSS.split(':')
        h_int = int(h)
        m_int = int(m)
        s_int = int(s)
    except ValueError:
        return False
    if h_int >= 0 and h_int < 25 and m_int >= 0 and m_int < 60 and s_int >= 0 and s_int < 60:
        return True
    else:
        return False