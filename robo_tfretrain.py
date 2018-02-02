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



import os, sys, shutil, time
from subprocess import Popen, PIPE

#import roboflow specific stuff
import robo_config as cfg
import robo_support as robo 
os.environ['TF_CPP_MIN_LOG_LEVEL']='0' # suppress some inherent TensorFlow error msgs


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

  #build up shared commands
  cmd1 = "../scripts/retrain.py"
  cmd2 = "--bottleneck_dir=" + cfg.path_to_bottlenecks
  cmd3 = "--model_dir=" + cfg.path_to_trainingmodels
  cmd4 = "--how_many_training_steps=" + steps
  cmd5 = "--train_batch_size=" + batchsize
  cmd6 = "--testing_percentage=" + testpercent
  cmd7 = "--summaries_dir=" + path_to_trainingsumm_name
  cmd8 = "--output_graph=" + path_to_output_graph
  cmd9 = "--output_labels=" + path_to_output_labels
  cmd10 = "--image_dir=" + path_to_trainimgs_basetag
  cmd11 = ""

  #BUILD an array of CMDS based on model
  if modeltype == "inceptionv3":
    cmds=['1',cmd1,cmd2,cmd3,cmd4,cmd5,cmd6,cmd7,cmd8,cmd9,cmd10]
  else:
    # build a command WITH ARCHITECTURE, since not default
    mobilepercent = retrain_dict["mobilepercent"]
    ARCHITECTURE = modeltype + "_" + str(mobilepercent) + "_" + str(imagesize)
    cmd11 = "--architecture=" + ARCHITECTURE
    cmds=['1',cmd1,cmd2,cmd3,cmd4,cmd5,cmd6,cmd7,cmd8,cmd9,cmd10,cmd11]    

    
  print "\n------------------------------"
  print "start retraining tensorflow model/graph"
  print "when it breaks, look for 'RuntimeError: Error during processing file' "
  print cfg.color.yellow + "retraining command:" + cfg.color.white
  #print retrain_command
  print cmd1, cmd2, cmd3, cmd4, cmd5, cmd6, cmd7, cmd8, cmd9, cmd10,
  if len(cmd11): print cmd11

  # use the tensorflow RETRAIN script
  try:
    #training_results = subprocess.check_output(retrain_command, shell=True)
    training_results = Popen(cmds,shell=False,stderr=PIPE,bufsize=1,executable="python")
    for line in iter(training_results.stderr.readline, b''):
      print line
      if line.startswith("INFO:tensorflow:Final test accuracy"):
        tf_final_acc = line
    training_results.wait() # wait for the subprocess to exit

  except Exception:
    ### log something or?
    ### remove specific image or modeldir? regex thru output to find it-- or just skip?
    pass

  # see need/description at this function
  add_accuracy_to_modeldir(path_to_trainingsumm_name,tf_final_acc)
  
  
  return training_results



#################################	
def add_accuracy_to_modeldir(path_to_trainingsumm_name,tf_final_acc):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #clean up final accuracy (ex: 'INFO/tensorflow/Final test accuracy = 80.8% (N=73)' )
  final_acc = tf_final_acc.split("=")[1].replace("% (N","")
  #append final_accuracy to modeldir name
  acc_label = "_acc"+final_acc
  shutil.move(path_to_trainingsumm_name, path_to_trainingsumm_name+acc_label)
  return



#################################
def retrain_dict_setup_modeltype():
  robo.whereami(sys._getframe().f_code.co_name)
  
  print cfg.color.cyan + "1. RETRAIN TENSORFLOW MODEL?" + cfg.color.white
  print "(default:" + cfg.retrain_model_default+") Enter [i]nceptionv3 or [m]obile:"
  modeltype_raw = raw_input()
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
  
  print cfg.color.cyan + "2. TRAINING STEPS?" + cfg.color.white
  print "(default:"+str(cfg.retrain_steps_min)+") Too many leads to overfitting, too few leads to weak results,"
  print "so between 500 and 4000 is a good choice... "
  raw_steps = raw_input()
  try:
    if int(raw_steps) < cfg.retrain_steps_min: trainsteps = cfg.retrain_steps_min
    else: trainsteps = int(raw_steps)
  except:
    trainsteps = cfg.retrain_steps_min
    
  return trainsteps


#################################
def retrain_dict_setup_imgsize():
  robo.whereami(sys._getframe().f_code.co_name)
  
  print cfg.color.cyan + "3. IMAGE SIZE?" + cfg.color.white
  print "(default: "+str(cfg.retrain_imgsize_default)+") Enter [128], [160], [192], or [224] pixels... "
  raw_imagesize = raw_input()
  try:
    if int(raw_imagesize) not in (128,160,192,224): imgsize = cfg.retrain_imgsize_default
    else: imgsize = int(raw_imagesize)
  except:
    imgsize = cfg.retrain_imgsize_default

  return imgsize


#################################
def retrain_dict_setup_testper():
  robo.whereami(sys._getframe().f_code.co_name)
  
  print cfg.color.cyan + "4. TESTING PERCENT?" + cfg.color.white
  print "(min:"+str(cfg.retrain_testper_min)+") Depending how many images in total, between 10 and 50 is a good starting point... "
  raw_testper = raw_input()
  try:
    if int(raw_testper) < cfg.retrain_testper_min: testper = cfg.retrain_testper_min
    else: testper = int(raw_testper)
  except:
    testper = cfg.retrain_testper_min
    
  return testper


#################################
def retrain_dict_setup_batchsize():
  robo.whereami(sys._getframe().f_code.co_name)
  
  print cfg.color.cyan + "5. BATCH SIZE?" + cfg.color.white
  print "(min:"+str(cfg.retrain_batchsize_min)+") While there is debate on a best number, from 10 to 100 (or more if you have many thousand of images) is a good starting point... "
  raw_batchsize = raw_input()
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
  
  print cfg.color.yellow + "retrain params:" + cfg.color.white
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
    print cfg.color.magenta
    print "This script not callable directly, as it needs data from "+cfg.download_script+" passed to it."
    print "maybe it's time read the help? copy/paste this:" + cfg.color.white
    print "\tpython roboflow.py --help"
    robo.goodbye()
  
  #keep going
  main(retrain_dict)



