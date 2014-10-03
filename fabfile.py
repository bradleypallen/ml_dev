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
def prepare_data(data='data.csv', target_field='class', validate_holdout=0.1, train='train.dat', validate='validate.dat'):
	"""
	Transform CSV data file into train/validate files in Vowpal Wabbit data format.
	"""
	records = list(csv.DictReader(open(data)))
	feature_fields = records[0].keys()
	feature_fields.remove(target_field)
	random.shuffle(records)
	split_idx = int(float(len(records))*validate_holdout)
  	with open(train, "wb") as outfile:
		for record in records[split_idx:]:
			outfile.write(record_to_vw(record, feature_fields, target_field))
  	with open(validate, "wb") as outfile:
		for record in records[:split_idx]:
			outfile.write(record_to_vw(record, feature_fields, target_field))

@task
def train(data='train.dat', model='model.vw', predictions='predict.dat', passes=1, logistic=True):
	"""
	Create a Vowpal Wabbit model by training it on a training data set.
	"""
	if logistic:
		local("vw -d %s -c --passes=%s -f %s -p %s --loss-function=logistic --link=logistic" % (data, passes, model, predictions))
	else:
		local("vw -d %s -c --passes=%s -f %s -p %s" % (data, passes, model, predictions))

@task
def varinfo(data='train.dat', passes=1, logistic=True):
	"""
	Display the features in a Vowpal Wabbit model.
	"""
	if logistic:
		local("/usr/local/src/vowpal_wabbit/utl/vw-varinfo -c --passes=%s  --loss-function=logistic %s" % (passes, data))
	else:
		local("/usr/local/src/vowpal_wabbit/utl/vw-varinfo -c --passes=%s %s" % (passes, data))

@task
def validate(data='validate.dat', model='model.vw', predictions='predict.dat', logistic=True):
	"""
	Validate a Vowpal Wabbit model by testing it on a validation data set.
	"""
	if logistic:
		local("vw -d %s -i %s -r %s --loss_function=logistic" % (data, model, predictions))
	else:
		local("vw -d %s -i %s -r %s" % (data, model, predictions))

@task
def performance(data='validate.dat', predictions='predict.dat', metric=None):
	"""
	Display the performance of a Vowpal Wabbit model.
	"""
	local("cut -d ' ' -f 1 %s | sed -e 's/^-1/0/' > gold.dat" % data)
	local("/usr/local/src/vowpal_wabbit/utl/logistic -0 %s > probabilities.dat" % predictions)
	if metric:
		local("perf -%s -files gold.dat probabilities.dat" % metric)
	else:
		local("perf -files gold.dat probabilities.dat")
