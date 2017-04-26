# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:31:38 2017

@author: song-isong-i
"""

import json
import os
import unicodecsv as csv

#read all the json files in the folder and save the data sorted by posts into csv
def read_files(json_dir):
    print('reading profiles...')
    with open('posts.csv', "wb") as o_posts:
        writer = csv.writer(o_posts, lineterminator='\n') 
        for f in os.listdir(json_dir):
            if f != '.DS_Store':
                with open(json_dir+f) as json_data:
                    d = json.load(json_data)
                    sort_by_posts(d, writer)

def sort_by_posts(dic, writer):
    username = dic['username'] #2
    user_id = dic['user_id'] #3
    full_name = dic['full_name'] #4
    profile_pic_url = dic['profile_pic_url'] #5
    media_count = dic['media_count'] #6
    follower_count = dic['follower_count'] #7
    posts = dic['posts']
    
    #don't save if no post
    if len(posts) > 0:    
        
        for p in posts:
            post = []
            pic_url = p['pic_url'] #0
            like_count = p['like_count'] #1
            comment_count = p['comment_count'] #8
            date = p['date'] #9
            caption = p['caption'] #10
            tags = p['tags'] #11
            post = [pic_url, like_count, username, user_id, full_name, profile_pic_url, media_count, follower_count, comment_count, date, caption, tags]           
            writer.writerow(post)
            

        
        
