# Read JSON file
import json
import csv
import cv2
import os
#opening JSON file
f = open('rail_trackCOCO.json')
#returns JSON object as a dictionary
training_data = json.load(f)
imgLocation = "/home/rehman_mf/TrainYourOwnYOLO/Data/Source_Images/Training_Images/vott-csv-export/"
csv_file = ['', '', '', '', '', '']
csvhandle=open('Annotations-export.csv', 'w', newline='')
csvwriter = csv.writer(csvhandle)
csvhandle.write('image,"xmin","ymin","xmax","ymax","label"\n')
def convert_labels(x1, y1, x2, y2):
    # Definition: Parses label files to extract label and bounding box coordinates. Converts (x1, y1, x1, y2) KITTI format to (x, y, width, height) normalized YOLO format.
    def sorting(l1, l2):
        if l1 > l2:
            lmax, lmin = l1, l2
            return lmax, lmin
        else:
            lmax, lmin = l2, l1
            return lmax, lmin
    size = (640,512)
    xmax, xmin = sorting(x1, x2)
    ymax, ymin = sorting(y1, y2)
    dw = 1./size[1]
    dh = 1./size[0]
    x = (xmin + xmax)/2.0 #center x
    y = (ymin + ymax)/2.0 #center y
    w = (xmax - xmin)   #width
    h = (ymax - ymin)   #height
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
check_set = set()
for i in range(len(training_data["annotations"])):
    image_id = str(training_data["annotations"][i]["image_id"])
    image_id_num = training_data["annotations"][i]["image_id"] - 1
    category_id = str(training_data["annotations"][i]["category_id"])
    bbox = training_data["annotations"][i]["bbox"]
    #image_path = image_id + '.jpg'
    kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
    out_list.append(kitti_bbox)
    #yolo_bbox = convert_labels(kitti_bbox[0], kitti_bbox[1], kitti_bbox[2], kitti_bbox[3])
    filename = str(training_data["images"][image_id_num]["file_name"])
    imgAddress = imgLocation+filename
    content = imgAddress + ' ' + str(kitti_bbox[0]) + ',' + str(kitti_bbox[1]) + ',' + str(kitti_bbox[2]) + ',' + str(kitti_bbox[3]) + ',' + category_id
    csvhandle = open('Annotations-export.csv', 'a', newline='')
    csv_file[0] = filename
    csv_file[1] = str(kitti_bbox[0])
    csv_file[2] = str(kitti_bbox[1])
    csv_file[3] = str(kitti_bbox[2])
    csv_file[4] = str(kitti_bbox[3])
    csv_file[5] = 'Railtrack'
    csvwriter.writerow(csv_file)
    csvhandle.close()
    if image_id in check_set:
        # Append to file files
        file = open('data_train.txt', 'a')
        #file.write(filename)
        #file.write('\n')
        file.write(' ' + str(kitti_bbox[0]) + ',' + str(kitti_bbox[1]) + ',' + str(kitti_bbox[2]) + ',' + str(kitti_bbox[3]) + ',' + category_id)
        file.close()
    elif image_id not in check_set:
        check_set.add(image_id)

    #    # Write files
    #    file = open(filename, 'w')
        file = open('data_train.txt', 'a', newline='')
        file.write('\n')
        file.write(content)
        #file.write('\n')
        file.close()

