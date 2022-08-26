import csv
import json
data = csv.reader(open('Annotations-export.csv'))
header = next(data)
out_data = list(data)

my_list = []
s_list = []
final_list = []

image_name = out_data[0][0]
dict_keys = [image_name]
last_image_name = out_data[-1][0]

def append_to_list(rows):
    xmin = int(rows[1])
    ymin = int(rows[2])
    xmax = int(rows[3])
    ymax = int(rows[4])
    s_list = [xmin, ymin, xmax, ymax]
    my_list.append(s_list)


if __name__ == '__main__':
    for rows in out_data:
        if image_name != rows[0]:
            image_name = rows[0]
            dict_keys.append(image_name)
            final_list.append(my_list[:])
            my_list.clear()
            append_to_list(rows)
        elif last_image_name == rows[0]:
            append_to_list(rows)
        else:
            append_to_list(rows)

    final_list.append(my_list[:])
    my_list.clear()
    dict_keys.append(last_image_name)
    print(final_list)
    new_dict = dict(zip(dict_keys, final_list))
    json_string = json.dumps(new_dict)
    print(json_string)
    with open("ground_truth_boxes.json", "w") as outfile:
        outfile.write(json_string)
    #print(z_dict)
    #print(s_dict)
