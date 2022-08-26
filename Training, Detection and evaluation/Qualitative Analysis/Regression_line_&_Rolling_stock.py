"""
author: Zeeshan Rehman
date: 16 Jan 2022

Calculate Regression Line and Rolling Stock according to given dimensions:

> Regression_line_&_Rolling_stock.pi

Will display the selected Image with Regression Line and Rolling Stock

NOTE: Requires the files Images from test data set and `Detection_Results.csv`.
"""

from matplotlib import image
from matplotlib import pyplot as plt
import numpy as np
import csv

# Choose image
image_name = 'frame00510_thermalRT.png'

#Defining Lists
x_min = []
x_max = []
y_max = []
y_min = []
y_rs = []

#Defining Function for Drawing Regression line
def get_line():
    global y_rs,x_min,x_max,y_pred_l,y_pred_r #defining global parameters
    plt.plot(x_min_new, y_pred_l, color='red') #Drawing Regression line
    plt.plot(x_max_new,y_pred_r, color='red')

#Defining Function for Drawing Rolling Stock
def get_rs():
    global y_rs, x_min_new_new, x_max_new_new, y_pred_l, y_pred_r #defining global parameters
    y_pred_l, y_pred_r = list(y_pred_l), list(y_pred_r) #Converting numpy array into List
    x_min_new_new, x_max_new_new = list(x_min_new_new), list(x_max_new_new)

    for i in range(len(x_min_new_new)):
        y_rs.append(arr1[i])
        y_rs.append(arr1[i])
        #Converting pixel value into mm
        ref_px = x_max_new_new[i] - x_min_new_new[i]
        mm = ref_px / 1500
        len_A = mm * 400
        len_B = mm * 895
        len_C = mm * 3910
        #Drawing Rolling Stock
        plt.plot([x_min_new_new[i], x_max_new_new[i]], y_rs, color='yellow', linewidth=0.5)
        plt.plot([x_max_new_new[i], x_max_new_new[i]], [y_rs[1],y_rs[1] - len_A], color='yellow', linewidth=0.5)
        plt.plot([x_min_new_new[i], x_min_new_new[i]], [y_rs[0], y_rs[0] - len_A], color='yellow', linewidth=0.5)
        plt.plot([x_min_new_new[i], x_min_new_new[i] - len_B], [y_rs[0] - len_A, y_rs[0] - len_A], color='yellow', linewidth=0.5)
        plt.plot([x_max_new_new[i], x_max_new_new[i] + len_B], [y_rs[1] - len_A, y_rs[1] - len_A], color='yellow', linewidth=0.5)
        plt.plot([x_min_new_new[i] - len_B, x_min_new_new[i] - len_B], [y_rs[0] - len_A, y_rs[0] - len_A - len_C], color='yellow', linewidth=0.5)
        plt.plot([x_max_new_new[i] + len_B, x_max_new_new[i] + len_B], [y_rs[1] - len_A, y_rs[1] - len_A - len_C], color='yellow', linewidth=0.5)
        plt.plot([x_min_new_new[i] - len_B, x_max_new_new[i] + len_B], [y_rs[0] - len_A - len_C, y_rs[1] - len_A - len_C], color='yellow', linewidth=0.5)
        y_rs.clear()

if __name__ == '__main__':
    data = image.imread('Test_Images/{}'.format(image_name))
    csv_data = csv.reader(open('Detection_Results.csv'))
    header = next(csv_data)
    out_data = list(csv_data)

    for rows in out_data:
        if rows[0] == image_name:
            x_min.append(int(rows[2]))
            y_min.append(int(rows[3]))
            x_max.append(int(rows[4]))
            y_max.append(int(rows[5]))
        else:
            continue
    x_min = np.array(x_min)
    x_max = np.array(x_max)
    y_max = np.array(y_max)

    #Calculating Regression Line using Formula y = mx +b
    m_l, b_l = np.polyfit(x_min, y_max, 1)
    m_r, b_r = np.polyfit(x_max, y_min, 1)
    y_pred_l = m_l * x_min + b_l
    y_pred_r = m_r * x_max + b_r
    y_pred_l = np.append(y_pred_l, min(y_pred_r))
    y_pred_r = np.append(y_pred_r, max(y_pred_l))
    x_min_new = (y_pred_l-b_l) / m_l
    x_max_new = (y_pred_r-b_r) / m_r

    #defining Linear points on rail rack to draw Rolling Stock
    arr1 = np.linspace(min(y_pred_l), max(y_pred_l), len(y_pred_l))
    #Define new values on X-axis for the calculated y-axis
    x_min_new_new = (arr1 - b_l) / m_l
    x_max_new_new = (arr1 - b_r) / m_r
    get_line()
    get_rs()

    #Draw the plot on selected Image
    plt.imshow(data)
    plt.xlabel('Width (px)')
    plt.ylabel('Height (px)')
    plt.show()