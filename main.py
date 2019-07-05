import unet_model
from data_helper import dataGenerator,load_data_Kfold, get_items, test_file_reader, plot_imgs , saveResult, plot_segm_history
#import ipdb
import numpy as np
from keras.callbacks import ModelCheckpoint
import time

start_time=time.time() 


BATCH_SIZE = 2
        
data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                   # vertical_flip=True,
                    fill_mode='nearest')

im_path = '/lustre/home/d167/s1137563/Paolo_repository/unet/data/membrane/train/image'
label_path = '/lustre/home/d167/s1137563/Paolo_repository/unet/data/membrane/train/label'
im_test = '/lustre/home/d167/s1137563/Paolo_repository/unet/data/membrane/test'

k = 2
seed = 1

#Create folds
x_train,x_validation,y_train,y_validation = load_data_Kfold(im_path,label_path,k)

#Load model
model = unet_model.unet()
model_filename = 'segm_model_v0.h5'
callback_checkpoint = ModelCheckpoint(
    model_filename, 
    verbose=1, 
    monitor='val_loss', 
    save_best_only=True,
)

cv_losses=[]
cv_acc=[]
#CV and training
for fold_number in range(k):
    x_training = get_items(x_train[fold_number])
    y_training = get_items(y_train[fold_number])
    x_valid = get_items(x_validation[fold_number])
    y_valid = get_items(y_validation[fold_number])
    print('Training fold' + str(fold_number))
    generator = dataGenerator(BATCH_SIZE, x_training,y_training,data_gen_args,seed = 1) 
    history=model.fit_generator(generator,steps_per_epoch=len(x_training)/BATCH_SIZE,epochs=10,verbose=1,validation_data = (x_valid,y_valid), callbacks=[callback_checkpoint])
    figure = plot_segm_history(history, fold_number) #COMMENTED OUT BECAUSE OF GPU - TO BE FIXED
 
testGen = test_file_reader(im_test)


model.load_weights(model_filename)
y_pred = model.predict(x_valid)

images= plot_imgs(org_imgs=x_valid, mask_imgs=y_valid, pred_imgs=y_pred, nm_img_to_plot=9) # COMMENTED OUT BECAUSE OF GPU ERROR - TO BE FIXED


results = model.predict_generator(testGen,10,verbose=1)
saveResult(im_test,results) # COMMENTED OUT DUE TO GPU - TO BE FIXED


print("--- %s seconds ---" % (time.time() - start_time))
