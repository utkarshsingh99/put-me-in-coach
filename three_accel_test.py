import board
import os
import csv
import adafruit_tca9548a
import adafruit_mpu6050
import time as timesleep
from time import time

import numpy as np
from fastdtw import fastdtw
from sklearn.utils import shuffle


def save_csv_with_unique_name(base_filename, data, directory="."):
    """
    Saves data to a CSV file, appending a number to the filename if it already exists.

    :param base_filename: The base name of the file (e.g., 'example.csv')
    :param data: The data to be saved in the file, a list of rows, with each row being a list of values.
    :param directory: The directory where the file will be saved. Defaults to the current directory.
    :return: The path to the saved file.
    """
    # Ensure the directory ends with a separator if it's not empty
    if directory and not directory.endswith(os.path.sep):
        directory += os.path.sep

    filename, file_extension = os.path.splitext(base_filename)
    unique_filename = f"{directory}{filename}{file_extension}"


    # Save the data to the CSV file
    with open(unique_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # print(f"CSV file saved as {unique_filename}")
    return unique_filename

# Define a function to read the sensor data
def read_sensor_data(mpu):

    # Read the accelerometer values
    accelerometer_data = mpu.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu.get_gyro_data()

    # Read temp
    temperature = mpu.get_temp()

    return accelerometer_data, gyroscope_data, temperature

# Compute DTW distances
def NNDTW(test_point):
    dtw_distances = []
    #print(test_point)
    for train_point in train_data:
        dtw_distance, _ = fastdtw(test_point, train_point)
        dtw_distances.append(dtw_distance)

    # 1-Nearest Neighbors classification to classify our given test point relative to training points.
    nearestidx = np.argmin(dtw_distances)
    nearestneighbor = train_labels[nearestidx]

    # print(nearestidx)
    return nearestneighbor

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

mpu1 = adafruit_mpu6050.MPU6050(tca[2])
mpu2 = adafruit_mpu6050.MPU6050(tca[3])
mpu3 = adafruit_mpu6050.MPU6050(tca[4])

clfdict = {}
train_data = []
train_labels = []
good_idx = 0
#aggregate training samples for good data
for subdir in os.listdir():
    if ('good') in subdir:
        for file in os.listdir(subdir):
            with open(os.path.join(subdir,file),"r") as f:
                point = []
                for line in f:
                    point.append([float(x) for x in line.split(',')[1:]])
                train_data.append(point)
                train_labels.append(0)
        clfdict[good_idx] = subdir
        good_idx = good_idx + 1


badidx = good_idx + 1

#aggregate training samples for any number of "bad form" classes, and assign a corresponding class label
for subdir in os.listdir():
    if ('(bad)') in subdir:
        for file in os.listdir(subdir):
            with open(os.path.join(subdir,file),"r") as f:
                point = []
                for line in f:
                    point.append([float(x) for x in line.split(',')[1:]])
                train_data.append(point)
                train_labels.append(badidx)

        clfdict[badidx] = subdir
        badidx = badidx + 1



data = np.array([time()] + list(mpu1.acceleration) + list(mpu1.gyro) +list(mpu2.acceleration) + list(mpu2.gyro) +list(mpu3.acceleration) + list(mpu3.gyro))
std_values_num = 20
off_tick = 0
flip_off = False
flip_on = False
flip_off_count = 0
idx_start = 0
idx_end = 0
flags = []
ticks = []

not_stopped = True

idx = 0
while not_stopped:
    new_row = [time()] + list(mpu1.acceleration) + list(mpu1.gyro) +list(mpu2.acceleration) + list(mpu2.gyro) +list(mpu3.acceleration) + list(mpu3.gyro)
    data = np.vstack([data, new_row])
    #0, 1 2 3, 4 5 6, 7 8 9, 10 11 12, 13 14 15, 16 17 18
    # print(max(0, idx-std_values_num):idx)
    std_dev_last_10 = np.std(data[max(0, idx-std_values_num):idx,15])
    if std_dev_last_10 > 2:
        off_tick = min(off_tick + 1, 10)
    else:
        off_tick = 0

    if off_tick > 6:
        flags.append(10)
        flip_on = True
        if idx_start == 0:
            idx_start = max(0, idx - 40)
            print("Started")
    else:

        if flip_on:
            flip_off = True
        flags.append(0)

    if flip_off:
        flip_off_count += 1
    else:
        flip_off_count = 0

    if flip_off_count > 40:
        idx_end = idx
        print("End")

        break

    ticks.append(off_tick)
    idx += 1

cut_data = data[idx_start:idx_end,:]
#
# print("Data:", len(data), idx_start, idx_end, cut_data.shape)
# print("CLF:", clfdict)
print(NNDTW(cut_data[:,1:]))
unique_name = save_csv_with_unique_name("accel_data.csv", data)
# print(unique_name)

