import json
import os
import utils
from pytube import YouTube
import gflags
import sys


youtube_link ='https://www.youtube.com/watch?v='


def read_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    print ('Done reading {:s}: {:d} items'.format(json_file, len(data)))
    return data


# duration is in seconds
def check_duration(json_data, dstfile, duration = 12):
    counts = 0
    refined_list = []
    for i, datum in enumerate(json_data):
        if datum['duration'] > duration:
            continue

        videolink = youtube_link + datum['id']
        try:
            yt = YouTube(videolink)
            print ('{:05d} : {:s} -- {:d} seconds'.format(i,datum['id'], datum['duration']))
            counts += 1
            refined_list.append(datum)
        except:
            print ('{:05d} : {:s} NOT valid'.format(i, datum['id']))
            continue

        # debug check:
        if i >200:
            break

    with open(dstfile, 'w') as outfile:
        json.dump(refined_list, outfile)

    print ('Done Checking, {:d} valid'.format(counts))


def main(argv):
    FLAGS = gflags.FLAGS
    gflags.DEFINE_integer('duration', 12, 'keep videos with duration less than [12]')
    gflags.DEFINE_string('srcfile', 'json/sports1m_test.json', 'source jason file[json/sports1m_test.json]')
    gflags.DEFINE_string('dstfile', None, 'dstination json file[json/sports1m_test_(duration).json]')

    argv = FLAGS(argv)
    
    srcfile = FLAGS.srcfile
    dstfile = FLAGS.dstfile
    if not dstfile:
        srcname, srcext = os.path.splitext(srcfile)
        dstfile = '{:s}_{:02d}.{:s}'.format(srcname,FLAGS.duration, srcext)


    raw_json_data = read_json(srcfile)
    check_duration(raw_json_data, dstfile=dstfile, duration=FLAGS.duration)

if __name__=='__main__':
    main(sys.argv)
