# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 18:45:17 2017

@author: song-isong-i
"""

from requests import get  # to make GET request
from PIL import Image
from util import file_to_list
import os
import sys
import csv
import numpy as np

def download(url, file_name, path, overwrite=False):
    if not overwrite and os.path.exists(path+file_name):
        return
    while True:
        try:
            with open(path + file_name, "wb") as file:
                response = get(url)
                file.write(response.content)
        except Exception as e:
            print('Failed to download %s, retrying.' % file_name, e)
        else:
            break
        
def download_all(start, end, urls, down_dir):
    if not os.path.exists(down_dir):
        os.mkdir(down_dir)
    os.system('cd ' + down_dir)
    print("downloading images...")
    try:
        for i in range(start, end):
            file_name = str(i+1) + '.jpg'
            download(urls[i], file_name, down_dir)
    except Exception as e:
        raise Exception('Download failed on %s' % file_name, e)

def resize_all(start, end, input_dir, output_dir, img_size, errors_file='resize_errors.txt'):
    try:
        input_dir  = str(input_dir.rstrip('/'))  #path to img source folder
        output_dir  = str(output_dir.rstrip('/')) #output directory
        print ("Collecting data from %s " % input_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print ("Resizing images...")

        for d in os.listdir(input_dir)[start:end]:
            fname, extension = os.path.splitext(d)
            if extension == ".jpg":
                try:
                    img = Image.open(os.path.join(input_dir,d))
                    img = img.resize((img_size,img_size),Image.ANTIALIAS)
                    img.save(os.path.join(output_dir,fname+'.jpg'),"JPEG",quality=90)
                    #print ("Resizing file : %s " % (d))
                except Exception as e:
                    print ("Error resize file : {!s}, will remove from posts.csv and from down dir".format(d))
                    with open(errors_file, 'a') as f:
                        f.write(d+'\n')
                    # sys.exit(1) 
    except Exception as e:
        print ("Error, check Input directory etc : ", e)
        sys.exit(1)



def pixels(image):
    with Image.open(image) as im:
        pixels = np.array(im.getdata(), dtype=int)
    return pixels


def pixeldata_to_csv(resized_dir, csv_dir, file_name='rgbdata.csv'):
    pixeldata = np.array([], dtype=int)
    with open(os.path.join(csv_dir,file_name), "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for file_name in os.listdir(resized_dir):
            try:
                if file_name.endswith('.jpg'):
                    pixeldata = pixels(resized_dir + os.sep + file_name).reshape(-1,3).T.tolist()
                    writer.writerows(pixeldata)
            except ValueError as e:
                print(e)
                pixeldata = np.repeat(pixels(resized_dir + os.sep + file_name).reshape(-1,1).T, 3, axis=0).tolist()
                writer.writerows(pixeldata)

            except Exception as e:
                print('Exception while saving RGB with file {}'.format(file_name), e)


def labels_to_csv(likes, followers, csv_dir, file_name='labels.csv'):    
    with open(os.path.join(csv_dir, file_name), "w") as lo:
        writer = csv.writer(lo, lineterminator='\n')
        for i in range(len(likes)):
            try:
                writer.writerow([likes[i]/followers[i]]) 
            except ZeroDivisionError as e:
                print(e)
                writer.writerow([0]) 


def remove_records(errors_file, input_file, output_file, down_dir,csv_dir):
    '''cleans up erronoeous records from csv and download directory'''
    print("removing erroneous records")
    try:
        with open(errors_file, 'r') as f:
            errors_list = [line.strip() for line in f]
            if len(errors_list) == 0: return
    except Exception as e:
        print(e)
        return
    f = file_to_list(csv_dir + '/'+input_file)
    output = []
    for i, line in enumerate(f):
        if not str(i+1)+'.jpg' in errors_list:
            output.append(line)
    print(len(output), len(errors_list))
    with open(os.path.join(csv_dir,output_file), 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output)
    for file_name in os.listdir(down_dir):
        if file_name in errors_list:
            os.remove(down_dir + file_name)


