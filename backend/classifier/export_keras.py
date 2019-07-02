import tensorflow as tf
import os

def keras2tf(model_path = "models/keras/model.hdf5", export_path="models/tf/"):

    #extract model name from path
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    # create output path 
    export_dir = export_path + model_name
   # os.mkdir(export_dir)
    ## deactivate learning phase
    tf.keras.backend.set_learning_phase(0)
    ##load keras model
    model = tf.keras.models.load_model(model_path)

    # exporting as tf model
    with tf.keras.backend.get_session() as sess:
        tf.saved_model.simple_save(
            sess,
            export_dir,
            inputs={'input_image': model.input},
            outputs={t.name: t for t in model.outputs})


if __name__ == "__main__":
    keras2tf()