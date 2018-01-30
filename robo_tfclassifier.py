#!/usr/bin/env python
'''
ROBOFLOW CLASSIFIER - PURPOSE:
this script autoruns or triggers the TensorFlow labeling script (label_image.py),
looping through 'unsorted_*' downloaded images to classify/label and sort them, 
according to how the returned TensorFlow score compares to the 'confidencemin' 
variable set in the config file.

the user chooses a classification model, if any, created by a previous retraining
stage, but if none are available, no option for classifying is presented and this 
script will not be triggered.
'''
# ===================================================================
## ROBOFLOW - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/roboflow
## released under the Apache License 2.0. (http://www.apache.org/licenses/LICENSE-2.0)
#
### much of classify_image function are tweaked from work at 
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

os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # suppress some inherent TF error msgs
logtime = time.strftime("%Y%m%d%H%M%S") # just some timestamping


##################################	  
###  hey, have some functions  ###	  
##################################

#################################	
def classify_image(testimg, model_data):
  robo.whereami(sys._getframe().f_code.co_name)
  
  basetag = model_data["basetag"]
  model_type = model_data["model_type"]
  model_dir = model_data["model_dir"]
  path_to_retrainedgraph = cfg.path_to_trainingsumms +cfg.dd + basetag + cfg.dd + model_dir + cfg.dd + cfg.retrainedgraph_file
  path_to_labels = cfg.path_to_trainingsumms +cfg.dd + basetag + cfg.dd + model_dir + cfg.dd + cfg.retrainedlabels_file
  # build a command  
  if model_type == cfg.mobile_model:
    testimgcommand = "python ../scripts/label_image.py \
    --graph='"+path_to_retrainedgraph+"' \
    --labels='"+path_to_labels+"' \
    --input_height=224 \
    --input_width=224 \
    --input_mean=128 \
    --input_std=128 \
    --image=" + testimg

  elif model_type == cfg.inception_model:
    testimgcommand = "python ../scripts/label_image.py \
    --graph='"+path_to_retrainedgraph+"' \
    --labels='"+path_to_labels+"' \
    --input_height=299 \
    --input_width=299 \
    --input_mean=128 \
    --input_std=128 \
    --input_layer='Mul' \
    --image=" + testimg
  else:
    robo.goodbye("woops no classification model! Program stopping...")
  
  print "image: "+testimg
  
  # use the tensorflow label_image script
  try:
    imagelabel_raw = subprocess.check_output(testimgcommand, shell=True)
  except Exception:
    # just remove file for now (rather than store for later analysis)
    # because they are broken images, not misclassified
    os.remove(testimg)
    imagelabel_raw = False
  
  return imagelabel_raw



#################################	
def process_imagelabel_for_final(label_raw):
  robo.whereami(sys._getframe().f_code.co_name)

  # do some things to strings
  imagelabel_2 = label_raw.split("\n")
  
  ## change in tensorflow script it now adds an evaluation string, 
  ## so there is a new conditional here (jan 2018) -- mmc
  if "Evaluation" in imagelabel_2[1]:
    imagelabel_2b = imagelabel_2[3]
  else:
    imagelabel_2b = imagelabel_2[0]
  
  imagelabel_2c = imagelabel_2b.split(" ")  

  imagelabel_score = imagelabel_2c[-1]
  imagelabel_name = imagelabel_2b.replace(" "+imagelabel_score, "").replace(" ","_")
  imagelabel_processed = (imagelabel_name, imagelabel_score)

  return imagelabel_processed


#################################
def getretrainedlabels(model_data):
  robo.whereami(sys._getframe().f_code.co_name)

  basetag = model_data["basetag"]
  model_dir = model_data["model_dir"]
  path_to_labels = cfg.path_to_trainingsumms +cfg.dd + basetag + cfg.dd + model_dir + cfg.dd + cfg.retrainedlabels_file
  f = open(path_to_labels, "rU")
  labels_list = []
  for line in f:
    lineclean = line.replace("\n","").replace(" ", "_")
    labels_list.append(lineclean)
    
  return labels_list
   

#################################
def makesortedlabels_dirs(model_data):
  robo.whereami(sys._getframe().f_code.co_name)  
  
  path_to_sortedimg_basetag = cfg.path_to_testimgs + cfg.dd + model_data["basetag"] + cfg.dd + cfg.sorted_dirname
  #make master sorted_dir
  if not os.path.exists(path_to_sortedimg_basetag):
    os.makedirs(path_to_sortedimg_basetag)
  
  labels_list = getretrainedlabels(model_data)
  for label in labels_list:
    abovemin_dir = path_to_sortedimg_basetag + cfg.dd + label
    if not os.path.exists(abovemin_dir):
      os.makedirs(abovemin_dir)
    
    #also make dir for images that are under the confidence min
    belowmin_labeldir = abovemin_dir + cfg.belowminlabel_dir_suffix
    if not os.path.exists(belowmin_labeldir):
      os.makedirs(belowmin_labeldir)
    
  status = True #make this a check
  return status
  

#################################	 
def processclassifiedimages(origfilename, labelresults, basetag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #setup the new namescheme (could prolly be small func)
  labelname = labelresults[0]
  labelscore = labelresults[1]
  score_suffix = labelscore[2:5]
  filename_parts = origfilename.split(".")
  newfilename = filename_parts[0] + "_" + score_suffix + "." + filename_parts[1]
  rootdir = cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + cfg.sorted_dirname + cfg.dd + labelname
  subdir = rootdir + cfg.belowminlabel_dir_suffix
  
  if float(labelscore) > float(cfg.confidence_min):  
    print cfg.color.green + "yay! score HIGH: " +cfg.color.black+cfg.bkcolor.green + " "+labelscore+" " + cfg.bkcolor.resetall
    print "== moved to: ..."+ cfg.sorted_dirname + cfg.dd + labelname
    shutil.move(cfg.path_to_testimgs +cfg.dd + basetag + cfg.dd + origfilename, rootdir + cfg.dd + newfilename)
    proc_result = (newfilename, labelname, labelscore)
    
  else:
    print cfg.color.magenta + "sad score low: " +cfg.color.white+cfg.bkcolor.magenta + " "+labelscore+" " + cfg.bkcolor.resetall
    print "==== moved to dir: ..."+cfg.sorted_dirname + cfg.dd + labelname+cfg.belowminlabel_dir_suffix
    shutil.move(cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + origfilename, subdir + cfg.dd + newfilename)
    proc_result = (newfilename, labelname+cfg.belowminlabel_dir_suffix, labelscore)

  print
  return proc_result 





#################################	 
#################################	
def main(model_data):
  robo.whereami(sys._getframe().f_code.co_name)
  
  basetag = model_data["basetag"]
  model_type = model_data["model_type"]
  path_to_sortedimgs_basetag = cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + cfg.sorted_dirname
  
  if makesortedlabels_dirs(model_data) == False:
    robo.goodbye("Dirs for final output NOT created or available. Check your permissions. Stopping program...")
    

  #get images
  images_list = robo.getimagelist_fromdir(cfg.path_to_testimgs + cfg.dd + basetag)

  #call the labeling function
  testimages_dict = {}
  
  
  for testimage in images_list:
    timestart = time.strftime("%H%M%S")
    
    ##### call tensorflow label_image script
    imagelabel_raw = classify_image(testimage, model_data)
    #######################################
    
    # process the label 
    if imagelabel_raw:
      imagelabel_processed = process_imagelabel_for_final(imagelabel_raw)
      testimage_clean = testimage.replace(cfg.path_to_testimgs+cfg.dd+basetag+cfg.dd,"")
      #process the classifiedimages
      proc_classed_images_list = {}
      proc_result = processclassifiedimages(testimage_clean, imagelabel_processed, basetag)
      
      # save to dict for later analysis
      timeend = time.strftime("%H%M%S")
      timespent = float(timeend) - float(timestart)
      testimages_dict[proc_result[0]] = (proc_result[1],proc_result[2], timespent)
    
  #make a CLASSIFICATION log file
  filetitle = cfg.imagelog_prefix + model_type + "_" + logtime + cfg.imagelog_suffix
  path_to_thisfile = path_to_sortedimgs_basetag + cfg.dd + filetitle
  robo.createfilefromdict(path_to_thisfile, testimages_dict)
    
  #make a MODEL INFO log file
  thatfile = cfg.imagelog_prefix + cfg.modeldatalog_name + logtime + cfg.imagelog_suffix
  path_to_thatfile = path_to_sortedimgs_basetag + cfg.dd + thatfile
  robo.createfilefromdict(path_to_thatfile, model_data)


  
  #AFTER -- send a message
  if cfg.twilio_active == True:
    num_of_testimages = len(testimages_dict)
    sms_msg = "roboclassified and moved " + str(num_of_testimages) + " imgs! now, do a manual QA sortcheck (and/or re-sort) for best longterm success. boop boop."
    sms_status = robo.sendsms(sms_msg)
  
  print "exiting robo_classify..."
  return
  
  sys.exit(1) #shouldnt get here, but just in case...



#################################	 
#################################
# boilerplate kicker offer (yes thats a tech term!)   
if __name__ == '__main__':
  try:
  	model_data
  except:
    print
    print "This script not callable directly, as it needs data from "+cfg.download_script+" passed to it."
    print "maybe it's time read the help? copy/paste this:"
    print "\tpython roboflow.py --help"
    robo.goodbye()
 
  #go get 'er done
  main(model_data)






