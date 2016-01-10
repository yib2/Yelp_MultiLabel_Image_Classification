# Kaggle Yelp Multi-label Image Classification
Code  adapted from https://github.com/sveitser/kaggle_diabetic, the Team o_O solution for the Kaggle Diabetic Retinopathy Detection Challenge. 


### Preprocessing:
	substract mean and divide by std of all images.
	no augmentation  at first, since data is quite large enough.

## Stage 1 :
	Use 20% of data to tune parameters for CNN, since it takes more than 1 hours per epochs for full data , customer the F1 score.  Approach the multi-label problem as regression problem 
	
## Stage 2 :


