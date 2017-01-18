import json
import os
import utils
from pytube import  YouTube

test_json_file ='json/sports1m_test.json'
train_json_file = 'json/sports1m_train.json'


youtube_link ='https://www.youtube.com/watch?v='
save_dir = './videos'


def read_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    print ('Done reading {:s}: {:d} items'.format(json_file, len(data)))
    return data


# duration is in seconds
def check(json_data, duration = 10):
    counts = 0
    for datum in json_data:
        if datum['duration'] > 10:
            continue

        videolink = youtube_link + datum['id']
        try:
            yt = YouTube(videolink)
            # video = yt.get('mp4', '360p' )
            # video.filename = datum['id']
            # video.download(save_dir)
            # add a rename process:
            print ('{:s} -- {:d} seconds'.format(datum['id'], datum['duration']))
            counts += 1

        except:
            print ('{:s} NOT valid'.format(datum['id']))
            continue


    print ('Done Checking, {:d} valid'.format(counts))

if __name__=='__main__':
    json_data = read_json(test_json_file)
    check(json_data)