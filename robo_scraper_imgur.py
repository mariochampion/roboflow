#!/usr/bin/env python
'''
robo_scraper_imgur contains the IMGUR API specific versions of the scraping functions:
-getimagesmaster()
-getnexturl()
-getcursorandimgsrcs()

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

import os, sys
import robo_config as cfg
import robo_support as robo 


print cfg.color.yellow
print "++++++++++++++++++++++++++++++++++++"
print "     IMGUR API FUNCTIONS LOADED"
print "++++++++++++++++++++++++++++++++++++"
print cfg.color.white


##################################	  
###  hey, have some functions  ###	  
##################################


##################################	
def imgurapi_clientid_confirm():
  robo.whereami(sys._getframe().f_code.co_name)
  
  try:
    imgur_client_id = 'Client-ID '+os.environ.get('IMGURAPI_ID')
    return imgur_client_id
    
  except:
    print cfg.color.yellow + '''
Slowwww down -- no Imgur API Client-ID in environment variables.
(and thus, no ability to download images from imgur.com...) 
Set yourself up at: 
\thttps://apidocs.imgur.com/
take 10 seconds to add it to your environment (on mac) at:
\thttp://osxdaily.com/2015/07/28/set-enviornment-variables-mac-os-x/
'''
    print cfg.color.white 
    goodbye() 
  
  sys.exit(1) # for safety
   


#################################	