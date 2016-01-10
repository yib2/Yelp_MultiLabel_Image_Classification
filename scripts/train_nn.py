"""Conv Nets training script."""
import click
import numpy as np

import data
import util
from nn import create_net


@click.command()
@click.option('--cnf', default='configs/c_512_4x4_32.py', show_default=True,
              help='Path or name of configuration module.')
@click.option('--weights_from', default = 'weights/c_256_4x4_32/best/0020_2016-01-08-10-45-25_0.186856225133.pkl', show_default = True,
            help='weight for nn')

@click.option('--classes', default = 1, show_default = True)
def main(cnf, classes):

    config = util.load_module(cnf).config
    files = data.get_image_files(config.get('train_dir'))
    names = data.get_names(files)
    names = [int(x) for x in names ]
    labels = data.get_labels(names, int(classes))
    net = create_net(config)

    try:
        net.load_params_from(weights_from)
        print("loaded weights from {}".format(weights_from))
    except IOError:
        print("couldn't load weights starting from scratch")

    #print("fitting ...")
    #net.fit(files, labels)
    print("predicting ...")
    test_files = data.get_image_files(config.get('test_dir'))
    net.predict(test_files)
if __name__ == '__main__':
    main()

