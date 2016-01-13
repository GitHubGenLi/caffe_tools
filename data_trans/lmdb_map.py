import sys, os
from os.path import normpath, join, split
from random import shuffle
import cv2
import numpy as np
from scipy import io
import lmdb
import argparse
parser = argparse.ArgumentParser(description='split data to training and testing subset.')
parser.add_argument('--caffe_root', type=str, help='caffe root folder', default='~/caffe/')
parser.add_argument('--txt', type=str, help='txt list file', default='train.txt')
parser.add_argument('--dst', type=str, help='destination dir to save lmdb', default='./lmdb')
args = parser.parse_args()
caffe_root = args.caffe_root
txt_fn = args.txt
dst_dir = args.dst
sys.path.insert(0, join(caffe_root, 'python'))
import caffe
def make_lmdb_map(txt_list, lmdb_dir = './', mat_field = 'map', shuf = True, mean = None, display = False):
    NUM_IDX_DIGITS = 10
    IDX_FMT = '{:0>%d' % NUM_IDX_DIGITS + 'd}'
    data_dir = os.path.split(txt_list)[0]
    with open(txt_list) as f:
        t = f.readlines()
    if len(t) == 0:
    	print 'empty in', txt_list
    	return
    if shuf:
        print 'shuffling data...'
        shuffle(t)
    imgs = []
    maps = []
    for i in t:
        t1, t2 = i.split()
        imgs.append(normpath(join(data_dir, t1)))
        maps.append(normpath(join(data_dir, t2)))

    lmdb_imgs_dir = os.path.join(lmdb_dir , 'lmdb_imgs')
    lmdb_maps_dir = os.path.join(lmdb_dir , 'lmdb_maps')
    
    #make images db
    if not os.path.exists(lmdb_imgs_dir):
        os.makedirs(lmdb_imgs_dir)
    imgs_db = lmdb.open(lmdb_imgs_dir, map_size=int(1e12))
    print 'converting images to lmdb...'
    with imgs_db.begin(write=True) as in_txn:
    	for idx, img_path in enumerate(imgs):
    		if display:
    			print idx+1, 'of',len(imgs)
    		img = cv2.imread(img_path)
    		if img is None:
    			print img_path,'not exists!'
    			return
    		if mean is not None:
    			img = img.astype(np.float32)
    			img -= mean
    			img = img.astype(np.float)
    		#rgb to bgr
    		if img.ndim == 3:
    			img = img.transpose([2, 0, 1])
    		else:
    			AttributeError("No. of dimensions (%d) not supported." % img.ndim)
    		img_data = caffe.io.array_to_datum(img)
    		in_txn.put(IDX_FMT.format(idx), img_data.SerializeToString())
    imgs_db.close()

    #now make maps_db
    if not os.path.exists(lmdb_maps_dir):
        os.makedirs(lmdb_maps_dir)
    maps_db = lmdb.open(lmdb_maps_dir, map_size=int(1e12))
    print 'converting mat to lmdb...'
    with maps_db.begin(write=True) as in_txn:
        for idx, map_path in enumerate(maps):
            if display:
                print 'mat', idx + 1, 'of', len(maps)
            map_data = io.loadmat(map_path)[mat_field]
            print map_data.shape
            map_data = np.expand_dims(map_data, axis=0)
            map_data = caffe.io.array_to_datum(map_data)
            in_txn.put(IDX_FMT.format(idx), map_data.SerializeToString())
    maps_db.close()

if __name__ == '__main__':
    make_lmdb_map(txt_fn, dst_dir, display = False, shuf=True)