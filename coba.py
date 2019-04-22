from __future__ import print_function
import tensorflow as tf

tensor = tf.constant([1, 2, 3, 4, 5, 6, 7])
print(tensor)

sess = tf.Session()
with sess.as_default():
	tensor_new = sess.run(tensor)
	print(tensor_new)
    #print_op = tf.print(tensor)

#tf.print(tensor,[tensor])
print('done')