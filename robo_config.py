#!/usr/bin/env python
'''
ROBOFLOW CONFIG - PURPOSE
This config file sets up global variables, names, paths, etc used in different roboflow scripts. It is imported to the other files as 'cfg' so variables that begin 'cfg.somevarname' are configured in this file.

Also, OPTIONAL txt msg notifications require twilio account setup with credit card to fund txt msgs.'''

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
## please open issues and pull requests,
## thanks and always remember: this robot loves you. 
## boop boop!
## ===================================================================


import os, time

#roboflow files and two core functions
download_script = "roboflow.py"
retrain_script = "robo_tfretrain.py"
classifying_script = "robo_tfclassifier.py"
config_script = "robo_config.py"

show_whereami = False # if True, prints '---functionname---' to help trace app flow
twilio_active = False # make True if you set up a twilio acct AND want to send txt notifs
# details at https://www.twilio.com/blog/2016/10/how-to-send-an-sms-with-python-using-twilio.html

## DOWNLOAD SOURCE can be:
# "imgurapi" (requires you get API KEY from https://apidocs.imgur.com/) 
# "webstagram" (which can be used anonymously)
scrapesite_default = "webstagram"


# dynamically created files, etc
urlfile_prefix = "_urls_"
urlfile_suffix = ".txt" # sep name for max flex of diff later needs
img2url_prefix = "_img2url_"
img2url_suffix = ".txt" # sep name for max flex of diff later needs
imagelog_prefix = "_log_"
imagelog_suffix = ".txt" # sep name for max flex of diff later needs
img_suffix = ".jpg"
modeldatalog_name = "modeldata_"
harvested_basename = "harvested_"
harvested_suffix = ".txt" # sep name for max flex of diff later needs
unsorted_name = "unsorted_"
sorted_name = "sorted_"


# destinations and some defaults
labels_file = "retrained_labels.txt"
flow_default = "classify"
tagname_default = "robot"
inception_model = "inceptionv3"
mobile_model = "mobilenet"
retrainedgraph_file = "retrained_graph.pb"
retrainedlabels_file = "retrained_labels.txt"


# named paths
logtime = time.strftime("%Y%m%d%H%M%S")
harvested_dirname = harvested_basename + logtime
sorted_dirname = sorted_name + logtime
dd = "/"
path_to_tensorflow_files = "../tf_files"
path_to_testimgs = path_to_tensorflow_files + dd + "testing_photos"
path_to_trainingsumms = path_to_tensorflow_files + dd + "training_summaries"
path_to_trainingimgs = path_to_tensorflow_files + dd + "training_photos"
paths_to_reqddirs_list = (path_to_testimgs, path_to_trainingsumms, path_to_trainingimgs)


# classify vars
confidence_min = .925
imgnum_maxpercycle = 250 #please stay under 250 to limit stress on other people's servers
conmin2 = str(confidence_min).replace("0.","")
belowminlabel_dir_suffix = "_under"+conmin2


# retrain vars
retrain_imgcount_default = 800
retrain_model_default = inception_model
#retrain_model_default = mobile_model
retrain_mobile_percent_default = 1.0
retrain_imgsize_default = 224
retrain_label_min = 2
retrain_steps_min = 500
retrain_steps_default = 2600
retrain_testper_min = 10
retrain_testper_default = 16
retrain_batchsize_min = 10
retrain_batchsize_default = 64
retrain_imgmove_check_default = False #do not harvest images, True to harvest
trainingmodels_dir = "models"
path_to_trainingmodels = path_to_tensorflow_files + dd +  trainingmodels_dir
trainingbottlenecks_dir = "bottlenecks"
path_to_bottlenecks = path_to_tensorflow_files + dd +  trainingbottlenecks_dir


# rando presentation strings and such like
nomoreurls = "nomoreurls"
except_tooslowload = "download bad"
except_tooslowload_response = "TOOOO SLOW TO D-LOAD! moving on..."
sigline = "boop boop."
finalwords_list = []
finalwords_list.append("goodbye and i love you.")
finalwords_list.append("buh bye.")
finalwords_list.append("ok bye.")
finalwords_list.append("ok. stopping program. (i still love you.)")
finalwords_list.append("stopping...")
finalwords_list.append("see you soon!")
finalwords_list.append("exiting...")
finalwords_list.append("bye bye for now.")
finalwords_list.append("bye byes!")
finalwords_list.append("ok good bye i love you.")


# pinched and tweaked from https://github.com/impshum/Multi-Quote/blob/master/run.py
class color:
  white, cyan, blue, red, green, yellow, magenta, black, gray, bold = '\033[0m', '\033[96m','\033[94m', '\033[91m','\033[92m','\033[93m','\033[95m', '\033[30m', '\033[30m', "\033[1m"  

# maybe add bks, bolds, etc from https://godoc.org/github.com/whitedevops/colors
class bkcolor:
  resetall = "\033[0m"
  default      = "\033[49m"
  black        = "\033[40m"
  red          = "\033[41m"
  green        = "\033[42m"
  yellow       = "\033[43m"
  blue         = "\033[44m"
  magenta      = "\033[45m"
  cyan         = "\033[46m"
  lightgray    = "\033[47m"
  darkgray     = "\033[100m"
  lightred     = "\033[101m"
  lightgreen   = "\033[102m"
  lightyellow  = "\033[103m"
  lightblue    = "\033[104m"
  lightmagenta = "\033[105m"
  lightcyan    = "\033[106m"
  white        = "\033[107m"


# sms/txt msg variables
sms_minsecstonotify = 60 # to be notified, downloading must run at least this many seconds.
sms_end = sigline
