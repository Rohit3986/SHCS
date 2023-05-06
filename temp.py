from datetime import datetime, timedelta

def split_time(start_time, end_time, slot_duration):
    # convert start and end times to datetime objects
    start_time = datetime.strptime(start_time, '%H:%M')
    end_time = datetime.strptime(end_time, '%H:%M')

    # calculate the total number of minutes between start and end time
    total_minutes = int((end_time - start_time).total_seconds() / 60)

    # calculate the number of slots
    num_slots = int(total_minutes / slot_duration)

    # initialize the list of time slots
    slots = []

    # iterate through the slots and calculate the start and end time of each slot
    for i in range(num_slots):
        slot_start = start_time + timedelta(minutes=i * slot_duration)
        slot_end = slot_start + timedelta(minutes=slot_duration)

        # format the start and end times in am-pm format
        slot_start_str = slot_start.strftime('%I:%M %p')
        slot_end_str = slot_end.strftime('%I:%M %p')

        # add the time slot to the list of slots
        slots.append((slot_start_str, slot_end_str))

    return slots
