#!/usr/bin/env python
'''
robo_scraper_imgur contains the WEBSTAGRAM specific versions of the scraping functions:
- getimagesmaster()
- getnexturl()
- getcursorandimgsrcs()
- urlbuild()
- webfileprep()

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

import os, sys, re, json
from urllib2 import Request, urlopen
from urllib import urlopen as urlopen_alt
import robo_config as cfg
import robo_support as robo 

# SPECIFIC 'GLOBAL' VARS FOR THIS SCRAPER
scrapeurl = "https//web.stagram.com/tag" # no colon as it breaks this file. added JIT
imgdlfile_url_prefix = "https//web.stagram.com/p/"
imgdlfile_url_suffix = ".jpg"
scrapefile_prefix = "__webstagram_"
scrapefile_suffix = ".txt" # sep name for max flex of diff later needs
scrape_sort = None
scrapeurl_pagenum = "?cursor="



##################################	  
###  hey, have some functions  ###	  
##################################

##################################
def functionsloaded():
  robo.whereami(sys._getframe().f_code.co_name)
  print cfg.color.yellow + "WEBSTAGRAM FUNCTIONS LOADING..."
  print cfg.color.white
  return
  
#################################
def getcursorandimgsrcs(webfile_prepped, imgnum_needed, progressdata):
  robo.whereami(sys._getframe().f_code.co_name)
  
  imgurl_list = [] # specific to going to big image page, not thumbnail
  imgsrc_list = []
  img2url_dict = {}
  cursor = None	
  basetag = progressdata["basetag"]
  thistag = progressdata["thistag"]

  #build a list of images for de-dupe. with a refactor, i would make a single list of 
  # imgnum_needed urls and pass that to a download module... for now i ll check the logfile
  imgs_existing = robo.imgs_existing_build(progressdata["img2url_file"])
  
  #get cursor - \/(.+)Load more
  cursor_match = re.findall( r'(.+)Load More', webfile_prepped.read() )
  try:
    cursor_thegoodpart = cursor_match[0].split("?cursor=")[1]
    cursor = cursor_thegoodpart.replace('">','')
  except:
    pass #regex issue
  
  webfile_prepped.seek(0)    
  imgs_in_file = re.findall( r'\/p\/(.{11})', webfile_prepped.read() )
  for img_loc in imgs_in_file:
    imgdlfile_url_a = imgdlfile_url_prefix.replace("https","https:") + img_loc
    imgdlfile_url = imgdlfile_url_a.replace('"','')#strip trailing quotes
    imgurl_list.append(imgdlfile_url)
    
    #now go to primary page to get useful sized image
    if len(imgsrc_list) < imgnum_needed:
      print "imgdlfile_url", imgdlfile_url
      imgdlfile_url_txt = urlopen(imgdlfile_url)
      rawimg_url_big = re.findall( r'(.+)img-fluid', imgdlfile_url_txt.read() )
      try:
        rawimg_url = rawimg_url_big[0].split('"')[1]
        if rawimg_url not in imgs_existing: #prevent dupes
          #this is rhe download list
          imgsrc_list.append(rawimg_url)
          # this is dict for img2url logfile
          for imgurl in imgsrc_list:img2url_dict[rawimg_url] = [imgdlfile_url]

      except:
        pass #regex issue, skip it
  
  cursor_and_imgs = [cursor, imgsrc_list, img2url_dict]
  
  if len(imgsrc_list) < 1:
    print cfg.color.yellow + '''
=================================
       ***** WARNING *****
   no JPG images found online! 
================================='''
    print cfg.color.white
  
  return cursor_and_imgs
  


#################################
def urlbuild(vars_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  
  thiscursor = vars_dict["cursor"]
  thistag = vars_dict["thistag"]
  
  if thiscursor == None: url_built = scrapeurl.replace("https","https:") + cfg.dd + thistag
  else: url_built = scrapeurl.replace("https","https:") + cfg.dd + thistag+scrapeurl_pagenum+thiscursor
  
  vars_dict["url_built"] = url_built
  
  return vars_dict



#################################
def getwebfile(webfileurl):
  robo.whereami(sys._getframe().f_code.co_name)
  
  print "get data from:", webfileurl

  try:
    webfile = urlopen(webfileurl)
    return webfile
  except:
    print cfg.color.red
    print "doh, didnt get file...(todo:better msgs. ha!)"
    print cfg.color.white
    robo.goodbye()
    
  sys.exit(1) #shouldnt get here, but for safety 



#################################
def webfile_prep(fwebname):
  robo.whereami(sys._getframe().f_code.co_name)
  
  try:
    webfile_prepped = open(fwebname, "r")
    return webfile_prepped
  except:
    print cfg.color.yellow
    print "Hmm, Unable to load WEBSTAGRAM response: "+fwebname
    print "(usually, the tag has no images. so check the txt file, and also give it a look online.)"
    print cfg.color.white
    robo.goodbye()

  sys.exit(1) #shouldnt get here, but for safety 


#################################
def getnexturl(vars_dict):
  
  robo.whereami(sys._getframe().f_code.co_name)

  with open(vars_dict["localurlfile"], "rU") as f:
    urls_list = [line for line in f]
    
  nexturl_raw= urls_list[ (len(urls_list)-1)]
  nexturl = nexturl_raw.replace("\n","")
  print "nexturl "+ nexturl
  vars_dict["nexturl"]  = nexturl

  if nexturl == cfg.nomoreurls: iscomplete(progressdata)
  
  for k,v in vars_dict.items():
    print k,":",v
  
  return vars_dict










