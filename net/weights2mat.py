import numpy as np
import scipy.io as io
import sys
#options:
#caffe root folder
caffe_root = '/home/server002/zk/caffe/'
sys.path.insert(0, caffe_root + 'python/')
import caffe
#trained model
model_weights = '/home/server002/zk/github/dmil/examples/stage1/DS_iter_20000.caffemodel'
#deplot prototxt
net_deploy = '/home/server002/zk/github/dmil/examples/stage1/vgg_deploy.prototxt'
#saved .mat filename
sav_mat_fn = 'weights'

caffe.set_mode_cpu()
net = caffe.Net(net_deploy, model_weights, caffe.TEST)
weights = {}
for i in net.params:
	weights[i] = {'weights':net.params[i][0].data,'bias':net.params[i][1].data}
io.savemat(sav_mat_fn, weights)