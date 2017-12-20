# RoboFlow
## a semi-automated TensorFlow image classification explorer<br>in a python command line app.

(working on this right now: 2017-12-20)

## Purpose & Goal
RoboFlow was created to get a better sense for TensorFlow's image classifier by making it easier to gather 1000s of similar images by hashtag (such as "#robot" or "#robotart") to serve as re/training examples, and to enable easy testing of different TensorFlow hyperparameter settings for creating classifiers. specifically, tagged images are downloaded (right now from webstagram) and then sorted, according to a 'confidencemin' variable, into labeled sub-directories, which are periodically 'harvested' to retrain TensorFlow to create new classifiers. 

Issues, Contributions, and Pull Requests welcomed!


### 'basetag' concept
because you can use roboflow for many separate classifiers, you need to pick a term for the broad master classification or theme of your classifier (such as 'robots', or 'birds', or whatever) so that images, classifier models and more can be stored separately under that BASETAG directory.

## Bootstrapping
There is an initial bootstrap stage in which you must manually sort a minimum number of images to allow the first retraining to create the first classifier. This tool will help you download 1000s of images pretty easily. After that, subsequent cycles of downloading, classifying/auto-sorting, and harvesting sorted images into the training_photos/labeled_directories for another cycle of retraining is waaaaay more automated. 

## Guided Usage
```
python roboflow.py
```
## Advanced usage:
```
python roboflow.py [basetag] [imagequantity] [searchtag] [optional flowsteps]
```
### help:
```
python roboflow.py --help
```

### and dont forget to explore the config file. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

#### software
* Python (2.7 - but i havent tried 3.x so that might work, too)
* TensorFlow - what i used: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/ <br>
  but also at https://www.tensorflow.org/install/
* Terminal/Command Line familiarity
* Optional: Tensorboard (https://github.com/tensorflow/tensorboard)
* Optional: Twilio for txt msg notifications (https://www.twilio.com/sms)


#### permissions
* Internet Access
* Image downloading
* File and directory creation permissions


## Installing

First, you must install and test TensorFlow. Follow instructions at

```
https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/
```
or 

```
https://www.tensorflow.org/install/
```

Next, install the RoboFlow files contained in this git repository.<br>
Make sure to 'cd' into your TensorFlow directory at the same level as "tf_files" and "scripts" first.<br>
Then clone the RoboFlow git repository with:

```
git clone https://github.com/mariochampion/roboflow
```


Et voila, you are ready to explore!

### guided usage:
```
python roboflow.py
```
### advanced usage:
```
python roboflow.py [basetag] [imagequantity] [searchtag] [optional flowsteps]
```


End with an example of getting some data out of the system or using it for a little demo



## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```


## Built With

* [Python 2.7](https://docs.python.org/2/index.html/) - The programming language
* [TensorFlow](https://www.tensorflow.org/) - An open-source software library for Machine Intelligence

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Mario Champion** - *Initial work* - [mariochampion](https://github.com/mariochampion)

Contributions, Issues, and Pull requests Welcome!

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Google's TensorFlow-for-poets2
* Webstagram 
* StackExchange
* Twilio sms/python tools
