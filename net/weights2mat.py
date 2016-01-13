import numpy as np
import scipy.io as io
import sys
import argparse
from os.path import normpath, join, split
#options:
#caffe root folder
parser = argparse.ArgumentParser(description='transform model weights to mat')
parser.add_argument('--caffe_root', type=str, help='caffe root folder', default='~/caffe/')
parser.add_argument('--model', type=str, help='source model', default='model.caffemodel')
parser.add_argument('--deploy', type=str, help='net deplot prototxt', default='deploy.prototxt')
parser.add_argument('--mat', type=str, help='mat file to save weights', default='model.caffemodel')
args = parser.parse_args()

caffe_root = args.caffe_root
sys.path.insert(0, join(caffe_root, 'python'))
import caffe
#trained model
model_weights = args.model
#deplot prototxt
net_deploy = args.deploy
#saved .mat filename
sav_mat_fn = args.mat

caffe.set_mode_cpu()
net = caffe.Net(net_deploy, model_weights, caffe.TEST)
weights = {}
for i in net.params:
	weights[i] = {'weights':net.params[i][0].data,'bias':net.params[i][1].data}
io.savemat(sav_mat_fn, weights)