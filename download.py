import json
import os
import utils
from pytube import  YouTube
import gflags
import sys


youtube_link ='https://www.youtube.com/watch?v='


def read_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    print ('Done reading {:s}: {:d} items'.format(json_file, len(data)))
    return data


def download(json_data, save_dir, video_format='mp4', video_resolution='360p'):
    save_dir = utils.get_dir(save_dir)
    count = 0
    nfiles =len(json_data)
    for i, datum in enumerate(json_data):
        videolink = youtube_link + datum['id']
        try:
            yt = YouTube(videolink)
            video = yt.get(video_format, video_resolution)
            video.filename = datum['id']
            video.download(save_dir)
            count += 1
            print ('{:d} : {:d} -- {:s}'.format(i, nfiles, datum['id']))
            
            # debug here:
            # if count == 5:
                # break
        except:
            print ('{:s} NOT valid'.format(datum['id']))
            continue

    print ('Done Download, {:d} is downloaded'.format(count))


def main(argv):
    FLAGS = gflags.FLAGS
    gflags.DEFINE_string('jsonfile', 'json/sports1m_test.json', 'jason file to read from[json/sports1m_test.json]')
    gflags.DEFINE_string('savedir', 'tmp', 'dstination directory to save files[tmp]')
    gflags.DEFINE_string('video_format', 'mp4', 'video format[mp4]')
    gflags.DEFINE_string('video_resolution', '360p', 'video resolution 360p, 720p and so on[360p]')
    argv = FLAGS(argv)

    jsonfile = FLAGS.jsonfile
    savedir = utils.get_dir(FLAGS.savedir)

    raw_json_data = read_json(jsonfile)
    download(raw_json_data, save_dir=savedir)

if __name__=='__main__':
    main(sys.argv)