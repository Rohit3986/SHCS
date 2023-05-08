from datetime import datetime, timedelta

#2023-05-07 2023-05-10 23:11 03:15
def split_time(start_time=None, end_time=None, slot_duration=30, curr_date=None):
    

    # convert start and end times to datetime objects
    start_time = timedelta(hours=int(start_time[:2]),minutes=int(end_time[-2:]))
    end_time = timedelta(hours=int(end_time[:2]),minutes=int(end_time[-2:]))

    # calculate the total number of minutes between start and end time
    total_minutes = int((end_time - start_time).total_seconds() / 60)

    # calculate the number of slots
    num_slots = int(total_minutes / slot_duration)
    
    # initialize the list of time slots

    s=[]
    # iterate through the slots and calculate the start and end time of each slot
    for i in range(num_slots):
        start_time = datetime(2023, 5, 6, 9, 0, 0)
        slot_start = start_time + timedelta(minutes=i * slot_duration)
        slot_end = slot_start + timedelta(minutes=slot_duration)
        start_time = datetime(2023, 5, 6, 0, 0, 0)
        # format the start and end times in am-pm format
        slot_start_str = slot_start.time().strftime('%I:%M %p')
        slot_end_str = slot_end.time().strftime('%I:%M %p')
        appointment_dict = {}
        appointment_dict['appointment_date']=curr_date
        appointment_dict['start_time']=slot_start_str
        appointment_dict['end_time']=slot_end_str
        appointment_dict['is_available']=True
        s.append(appointment_dict)
        # add the time slot to the list of slots
        

    return s

def create_appointment_slots(start_date,end_date,start_time,end_time):
    start_date="2023-05-07"
    end_date="2023-05-09"
    start_date=datetime(day=int(start_date[-2:]),month=int(start_date[5:7]),year=int(start_date[:4]))
    print(start_date.strftime('%Y-%m-%d : %A'))
    end_date=datetime(day=int(end_date[-2:]),month=int(end_date[5:7]),year=int(end_date[:4]))
    date_diff=int((end_date-start_date).days)
    k=[]
    for i in range(date_diff+1):
        curr_date = start_date+timedelta(days=i)
        curr_date = curr_date.strftime('%Y-%m-%d : %A')
        k.extend(split_time(start_time='09:00',end_time='12:00',curr_date=curr_date))
    print(k)