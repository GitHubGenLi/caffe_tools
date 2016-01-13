###CAFFE_DATA:
=====
####lmdb_map.py  
convert image-mat pair into lmdb according to a text file

usage:  

```bash
python lmdb_map.py --caffe_root CAFFE_ROOT --txt data.txt --dst DST_DIR
```
* use `python lmdb_map.py --help` for help

=====
####split_data.py

split dataset into training and testing subset according to text file

* usage:

```bash
python split_data.py --txt data.txt --ratio 0.1
```

* use `python split_data.py --help` for help