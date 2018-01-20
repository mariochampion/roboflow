#!/usr/bin/env python
''' 
ROBOFLOW support functions - 
central location for functions used across various roboflow scripts.
Also, twilio account setup requires credit card to fund txt msgs.
Details at https://www.twilio.com/blog/2016/10/how-to-send-an-sms-with-python-using-twilio.html
'''

## ===================================================================
## ROBOFLOW - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/roboflow
## released under the Apache License 2.0. (http://www.apache.org/licenses/LICENSE-2.0)
## and depends on many contributions from the internets, stackexchange, twilio, and 
## of course and especially the Google TensorFlow for Poets codelab:
##     tutorials: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/ 
##     code: https://github.com/googlecodelabs/tensorflow-for-poets-2
## 
## ROBOFLOW scripts were  written by mario champion (mariochampion.com) as an exercise to learn 
## more python file/dir manipulation, in a commandline driven app, and to better understand the
## Google's TensorFlow image classification elements and hyperparameter effects.
##
## please open issues and pull requests,
## thanks and always remember: this robot loves you. 
## boop boop!
## ===================================================================



import os, sys, random, time
from glob import glob1
#import roboflow specific stuff
import robo_config as cfg
import robo_help as help
if cfg.twilio_active == True: from twilio.rest import Client



##################################	
## just a debug placefinder to help trace actions
def whereami(funcname):
  if cfg.show_whereami == True:
    print
    print "-------------", funcname, " ------------------" 
    print



#################################
def makebeep():
  print '\a' # trick to make beep noise when user input required



##################################	
def greeting():

  print "----------------------------------------------------------------"
  print "     hello and welcome to roboflow, a tensorflow explorer."
  print "(a virtuous cycle of 1. download 2. classify/label 3. retrain.)"
  print "----------------------------------------------------------------"
  return ""
  

def greeting_big():
  print cfg.color.green
  print '''
----------------------------------------------------------------
     hello and welcome to roboflow, a tensorflow explorer.
             __   __   __   __   __      __ 
            |__| |  | |__) |  | |__ |   |  | \    /
            |  \ |__| |__) |__| |   |__ |__|  \/\/
 
 (a virtuous cycle of 1. download 2. classify/label 3. retrain.)
----------------------------------------------------------------'''
  print cfg.color.white
  return ""



#################################
def zero_dl_classify_msg(msg):
  
  print msg
  print cfg.color.yellow + "Note: Classification will be skipped as you are not downloading any new images." + cfg.color.white
  print "(set 'imagequantity' parameter > 0 to run a classifier')"
  print
  return



#################################
# should prolly adapt this to also accept list of dirs and loop thru them
def findormakedir(path_to_thisdir):
  whereami(sys._getframe().f_code.co_name)
  
  #make if needed
  if not os.path.exists(path_to_thisdir):
    os.makedirs(path_to_thisdir)
    print "find or make: "+path_to_thisdir
    print
    status = True
  else:
    status = False
  
  return status



#################################
def getDLedfilecount(imagedir):
  whereami(sys._getframe().f_code.co_name)

  #look for existing local dir
  if os.path.exists(imagedir): dledfilecount = (len(glob1(imagedir,"*"+cfg.img_suffix)))
  else: dledfilecount = 0

  return dledfilecount



#################################	 
def getdirlist_dict(path_to_dir):
  whereami(sys._getframe().f_code.co_name)

  dirlist_dict = {}
  i = 0
  for dir in os.listdir(path_to_dir):
    if not dir.startswith('.'): #remove hidden dirs/files
      dirlist_dict[i] = dir
      i += 1
  
  return dirlist_dict
  


#################################	 
def getimgdirscount_dict(path_to_dir):
  whereami(sys._getframe().f_code.co_name)
  
  imgdirscount_dict = {}
  for imagedir in os.listdir(path_to_dir):
    if not imagedir.startswith('.'): #remove hidden files
      imgdirscount_dict[imagedir] = getDLedfilecount(path_to_dir + cfg.dd + imagedir)
      
  return imgdirscount_dict



#################################
def get_imgnumcycle(thisint):
  whereami(sys._getframe().f_code.co_name)	
  
  imgnumcycle = thisint
  if imgnumcycle > cfg.imgnum_maxpercycle:
    imgnumcycle = cfg.imgnum_maxpercycle
    makebeep()
    print cfg.color.magenta
    print "WHOA! Too many images requested at once."
    print "To not hammer their server, it has been reduced to " + cfg.color.cyan + str(imgnumcycle) + cfg.color.magenta + " per cycle.\n"
    print cfg.color.white
    print "Press [q] to stop app, and go change 'imgnum_maxpercycle' var in "+cfg.config_script+", or"
    print "enter any other key to keep going..."
    keepgoing = raw_input()
    if keepgoing == 'q': goodbye()
  
  print #just a line for readability
  return imgnumcycle	



#################################	 
def createfilefromdict(path_to_file, thisdict):
  whereami(sys._getframe().f_code.co_name)
  
  #make / append a file from a dict
  fmake = open(path_to_file, "a")
  for k,v in thisdict.items():
    fmake.write(str(k)+","+str(v)+"\n")  
  fmake.close()
  
  if os.stat(path_to_file).st_size == 0:
    status = False
  else:
    print "yay! created: " + path_to_file
    status = True 

  print #just a line for readability
  return status


#################################	 
def makelocalofwebfile(webfile, progressdata):
  whereami(sys._getframe().f_code.co_name)
  
  basetag = progressdata["basetag"]
  thistag = progressdata["thistag"]
  scrapefile_prefix = progressdata["scrapefile_prefix"]
  scrapefile_suffix = progressdata["scrapefile_suffix"]
  
  fwebpath = cfg.path_to_testimgs + cfg.dd + basetag + cfg.dd + cfg.unsorted_name + thistag
  webfile_local = fwebpath + cfg.dd + scrapefile_prefix + thistag + "_" + time.strftime("%M%S") + scrapefile_suffix
  with open(webfile_local, 'a') as fweb:
    fweb.write(webfile.read())
      
    ## provide a little feedback/update to user
    print cfg.color.yellow
    print "URL:\t",progressdata["nexturl"]
    print "as:\t", webfile_local
    print cfg.color.white
    
  return webfile_local



##################################
def imgs_existing_build(img2url_filename):
  whereami(sys._getframe().f_code.co_name)
  
  imgs_existing = []
  if img2url_filename:
    print "DLed imgs list", img2url_filename
    if os.path.exists(img2url_filename):
      img2url_contents = open(img2url_filename, "r").read().split("\n")
      for i in img2url_contents:
        imgs_existing.append(i.split(",")[0])
  else:
    print "no img2url_filename"
  
  print "DLed imgs count:", len(imgs_existing)
  
  
  return imgs_existing


##################################
def getimagelist_fromdir(thisdir):
  whereami(sys._getframe().f_code.co_name)
  
  images_list = []
  for file in os.listdir(thisdir):
    if file.endswith(cfg.img_suffix): #JPG ONLY! (should this be more open?
      images_list.append( (os.path.join(thisdir, file)) )
  
  if len(images_list) < 1:
    print cfg.color.magenta
    print "DOH! no '"+cfg.img_suffix+"' images to test at "+thisdir
    print cfg.color.white
    print "maybe go check for actual images there..."
    print 
    goodbye("this is how we end...")

  return images_list
  


##################################	
def sendsms(sendmsg):
  whereami(sys._getframe().f_code.co_name)
  
  #chk for required vars
  if not sendmsg:
    status = False
  else:
    account_sid	= os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token	= os.environ.get('TWILIO_AUTH_TOKEN')
    sigline		= os.environ.get('TWILIO_SIGLINE')
    
    try:
      client = Client(account_sid, auth_token)
      client.messages.create(from_ = os.environ.get('TWILIO_PHONE_NUMBER'),
    						to = os.environ.get('TWILIO_SENDTONUM'),
    						body = '"'+sendmsg+'"'+sigline)
      status = True
    except:
      status = False						

  return status                    




##################################	
def goodbye(msg = None):
  whereami(sys._getframe().f_code.co_name)
  
  if not msg: finalwords = random.choice(cfg.finalwords_list)
  else: finalwords = msg
  
  print
  print finalwords
  print cfg.sigline
  print
  
  sys.exit(1)
