import sys, os
import numpy as np
import pandas as pd
import collections
import os, random
def submit_vote_by_label(fn, file_pid_to_bid):
	test_id_labels = pd.read_csv('../data/sample_submission.csv')
	#test_pid_bid = pd.read_csv('../data/test_photo_to_biz.csv')
	test_pid_bid = pd.read_csv(file_pid_to_bid)
	test_id_labels['labels']= test_id_labels['labels'].apply(lambda x : sorted(np.random.choice(range(9), 9,  replace=False))).apply(lambda x : ' '.join([ str(xx) for xx in x]))
	for i in range(9):
		bench = pd.read_csv(fn)
		sample = bench
		sample['labels'] = bench['labels'].apply(str).apply(lambda x : x.split()[i])
		sample.to_csv('sub{0}.csv'.format(i), index=False)
		count = 0
		sub1 = pd.read_csv('sub{0}.csv'.format(i), index_col = 0)
		tmp1 = test_pid_bid.groupby('business_id')['photo_id'].apply(list)
		for bid in test_id_labels.business_id.values.tolist():
		    #print bid
		    img_list  = tmp1[bid]
		    labels = [sub1.loc[x]['labels'] for x in img_list]
		    if count % 100 == 0:
		        print count
		    count = count + 1
		    #print np.sum(labels)/1.0/len(labels)
		    #print labels
		    if (np.sum(labels) < 0.3 * len(labels)):
		        tmp =  test_id_labels.loc[test_id_labels['business_id'] == bid, 'labels'].apply(str).apply(lambda x : x.split()).values.tolist()[0]
		        #tmp = [int(x) for x in tmp]
		        #print tmp, classes-1
		        # iterable , tmp.remove does it inplace, need to pass tmp to join
		        tmp.remove(str(i))
		        #print test_id_labels.loc[test_id_labels['business_id'] == bid, 'labels']
		        test_id_labels.loc[test_id_labels['business_id'] == bid, 'labels'] = ' '.join(tmp)
		        #print test_id_labels.loc[test_id_labels['business_id'] == bid, 'labels']

	test_id_labels.to_csv('submission.csv',index=False)


def submit_vote_totally(fn):
	test_id_labels = pd.read_csv('../data/sample_submission.csv')
	test_pid_bid = pd.read_csv('../data/test_photo_to_biz.csv')
	test_id_labels['labels']= test_id_labels['labels'].apply(lambda x : sorted(np.random.choice(range(9), 9,  replace=False))).apply(lambda x : ' '.join([ str(xx) for xx in x]))
	bench = pd.read_csv(fn, index_col = 0)

	count = 0
	tmp1 = test_pid_bid.groupby('business_id')['photo_id'].apply(list)
	for bid in test_id_labels.business_id.values.tolist():
	    #print bid
	    img_list  = tmp1[bid]
	    labels = [bench.loc[x]['labels'] for x in img_list]
	    if count % 100 == 0:
	        print count
	    count = count + 1

	    counter = collections.Counter(labels)
	    best = counter.most_common(1)[0][0]
	    test_id_labels.loc[test_id_labels['business_id'] == bid, 'labels'] = best
	test_id_labels.to_csv('submission.csv',index=False)

def getTopBid(bid_list, pid, test_pid_bid, pid_to_labels):
	ranks = []
	for bid in bid_list:
		bid_photo_list = test_pid_bid.groupby('business_id')['photo_id'].apply(list)
		photos = bid_photo_list[bid]
		labels = [ pid_to_labels.loc[x]['labels'] for x in photos]	
		counter = collections.Counter(labels)
		rank = counter[pid_to_labels.loc[pid]['labels']]
		ranks.append((bid, rank))
	ranks = sorted(ranks, key = lambda x : x[1], reverse = True)
	return ranks[0][0]


def make_one_photo_per_bid(fn):
	'''
		too slow 
	'''
	if not os.path.exists('test_one_photo_per_bid.csv'):
		test_id_labels = pd.read_csv('../data/sample_submission.csv')
		test_pid_bid = pd.read_csv('../data/test_photo_to_biz.csv')
		test_id_labels['labels']= test_id_labels['labels'].apply(lambda x : sorted(np.random.choice(range(9), 9,  replace=False))).apply(lambda x : ' '.join([ str(xx) for xx in x]))
		bench = pd.read_csv(fn, index_col = 0)
		count = 0
		photo_bid_list = test_pid_bid.groupby('photo_id')['business_id'].apply(list)
		bid_photo_list = test_pid_bid.groupby('business_id')['photo_id'].apply(list)
		result_bid = []
		for pid in test_pid_bid.photo_id.unique():
		    bid_list  = photo_bid_list[pid]
		    best_bid =  random.choice(bid_list)#getTopBid(bid_list, pid, test_pid_bid, bench)
		    if count % 100 == 0:
		        print count
		    count = count + 1
		    result_bid.append(best_bid)
		x1 = pd.Series(test_pid_bid['photo_id'].unique())
		y1 = pd.Series(result_bid)
		r = pd.concat([x1, y1], axis = 1)
		r.columns = ['photo_id', 'business_id']
		r.to_csv('test_one_photo_per_bid.csv',index=False)
	else:
		submit_vote_by_label(fn, 'test_one_photo_per_bid.csv')	

submit_vote_by_label(sys.argv[1], '../data/test_photo_to_biz.csv')

