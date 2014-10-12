# bradleypallen/ml_dev

## Description

The purpose of this image is to support the rapid development of machine learning applications using Vowpal Wabbit, a terascale online learning engine that can be used to train a variety of linear models for prediction, classification, LDA. etc. Perf is included to support the evaluation of such models by calculating different performance metrics such as ROC, F-measure, accuracy, etc.

This image is based on Ubuntu:latest. Source for vw and perf installed to /usr/local/src. Additional tools installed are emacs, g++, git, wget, curl and python. Pip, virtualenv and fabric installed for using python to orchestrate data ETL and prototype machine learning pipelines. fabfile.py provides a simple workflow for generating and evaluating models trained from data provided in CSV format.

## Usage

### Starting a container

    $ docker run -ti bradleypallen/ml-dev bash

### Using fabric to execute machine learning workflow tasks

Change to the pre-defined working directory ml_dev:

    $ cd /home/ml_dev
    
Then list the tasks:

    $ fab -l
    
Look at the Python source in fabfile.py and you will see what each of those tasks is doing. To build a logistic regression model for the breast cancer data, execute the following commands:

    $ fab build_data:data=./data/breast-cancer-wisconsin/breast-cancer-wisconsin.data
    $ fab train
    $ fab validate
    $ fab performance

Beyond that, you're probably best to work out using VW and perf, etc. on your own tasks in a way that calls those tools directly.

## License

MIT.
