# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:27:15 2017

@author: song-isong-i
"""
import unicodecsv as csv
import read_json as rj
import preprocessing as pp

#what I need : json_dir, down_dir, resize_dir  (down_dir and resize_dir folders should not exist)

def main():   
    json_dir = '/Users/ ' #directory of json files 
    datafile = 'posts.csv'
    rj.read_files(json_dir)
    
    data = file_to_list(datafile)
    urls, likes, followers = important_lists(data)
    
    down_dir = '/Users/ '  #folder to download images    
    resize_dir = '/Users/ '   #folder to resize images
    pp.download_all(urls, down_dir)    
    img_size = 100
    pp.resize(down_dir, resize_dir, img_size)
    
    pp.save_to_csv(pp.get_data(resize_dir))
    pp.labels_csv(likes, followers)


def file_to_list(file):
    data = []
    f = open(file, 'rb')
    contents = csv.reader(f)
    for c in contents:
        data.append(c)
    return data
    
def important_lists(data):
    urls = []
    likes = []
    followers = []
    for d in data:
        urls.append(d[0])
        likes.append(int(d[1]))
        followers.append(int(d[7]))
    return urls, likes, followers
    

        
main()





        
        
