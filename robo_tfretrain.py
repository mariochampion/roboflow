#!/usr/bin/env python
'''
ROBOFLOW RETRAINER - PURPOSE
this script autoruns or triggers the TensorFlow retraining script (retrain.py), 
when certain conditions are met:
1. triggered from main 'roboflow.py' script with the parameter 'retrain'
2. there are more than the 'retrainimages_min_count' specified in robo_config.py 
   (or manually overridden, which is ok if you're just exploring, but otherwise...)
3. TensorFlow is installed and running (a simple task beyond the scope of this doc).
   https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/
'''

# ===================================================================
## ROBOFLOW - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/roboflow
## released under the Apache License 2.0. (http://www.apache.org/licenses/LICENSE-2.0)
#
### much of retrain_tensorflow function are tweaked from work at 
### https://github.com/googlecodelabs/tensorflow-for-poets-2
### Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================



import os, sys, subprocess, shutil, time

#import roboflow specific stuff
import robo_config as cfg
import robo_support as robo 
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # suppress some inherent TensorFlow error msgs


##################################	  
###  hey, have some functions  ###	  
##################################

#################################	
def retrain_tensorflow(retrain_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  #SETUP
  basetag = retrain_dict["basetag"]
  thistag = retrain_dict["thistag"]
  imagesize = str(retrain_dict["imagesize"])
  steps = str(retrain_dict["steps"])
  testpercent = str(retrain_dict["testpercent"])
  batchsize = str(retrain_dict["batchsize"])
  modeltype = retrain_dict["modeltype"]
  mobilepercent = retrain_dict["mobilepercent"]
  
  if modeltype == "mobilenet":
    trainsumm_name = modeltype + "_" + str(mobilepercent) + "_batch" + str(batchsize) + "_steps" + str(steps) + "_test" + str(testpercent) + "_img" + str(imagesize) + ""
  else:
    trainsumm_name = modeltype + "_batch" + str(batchsize) + "_steps" + str(steps) + "_test" + str(testpercent) + "_img" + str(imagesize) + ""
  
  path_to_trainingsumm_name = cfg.path_to_trainingsumms + cfg.dd + basetag + cfg.dd + trainsumm_name
  path_to_trainimgs_basetag = cfg.path_to_trainingimgs + cfg.dd + basetag
  path_to_output_graph = path_to_trainingsumm_name + cfg.dd + cfg.retrainedgraph_file
  path_to_output_labels = path_to_trainingsumm_name + cfg.dd + cfg.retrainedlabels_file 

  
  #CHOOSE
  if modeltype == "inceptionv3":
    # build a command
    retrain_command = "python ../scripts/retrain.py \
    --bottleneck_dir=" + cfg.path_to_bottlenecks + " \
    --model_dir=" + cfg.path_to_trainingmodels + " \
    --how_many_training_steps=" + steps + " \
    --train_batch_size=" + batchsize + " \
    --testing_percentage=" + testpercent + " \
    --summaries_dir=" + path_to_trainingsumm_name + " \
    --output_graph=" + path_to_output_graph + " \
    --output_labels=" + path_to_output_labels + " \
    --image_dir=" + path_to_trainimgs_basetag
    
  else:
    # build a command WITH ARCHITECTURE, since not default
    mobilepercent = retrain_dict["mobilepercent"]
    ARCHITECTURE = modeltype + "_" + str(mobilepercent) + "_" + str(imagesize)
    
    retrain_command = "python ../scripts/retrain.py \
    --bottleneck_dir=" + cfg.path_to_bottlenecks + " \
    --model_dir=" + cfg.path_to_trainingmodels + " \
    --how_many_training_steps=" + steps + " \
    --train_batch_size=" + batchsize + " \
    --testing_percentage=" + testpercent + " \
    --summaries_dir=" + path_to_trainingsumm_name + " \
    --output_graph=" + path_to_output_graph + " \
    --output_labels=" + path_to_output_labels + " \
    --image_dir=" + path_to_trainimgs_basetag + " \
    --architecture=" + ARCHITECTURE
    
  print 
  print "------------------------------"
  print "start retraining tensorflow model/graph"
  print "when it breaks, look for 'RuntimeError: Error during processing file' "
  print "retraining command:"
  print retrain_command

  # use the tensorflow RETRAIN script
  try:
    #process = subprocess.Popen([retrain_command], stdout = subprocess.PIPE, shell=True)
    #training_results = process.communicate()[0]
    training_results = subprocess.check_output(retrain_command, shell=True)
  except Exception:
    ### log something or?
    ### remove specific image? regex thru output to find it-- or just skip?
    #training_results = False #or this for now
    pass
  
  # see need/description at this function
  add_accuracy_to_modeldir(path_to_trainingsumm_name,path_to_output_labels)
  
  #print "type:", type(training_results)
  #print "training_results:", training_results
  return training_results



#################################	
def add_accuracy_to_modeldir(path_to_trainingsumm_name,path_to_output_labels):
  robo.whereami(sys._getframe().f_code.co_name)

  # pull accuracy from temp spot in retrained_labels.txt in this ugly hack
  # because stdout to subprocess.PIPE not work like it would seem is obvious...
  # See https://github.com/tensorflow/tensorflow/issues/3047 
  # See https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
  # see https://stackoverflow.com/questions/6657690/python-getoutput-equivalent-in-subprocess
  # and many others... open to suggestions for reading tf.logging.info from retrain script!
  f = open(path_to_output_labels, "rU")
  labels_list = []
  for line in f:
    labels_list.append(line.replace("\n","").replace(" ", "_"))
  f.close()
  acc_label = labels_list[-1]
  if "_acc" in acc_label:
    #append this to modeldir name
    shutil.move(path_to_trainingsumm_name, path_to_trainingsumm_name+acc_label)
    #then delete last line in labels file
    newpath_to_output_labels = path_to_trainingsumm_name+acc_label + cfg.dd + cfg.retrainedlabels_file
    f = open(newpath_to_output_labels, "w")
    for reallabel in labels_list[:-1]:
  	  f.write(reallabel+"\n")
    f.close()
  return



#################################
def retrain_dict_setup_modeltype():
  robo.whereami(sys._getframe().f_code.co_name)
  
  modeltype_raw = raw_input("1. RETRAIN TENSORFLOW MODEL?(default: "+cfg.retrain_model_default+") Enter [i]nceptionv3 or [m]obile:")
  if modeltype_raw == "i": 
    modeltype = cfg.inception_model
    mobilepercent = None
  elif modeltype_raw == "m": 
    modeltype = cfg.mobile_model
    robo.makebeep()
    mp_raw = raw_input("Please enter percent of pretrained '"+cfg.mobile_model+"' model to use: [25], [50], [75] or [100] : ")
    if mp_raw == "25"	: mobilepercent = "0.25"
    elif mp_raw == "50"	: mobilepercent = "0.50"
    elif mp_raw == "75"	: mobilepercent = "0.75"
    elif mp_raw == "100": mobilepercent = "1.0"
    else: 
      mobilepercent = cfg.retrain_mobile_percent_default
      robo.makebeep()
      print"Woops, non-valid choice, so '"+str(cfg.retrain_mobile_percent_default)+"' was chosen for you."
      
  else:
    modeltype = cfg.retrain_model_default
    mobilepercent = cfg.retrain_mobile_percent_default

  return (modeltype, mobilepercent)


#################################
def retrain_dict_setup_trainsteps():
  robo.whereami(sys._getframe().f_code.co_name)
  
  raw_steps = raw_input("2. TRAINING STEPS?(default:"+str(cfg.retrain_steps_min)+") Too many leads to overfitting, too few leads to weak results, so between 500 and 4000 is a good choice... ")
  try:
    if int(raw_steps) < cfg.retrain_steps_min: trainsteps = cfg.retrain_steps_min
    else: trainsteps = int(raw_steps)
  except:
    trainsteps = cfg.retrain_steps_min
    
  return trainsteps


#################################
def retrain_dict_setup_imgsize():
  robo.whereami(sys._getframe().f_code.co_name)
  
  raw_imagesize = raw_input("3. IMAGE SIZE?(default: "+str(cfg.retrain_imgsize_default)+") Enter [128], [160], [192], or [224] pixels... ")
  try:
    if int(raw_imagesize) not in (128,160,192,224): imgsize = cfg.retrain_imgsize_default
    else: imgsize = int(raw_imagesize)
  except:
    imgsize = cfg.retrain_imgsize_default

  return imgsize


#################################
def retrain_dict_setup_testper():
  robo.whereami(sys._getframe().f_code.co_name)
  
  raw_testper = raw_input("4. TESTING PERCENT?(min:"+str(cfg.retrain_testper_min)+") Depending how many images in total, between 10 and 50 is a good starting point... ")
  try:
    if int(raw_testper) < cfg.retrain_testper_min: testper = cfg.retrain_testper_min
    else: testper = int(raw_testper)
  except:
    testper = cfg.retrain_testper_min
    
  return testper


#################################
def retrain_dict_setup_batchsize():
  robo.whereami(sys._getframe().f_code.co_name)
  
  raw_batchsize = raw_input("5. BATCH SIZE?(min:"+str(cfg.retrain_batchsize_min)+") While there is debate on a best number, from 10 to 100 (or more if you have many thousand of images) is a good starting point... ")
  try:
    if int(raw_batchsize) < cfg.retrain_batchsize_min: bs = cfg.retrain_batchsize_min
    else: bs = int(raw_batchsize)
  except:
    bs = cfg.retrain_batchsize_min
  
  return bs
  
  
  
  
#################################	 
#################################	
def main(retrain_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  
  print "retrain params:"
  for k,v in retrain_dict.items():
    print k, ":" ,v
  print
  
  timestart = time.strftime("%H%M%S")
  
  #### ACTUAL WORK HERE
  retrained_output = retrain_tensorflow(retrain_dict)
  print "retrained_output:", retrained_output
  #####################
    
  #AFTER -- send a message
  timeend = time.strftime("%H%M%S")
  timespent = float(timeend) - float(timestart)
  
  if cfg.twilio_active == True:
    sms_msg = "tensorflow retrained and new model created in "+str(timespent)+" seconds! boop boop."
    sms_status = robo.sendsms(sms_msg)
  
  print "exiting robo_retrain..."
  return
  
  sys.exit(1)#shouldnt get here, but just in case...


# boilerplate kicker offer (yes thats a tech term!)   
if __name__ == '__main__':
  try:
  	retrain_dict
  except:
    print
    print "This script not callable directly, as it needs data from "+cfg.download_script+" passed to it."
    print "maybe it's time read the help? copy/paste this:"
    print "\tpython roboflow.py --help"
    robo.goodbye()
  
  #keep going
  main(retrain_dict)



