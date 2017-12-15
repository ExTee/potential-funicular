from keras.models import Model,Sequential
from keras.models import load_model
from keras.layers import Input, Conv2D, MaxPooling2D, Dense, Dropout, Activation, Flatten, ZeroPadding2D
from keras.utils import np_utils, plot_model # utilities for one-hot encoding of ground truth values
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.utils import plot_model


WEIGHTS_FILEPATH = 'cnn.best.weights.hdf5'
OUTPUT_PATH = 'cnn.model.hdf5'


INPUT_TRAIN_FOLDER = './patches/subset0'
INPUT_VALID_FOLDER = './patches/subset0'

def buildmodel():

	'''
	3. This convolution layer uses 64 10X10 convolutions with a 1X1 stride and 5X5 padding to further convolve the features folowed by a Rectified Linear Unit (ReLU) layer to set all negative elements to zero.
	4. The convolved features then go into the maximum pooling layer. The pooling layer cal- culates the maximum value of the feature over a region of the image so we can use the features for classification. This max pooling layer has a filter size of 3X3.


	'''
	batch_size = 10 #tbd


	DATA_SIZE = (512,512, 1)
	STRIDE_SIZE = (1,1)
	PADDING_SIZE = (5,5)
	POOLING_SIZE = (3,3)
	DROPOUT_PROB = 0.1


	#5x5 padding for data
	zeropadding_1 = ZeroPadding2D(padding = PADDING_SIZE, input_shape = DATA_SIZE)


	#First Convolutional Layer
	#CONV64, 10x10, 1x1 strides, relu
	conv_2d_layer_1 = Conv2D(filters = 64, kernel_size = 10, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')

	#3x3 Pooling
	pool_1 = MaxPooling2D(pool_size = POOLING_SIZE)

	#10% dropout
	drop_1 = Dropout(0.1)


	#Second convolutional layer
	zeropadding_2 = ZeroPadding2D(padding = PADDING_SIZE, input_shape = DATA_SIZE)

	#CONV192, 5x5, 1x1 strides, relu
	conv_2d_layer_2 = Conv2D(filters = 192, kernel_size = 5, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')

	#2x2 Pooling
	pool_2 = MaxPooling2D(pool_size = (2,2))

	#10% dropout
	drop_2 = Dropout(0.1)


	#Convolutional layers 3 to 7
	#CONV384, 5x5, 1x1 strides, relu, NO PADDING
	conv_2d_layer_3 = Conv2D(filters = 384, kernel_size = 5, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')
	conv_2d_layer_4 = Conv2D(filters = 256, kernel_size = 3, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')
	conv_2d_layer_5 = Conv2D(filters = 256, kernel_size = 3, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')
	conv_2d_layer_6 = Conv2D(filters = 256, kernel_size = 3, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')
	conv_2d_layer_7 = Conv2D(filters = 128, kernel_size = 3, padding = 'valid', strides = STRIDE_SIZE, activation = 'relu')

	pool_3 = MaxPooling2D(pool_size = (3,3))

	drop_3 = Dropout(0.5)

	#Fully connected layer with softmax

	fc_layer = Dense(2, activation = 'softmax')

	model = Sequential()
	model.add(zeropadding_1)
	model.add(conv_2d_layer_1)
	model.add(pool_1)
	model.add(drop_1)

	model.add(zeropadding_2)
	model.add(conv_2d_layer_2)
	model.add(pool_2)
	model.add(drop_2)

	model.add(conv_2d_layer_3)
	model.add(conv_2d_layer_4)
	model.add(conv_2d_layer_5)
	model.add(conv_2d_layer_6)
	model.add(conv_2d_layer_7)
	model.add(pool_3)
	model.add(drop_3)

	model.add(fc_layer)

	model.compile(loss='categorical_crossentropy', # using the cross-entropy loss function
				  optimizer='adam', # using the Adam optimiser
				  metrics=['accuracy']) # reporting the accuracy

	return model
	#plot_model(model, to_file='model.png', show_shapes = True, show_layer_names = False)

def generate_images():
	#the split is performed beforehand
	train_datagen = ImageDataGenerator()
	valid_datagen = ImageDataGenerator()

	train_generator = train_datagen.flow_from_directory(
        INPUT_TRAIN_FOLDER,
        target_size=(152,152),
        batch_size=32,
        classes=['benign','cancer']
        class_mode='binary')

	valid_generator = test_datagen.flow_from_directory(
        INPUT_VALID_FOLDER,
        target_size=(152,152),
        batch_size=32,
        classes=['benign','cancer']
        class_mode='binary')



	return train_generator, valid_generator


def train_model(model):

	#Model parameters
	batch_size = 32
	num_epochs = 100

	checkpoint = ModelCheckpoint(weights_filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
	
	stopping = EarlyStopping(monitor='val_acc', min_delta=0.0007, patience=10, verbose=1, mode='auto')
	
	callbacks_list = [checkpoint, stopping]

	print("Training CNN")

	train_generator, valid_generator = generate_images()


	model.fit_generator( train_generator,
		batch_size=batch_size, epochs=num_epochs,
		validation_data= valid_generator,
		verbose=1,callbacks = callbacks_list)

	#save the model

	model.save(output_path)

	print("Model trained and saved as {}".format(output_path))




def main():
	my_model = buildmodel()

	train_model(my_model)


if __name__ == '__main__':
	main()
