import json
import os
import utils
from pytube import  YouTube
import gflags

test_json_file ='json/sports1m_test.json'
train_json_file = 'json/sports1m_train.json'


youtube_link ='https://www.youtube.com/watch?v='
save_dir = './videos'


def read_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    print ('Done reading {:s}: {:d} items'.format(json_file, len(data)))
    return data


def download(json_data, list_info_file, save_dir):
    save_dir = utils.get_dir(save_dir)
    for idx in xrange(len(json_data)):
        videolink = youtube_link + json_data[idx]['id']
        try:
            yt = YouTube(videolink)
            video = yt.get('mp4', '360p' )
            video.filename = json_data[idx]['id']
            video.download(save_dir)
            # add a rename process:


        except:
            print ('{:s} not valid'.format(json_data[idx]['id']))
            continue


        print ('Breakpoint')

    print ('Done Download')


if __name__=='__main__':
    json_data = read_json(test_json_file)
    download(json_data, None, save_dir= save_dir)