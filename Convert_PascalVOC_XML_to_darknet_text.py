# This program converts Pascal VOC xml files to Alexey darknet .txt files.
# Note - I have not found 'class' attribute in pascal voc xml file. So, for now I have hardcoded the class as 0 as I only 
# have a single class to deal with. Otherwise you might have to map each unique object name to a different class and 
# accordingly convert to the .txt file

import xml.etree.ElementTree as ET
import os
import numpy as np
import pathlib

# Specify the full path to your annotation xml files. The output folder is created in the same directory

path = '/test_annot'

def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    
    # get the size of the image
    size_o = tree.find('size')
    width = int(size_o.find('width').text)
    height = int(size_o.find('height').text)

    # get the bounding box for each object
    for obj in tree.findall('object'):
        obj_param = []
        obj_param.append(0)
        
        bbox = obj.find('bndbox')
        
        dw = 1.0/width;
        dh = 1.0/height;
        
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)        
        
        # Computing the center of the bounding box, width and height
        x = (xmin+xmax)/2.0
        y = (ymin+ymax)/2.0
        w = xmax - xmin
        h = ymax - ymin
        
        # Computing the relative sizes of the bounding box co-ordinates, width and height wrt image so that all values fall in between 0 and 1.
        x = '%.6f'%(x * dw)     # limit to 6 decimals
        w = '%.6f'%(w * dw)
        y = '%.6f'%(y * dh)
        h = '%.6f'%(h * dh)
        
        obj_param.extend((x,y,w,h))

        objects.append(obj_param)

    return objects


def create_output_folder():
    path_out = os.path.join(path , 'out')
    pathlib.Path(path_out).mkdir(parents=True, exist_ok=True) 
    return path_out


def read_and_convert_files(folder):
    for filename in os.listdir(folder):
        input_file_path = os.path.join(folder,filename)
        if os.path.isfile(input_file_path):                   # check if the read filename is not a directory ( otherwise it is going to throw an error for 'out' directory
            output_file_path = os.path.join(path_out, filename.split('.')[0]+'.txt')
            txtOut = open(output_file_path,'w') 
            
            # read all the objects from the XML file. There could be multiple bounding boxes even if there is a single object.
            objects = parse_rec(input_file_path)

            # write each 
            for obj in objects:
                str1 = ' '.join(str(e) for e in obj)
                txtOut.write(str1)
                if (len(objects)>1):
                    txtOut.write("\n")
            txtOut.close()

path_out = create_output_folder()
read_and_convert_files(path)
