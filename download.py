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


def download(json_data, save_dir, max_len=100000, min_len=-1, video_format='mp4', video_resolution='360p', dstfile=None):
    save_dir = utils.get_dir(save_dir)
    count = 0
    nfiles =len(json_data)
    testids = []
    testlabels = []

    with open(dstfile, 'w') as f:


        for i, datum in enumerate(json_data):

            if datum['duration']>min_len and datum['duration']<max_len:

                videolink = youtube_link + datum['id']

                try:
                    yt = YouTube(videolink)
                    video = yt.get(video_format, video_resolution)
                    video.filename = datum['id']
                    video.download(save_dir)
                    count += 1
                    print ('{:d} : {:d} -- {:s}, len: {:d}'.format(i, nfiles, datum['id'], int(datum['duration'])))
                    videoname = os.path.join(save_dir, '{:s}.{:s}'.format(datum['id'], video_format))
                    videolabel = datum['label487']
                    f.write('{:s} {:s}\r\n'.format(videoname, ' '.join(map(str, videolabel))))
                    f.flush()
                except:
                    print ('{:s} NOT valid'.format(datum['id']))
                    continue





    print ('Done Download, {:d} is downloaded, information saved to '.format(count))


def main(argv):
    FLAGS = gflags.FLAGS
    gflags.DEFINE_string('srcfile', 'json/sports1m_test.json', 'jason file to read from[json/sports1m_test.json]')
    gflags.DEFINE_string('savedir', 'tmp', 'dstination directory to save files[tmp]')
    gflags.DEFINE_string('video_format', 'mp4', 'video format[mp4]')
    gflags.DEFINE_string('video_resolution', '360p', 'video resolution 360p, 720p and so on[360p]')
    gflags.DEFINE_integer('min_len', 4, 'Minimal length(4 seconds)')
    gflags.DEFINE_integer('max_len', 30, 'Maximal length (30 seconds)')
    gflags.DEFINE_string('dstfile', None, 'dstination json file[json/sports1m_test_(duration).json]')
    gflags.DEFINE_boolean('rewrite', True, 'rewrite everything in saved dir[True]')
    argv = FLAGS(argv)

    srcfile = FLAGS.srcfile
    dstfile = FLAGS.dstfile

    savedir = os.path.abspath(FLAGS.savedir)
    savedir = utils.get_dir(savedir)

    if FLAGS.rewrite:
        utils.clear_dir(savedir)

    raw_json_data = read_json(srcfile)
    if not dstfile:
        srcname, srcext = os.path.splitext(srcfile)
        dstfile = '{:s}-{:02d}-{:02d}{:s}'.format(srcname, FLAGS.min_len, FLAGS.max_len, '.txt')
    download(raw_json_data, save_dir=savedir, dstfile=dstfile, max_len=FLAGS.max_len, min_len=FLAGS.min_len)

if __name__=='__main__':
    main(sys.argv)