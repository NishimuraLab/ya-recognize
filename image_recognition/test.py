import tensorflow as tf

sess = tf.Session()
hello = tf.constant("hello tensorflow")
a = tf.constant(31)
b = tf.constant(11)
print sess.run(hello)
print sess.run(a+b)
