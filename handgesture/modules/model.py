#deprecated module, new model created and trained in the Jupyter Notebook

#Folder used to create a pretrained model and save it for later use
# Import of keras model and hidden layers for our convolutional network
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Dense, Flatten

def constructmodel():
    # Construction of model
    print("Status : constructing model")
    model = Sequential()
    model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(120, 320, 1))) 
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu')) 
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    print("Status : Done")
    return model


def trainmodel(currentpath, model, X_train, y_train, X_test, y_test):
    print("Status : Training Model")
    # Configures the model for training
    model.compile(optimizer='adam', # Optimization routine, which tells the computer how to adjust the parameter values to minimize the loss function.
                loss='sparse_categorical_crossentropy', # Loss function, which tells us how bad our predictions are.
                metrics=['accuracy']) # List of metrics to be evaluated by the model during training and testing.

    # Trains the model for a given number of epochs (iterations on a dataset) and validates it.
    model.fit(X_train, y_train, epochs=5, batch_size=64, verbose=2, validation_data=(X_test, y_test))

    print("Status : Model Trained - Saving Model")
    # Save entire model to a HDF5 file
    model.save(currentpath + "\\data\\handrecognition_model.h5")
