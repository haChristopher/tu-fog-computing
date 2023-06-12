def average_sensor_data(data):
    sum = 0
    size = len(data)
    for i in range(size):
        sum += data[i]
    return sum/size

