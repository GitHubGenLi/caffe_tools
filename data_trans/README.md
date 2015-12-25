###lmdb_map:
convert image-mat pair into lmdb according to a text file  
example of text file `ex.txt`:  
* input:  text file containing image-mat pairs  
  
> ex1.png ex1.mat  
> ex2.png ex2.mat  
  
 
###split_dset
split dataset into training and testing subset according to text file  

* input: a text file including dataset **data** and **label** pairs  

* output: two text files containing training and testing **data** and **testing** pairs respectively  

* options:  
1.ratio: fraction to split dataset
