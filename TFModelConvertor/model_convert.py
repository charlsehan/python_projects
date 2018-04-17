from keras.models import load_model
from keras import backend as K
import tensorflow as tf
from tensorflow.python.tools import freeze_graph, optimize_for_inference_lib

MODEL_NAME = 'cat_vs_dog_model'
MODEL_FILE = 'model-tune-02-0.0373.hdf5'

model = load_model(MODEL_FILE)

#for i, layer in enumerate(model.layers):
#    print(i, layer.name)

#for n in tf.get_default_graph().as_graph_def().node:
#    print(n.name)


input_node_names = ['input_1']
output_node_name = 'dense_1/Sigmoid'


tf.train.write_graph(K.get_session().graph_def, 'out',
                     MODEL_NAME + '_graph.pbtxt')

tf.train.Saver().save(K.get_session(), 'out/' + MODEL_NAME + '.chkp')

freeze_graph.freeze_graph('out/' + MODEL_NAME + '_graph.pbtxt', None,
                          False, 'out/' + MODEL_NAME + '.chkp', output_node_name,
                          "save/restore_all", "save/Const:0",
                          'out/frozen_' + MODEL_NAME + '.pb', True, "")

input_graph_def = tf.GraphDef()
with tf.gfile.Open('out/frozen_' + MODEL_NAME + '.pb', "rb") as f:
    input_graph_def.ParseFromString(f.read())

output_graph_def = optimize_for_inference_lib.optimize_for_inference(
    input_graph_def, input_node_names, [output_node_name],
    tf.float32.as_datatype_enum)

with tf.gfile.FastGFile('out/opt_' + MODEL_NAME + '.pb', "wb") as f:
    f.write(output_graph_def.SerializeToString())

print("graph saved!")



