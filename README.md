# Kaggle Yelp Multi-label Image Classification
Python Code adapted from https://github.com/sveitser/kaggle_diabetic, the Team o_O solution for the Kaggle Diabetic Retinopathy Detection Challenge. 

## Preprocessing:
Substract mean and divide by std of all images.
No augmentation at first, since data is quite large enough.

## Stage 1 :
Use 20% of data to tune parameters for CNN, since it takes more than 1 hours per epochs for full data , customer the F1 score.  Approach the multi-label problem as regression problem 
	
## Stage 2 :

Training a big CNN from scratch is time-consuming, 
	1.fine tuning with pre-trained model and extract features from the layers fc6, fc7 with Alexnet
	2. average the features for data with same label. 
	3. train a linear svm to do the classification 
	
This method achieves 0.81 F1 score on private LB.