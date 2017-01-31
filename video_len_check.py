import json
import os
import utils
# from pytube import YouTube
import gflags
import sys


# youtube_link ='https://www.youtube.com/watch?v='


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
        else:

            print ('{:05d} : {:s} -- {:d} seconds'.format(i,datum['id'], datum['duration']))
            sys.stdout.flush()
            counts += 1
            refined_list.append(datum)




    print ('Done Checking, {:d} invalid'.format(counts))


def main(argv):
    FLAGS = gflags.FLAGS
    gflags.DEFINE_integer('duration', , 'keep videos with duration less than [12]')
    gflags.DEFINE_string('srcfile', 'json/sports1m_test.json', 'source jason file[json/sports1m_test.json]')
    gflags.DEFINE_string('dstfile', None, 'dstination json file[json/sports1m_test_(duration).json]')

    argv = FLAGS(argv)

    srcfile = FLAGS.srcfile
    dstfile = FLAGS.dstfile
    if not dstfile:
        srcname, srcext = os.path.splitext(srcfile)
        dstfile = '{:s}_{:02d}{:s}'.format(srcname,FLAGS.duration, srcext)


    raw_json_data = read_json(srcfile)
    check_duration(raw_json_data, dstfile=dstfile, duration=FLAGS.duration)

if __name__=='__main__':
    main(sys.argv)
