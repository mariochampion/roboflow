# RoboFlow
## a semi-automated TensorFlow image classification explorer<br>in a python command line app.

(working on this right now: 2017-12-20)

## THE GOAL
of this project is to get a better sense for TensorFlow's classifier by automating the gathering of large amounts of similar images (by hashtag, such as "#robot" or "#hydrant" or whatever) which serve as re/training examples of various qualities, and to enable easy testing of different TensorFlow hyperparameter settings. The more you do this, the better the classifier becomes.

## THE PROCESS
According to the 'confidencemin' variable, the downloaded images are sorted into timestamped directories, which correspond to the labels in TensorFlow's 'tf_files/training_photos' directory. When there are enough well-classified* images in these 'testing_photos/sorted_{timestamp}/{labelname}" subdirectories, you can opt to then retrain the classifier. 

In this cycle of download & classify then QA re-sort & harvest & retrain, the classifier gets better and better at sorting to provide training data -- resulting, at some point, in an ability to be an as-automated-as-you-are-comfortable self-improving image classifier.

*well-classified means according to initial and periodic manual quality control re-sorting by you (or other humans). That is, before harvesting the robo-sorted images back into retraining, look through the 'testing_photos/sorted_{timestamp}/{labelname}' subdirs and delete the ones with which you disagree, which have fooled the classifier. Feel free to keep these for some other type of analysis, although any specific suggestion of how is still way beyond my fluency, but i would be very interested if you have insights. 

## LOG FILES
Speaking of later analysis, there are several log files with timestamps created along the way. One maps the downloaded images original name and url to the images new name -- which includes a timestamp and after classification 3 digits of its confidence number. Another tracks the classification model used, another the image name along with its percentage and seconds to classify, and another the images harvested from various "sorted_*" directories. take a look at them, wont ya?


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

#### software
* Python (2.7 - but i havent tried 3.x so that might work, too)
* TensorFlow -what i used: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/
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

All the code used in ROBOFLOW is contained in this git repository. First, cd into your TensorFlow directory
at the same level as "tf_files" and "scripts" and then clone the ROBOFLOW git repository.

```
git clone https://github.com/mariochampion/roboflow
```

And also...

```
until finished
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

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python 2.7](https://docs.python.org/2/index.html/) - The programming language
* [TensorFlow](https://www.tensorflow.org/) - An open-source software library for Machine Intelligence

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Mario Champion** - *Initial work* - [mariochampion](https://github.com/mariochampion)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Google's TensorFlow-for-poets2
* StackExchange
* Twilio sms/python tools
