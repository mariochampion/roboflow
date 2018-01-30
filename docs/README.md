# RoboFlow
##### jump to: <a href="https://mariochampion.github.io/roboflow">RoboFlow</a> | <a href="https://mariochampion.github.io/roboflow/help">Help</a> | <a href="https://mariochampion.github.io/roboflow/helpmore">DetailedHelp</a>


## Purpose & Goal
RoboFlow was created to get a better sense for TensorFlow's image classifier by making it easier to gather 1000s of similar images by hashtag (such as "#robot" or "#robotart") to serve as re/training examples, and to enable easy testing of different TensorFlow hyperparameter settings for creating classifiers. specifically, tagged images are downloaded (your choice of Imgur API or Webstagram) and then sorted, according to a 'confidencemin' variable, into labeled sub-directories, which are periodically 'harvested' to retrain TensorFlow to create new classifiers.<br>

![roboflow start](http://mariochampion.com/roboflow/roboflow_cover_640.png)


### downloads sources (imgur api or webstagram)
as of now, choose in the config file from two useful (and randomly non-responsive) sources:<br>
Imgur API (much quicker, fewer tags, requires you get a free API key) or<br>
webstagram (slower, more tags, no API key required)

## 'BASETAG' concept
because you can use roboflow for many separate classifiers, you need to pick a term for the broad master classification or theme of your classifier (such as 'robots', or 'birds', or whatever) so that images, classifier models and more can be stored separately under that BASETAG directory. You will do this in either the guided or advanced usages (see below).


## Bootstrapping
There is an initial bootstrap stage in which you must manually sort a minimum number of images to allow the first retraining to create the first classifier per basetag. This tool will help you download 1000s of images pretty easily. After that first manual sorting, subsequent cycles of downloading, classifying/auto-sorting, and harvesting sorted images into the training_photos/labeled_directories for another cycle of retraining is waaaaay more automated. 
#### hint: you can skip this step with a 1.4 gb download of robot images to place into training_photos/ 
```
https://drive.google.com/file/d/1zvTq5vKqME7sW9O8lEtgn-Wosoavc2gi/view?usp=sharing
```


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#### PREREQUISITES
#### software
* Python (2.7 - but i havent tried 3.x so that might work, too) (<a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>)
* TensorFlow - learn about it: <a href="https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/">https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/</a> <br>
install shortcut: <a href="https://github.com/googlecodelabs/tensorflow-for-poets-2">https://github.com/googlecodelabs/tensorflow-for-poets-2</a><br>
or also at <a href="https://www.tensorflow.org/install/">https://www.tensorflow.org/install/</a>
* Terminal/Command Line familiarity
* <b>Optional</b>: Imgur API Client-ID (<a href="https://apidocs.imgur.com/">https://apidocs.imgur.com/</a>)<br>
 ** added to your ENVIRONMENT variables as 'IMGURAPI_ID', see config file line 59<br>
 ** <a href="http://osxdaily.com/2015/07/28/set-enviornment-variables-mac-os-x/">http://osxdaily.com/2015/07/28/set-enviornment-variables-mac-os-x/</a>
* <b>Optional</b>: Tensorboard (<a href="https://github.com/tensorflow/tensorboard">https://github.com/tensorflow/tensorboard</a>)
* <b>Optional</b>: Twilio for txt msg notifications (<a href="https://www.twilio.com/sms">https://www.twilio.com/sms</a>)
#### permissions
* Internet Access
* Image downloading
* File and directory creation permissions
* Create ENVIRONMENT variables in ~./bash_profile (or equivalent)


## Installing
You will need tensorflow, the image classification codelab, and then roboflow:<br>
STEP 1 (to get tensorflow)
```
https://www.tensorflow.org/install/
```
STEP 2 (to get the image classification setup)
```
https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/
```

STEP 3 (to get the exploration/semi-automation tool)<br>
Make sure to 'cd' into your TensorFlow directory at the same level as "tf_files" and "scripts" first.<br>
Then clone the RoboFlow dirs/files with:

```
git clone https://github.com/mariochampion/roboflow
```

FINALLY and CRITICALLY, you must change one line in TensorFlow's scripts/retrain.py file.<br>
(see https://github.com/mariochampion/roboflow/issues/3)<br>
simply go to the literal last line of <b>tensorflow-for-poets-2/scripts/retrain.py</b>'s main() function, around line 1144 and add
```
############################################
# this line added because stdout not available / no return from main
# See https://github.com/tensorflow/tensorflow/issues/3047 
f.write(str("_acc"+str(test_accuracy*100)[:5]) + '\n')
```

Your directories should look like this:
```
├── tensorflow
|  ├── roboflow
|  ├── scripts
|  ├── tf_files
|  |  ├── bottlenecks
|  |  ├── models
|  |  ├── testing_photos
|  |  |  ├── [autogenerated basetag dirs...]
|  |  ├── training_photos
|  |  |  ├── [autogenerated basetag dirs...]
|  |  ├── training_summaries
|  |  |  ├── [autogenerated basetag dirs...]
```

Et voila, you are ready to explore!


## Guided usage:
```
python roboflow.py
```
#### As a shortcut, add an alias in your .bash_profile to launch it via alias 'roboflow':
```
alias roboflow="cd path/to/dir/roboflow/;python roboflow.py"
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
#### and dont forget to explore the <a href="https://github.com/mariochampion/roboflow/blob/master/robo_config.py">config file.</a> 


--------------------------------------------------------------------------------


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
* Imgur API (altho originally from Webstagram )
* StackExchange
* Twilio sms/python tools
