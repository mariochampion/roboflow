#!/usr/bin/env python
## ===================================================================
## ROBOFLOW - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/roboflow
## released under the Apache License 2.0. (http://www.apache.org/licenses/LICENSE-2.0)
## and depends on many contributions from the internets, stackexchange, twilio, 
## and of course and especially the Google TensorFlow for Poets codelab:
##     tutorials: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/ 
##     code: https://github.com/googlecodelabs/tensorflow-for-poets-2
## 
## ROBOFLOW scripts were  written by mario champion (mariochampion.com) as an exercise to learn 
## more python(2.7) file/dir manipulations, in a commandline driven app, and to better understand the
## Google's TensorFlow image classification elements and hyperparameter effects.
##
## please open issues and pull requests and comments
## thanks and always remember: this robot loves you. 
## boop boop!!!
## ===================================================================


import robo_config as cfg

#################################
def helper(which):

  print "Enter:"
  if which == "summ":
    print "[helpmore] for more detailed help,"
  else:
    print "[h] for LESS detailed help," 
  print "[g] for a guided setup, or "
  print "[q] to quit... "
  help_input = raw_input()

  return help_input
  
  
#################################
def summary():

  	
  print "-----------------------------------------"
  print cfg.color.cyan + "ROBOFLOW: help" + cfg.color.white
  print'''-----------------------------------------
This roboflow guide assumes you have at least passing familiarity with TensorFlow:
\thttps://codelabs.developers.google.com/codelabs/tensorflow-for-poets/
\thttps://www.tensorflow.org/tutorials/image_retraining
'''
  print cfg.color.cyan + "HOW TO USE:" + cfg.color.white
  print "guided:\t\t'python " + cfg.download_script +"'"
  print "advanced:\t'python " + cfg.download_script + " robots 200 robotart download'"
  print "\t\t'python "+ cfg.download_script + " [basetag] [imagequantity] [searchtag] [optional flowsteps]'"
  print cfg.color.cyan +"PARAMETERS:"+cfg.color.white
  print '''
basetag: \tthe master classification tag or theme ('robots' or 'birds' or whatever)'''
  print "imagequantity:\tan integer between 0 and "+str(cfg.imgnum_maxpercycle)+", to not hammer other people's servers"
  print '''searchtag:\tthe searchterm, such as 'robot' or 'robotart' etc
flowsteps:\tOPTIONAL parameter to determine which stages to implement of --'''
  print cfg.color.yellow+"\t\t'download'" + cfg.color.white + " - only downloads the tagged images"
  print cfg.color.yellow+"\t\t'classify'" + cfg.color.white + " (default, if blank) - download, classify/sort images w/model of your choice"
  print cfg.color.yellow+"\t\t'classify_top'" + cfg.color.white + " - download, classify with TOP accuracy model (skips setup)"
  print cfg.color.yellow+"\t\t'retrain'" + cfg.color.white + " - download, classify, and retrain (w/optional harvest) a new classifier with images from training_photos/{basetag}"
  print cfg.color.yellow+"\t\t'retrain_defaults'" + cfg.color.white + " (as in 'robots 0 0 retrain_defaults') will skip the retrain SETUP, using values from config file setup."
  print cfg.color.yellow+"\t\t'automatic'" + cfg.color.white + " - combo of 'classify_top + retrain_defaults' in one parameter"
  print cfg.color.cyan + "BOOTSTRAP NOTE: Quality initial labeling/sorting makes ALLL the difference!" + cfg.color.white
  print '''When starting, you must manually sort a minimum number of images to allow the first 
retraining to create the first classifier. After that, downloading, classifying/auto-sorting, 
and harvesting to retrain to make a better classifier is waaaaay more automated.

Read the extensive detailed help for useful and important advice.

thanks and boop boop.'''


#################################
def details():
  	
  print "-----------------------------------------"
  print cfg.color.cyan + "ROBOFLOW: detailed help" + cfg.color.white
  print'''-----------------------------------------
(please read the general help first: 'python roboflow.py --help')
'''
  print cfg.color.cyan + "Sections" + cfg.color.white
  print '''- requirements
- definitions
- general workflow
- how to start over
- bootstrapping details
- basetag details
- preventing dupes when RE-using classification models
- improving clasiification & retraining results
- optional txt msg notifications with twilio

note: important and defined words are CAPITALIZED
'''
  print cfg.color.cyan + "REQUIREMENTS" + cfg.color.white
  print '''-----------------------------------------
- python 2.7 (i used 2.7, but i dont know it wont run in 3.x)
- tensorflow (https://www.tensorflow.org/install/) 
- permissions to download and create files and directories
- terminal/command line comfort (or willingness to learn)
- optional: Imgur API Client-ID (https://apidocs.imgur.com/)
- optional: tensorboard (https://github.com/tensorflow/tensorboard)
- optional: twilio for txt msg notifications (https://www.twilio.com/sms)

'''

  print cfg.color.cyan + "DEFINITIONS" + cfg.color.white
  print "-----------------------------------------"
  print cfg.bkcolor.lightmagenta + " BASETAG " + cfg.color.white + ''' - because you can use roboflow for many/separate classifiers, you need to 
pick a term for the broad master classification or theme of each classifier 
(such as 'robots', or 'birds', or whatever) so that images, classifier models 
and more can be stored separately under that BASETAG directory.
'''

  print cfg.bkcolor.lightmagenta + " CLASSIFYING/LABELING " + cfg.color.white + ''' - downloaded images, stored in 'unsorted_{searchtag}' dirs,
are moved into 'sorted_{timestamp}' dirs by running a classifier, which is in turn 
created by retraining. a classifier is used repeatedly and on many different 
searchtags, while a retraining creates one classifier per retraining. after classifying 
many images, you should manually do a QUALITY CONTROL CHECK and then HARVEST them, 
before RETRAINING.
'''

  print cfg.bkcolor.lightmagenta + " CONFIDENCEMIN " + cfg.color.white + ''' - set in the config file, this variable determines how 
images are labeled and sorted. as you know, tensorflow assigns a numeric likelihood
that an image belongs to a certain LABEL. images below CONFIDENCEMIN are sorted 
into subdirs which are ignored during harvesting, and so removed from retraining. 
if this number is too low, poor examples will pollute your training data, 
and make for a weak classifier; too high and good examples get missed.
SEE ALSO: 'QUALITY CONTROL'
'''

  print cfg.bkcolor.lightmagenta + " CONFIG FILE " + cfg.color.white + ''' - The config file 'robo_config.py' sets up global variables, names, 
paths, etc used in different roboflow scripts. It is imported to the other files 
as 'cfg' so variables that begin 'cfg.somevarname' are set here. worth exploring!
'''

  print cfg.bkcolor.lightmagenta + " DIRECTORY STRUCTURE " + cfg.color.white + ''' - roboflow dir and scripts are intended to live at the same 
level as "tf_files" and "scripts" in the tensorflow-for-poets-2 structure as setup
by https://github.com/googlecodelabs/tensorflow-for-poets-2. however, you can monkey 
that around in the config file. BASETAG directories will be created under all three
core TF subdirs of testing_photos, training_photos, training_summaries, -- and 
in those will be created sorted_*, unsorted_*, harvested_* and other .txt logfiles. 
'''

  print cfg.bkcolor.lightmagenta + " HARVESTING (optional) " + cfg.color.white + ''' - this is the moving of classified and sorted images from 
testing_photos to training_photos before retraining. This is the physical step 
that accomplishes the goal of downloading and classifying all those images -- to
get high-confidence images into training data to improve the next classifier's accuracy. 
NOT used with every retraining. SEE ALSO: CONFIDENCEMIN and QUALITY CONTROL
'''

  print cfg.bkcolor.lightmagenta + " LABELS " + cfg.color.white + ''' - the sub-classes of images you enter during guided setup of creating a 
new BASETAG. continuing the "robot" BASETAG example, these might be: 
\t'drawn', 'built', 'mechs' and 'not'.
sub-classes are used to auto-generate directories in the training_photos directory 
and 'sorted_{timestamp}' directories when classifying/sorting images.
it is a VERY GOOD idea to have a general 'other' or 'not' category because 
searchtag images can be wildly not on theme to the related BASETAG. that is, lots
of images tagged 'robot' are not even close to any meaningful 'robot' sub-class.
'''

  print cfg.bkcolor.lightmagenta + " LOG FILES " + cfg.color.white + ''' -this program creates several files along the way to track various 
aspects of the process, and stores them as .txt files, often with a 
'_{timestamp}.txt' ending. Tracked information includes original names and urls of 
files, names and params of classifying model, which 'sorted_{timestamp}' dirs were 
harvested and how the images were moved, etc etc.
'''

  print cfg.bkcolor.lightmagenta + " SEARCHTAG " + cfg.color.white + ''' -the tag, related to the BASETAG, which will serve as the search term
for images to be downloaded, sorted and classified.
examples: 'robotart' or 'owl', per the previous BASETAG examples.
'''

  print cfg.bkcolor.lightmagenta + " QUALITY CONTROL CHECK " + cfg.color.white + ''' -along with adjusting 'CONFIDENCEMIN', periodic and manual 
human-sorting of robo-sorted images is critical. that is, you need to go into 
the 'sorted_{timestamp}' dirs, spot-check and move images among the labeled dirs as 
you, human, think best -- and BEFORE a harvest. Poorly labeled images getting back
into training data makes for weak classifiers. 
'''

  print cfg.bkcolor.lightmagenta + " SORTED_{TIMESTAMP} and  UNSORTED_{SEARCHTAG} DIRS " + cfg.color.white + ''' -downloaded images are 
initially stored in testing_photos/{basetag}/unsorted_{searchtag} directory. 
When a classifier is run, they are copied (not moved) into a labeled-dir under 
testing_photos/{basetag}/sorted_{timestamp}/ according to the CONFIDENCEMIN var. 
for example, if your CONFIDENCEMIN is 92.5, and your labels are 'built', 'drawn',
'not', then you will have the labeled-dirs: built, built_under925, drawn, drawn_under925, 
not, not_under925. when HARVESTING occurs, images in the '*_under*' dirs will be ignored.
'''

  print cfg.bkcolor.lightmagenta + " TENSORFLOW " + cfg.color.white + ''' -A MACHINE-LEARNING LIBRARY FROM GOOGLE
This whole roboflow endeavor assumes you have at least passing familiarity 
with TensorFlow and image classification. If not, go read:
\thttps://codelabs.developers.google.com/codelabs/tensorflow-for-poets/
\thttps://www.tensorflow.org/tutorials/image_retraining
'''


  print cfg.color.cyan + "GENERAL WORKFLOW" + cfg.color.white
  print '''-----------------------------------------
(note: all these descriptions use default names of directories as set in config file).
'''
  print cfg.bkcolor.lightmagenta + " GUIDED " + cfg.color.white + '''
1. create or choose an existing BASETAG
2. choose number of images to download and
3. enter the searchtag of those images.

conditionally:
4. if you have any classification models, you will be guided to choose one
(or you can skip classifying and just download the images)

conditionally:
5. if you have enough images in training_photos/BASETAG/labeled-subdirs you will 
be prompted to retrain or not. if yes, you will be guided through the retraining 
parameters, or you can always just hit [enter] to accept the defaults as set in 
the config file (although too much of that defeats the goal of comparing/learning 
how hyperparameters affect classification accuracy!)
'''
  print cfg.bkcolor.lightmagenta + " ADVANCED " + cfg.color.white + '''
- enter parameters at the command line. as noted in the regular help:'''
  print "'python " + cfg.download_script + " [BASETAG] [imagequantity] [searchtag] [optional flowsteps]'"
  print '''note: the flowsteps parameter is optional, and defaults to classify if blank, 
meaning roboflow will download [imagequantity] of [searchtags] and then classify them.

- optional flowstep parameters: 
\t'download | classify | classify_top | retrain | retrain_defaults'

- classify_top as flowstep paramter:
if you want to automatically choose the classifier with the highest training_accuracy, 
use the parameter 'classify_top' as the optional flowstep. this will skip a step 
and make the whole flow more automated, if that is what you desire.
\texample: 'python roboflow.py robots 200 robotart classify_top' 

- hint: if you have more than the minimum number of images required in labeled 
sub-dirs at training_photos/BASETAG, and want to skip both downloading and 
classifying stages, enter '0' for both the imagequantity and seachtag parameters. 
\texample: 'python roboflow.py robots 0 0 retrain' 

-- double hint: if you want to JUST retrain and have it run unattended, 
you can use with '0 0' setup a flowstep parameter of 'retrain_defaults' to choose
the retraining parameter values set in the config file.
\texample: 'python roboflow.py robots 0 0 retrain_defaults' 

'''
  print cfg.color.cyan + "HOW TO START OVER" + cfg.color.white
  print '''-----------------------------------------
if you want a clean slate, first make a back up first of what you currently have 
because that is always a good idea, then simply delete the directories under 
tf_files directory named testing_photos, training_photos, and training_sumamries.

'''
  print cfg.color.cyan + "BOOTSTRAPPING DETAILS" + cfg.color.white
  print '''-----------------------------------------
There is an initial bootstrap stage in which you must manually sort a minimum number 
of images to allow the first retraining to create the first classifier. This tool 
will help you download 1000s of images pretty easily. It can take a while to 
manually sort the first 1000 images per label, but, seriously, dont skip it. 
it is not worth it. After that, subsequent cycles of downloading, classifying/auto-sorting, 
and harvesting sorted images into the training_photos/labeled_directories for 
another cycle of retraining is waaaaay more automated.

specifically, before the FIRST retraining you must MANUALLY SORT at least'''
  print ""+str(cfg.retrain_imgcount_default)+"* images into labeled sub-dirs of '"+cfg.path_to_trainingimgs+"/{BASETAG}'. "
  print '''after that, the 'retrain' parameter will, at your option, harvest 
previously classified high-confidence* images into the  training data sub-directories at '''
  print ""+cfg.path_to_trainingimgs+"/{BASETAG}/{labeled-subdirs}."
  print "* as setup in config file: "+cfg.config_script+""
  print '''

'''
  print cfg.color.cyan + "BASETAG DETAILS" + cfg.color.white
  print '''-----------------------------------------
you can create an many different classifier themes, which are called BASETAGs, 
from the guided or advanced usage. in guided use, you choose to use an existing 
or create a new basetag. in advanced use, whatever BASETAG name you enter will be 
created if it doesnt exist. NOTE: if you typo an existing BASETAG, you cannot
classify or retrain because you wont have any images under this 'new' BASETAG.
 
also, in advanced use, a new BASETAG & SEARCHTAG will create new label dirs in 
training data directory, but in guided mode, it would not. this is because a new 
BASETAG from the command line needs at least one label dir, so it is created. 
if you dont want to sort training data into them, there is no danger in removing 
the unwanted trainingdata/labeled-dirs BEFORE the first retraining. after that, 
you will mess things up if you remove them. 


'''
  print cfg.color.cyan + "PREVENTING DUPES when REUSING CLASSIFICATION MODELS" + cfg.color.white
  print '''-----------------------------------------
IMPORTANT: when classifying, unsorted images are COPIED so they can be reused 
with different models to see how it classifies them differently. that is, when you 
run a classifier, it classifies EVERYTHING in that unsorted_{searchtag} folder, 
which also means if you download 250 images tagged 'robotart' and classify them, 
AND THEN download 250 more tagged 'robotart' and classify them, you ll actually 
classify the first 250 again as well, although into a different sorted_{timestamp} dir.

This can be not ideal for your training data, as it includes repeated images when 
harvesting. the easy answer is to toss the repeats from the more recent sorted_{timestamp} 
dir. simply look into the most recent 'sorted_{timestamp}' dirs, check the 
highest sequence number and delete the overlap.

note: per not-great coding convention, some MAGIC LETTERS are employed when 
choosing a classification model. that is, the first letter of 'inceptionv3' and 
'mobilenet' are interlinked between classify_model, classify_model_dir, modeltype 
-- so do not change without following thru code! i didnt totally allow for 
infinite model names in favor of speed of dev over future flexibility. but, this
is on a list...


'''
  print cfg.color.cyan + "IMPROVING CLASSIFICATION/RETRAIN RESULTS" + cfg.color.white
  print '''-----------------------------------------
the likelihood of images from a SEARCHTAG matching a BASETAG varies wildly, and 
so sorting is adjusted with the 'CONFIDENCEMIN' variable. Tuning this variable 
is the seed of improving results, but periodic manual quality control is how you 
tend that garden. That is, YOU need to go into the 'sorted_{timestamp}' dirs and 
move images among the labeled dirs as you, a human, think they should be. This is 
how the classifiers created by retraining get better and better, until you arent 
really needed anymore! YAAY..?

when there are enough images in these directories, you can harvest them to 'retrain' 
the classifier, experimenting with many retraining permutations to increase the 
accuracy. In this cyclical loop, the classifier gets better and better at 
classifying and sorting -- resulting, at some point, in its ability to be a 
semi-automated self-improving image classifier, depending of course on your 
ability to bootstrap the classifier with good images and to keep them high-quality 
with periodic quality control.

during retraining, images from the labeled dirs are moved to training_photos/BASETAG 
dir, while the newly created classification model is stored at 
training_summaries/BASETAG/{model_name}. the model_name includes useful parameter 
info so you can pick the right model when classifying/labeling. the model_name 
ends with the accuracy percentage of the model, such as '_acc91.72' or the like,
again to help you in choosing which model to use when classifying.

  

'''
  print cfg.color.cyan + "OPTIONAL TXT MSG NOTIFICATIONS" + cfg.color.white
  print '''-----------------------------------------
because a cycle might take a while, especially for a full retrain (or even a 
large download/classify/sort cycle) there are three(3) txt msg notification points 
built into this tool. specifically, you can be optionally notified at the end of 
download, classification, and retrain stages. i personally found it quite useful, 
and if you want txts, you will need to setup your own TWILIO account, which requires 
a credit card to charge up their txt msg service. txt msg notifications are by 
default turned off, via the 'twilio_active' variable in the config file.
'''






