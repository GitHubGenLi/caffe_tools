from random import shuffle
import argparse
from os.path import normpath, join, split
parser = argparse.ArgumentParser(description='split data to training and testing subset.')
parser.add_argument('txt', help='txt file that data item stored')
parser.add_argument('ratio', type=float, help='split ration')
args = parser.parse_args()
txt_fn = args.txt
ratio = args.ratio
txt_folder = split(txt_fn)[0]
test_txt_fn = 'test.txt'
train_txt_fn = 'train.txt'
with open(txt_fn, 'r') as txt:
	lines = txt.readlines()
txt.close()
shuffle(lines)
n = len(lines)
n_test = int(n * ratio)
n_train = n - n_test
print n_train, 'training images and ', n_test, 'testing images'
train_txt = open(join(txt_folder, train_txt_fn), 'w')
test_txt  = open(join(txt_folder, test_txt_fn), 'w')
print type(test_txt)
print 'writing txt into '+join(txt_folder, train_txt_fn)+' and '+join(txt_folder, test_txt_fn)+' respectively...'
for i in range(n):
    if i < n_train:
    	train_txt.write(lines[i])
    else:
    	test_txt.write(lines[i])
test_txt.close()
train_txt.close()