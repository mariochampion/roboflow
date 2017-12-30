#!/usr/bin/env python
'''
ROBOFLOW - PURPOSE
roboflow was created to get a better sense for TensorFlow's image classifier by making it easier to gather 1000s of similar images by hashtag (such as "#robot" or "#robotart") to serve as re/training examples, and to enable easy testing of different TensorFlow hyperparameter settings for creating classifiers. 

specifically, tagged images are downloaded (right now from webstagram) and then sorted into labeled sub-directories, which are periodically 'harvested' to retrain TensorFlow (which creates classifiers). 

BOOTSTRAPPING: There is an initial bootstrap stage in which you must manually sort a minimum number of images to allow the first retraining to create the first classifier. This tool will help you download 1000s of images pretty easily. After that, subsequent cycles of downloading, classifying/auto-sorting, and harvesting sorted images into the training_photos/labeled_directories for another cycle of retraining is waaaaay more automated. 

USAGE: GUIDED v ADVANCED
there are two ways to use this tool: guided walkthrough and advanced via command line parameters, both of which allow creation of multiple classifiers for various topics (say 'robots', or 'birds' or 'pirates') through use of a 'master classification tag' or 'basetag'. 

HELP:
read help with 'python roboflow.py --help' at the command line,
and dont forget to explore the config file. 
'''

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
## more python(2.7) file/dir manipulations, in a commandline driven app, and to better understand
## Google's TensorFlow image classification elements and hyperparameter effects.
##
## please open issues and pull requests,
## thanks and always remember: this robot loves you. 
## boop boop!
## ===================================================================



import os, sys, signal, time, shutil, re
from urllib import urlretrieve, urlopen

#import roboflow specific stuff
import robo_config as cfg
import robo_support as robo 
import robo_tfclassifier as roboclass
import robo_tfretrain as roboretrain
import robo_help as help


##################################	  
###  hey, have some functions  ###	  
##################################

#################################	
def releasethehelp():
  
  help.summary()
  robo.makebeep()
  help_input_process(help.helper("summ")) 
  
#################################
def releasethehelp_details():
    
  help.details()
  robo.makebeep()
  help_input_process(help.helper("details"))
  
#################################
def help_input_process(help_input):
  robo.whereami(sys._getframe().f_code.co_name)
  
  if help_input == 'helpmore': releasethehelp_details() 
  elif help_input == 'h': releasethehelp()
  elif help_input == "g":
    print "ok, let us start the guided setup!"
    main([])
  else: robo.goodbye()
  
  sys.exit(1) # shouldnt get here, but just in case...



#################################
def getimages_master(progressdata):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #now build some urls and download files -- IF imgnum_have<imgnum_max
  imgnum_needed = int(progressdata["imgnum_max"]) - int(progressdata["imgnum_dled_thiscycle"])
  if imgnum_needed < 0: imgnum_needed = 0 # in case gets out of whack, still cut off loop
  print
  print "imgnum_needed: ", imgnum_needed
  print

  if imgnum_needed > 0:
    webfile = None #clear it up for recursive runs
    webfile = urlopen( progressdata["nexturl"])
  
    #scrape for cursor for next url and img_list
    cursor_and_imgs = getcursorandimgsrcs(webfile, imgnum_needed)
    progressdata["cursor"] = cursor_and_imgs[0]

    #bulld NEXT url, already
    if "url_built" in progressdata and progressdata["cursor"] == None:
        progressdata["nexturl"] = cfg.nomoreurls #done
    else:
      progressdata = urlbuild(progressdata)
      updatenextandbuilturls(progressdata) #swap in vars_dict (also for logfile later)
    
    #save image2url_list
    img2url_dict = cursor_and_imgs[2]
    if len(img2url_dict) > 0: progressdata["img2url_dict"] = img2url_dict
    else: progressdata["img2url_dict"] = False
      
    #and download them to imagedir
    imgsrc_list = cursor_and_imgs[1]
    if len(imgsrc_list) > 0:
      progressdata = imgsrc_getfiles(progressdata, imgsrc_list)
      
    #blank after use (prolly should be wrapped in a check...)
    imgsrc_list = []
    img2url_dict = {}    
  
  #build img2url log file
  if progressdata["img2url_dict"] :
    buildfile = buildimg2url_file(progressdata)
    if buildfile[0] == True:
      print "YAY! written/appended: " + buildfile[1]
      progressdata["img2url_dict"] = img2url_dict # which should be empty at this point
    else:
      print"---doh! NOT written! " + buildfile[1]
  
    
  #### OR RECURSE - SO WATCH OUT!
  iscomplete(progressdata)
  if progressdata["iscomplete"] == True: return progressdata
  else: getimages_master(progressdata)   #RECURSION!
  
  return progressdata #shouldnt get here, but, ya know...


#################################
def iscomplete(progressdata):
  robo.whereami(sys._getframe().f_code.co_name)

  if int(progressdata["imgnum_dled_thiscycle"]) >= int(progressdata["imgnum_max"]) or progressdata["nexturl"] == cfg.nomoreurls:
    progressdata["iscomplete"] = True
  else:
    progressdata["iscomplete"] = False
    
  return progressdata
  

#################################
def urlbuild(vars_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  
  thiscursor = vars_dict["cursor"]
  thistag = vars_dict["thistag"]
  
  if thiscursor == None: url_built = cfg.scrapeurl.replace("https","https:") + cfg.dd + thistag
  else: url_built = cfg.scrapeurl.replace("https","https:") + cfg.dd + thistag+"?"+thiscursor
  
  vars_dict["url_built"] = url_built
  return vars_dict


#################################
def getnexturl(vars_dict):
  
  robo.whereami(sys._getframe().f_code.co_name)
  
  #open local log file
  urls_list = []
  f = open(vars_dict["localurlfile"], "rU")
  for line in f:
    urls_list.append(line)
    
  nexturl_raw= urls_list[ (len(urls_list)-1)]
  nexturl = nexturl_raw.replace("\n","")
  print "nexturl "+ nexturl
  vars_dict["nexturl"]  = nexturl
  
  if nexturl == cfg.nomoreurls: iscomplete(progressdata)
    
  return vars_dict


#################################
def getcursorandimgsrcs(webfile, imgnum_needed):
  robo.whereami(sys._getframe().f_code.co_name)
  
  imgsrc_list = []
  img2url_dict = {}
  cursor = None	
  
  for line in webfile:
    match = ""
    img_match = ""
    url_match = ""
    match = re.search('cursor=([\S]+)"', line)
    img_match =  re.search(r'addthis:media="(.+\.jpg)', line)
    url_match =  re.search(r'addthis:url="(.+) addthis:media', line)
    if match:
      cursorz = match.group()
      cursor = cursorz.replace('"',"") #trim off rare trailing double-quotes
  
    #scrape webfiles for the img srcs
    if img_match:
      rawimg = img_match.group()
      if len(imgsrc_list) < imgnum_needed:
        imgsrc_list.append( rawimg.replace('addthis:media="', '') )
        if url_match:
          rawurl = url_match.group()
          imgmatch_url = rawurl.replace('" addthis:media', '').replace('addthis:url="', '')
          img2url_dict[rawimg.replace('addthis:media="', '')] = [imgmatch_url]
        
  cursor_and_imgs = [cursor, imgsrc_list, img2url_dict]
  return cursor_and_imgs
  

#################################
def updatenextandbuilturls(vars_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #write to file
  sfile = open(vars_dict["localurlfile"], "a") #this will create if not exists, open if it does
  sfile.write(vars_dict["url_built"]+"\n") # NOTE !! not nexturl - this is being written log file instead
  sfile.close()
  
  vars_dict["nexturl"] = vars_dict["url_built"] #swap in vars_dict for sequencing reasons
  
  return vars_dict


#################################
def timeout_handler(num, stack):
    raise Exception(cfg.except_tooslowload)


#################################
def imgsrc_getfiles(vars_dict, imgsrc_list):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #just to shortenup and clarify
  thistag = vars_dict["thistag"]
  localdir = vars_dict["localdir"]
  imagedir = vars_dict["imagedir"]
  imgnum = 0
  imgnum = robo.getDLedfilecount(imagedir) + 1
  
  #do some downloading
  for imgsrc_url in imgsrc_list:
      newimgname = imgsrc_makenewname(thistag, imgnum, imagedir)
      imgsrc_newimgpath = imagedir + cfg.dd + newimgname
      # setup timer stuff
      # thx - https://chamilad.github.io/blog/2015/11/26/timing-out-of-long-running-methods-in-python/
      signal.signal(signal.SIGALRM, timeout_handler)
      signal.alarm(20)

      try:
        if imgsrc_literaldownload(imgsrc_url, imgsrc_newimgpath) == True:
          if imgsrc_url in vars_dict["img2url_dict"]:
            vars_dict["img2url_dict"][imgsrc_url].append(imgsrc_newimgpath)
          imgnum += 1
          vars_dict["imgnum_dled_thiscycle"] += 1
          print "DL COUNT: ", vars_dict["imgnum_dled_thiscycle"]
        else:
          os.remove(imgsrc_newimgpath) # if didnt work, so delete
      except Exception as xept:
        if cfg.except_tooslowload in xept:
          print "========  DOH!  ========"
          print cfg.except_tooslowload_response
      finally:
        signal.alarm(0)
        
  return vars_dict


################################# #this is a sep function so it can be timed by sigalarm
def imgsrc_literaldownload(imgsrc_url, imgsrc_newimgpath):
  robo.whereami(sys._getframe().f_code.co_name)
  print "downloading started: " + time.strftime("%M:%S")
  urlretrieve(imgsrc_url, imgsrc_newimgpath)
  print
    
  #check that file worked.
  try:
    newfilesize = os.path.getsize(imgsrc_newimgpath)
  except Exception as err:
    newfilesize = 0
  
  if newfilesize > 0: return True
  else: return False
    
  return #safetyreturn 


################################# 	
def imgsrc_makenewname(thistag, imgnum, imagedir):
  robo.whereami(sys._getframe().f_code.co_name)
  
  newimgname = thistag + "_" + str(imgnum)+ "_" + time.strftime("%H%M%S") + cfg.img_suffix
  if imgsrc_nameexists(imagedir, newimgname) == True:
    imgnum = imgnum + 1
    imgsrc_makenewname(thistag, imgnum, imagedir)
  else:
    print "image: " + newimgname

  return newimgname


#################################     
def imgsrc_nameexists(imagedir, newimgname):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #check for existing
  thispath = imagedir + cfg.dd + newimgname
  if os.path.exists(thispath): return True
  else: return False
  
  return #safetyreturn
    

#################################
def classifymodel_setup(modeldirs_dict, basetag, imagequantity, thistag):
  robo.whereami(sys._getframe().f_code.co_name)	
  
  classmodeldir_choice = None

  print "CLASSIFY/LABEL IMAGES:"
  print "You can pick among your trained models to classify your downloaded images, which will be sorted"
  print "(according to the 'confidence_min' variable in the config file, currently set at "+str(cfg.confidence_min)+")"
  print "to later be harvested in the retrain stage to further improve your TensorFlow classifier."
  print
  print "Enter a number below to choose a pretrained TensorFlow model"
  print "or [ENTER] to choose the model with highest accuracy.\n"
  
  print "LABELS: '"+modeldirs_dict[0][1]+"'"
  
  modeldirs_acc_list = [] #make a list so it can be sorted/shown to user
  for k,v in modeldirs_dict.items():
    tmp_tuple = ()
    accuracy_num = v[0].split("_")[-1].replace("acc","")
    tmp_tuple = (k,v,accuracy_num)
    modeldirs_acc_list.append(tmp_tuple)
    
  modeldirs_acc_list_sorted = sorted(modeldirs_acc_list, key=lambda x: x[2], reverse = True)
  topacc = modeldirs_acc_list_sorted[0][0]
  #print for user to choose
  for md in modeldirs_acc_list_sorted:
    print "["+str(md[0])+"] "+str(md[2])+"% w/ "+md[1][0]
  
  print "[d] nah, just download the images right now,\n[h] for help, or \n[q] to quit the program... "
  modelchoice_raw = raw_input()

  if modelchoice_raw == 'h': releasethehelp() 
  if modelchoice_raw == 'q': robo.goodbye()
  if modelchoice_raw == 'd': main((basetag, imagequantity, thistag, 'download'))
  try:
    modelchoice = int(modelchoice_raw)
    classmodeldir_choice = modeldirs_dict[modelchoice][0]
  except:
    classmodeldir_choice = modeldirs_dict[topacc][0] #if they picked outside range or letter, etc
  
  print "classmodeldir_choice:", classmodeldir_choice
  print "-----------------------------------------"
  print
  
  return classmodeldir_choice


#################################
def classifymodel_getlabels(path_to_models, modeldir):
  robo.whereami(sys._getframe().f_code.co_name)
  
  modeldir_labels = ""
  path_to_labels_file = path_to_models + cfg.dd + modeldir + cfg.dd + cfg.labels_file
  if path_to_labels_file:
    f = open(path_to_labels_file, "rU")
    labels_list = []
    for line in f:
      labels_list.append(line.replace("\n","").replace(" ", "_"))
    f.close()
    modeldir_labels = ', '.join(labels_list)
  return modeldir_labels


#################################	
def classifymodel_noneexists(basetag, imagequantity, thistag, imgqnty_verified):
  robo.whereami(sys._getframe().f_code.co_name)
  
  print "PRETRAINED MODEL NEEDED TO CLASSIFY/LABEL IMAGES."
  print "No classification model(s) available to label & sort images at "+cfg.path_to_trainingsumms+"/"+basetag+"."
  print "When there are (after at least one retraining), you will be guided to pick one."
  print
  print "Enter a choice:"
  if imgqnty_verified == True:
    print "[m] to make a classification model (by running a 'retrain' cycle)"
  print "[h] to read the help,"
  print "[q] to quit and think about things, or"
  print "just hit [enter] to download (and later sort & retrain) "+str(imagequantity)+" images tagged '"+thistag+"'..."
  print
  model_or_download = raw_input()
  if model_or_download == 'm': retrain_imagesneeded(basetag, thistag)
  elif model_or_download == 'h': releasethehelp()
  elif model_or_download == 'q': robo.goodbye()
  else:
    print
    print "Let us do some downloading! here we go..."
    main((basetag, imagequantity, thistag, 'download'))
    
  return primevars_dict
  


#### RETRAIN FUNCS
#################################	
def retrain_dict_master(basetag, thistag, imagequantity, defaults = False):
  robo.whereami(sys._getframe().f_code.co_name)
  
  if defaults == False:
    retrain_dict = retrain_dict_setup()
    retrain_dict["imgharvest"] = retrain_imgmove_check(basetag)
  else:
    retrain_dict = {}
    retrain_dict["modeltype"] = cfg.retrain_model_default
    retrain_dict["mobilepercent"] = cfg.retrain_mobile_percent_default
    retrain_dict["steps"] = cfg.retrain_steps_default
    retrain_dict["imagesize"] = cfg.retrain_imgsize_default
    retrain_dict["testpercent"] = cfg.retrain_testper_default
    retrain_dict["batchsize"] = cfg.retrain_batchsize_default
    retrain_dict["imgharvest"] = cfg.retrain_imgmove_check_default
    
  
  retrain_dict["basetag"] = basetag
  retrain_dict["thistag"] = thistag
  print "Great! Here is our retraining setup:" 
  for k,v in retrain_dict.items():
    print k,":",v
  print "-----------------------------------------"
  print

  return retrain_dict


#################################
def retrain_dict_setup():
  robo.whereami(sys._getframe().f_code.co_name)	
  
  retrain_dict = {}
  retrain_dict["retrainlabels_min_count"] = 2 # was gonna be a config, but it s static for now
  retrain_dict["mobilepercent"] = None	
  
  robo.makebeep()
  print "RETRAINING SETUP: "
  print "Ok, five(5) quick options (or just hit 'enter' to use defaults)."
  print 
  print "\tNote: If you have no knowledge yet of TensorFlow parameters, give it a quick read at"
  print "\thttps://codelabs.developers.google.com/codelabs/tensorflow-for-poets/"
  print
    
  #### NOTE - MAGIC LETTERS from 'inceptionv3' and 'mobilenet' for modeltype
  #### do not change without following thru code. i didnt totally var the model names 
  #### as there are only two for now and that seemed like premature flex, in favor of speed of dev
  
  ### 1 ###
  model_and_mobileper = roboretrain.retrain_dict_setup_modeltype()
  retrain_dict["modeltype"] = model_and_mobileper[0]
  retrain_dict["mobilepercent"] = model_and_mobileper[1]
  print
  
  ### 2 ###  
  retrain_dict["steps"] = roboretrain.retrain_dict_setup_trainsteps()
  print
  
  ### 3 ###
  retrain_dict["imagesize"] = roboretrain.retrain_dict_setup_imgsize()
  print
  
  ### 4 ###  
  retrain_dict["testpercent"] = roboretrain.retrain_dict_setup_testper()
  print
  
  ### 5 ###  
  retrain_dict["batchsize"] = roboretrain.retrain_dict_setup_batchsize()
  print


  return retrain_dict



#################################	 
def retrain_imgdirs_qntycheck(basetag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #get subdirs in trainingimages/basetag
  path_to_trainingimgs_basetag = cfg.path_to_trainingimgs + cfg.dd + basetag
  imagedir_counts = robo.getimgdirscount_dict(path_to_trainingimgs_basetag)
  
  status = True
  
  if len(imagedir_counts) == 0: status = False
  
  for k,v in imagedir_counts.items():    
    if v < cfg.retrain_imgcount_default: status = False

  return status


#################################	 
def retrain_imgdirs_qntycontinue(basetag, thistag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  status = True
  if retrain_imgdirs_qntycheck(basetag) == False:
    retrain_imagesneeded(basetag, thistag) #this does not return

  return status


#################################  
def retrain_imagesneeded(basetag, thistag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #get subdirs in trainingimages/basetag
  path_to_trainingimgs_basetag = cfg.path_to_trainingimgs + cfg.dd + basetag
  imagedir_counts = robo.getimgdirscount_dict(path_to_trainingimgs_basetag)

  print "MORE IMAGES NEEDED TO RETRAIN '"+basetag+" CLASSIFER."
  print "As set in the 'retrain_imgcount_default' variable in the config file, "
  print "we need at least "+str(cfg.retrain_imgcount_default)+" images as training data per 'label' (or subdirectory)."
  print "\tCurrent number of images in:"
  for k,v in imagedir_counts.items():
    print "\t"+cfg.path_to_trainingimgs+"/"+basetag+"/"+k+":",v

  print
  print "Sure, you could go change that variable, but tensorflow docs suggest about that many as a minimum. So, instead:"
  print "1. download lots of images first, and then "
  print "2. manually sort the training data images into "+cfg.path_to_trainingimgs+"/"+basetag+"/{labeledsubdirs}"
  print "3. then run again with the 'retrain' parameter to create classification model(s)!"
  print "(step 2 is a bootstrap/first-time/one-time only requirement before the first retraining. \nFuture retrainings will harvest the high-confidence labeled & sorted images automagically.)"
  print
  print "What do you want to do?"
  print "[q] to quit the program,"
  print "[h] to read the help or,"
  print "[enter] to get this download party started!\n \
  (will download the maxnum of "+str(cfg.imgnum_maxpercycle)+" images tagged '"+thistag+", as set by imgnum_maxpercycle var in config)."
  robo.makebeep()
  download_party_raw = raw_input()
  print "-----------------------------------------"  
  print
  
  if download_party_raw == 'q': robo.goodbye()
  elif download_party_raw == "h": releasethehelp()
  else: main((basetag, cfg.imgnum_maxpercycle, thistag, 'download'))
      
  return True # but shouldnt get here


#################################
def retrain_imgmove_check(basetag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  print "RETRAIN OPTION: HARVEST PREVIOUSLY CLASSIFIED IMAGES?"
  print "Before the retraining, would you like to automagically move all the 'HIGH CONFIDENCE' images "
  print "  from: '"+cfg.path_to_testimgs+"/"+basetag+"/sorted_*/{labeled_dirs}'"
  print "  to: '"+cfg.path_to_trainingimgs+"/"+basetag+"/{labeled_dirs}'?"
  print
  print "  (Note: 'LOW CONFIDENCE' images will be remain at:"
  print "  '"+cfg.path_to_testimgs+"/"+basetag+"/sorted_*/label_underNN')"
  print
  print '''IMPORTANT: If you have not manually checked at least some of these images 
to ensure the classifier is doing a good job, you can pollute your training data. 
BUT, after a few rounds of retraining with re-checked sorted images, your classifier 
will get better and better, meaning fewer images to manually re-sort.

Enter a choice to: 
[m] to move the images (specifically: not 'copy' but 'move')
[w] (or [enter]) to continue without moving images
[h] to read the help
[q] to quit app for now.
   (and maybe go inspect the sorted files, tossing out the bad examples...)'''
  imgmovecheck_raw = raw_input()
  
  if imgmovecheck_raw == 'm': 
    print "ok! let's MOVE!"
    status=True
  elif imgmovecheck_raw == 'w': 
    print "ok! images will stay..."
    status=False
  elif imgmovecheck_raw == 'h':
    releasethehelp() 
  elif imgmovecheck_raw == 'q':
    robo.goodbye("ok buh-bye, see ya after a some manual re-sorting!")
  else:
    status=False
  print "-----------------------------------------"
  print
  
  return status


#################################
def retrain_imgharvest(basetag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  path_to_trainimg_basetag = cfg.path_to_trainingimgs + cfg.dd + basetag
  path_to_testimg_basetag = cfg.path_to_testimgs + cfg.dd + basetag
  path_to_harvestimgs_basetag = cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + cfg.harvested_dirname
  
  robo.findormakedir(path_to_harvestimgs_basetag)
  
  # get labels from training_photos dir
  trainlabels_dirs_list = []
  for trainlabelsdir in os.listdir(path_to_trainimg_basetag):
    if not trainlabelsdir.startswith('.'): # skip including hidden files
      trainlabels_dirs_list.append(trainlabelsdir) # build labeldirs_list
  
  #build sorted_* list
  sortedimgdir_list = []
  for sortedimgdir in os.listdir(path_to_testimg_basetag): # get list of all the sorted_* dirs
    if sortedimgdir.startswith(cfg.sorted_name): # only starting with "sorted_" (not "harvested")
      sortedimgdir_list.append(sortedimgdir)

  # build the PER_LABEL list if images so now the corresponding LABEL DIR
  for trainlabel_dir in trainlabels_dirs_list:
    #start a log PER LABEL
    perharvestlog_path = path_to_harvestimgs_basetag + cfg.dd + trainlabel_dir + cfg.harvested_suffix
    perharvestlog = open(perharvestlog_path, "a")
    
    # add each label dir for bigger list
    for sortedimgdir in sortedimgdir_list:
      fruits_per_dir_list = [] # wipe it clean each loop
      
      # build path
      path_sortedimages_per_label = path_to_testimg_basetag + cfg.dd + sortedimgdir + cfg.dd + trainlabel_dir
      
      #get the images from there into a list
      for sortedimage in os.listdir(path_sortedimages_per_label):
        if sortedimage.endswith(cfg.img_suffix):
          fruits_per_dir_list.append(sortedimage)
            
      # loop list with fruit and basket dirs, partly as QA check, rather than move in .append() line
      for fruit in fruits_per_dir_list:
        path_to_fruit = path_sortedimages_per_label + cfg.dd + fruit
        path_to_basket = path_to_trainimg_basetag + cfg.dd + trainlabel_dir + cfg.dd + fruit
        #do the move         
        try:
          shutil.move( path_to_fruit, path_to_basket)
          print "MOVE FRUIT( "+path_to_fruit+" -to- "+path_to_basket+" )"
          perharvestlog.write(path_to_fruit+","+path_to_basket+"\n")
        except:
          print "===error "+path_to_fruit+" to "+trainlabel_dir+""
          perharvestlog.write(path_to_fruit+",error \n")
	print "---------"

  perharvestlog.close()
	
  #create log file of move before list gets wiped in next go round
  harvestlog_path = path_to_harvestimgs_basetag + cfg.dd + cfg.harvested_dirname + cfg.harvested_suffix
  harvestlog = open(harvestlog_path, "a")
  # then move all sorted_ dirs to harvested, so cycle can begin again
  for sortedimgdir in sortedimgdir_list:
    path_to_sortedimgdir = path_to_testimg_basetag + cfg.dd + sortedimgdir    
    try:
      shutil.move(path_to_sortedimgdir, path_to_harvestimgs_basetag)
      print "HARVEST: "+path_to_sortedimgdir+" -to- " + path_to_harvestimgs_basetag
      harvestlog.write(path_to_sortedimgdir+","+path_to_harvestimgs_basetag+"\n")
    except:
      harvestlog.write(path_to_sortedimgdir+",error \n")

  harvestlog.close()
  
  print "-----------------------------------------"
  print
  
  status = True # todo - get meaningful status
  return status


#################################	
def retrain_getstarted(retrain_dict):
  robo.whereami(sys._getframe().f_code.co_name)

  status = roboretrain.main(retrain_dict)
  return status  
 
 
#################################
def buildimg2url_file(progressdata):
  robo.whereami(sys._getframe().f_code.co_name)
  
  thistag = progressdata["thistag"]
  localdir = progressdata["localdir"]
  img2url_file = localdir + cfg.dd + cfg.img2url_prefix + thistag + cfg.img2url_suffix
  fmake = open(img2url_file, "a")

  #write log file
  try:
    thisdict = progressdata["img2url_dict"]
    if len(thisdict) > 0:
      for k,v in thisdict.items(): 
        fmake.write(k+","+v[0]+","+v[1]+"\n")
      fmake.close()
  except:
    pass
 
  #check it worked
  if os.stat(img2url_file).st_size == 0: status = False
  else: status = True 
  
  print
  return (status, img2url_file)


#################################
def senddonenotif(progressdata):
  robo.whereami(sys._getframe().f_code.co_name)
  
  #set up the txt msg
  sms_class_note = ""
  status = False
  timespent_downloading = int(progressdata["time_end"]) - int(progressdata["time_start"])
  if timespent_downloading > cfg.sms_minsecstonotify:
    if progressdata["d_c_r_flow"] == 'dl_class': sms_class_note = "Classification starting... "
    sms_start = "downloads done: " + str(progressdata["imgnum_dled_thiscycle"]) + " imgs of '"+progressdata["thistag"]+"'" 
    sms_msg = sms_start + sms_class_note + cfg.sms_end
    status = robo.sendsms(sms_msg)
  
  return status


#################################
def classify_downloadedimages(progressdata):
  robo.whereami(sys._getframe().f_code.co_name)
  
  dled_images = []
  for file in os.listdir(progressdata["imagedir"]):
    if file.endswith(cfg.img_suffix):
      dled_image = file
      print "---classify this image ---> "+ dled_image
      shutil.copy(progressdata["imagedir"]+cfg.dd+dled_image, progressdata["path_to_testimgs_basetag"]+cfg.dd+dled_image)
    
  #kick off testing script
  model_data = {}
  model_data["basetag"] = progressdata["basetag"]
  model_data["model_dir"] = progressdata["classify_model_dir"]
  classmodeldir_start = progressdata["classify_model_dir"][0]
  # warning MAGIC LETTERS! search "magic letters" for more details
  if classmodeldir_start == "i": model_data["model_type"] = cfg.inception_model 
  if classmodeldir_start == "m": model_data["model_type"] = cfg.mobile_model	

  print #special case here so speaicl top print spacer line
  print "============== START THE REAL ACTION ===================="
  print " classify with: "+ model_data["model_dir"]
  print "========================================================="
  print
  
  ### kick off tensorflow classifier
  status = roboclass.main(model_data)
  return status


#################################
def setup_args_vars_dirs(args, preflight_dict):
  robo.whereami(sys._getframe().f_code.co_name)	
  
  modeldirs_dict = {}
  primevars_dict = {}
  primevars_dict["modeldirs_dict"] = modeldirs_dict

  # vars from preflight/guided setup
  if preflight_dict["masterclass_verified"] == True:
    basetag = preflight_dict["mastertag_dict"]["basetag_dict"]["basetag"]
    imgnum_maxTHIScycle = preflight_dict["mastertag_dict"]["imagequantity"]
    thistag = preflight_dict["mastertag_dict"]["thistag"]
    flow = preflight_dict["flow_qualified"]
  else: # or use command line params
    robo.goodbye("preflightcheck() issue... must to stop now. lo siento.")

  #then build up the structure
  localdir = cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + cfg.unsorted_name+thistag
  imagedir = cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + cfg.unsorted_name+thistag + cfg.dd + thistag  	
  localurlfile = localdir + cfg.dd + cfg.urlfile_prefix + thistag + cfg.urlfile_suffix
  robo.findormakedir(cfg.path_to_testimgs)
  robo.findormakedir(localdir) #stores log files and imagedir
  robo.findormakedir(imagedir) #stores UNSORTED downloaded images
  robo.findormakedir(cfg.path_to_trainingsumms)
  robo.findormakedir(cfg.path_to_trainingsumms + cfg.dd + basetag)
  robo.findormakedir(cfg.path_to_trainingimgs)
  robo.findormakedir(cfg.path_to_trainingimgs + cfg.dd + basetag)   	  

  ### start the localurlfile/nextURL file
  fmake = open(localurlfile, "a")
  if os.stat(localurlfile).st_size == 0:
  	startingurl = cfg.scrapeurl.replace("https","https:") + cfg.dd + thistag
  	fmake.write(startingurl+"\n")
  else:
    #exists, so add nothing for now...
    pass
  fmake.close()

  	
  # add it all to a dict(s) for convenience, even if some duplimadupitercation
  primevars_dict["time_start"] = time.strftime("%H%M%S")
  primevars_dict["imgnum_max"] = imgnum_maxTHIScycle
  primevars_dict["basetag"] = basetag
  primevars_dict["thistag"] = thistag
  primevars_dict["localdir"] = localdir
  primevars_dict["imagedir"] = imagedir
  primevars_dict["localurlfile"] = localurlfile
  primevars_dict["imgnum_in_dir"] = robo.getDLedfilecount(imagedir)
  primevars_dict["path_to_testimgs_basetag"] = cfg.path_to_testimgs + cfg.dd + basetag
  primevars_dict["img2url_dict"] = {}
  primevars_dict["preflight_dict"] = preflight_dict
  primevars_dict["flow"] = flow
  primevars_dict["d_c_r_flow"] = preflight_dict["d_c_r_flow"]

  '''print "PRIMEVARS"
  for k,v in primevars_dict.items():
    print k,"",v'''
  

  ####### FLOW VAR (download, classify, retrain)
  flowlist = preflight_dict["flowlist"]## determine flow based on preflight checks
  
  path_to_models = cfg.path_to_trainingsumms + cfg.dd + basetag
  modeldirs_dict = robo.getdirlist_dict(path_to_models) #returns dict
  for k,modeldir in modeldirs_dict.items():
    modeldir_labels = classifymodel_getlabels(path_to_models, modeldirs_dict[k])
    modeldirs_dict[k] = (modeldir, modeldir_labels)

  # flowvar conjiggling
  if primevars_dict["d_c_r_flow"] == "dl_class": 
    if len(modeldirs_dict) > 0:
      #setup clasify
      primevars_dict["classify_model_dir"] = classifymodel_setup(modeldirs_dict, basetag, imgnum_maxTHIScycle,  thistag)
      classmodeldir_start = primevars_dict["classify_model_dir"][0]# (NOTE: search MAGIC LETTERS for description)
    else:
      imgqnty_verified = primevars_dict["preflight_dict"]["imgqnty_verified"] 
      classifymodel_noneexists(basetag, imgnum_maxTHIScycle, thistag, imgqnty_verified) #does not return    
  
  # DOWNLOAD CLASSIFY & RETRAIN
  if primevars_dict["d_c_r_flow"] == "dl_class_retrain":
    #setup classify
    primevars_dict["classify_model_dir"] = classifymodel_setup(modeldirs_dict, basetag, imgnum_maxTHIScycle,  thistag)
    classmodeldir_start = primevars_dict["classify_model_dir"][0]# (NOTE: search MAGIC LETTERS for description)

    # setup retrain
    if roboretrain.retrain_yes() == True:
      primevars_dict["retrain_dict"] = retrain_dict_master(basetag, thistag, imgnum_maxTHIScycle)
    else:
      primevars_dict["d_c_r_flow"] = "dl_class"
    
    #continue or not
    if retrain_imgdirs_qntycontinue(basetag, thistag) == False:
      robo.goodbye("retrain not gonna work msg... stopping.")
    

  # DOWNLOAD and RETRAIN
  if primevars_dict["d_c_r_flow"] == "dl_retrain":
    # setup retrain
    if roboretrain.retrain_yes() == True:
      primevars_dict["retrain_dict"] = retrain_dict_master(basetag, thistag, imgnum_maxTHIScycle)
    else:
      primevars_dict["d_c_r_flow"] = "dl_class"

    #continue or not
    if retrain_imgdirs_qntycontinue(basetag, thistag) == False:
      robo.goodbye("retrain not gonna work msg... stopping.")

  # RETRAIN with config file default values
  if primevars_dict["d_c_r_flow"] == "retrain_defaults":
    primevars_dict["retrain_dict"] = retrain_dict_master(basetag, thistag, imgnum_maxTHIScycle, defaults=True)
    

  return primevars_dict


#################################	
def preflightchecks(args):
  robo.whereami(sys._getframe().f_code.co_name)
  
  preflight_dict = {}
  # check for REQD dirs - train_photos, test_photos, training_summs
  for setupdir in cfg.paths_to_reqddirs_list:
    robo.findormakedir(setupdir)
  
  # check for masterclass(ie,basetag) and subclass
  if len(args) == 0: #if params passed, dont do this setup stuff...
    #step 1
    preflight_dict['mastertag_dict'] = preflight_setup() 
    basetag = preflight_dict["mastertag_dict"]["basetag_dict"]["basetag"]
     #step 2
    imagequantity = preflight_imagequantity(basetag)
    preflight_dict['mastertag_dict']["imagequantity"] = imagequantity
    #step 3
    thistag = preflight_thistag(basetag) 
    preflight_dict['mastertag_dict']["thistag"] = thistag
    
    #for convenience pull these out, too
    flowasinput = None
    preflight_dict["masterclass_verified"] = preflight_dict['mastertag_dict']["masterclass_verified"]  
    preflight_dict["flow_qualified"] = "download" #this will POTENTIALLY get updated as this func progresses
    
  else:
    basetag = args[0]
    imagequantity_arg = args[1]
    try:
      imagequantity_int = int(imagequantity_arg)
    except: 
      print "doh! NUMBERS ONLY for 2nd parameter. you might need some --help"
      releasethehelp()
    imagequantity = robo.get_imgnumcycle(imagequantity_int)
      
    thistag = args[2]
    flowasinput = args[3]
    basetag_dict = {}
    basetag_dict["basetag"] = basetag
    mastertag_dict = {}
    mastertag_dict["basetag_dict"] = basetag_dict
    mastertag_dict["imagequantity"] = imagequantity
    mastertag_dict["thistag"] = thistag
    preflight_dict["mastertag_dict"] = mastertag_dict
    preflight_dict["masterclass_verified"] = True
    preflight_dict["flow_qualified"] = flowasinput

    #other dirs from NEW advanced param basetag, thistag
    robo.findormakedir(cfg.path_to_trainingimgs + cfg.dd + basetag)
    robo.findormakedir(cfg.path_to_testimgs + cfg.dd + basetag)
    robo.findormakedir(cfg.path_to_trainingsumms + cfg.dd + basetag)

  
  # check tsumm dir for models
  modeldir_exists = robo.getdirlist_dict(cfg.path_to_trainingsumms + cfg.dd + basetag)
  if len(modeldir_exists) > 0:
    preflight_dict["classmodel_verified"] = True
    preflight_dict["flow_qualified"] = "classify" # update this to allow classify
  else:
    preflight_dict["classmodel_verified"] = False
    if flowasinput == "classify":
      print "----------- NOTE ----------- "
      print "No classification model(s) available to label & sort images.\nWhen there are (after at least one retraining), you will be guided to pick one.\n\nFor now, let us just do some downloading?"
      justdownload_raw = raw_input("[h] for help & additional explanation\n[q] to quit\n[enter] to get to downloadin'... \n")
      if justdownload_raw == 'q':robo.goodbye()
      elif justdownload_raw == 'h':releasethehelp()
      else: print "let us download!"

      
  # check traindir/subclass-dirs for min qnty
  if retrain_imgdirs_qntycheck(basetag) == True:
    preflight_dict["imgqnty_verified"] = True
    preflight_dict["flow_qualified"] = "retrain"  # update this to allow retrain
  else:
    preflight_dict["imgqnty_verified"] = False
    if flowasinput == "retrain":
      print "----------- NOTE ----------- "
      print "We do not have the required "+str(cfg.retrain_imgcount_default)+" sorted images"
      print "in "+cfg.path_to_trainingimgs+"/"+basetag+"/{labeled subdirs} to retrain!\n\nFor now, let us just do some downloading?"
      justdownload_raw = raw_input("[h] for help & additional explanation\n[q] to quit\n[enter] to get to downloadin'...\n")
      if justdownload_raw == 'q': robo.goodbye()
      elif justdownload_raw == 'h': releasethehelp()
      else: print "let us download!"

  #now use those _verified to make a list in one func rather than spread about
  preflight_dict["flowlist"] = preflight_getflowlist(preflight_dict)
  
  if "download" in preflight_dict["flowlist"]:
    preflight_dict["d_c_r_flow"] = "download"
    
  if "download" and "classify" in preflight_dict["flowlist"]: 
    if imagequantity > 0 :
      preflight_dict["d_c_r_flow"] = "dl_class"
    else:
      preflight_dict["d_c_r_flow"] = "download"
      
  if "download" and "classify" and "retrain" in preflight_dict["flowlist"]: 
    if imagequantity > 0 :
      preflight_dict["d_c_r_flow"] = "dl_class_retrain"
    else:
      preflight_dict["d_c_r_flow"] = "dl_retrain"
    
  if "download" and "retrain" in preflight_dict["flowlist"]:
      if "classify" not in preflight_dict["flowlist"]: 
        preflight_dict["d_c_r_flow"] = "dl_retrain"

  # allow input param to override, if qualified
  if flowasinput == "download": preflight_dict["d_c_r_flow"] = "download" 
  if flowasinput == "classify" and "classify" in preflight_dict["flowlist"]: preflight_dict["d_c_r_flow"] = "dl_class" 
  if flowasinput == "retrain" and "retrain" in preflight_dict["flowlist"]: 
    if imagequantity > 0:
      preflight_dict["d_c_r_flow"] = "dl_class_retrain" 
    else:
      preflight_dict["d_c_r_flow"] = "dl_retrain" 
      
  if flowasinput == "retrain_defaults" and "retrain" in preflight_dict["flowlist"]:
    if imagequantity > 0:
      preflight_dict["d_c_r_flow"] = "dl_retrain" 
    else:
      preflight_dict["d_c_r_flow"] = "retrain_defaults"  


  #print "preflight_dict", preflight_dict
  return preflight_dict


#################################	
def preflight_setup():
  robo.whereami(sys._getframe().f_code.co_name)
  
  # check for basetags in testphotos
  basetagdirs_dict = {}
  i = 1
  for basetagdir in os.listdir(cfg.path_to_testimgs):
    if not basetagdir.startswith('.'): #remove hidden files
      basetagdirs_dict[i] = basetagdir
      i += 1

  print "ROBOFLOW SETUP:"
  print "ok, to start we need 3 quick things:"
  print "1. a broad theme of this endeavor, aka a 'master classification tag'."
  print
  print "Enter a letter to make a choice:"
  print "[m] to make a new one"
  if len(basetagdirs_dict) > 0:
    for k,v in basetagdirs_dict.items():
      print "["+str(k)+"]: "+v+""
  print "--- or ---"
  print "[h] whhhhat the heck is all this? i should read the help..."
  print "[q] nah, imma quit..."
  setup_or_not_raw = raw_input()
  basetag_dict = {}

  try:
    setup_or_not = int(setup_or_not_raw)
    basetag_dict["basetag"] = basetagdirs_dict[setup_or_not]
  except:
    if setup_or_not_raw == 'q': robo.goodbye()
    elif setup_or_not_raw == 'h': releasethehelp()  
    else:
      print "ok, let us make a new one..."
      basetag_dict = preflight_basetag()
      #then make a basetag dir in the reqd dirs
      for reqdir in cfg.paths_to_reqddirs_list:
        path_to_basetagdir = reqdir + cfg.dd + basetag_dict["basetag"]
        robo.findormakedir(path_to_basetagdir)
        #now make some label dirs too
        for labeldir in basetag_dict["labeldirs_list"]:
          path_to_labeldir = path_to_basetagdir + cfg.dd + labeldir
          if reqdir == cfg.path_to_trainingimgs:
            robo.findormakedir(path_to_labeldir) 
 
  if len(basetag_dict) > 0: masterclass_verified = True
  else: masterclass_verified = False

  #return the info
  mastertag_dict = {}
  mastertag_dict["masterclass_verified"] = masterclass_verified
  mastertag_dict["basetag_dict"] = basetag_dict

  print
  return mastertag_dict	


#################################
def preflight_basetag():
  robo.whereami(sys._getframe().f_code.co_name)

  print
  print "MASTER CLASSIFICATION TAG ('basetag') SETUP:"
  print "because you can use this tool for multiple different classification tasks,"
  print "please enter a broad theme to call this one, like 'robots' or 'pirates' or 'birds_v2' etc."
  print "Next, under this master class you will add sub-classes, such as 'drawn, built, not' or whatever."
  print "(note: very good idea to have a 'not' category as many tagged images are NOT their tag at all.)"
  basetag_raw = raw_input("master classification: ")
  
  if basetag_raw == "q": robo.goodbye()
  if basetag_raw == "h": releasethehelp()
  if len(basetag_raw)<3: print "doh, must be at least THREE characters. start over! whaaa??\n", preflight_basetag()
  
  labeldirs_raw = raw_input("comma-separated list of lowercase no-space alphanumeric sub-classes: ")  
  basetag = basetag_raw.lower().replace(" ", "_")
  labeldirs_list = labeldirs_raw.lower().replace(" ", "").split(",")
  
  basetag_dict = {}
  basetag_dict["basetag"] = basetag
  basetag_dict["labeldirs_list"] = labeldirs_list
  
  return basetag_dict 



#################################
def preflight_imagequantity(basetag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  imagequantity_raw = raw_input("2. how many "+basetag+"-themed images to download: ")
  if imagequantity_raw == "h": releasethehelp()
  if imagequantity_raw == "q": robo.goodbye()
  try:
    imagequantity_int = int(imagequantity_raw)
  except: 
    print "doh! NUMBERS ONLY. try again!"
    imagequantity_int = preflight_imagequantity(basetag) # ojo RECURSION
  
  imagequantity = robo.get_imgnumcycle(imagequantity_int)

  return imagequantity


#################################
def preflight_thistag(basetag):
  robo.whereami(sys._getframe().f_code.co_name)
  
  thistag_raw = raw_input("3. and the '"+basetag+"'-related tag to search: ")
  if thistag_raw == "h": releasethehelp()
  if thistag_raw == "q": robo.goodbye()
  if len(thistag_raw.replace(" ","")) < 1: 
    print "No blank tags allowed. type something, yo!"
    thistag = preflight_thistag(basetag)# ojo RECURSION
  try:
    thistag = thistag_raw.lower().replace(" ","_")
  except:
    print "No blank tags allowed. type something, yo!"
    thistag = preflight_thistag(basetag)# ojo RECURSION

  return thistag
  
  
#################################
def preflight_getflowlist(preflight_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  
  flowlist = []
  if preflight_dict["imgqnty_verified"] == True: flowlist.append("retrain")  
  if preflight_dict["classmodel_verified"] == True: flowlist.append("classify")  
  if preflight_dict["masterclass_verified"] == True: flowlist.append("download")  
  
  return flowlist
  
 
#################################	 
#################################	
def main(args):
  robo.whereami(sys._getframe().f_code.co_name) #global show/dont show in config file

  print robo.greeting()
  
  #if some params present
  if len(args) > 0:
    if str(args[0]) in ('-h', '--help'): releasethehelp()
    if str(args[0]) in ('--helpmore'): releasethehelp_details()
    
    try:
      int(args[1]) 
    except:
      print "bad parameters are bad!"
      print
      print "guided: 'python " + cfg.download_script +"'"
      print "advanced: 'python " + cfg.download_script + " robots 100 robotart download'"
      print '  python ' + cfg.download_script + ' [basetag] [imagequantity] [searchtag] [download|classify=default|retrain]'
      print
      print "maybe it's time read the help?"
      print "[h] to read help\n[t] to try again "
      hq_raw = raw_input()
      if hq_raw == "h": releasethehelp()
      else: robo.goodbye("you can do this -- i believe in you!")
    
    if len(args) == 3: args.append(cfg.flow_default) #set as default if left blank  
    if len(args) < 3: releasethehelp()
  
  # do these no matter what
  preflight_dict = preflightchecks(args)
  vars_dict = setup_args_vars_dirs(args, preflight_dict)
  
  #get nexturl
  progressdata = getnexturl(vars_dict)
  
  #get some images from it
  progressdata["imgnum_dled_thiscycle"] = 0
  progressdata = getimages_master(progressdata)

  #end download actions (and kick off next actions in another module?)
  if progressdata["iscomplete"] == True:
    imgnumdled = progressdata["imgnum_dled_thiscycle"]
    if imgnumdled == 0: imgnumdled = 1 #evenif zero images dled, this prevents /0 error, not that critical...
    progressdata["time_end"] = time.strftime("%H%M%S")
    progressdata["time_avg"] = (float(progressdata["time_end"])-float(progressdata["time_start"])) / float(imgnumdled)
    
    print "iscomplete() PROGRESSDATA: "
    for k,v in progressdata.items(): print k,":",v
    print
    
    #send txt when downloading done, if taken longer than cfg.sms_minsecstonotify
    if cfg.twilio_active == True: 
      if progressdata["imgnum_dled_thiscycle"] > 0:
        sendtxt = senddonenotif(progressdata)
    
    
    path_to_trainingimgs_basetag = cfg.path_to_trainingimgs + cfg.dd + progressdata["basetag"]
    imagedir_counts = robo.getimgdirscount_dict(path_to_trainingimgs_basetag)
      
    print "-----------------------------------------------------------------------"
    print "\tWINNING! "+str(progressdata["imgnum_dled_thiscycle"])+" downloads done been downloaded to:"
    print "\t"+progressdata["localdir"]+""
    print "-----------------------------------------------------------------------"
    print
    
    
    
    
    ####### THE REAL POINT OF THIS: classify or re/train
   
    if progressdata["d_c_r_flow"] == 'dl_class' and progressdata["imgnum_dled_thiscycle"] > 0:
      print "now, kickoff TensorFlow image classification/labeling..."
      classify_downloadedimages(progressdata)
    
    elif progressdata["d_c_r_flow"] == 'dl_class_retrain':
      if progressdata["imgnum_dled_thiscycle"] > 0:
        print "first, do TensorFlow image labeling of downloaded images,"
        print "then, use the "+str(cfg.confidence_min)+"% confidence ones in retraining..."
        classify_downloadedimages(progressdata)

      if progressdata["retrain_dict"]["imgharvest"] == True: retrain_imgharvest(progressdata["basetag"])
      print "let us now use the "+str(cfg.confidence_min)+"% confidence ones in retraining..."
      retrain_getstarted(progressdata["retrain_dict"])
      
    elif progressdata["d_c_r_flow"] == 'dl_retrain' or progressdata["d_c_r_flow"] == 'retrain_defaults':
      if progressdata["retrain_dict"]["imgharvest"] == True: retrain_imgharvest(progressdata["basetag"])
      print "let us now use the "+str(cfg.confidence_min)+"% confidence ones in retraining..."
      retrain_getstarted(progressdata["retrain_dict"])
   
    else:
      # this is DOWNLOAD ONLY (as only one left)
      pass 
      
    
    print "-----------------------------------------------------------------------"
    if progressdata["preflight_dict"]["classmodel_verified"] == False:
      print "\tNOTE: No classification model(s) available to label & sort images.\n\tWhen there are (after at least one retraining), you will be guided to pick one."
      print
    print "\tNote: Classification models are created when you 'retrain' TensorFlow."
    print "\tTo retrain, you need "+str(cfg.retrain_imgcount_default)+" sorted images per label."
    print "\tCurrent counts:"
    for k,v in imagedir_counts.items():
      print "\t"+cfg.path_to_trainingimgs+"/"+progressdata["basetag"]+"/"+k+": "+str(v)
    print "-----------------------------------------------------------------------"
    print
    robo.goodbye("and thanks for helping a robot feel useful!")
    
    ###### MAIN EXIT    
    


  else:
    robo.goodbye("Somewun dun goofed, shouldnt be here... sad era sad era sad era!")



#################################
# boilerplate kicker offer (yes thats a tech term!)   
if __name__ == '__main__':
  
  try:
    args
  except:
    args = sys.argv[1:]
  
  main(args)





