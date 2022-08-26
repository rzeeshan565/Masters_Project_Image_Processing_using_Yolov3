import pandas as pd
import json

#filename = open('rail_trackCOCO.json')

def convert_coco_json_to_csv(filename):

    # COCO2017/annotations/instances_val2017.json

    s = json.load(open(filename, 'r'))
    out_file = filename[:-5] + '.csv'
    out = open(out_file, 'w')
    print(out)
    out.write('id,x1,y1,x2,y2,label\n')

    all_ids = []
    for im in s['images']:
        all_ids.append(im['id'])

    all_ids_ann = []
    for ann in s['annotations']:
        image_id = ann['image_id']
        all_ids_ann.append(image_id)
        xmin = ann['bbox'][0]
        xmax = ann['bbox'][0] + ann['bbox'][2]
        ymin = ann['bbox'][1]
        ymax = ann['bbox'][1] + ann['bbox'][3]
        label = ann['category_id']
        out.write('{},{},{},{},{},{}\n'.format(image_id, x1, y1, x2, y2, label))

    all_ids = set(all_ids)
    all_ids_ann = set(all_ids_ann)
    no_annotations = list(all_ids - all_ids_ann)
    # Output images without any annotations
    for image_id in no_annotations:
        out.write('{},{},{},{},{},{}\n'.format(image_id, -1, -1, -1, -1, -1))
    out.close()

    # Sort file by image id
    s1 = pd.read_csv(out_file)
    s1.sort_values('id', inplace=True)
    s1.to_csv(out_file, index=False)
convert_coco_json_to_csv('rail_trackCOCO.json')