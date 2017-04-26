# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 18:45:17 2017

@author: song-isong-i
"""

from requests import get  # to make GET request
import PIL
from PIL import Image
import os
import sys
import csv

def download(url, file_name, path):
    with open(path+file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
        
def download_all(urls,down_dir):
    os.mkdir(down_dir)
    os.system('cd ' + down_dir)
    print("downloading images...")
    for i in range(len(urls)):
        download(urls[i],str(i+1)+'.jpg', down_dir)        

def resize(input_dir, output_dir, img_size):
    try:
        input_dir  = str(input_dir.rstrip('/'))  #path to img source folder
        output_dir  = str(output_dir.rstrip('/')) #output directory
        print ("starting....")
        print ("Collecting data from %s " % input_dir)
        tclass = [ d for d in os.listdir( input_dir ) ]
        counter = 0
        os.makedirs(output_dir)
        print ("Resizing images...")

        for d in tclass:
            if d != '.DS_Store':
                try:
                    img = Image.open(os.path.join(input_dir,d))
                    img = img.resize((img_size,img_size),Image.ANTIALIAS)
                    fname,extension = os.path.splitext(d)
                    newfile = fname+extension
                    if extension != ".jpg" :
                        newfile = fname + ".jpg"
                    img.save(os.path.join(output_dir,newfile),"JPEG",quality=90)
                    #print ("Resizing file : %s " % (d))
                except Exception as e:
                    print ("Error resize file : %s " % (d))
                    sys.exit(1) 
            counter +=1
    except Exception as e:
        print ("Error, check Input directory etc : ", e)
        sys.exit(1)



def get_pixels(image):
    im = Image.open(image)
    pixels = list(im.getdata())
    return pixels
    
#return a list of pixels of all photos
def get_data(resized_dir): 
    pixeldata = []
    for f in os.listdir(resized_dir):
        if f != '.DS_Store':
            pixeldata.append(get_pixels(resized_dir+'/'+f))
    return pixeldata
        
def save_to_csv(pixeldata):
    with open('rgbdata.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(pixeldata)

def labels_csv(likes, followers):        
    with open('labels.csv', "w") as lo:
        writer = csv.writer(lo, lineterminator='\n')
        for i in range(len(likes)):
            writer.writerow([likes[i]/followers[i]]) 




