"""Conv Nets training script."""
import click
import numpy as np
import pandas as pd
import data
import util
from nn import create_net

def string_submit(x):
	y = [str(m) for m in x]
	y = ' '.join(y)
	return y


@click.command()
@click.option('--cnf', default='configs/c_256_4x4_32.py', show_default=True,
              help='Path or name of configuration module.')
@click.option('--classes', default = 1, show_default = True)
@click.option('--weights_from', default=None, show_default=True,
              help='Path to initial weights file.')
@click.option('--predict', default =0,show_default = True)
def main(cnf, classes, weights_from, predict):

    config = util.load_module(cnf).config
    files = data.get_image_files(config.get('train_dir'))
    names = data.get_names(files)
    names = [int(x) for x in names ]
    data.classes = int(classes)
    labels = data.get_labels(names)
    net = create_net(config)
    
    print files.shape
    print labels.shape
    if predict : 
    	if weights_from is None:
        	weights_from = config.weights_file
    	else:
        	weights_from = str(weights_from)
	print weights_from    
    	try:
        	net.load_params_from(weights_from)
        	print("loaded weights from {}".format(weights_from))
    	except IOError:
        	print("couldn't load weights starting from scratch")
    if not predict:
    	print("fitting ...")
    	net.fit(files, labels)
    else:
	print("predicting ...")
    	test_files = data.get_image_files(config.get('test_dir'))
    	y_pred = net.predict(test_files)
	y_pred = y_pred.transpose()
	print y_pred
        y_pred = np.clip(np.round(y_pred),
                         np.min(labels), np.max(labels)).astype(int)
        #print y_pred
	submission_filename = util.get_submission_filename()
        image_files = data.get_image_files(config.get('test_dir'))
        names = data.get_names(image_files)
        image_column = pd.Series(names, name='photo_id')
        level_column = pd.DataFrame(y_pred)#name='labels')
	level_column = level_column.apply(lambda x : string_submit(x))        
        predictions = pd.concat([image_column, level_column], axis=1)
        print("tail of predictions file")
        print(predictions.tail())
	predictions.columns = ['photo_id', 'labels']
        predictions.to_csv(submission_filename, index=False)
        print("saved predictions to {}".format(submission_filename))
if __name__ == '__main__':
    main()

