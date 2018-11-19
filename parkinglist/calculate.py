import datetime

def calculate(intime):
    flag = False
    time_now = datetime.datetime.now()
    parkingTime = str(time_now - intime)
    if 'day' in parkingTime:
        parkingTime = parkingTime.replace("days", "").replace("day", "").replace(',', ":")
    else:
        parkingTime = parkingTime.replace(',', '')
        flag = True
    parkingTime = parkingTime.split(":")
    if flag:
        parkingTime.insert(0,'0')

    cost = int((int(parkingTime[0]) * 24000) + (int(parkingTime[1]) * 4000) + (int(parkingTime[2]) // 10 * 500))
    return cost