# RoboFlow
##### jump to: <a href="https://mariochampion.github.io/roboflow">RoboFlow</a> | <a href="https://mariochampion.github.io/roboflow/help">Help</a> | <a href="https://mariochampion.github.io/roboflow/helpmore">DetailedHelp</a>



## Purpose & Goal
RoboFlow was created to get a better sense for TensorFlow's image classifier by making it easier to gather 1000s of similar images by hashtag (such as "#robot" or "#robotart") to serve as re/training examples, and to enable easy testing of different TensorFlow hyperparameter settings for creating classifiers. specifically, tagged images are downloaded (right now from webstagram) and then sorted, according to a 'confidencemin' variable, into labeled sub-directories, which are periodically 'harvested' to retrain TensorFlow to create new classifiers. 

Issues, Contributions, and Pull Requests welcomed!


### 'basetag' concept
because you can use roboflow for many separate classifiers, you need to pick a term for the broad master classification or theme of your classifier (such as 'robots', or 'birds', or whatever) so that images, classifier models and more can be stored separately under that BASETAG directory. You will do this in either the guided or advanced usages (see below).

## Bootstrapping
There is an initial bootstrap stage in which you must manually sort a minimum number of images to allow the first retraining to create the first classifier per basetag. This tool will help you download 1000s of images pretty easily. After that first manual sorting, subsequent cycles of downloading, classifying/auto-sorting, and harvesting sorted images into the training_photos/labeled_directories for another cycle of retraining is waaaaay more automated. 
#### hint: you can skip this step with a 1.4 gb download of robot images to place into training_photos/ 
```
https://drive.google.com/file/d/1zvTq5vKqME7sW9O8lEtgn-Wosoavc2gi/view?usp=sharing
```


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

#### software
* Python (2.7 - but i havent tried 3.x so that might work, too)
* TensorFlow - learn about it: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/ <br>
install shortcut: https://github.com/googlecodelabs/tensorflow-for-poets-2 <br>
or also at https://www.tensorflow.org/install/
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

FINALLY and CRITICALLY, you must change one line in TensorFlow's scripts/retrain.py file.<br>
(see https://github.com/mariochampion/roboflow/issues/3)<br>
simply go to the literal last line of retrain.py's main() function, around line 1144 and add
```
############################################
# this line added because stdout not available / no return from main
# See https://github.com/tensorflow/tensorflow/issues/3047 
f.write(str("_acc"+str(test_accuracy*100)[:5]) + '\n')
```


Et voila, you are ready to explore!

## Guided usage:
```
python roboflow.py
```
## Advanced usage:
```
python roboflow.py [basetag] [imagequantity] [searchtag] [optional flowsteps]
```
for example:
```
python roboflow.py robots 200 robotart classify
```

## Help: (or <a href="https://mariochampion.github.io/roboflow/help">read the help docs online</a>)
```
python roboflow.py --help
```

### and dont forget to explore the <a href="../robo_config.py">config file.</a> 




## Built With

* [Python 2.7](https://docs.python.org/2/index.html/) - The programming language
* [TensorFlow](https://www.tensorflow.org/) - An open-source software library for Machine Intelligence


## Contributing

I am very open to issues and pull requests. Looking for a place to start helping?<br>
https://github.com/mariochampion/roboflow/issues

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
