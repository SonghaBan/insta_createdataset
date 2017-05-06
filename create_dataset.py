# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:27:15 2017

@author: song-isong-i
"""

import read_json as rj
import preprocessing as pp
import argparse
import os
from util import file_to_list, important_lists, divide_work
from time import time


def main():   
    if not os.path.exists(c['csv_dir']):
        os.makedirs(c['csv_dir'])
            
    if 1 in c['stage']:
        # PROCESS PROFILES IN JSON AND WRITE TO CSV
        print(os.getcwd() + c['json_dir'])
        rj.read_profiles(os.getcwd() + os.sep + c['json_dir'], c['csv_dir'], c['posts_original'])
    
    if 2 in c['stage']:
        # DOWNLOAD PHOTOS
        data = file_to_list(c['posts_original'])
        urls, likes, followers = important_lists(data)
        divide_work(pp.download_all, 0, len(urls), 5, (urls, c['down_dir']))
        # pp.download_all(0, len(url), urls, down_dir)

    if 3 in c['stage']:
        # RESIZE PHOTOS
        # pp.resize_all(down_dir, resize_dir, img_size)
        if 4 not in c['stage'] and os.path.exists(c['posts_filtered']): # if you don't remove erroneous files now ie. you removed it before, there must be a filtered version
            posts = c['posts_filtered']
        else:
            posts = c['posts_original']
        with open(posts, 'r') as file:
            l = sum(1 for line in file)
        divide_work(pp.resize_all, 0, l, 5, (c['down_dir'], c['resize_dir'], c['img_size']))

    if 4 in c['stage']:
        # SAVE PIXEL DATA IN PHOTOS AS CSV
        print('Saving pixel data to csv...')
        pp.pixeldata_to_csv(c['resize_dir'], c['csv_dir'],file_name='rgbdata' + str(c['img_size']) + '.csv')

    if 5 in c['stage']:
        # REMOVE ERRONEOUS FILES FROM DOWNLOAD DIR AND CSV
        pp.remove_records('resize_errors.txt', c['posts_original'], c['posts_filtered'], c['down_dir'],c['csv_dir'])
    
    if 6 in c['stage']:
        
        # SAVE LABELS AS CSV
        print('Saving labels to csv...')
        data = file_to_list(c['csv_dir']+c['posts_filtered'])
        urls, likes, followers = important_lists(data)
        pp.labels_to_csv(likes, followers, c['csv_dir'], c['labels'])


if __name__ == '__main__':
        # Example command:
    # python create_dataset.py -s 50 --stage 35 --overwrite
    parser = argparse.ArgumentParser(description='This script preprocesses data collected from crawling instagram', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--imgsize', dest='img_size', type=int, required=False, help='Image resize dimension. Default value is 100.')
    parser.add_argument('--overwrite', help="overwrite existing files in download or resize folders", action="store_true")
    parser.add_argument('--stage', dest='stage', type=str, required=False, help='int values denoting which stage of the script to start from.\n(empty): If it\'s your first run\n1: Reprocess the JSON (not recommended to use alone)\n2: Download all photos. See also: --overwrite\n3: Resize photos. See also: -s, --overwrite\n4: Process photos in resize directory and save as CSV.\n5: If you want to clean up erroneous files and records detected during resize\n6: Save labels (currently supports label = ratio of #likes/#followers). Must use 5 beforehand')
    args = parser.parse_args()
    
    
    c = config = {
        'json_dir'       : 'profiles' + os.sep,
        'down_dir'       : 'down' + os.sep,
        'resize_dir'     : 'resize' + str(args.img_size) + os.sep if args.img_size else 'resize100' + os.sep,
        'csv_dir'        : 'csv' + os.sep,
        'img_size'       : args.img_size if args.img_size else 100,
        'stage'          : [int(c) for c in (list('123456') if args.stage is None else args.stage)],
        'posts_original' : 'posts_original.csv',
        'posts_filtered' : 'posts_filtered.csv',
        'labels'         : 'labels.csv',
        'resize_errors'  : 'resize_errors.txt',
    }

    start_time = time()
    main()
    end_time = time()
    print("Job terminated in {} seconds".format(end_time-start_time))


