from fabric.api import task, local
import csv, random

def record_to_vw(record, feature_fields, target_field):
	"""
	Convert a Python dictionary into a string in Vowpal Wabbit data format.
	"""
	vw_record = "%s |" % record[target_field]
	for f in feature_fields:
		vw_record += " %s:%s" % (f.replace(' ', '_'), record[f])
	return vw_record + "\n"	

@task
def prepare_data(data='data.csv', target_field='class', test_holdout=0.1, train='train.dat', validate='validate.dat'):
	"""
	Transform CSV data file into train/validate files in Vowpal Wabbit data format.
	"""
	records = list(csv.DictReader(open(data)))
	feature_fields = records[0].keys()
	feature_fields.remove(target_field)
	random.shuffle(records)
	split_idx = int(float(len(records))*test_holdout)
  	with open(train, "wb") as outfile:
		for record in records[split_idx:]:
			outfile.write(record_to_vw(record, feature_fields, target_field))
  	with open(validate, "wb") as outfile:
		for record in records[:split_idx]:
			outfile.write(record_to_vw(record, feature_fields, target_field))

@task
def train(data='train.dat', model='model.vw', predictions='predict.dat', passes=0):
	"""
	Create a Vowpal Wabbit model by training it on a training data set.
	"""
	if passes == 0:
		local("vw -d %s -f %s -p %s" % (data, model, predictions))
	else:
		local("vw -d %s -c --passes=%s -f %s -p %s" % (data, passes, model, predictions))

@task
def varinfo(data='train.dat', passes=0):
	"""
	Display the features in a Vowpal Wabbit model.
	"""
	if passes == 0:
		local("/usr/local/src/vowpal_wabbit/utl/vw-varinfo %s" % data)
	else:
		local("/usr/local/src/vowpal_wabbit/utl/vw-varinfo -c --passes=%s %s" % (passes, data))

@task
def validate(data='validate.dat', model='model.vw', predictions='predict.dat'):
	"""
	Validate a Vowpal Wabbit model by testing it on a validation data set.
	"""
	local("vw -d %s -i %s -p %s" % (data, model, predictions))

@task
def performance(predictions='predict.dat'):
	"""
	Display the performance of a Vowpal Wabbit model.
	"""
	# Load the index mappings schema
	local("perf < %s" % predictions)
