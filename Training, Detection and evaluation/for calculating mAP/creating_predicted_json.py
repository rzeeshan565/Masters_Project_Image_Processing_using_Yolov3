import json
import csv
data = csv.reader(open('Detection_Results.csv'))
header = next(data)
out_data = list(data)
image_name = out_data[0][0]
last_image_name = out_data[-1][0]
my_list = []
my_list2 = []
score_list = []
final_list = []
final_list1 = []
new_list = []
new_list = []
new_list1 = []
x = 0
image_name_ls = [image_name]
keys=["boxes","scores"]

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def append_to_list(rows):
    xmin = int(rows[2])
    ymin = int(rows[3])
    xmax = int(rows[4])
    ymax = int(rows[5])
    score = float(rows[7])
    score_list.append(score)
    s_list = [xmin, ymin, xmax, ymax]
    my_list.append(s_list)

for rows in out_data:
        #if last_image_name == rows[0]:
        #    append_to_list(rows)
    if image_name != rows[0]:
        my_list2.append(my_list[:])
        my_list2.append(score_list[:])
        my_list.clear()
        score_list.clear()
        append_to_list(rows)
        image_name = rows[0]
        image_name_ls.append(image_name)
    else:
        append_to_list(rows)
print(image_name_ls)
print(len(image_name_ls))
print(my_list2)
for i in range(len(my_list2)):
    if i%2==0:
        new_list = keys[0] + ": " + str(my_list2[i])
        final_list.append(new_list)

    else:
        new_list = keys[1] + ": " + str(my_list2[i])
        final_list.append(new_list)
for i in range(0,182,2):
    j = i+1
    final_list1.append(final_list[i:j+1])
print(final_list)
print(len(final_list))
print(final_list1)
print(len(final_list1))
new_dict = dict(zip(image_name_ls, final_list1))
json_string = json.dumps(new_dict)
print(json_string)
with open("my_predicted_boxes.json", "w") as outfile:
    outfile.write(json_string)

