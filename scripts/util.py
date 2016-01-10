from datetime import datetime
import importlib
import subprocess
import os
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
import numpy as np

def float32(k):
    return np.cast['float32'](k)

def F1Score(y_true, y_pred):
    thres = 0.5
    f1 = [0] * y_true.shape[0]
    for i in range(y_true.shape[0]):
        f1[i] = f1_score(y_true[i,:], np.where(y_pred[i,:]> thres , 1, 0), average='micro')  
    return np.sum(f1)/1.0/y_true.shape[0]

def load_module(mod):
    return importlib.import_module(mod.replace('/', '.').split('.py')[0])


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def get_submission_filename():
    return "data/sub_{}.csv".format(datetime.now().replace(microsecond=0))

