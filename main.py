#!/usr/bin/python

# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

#Link for playlists :::: https://developers.google.com/youtube/v3/docs/playlistItems/list

import os
from datetime import date
import urllib2

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

#check if the user connected to internet
def connection():
    try:
	import requests
	res = requests.get('https://www.google.com')
	return True
    except:
	print "You need to be connected to internet in order to use the application"
	import sys
	sys.exit()

#Check if Filename is not empty
def checkIfFileNameIsEmpty(fileName, defaultFN):
    if(fileName == ""):
	return defaultFN
    else:
	return fileName+".txt"

#Checkif Path and file name are ok
def checkIfFPandFexists(filePath, fileName):
   pathOk = False
   fileOK = False

	#Path
   if(filePath==""):
	filePath = "./BK"

   elif(os.path.isdir(filePath) == False):
	while os.path.isdir(filePath) == False:
		filePath = raw_input("Path Not valid, please enter a valid Path -> ")

	# check If file does not already in the selected directory
   if(os.path.isfile(str(filePath+"/"+fileName)) == True):
	while os.path.isfile(str(filePath+"/"+fileName)) == True:
		filePath = raw_input("A file with the same name already exists in the selected directory! \n Plese enter another path -> ")

	#If everyting OK
   return filePath

# make the duration string more readable
def transformDuration(duration):
    dur = ""
    tempDur = duration.strip('PT')
    for ind, char in enumerate(tempDur[:-1]):
	if(char==tempDur[-1]):
		dur = dur + ""
	elif(char.isalpha()):
		dur = dur+":"
	else:
		if(tempDur[ind-1].isalpha() and tempDur[ind+1].isalpha()):
			dur = dur + "0"+char
		else:
			dur = dur+char
    if(len(dur)==2):
	dur = dur+":00"
    return dur

# Page token part
def nextPageTokens(*args):
    response = ""
    if(len(args)==1):
	request = youtube.playlistItems().list(
	        part="snippet,contentDetails",
	        maxResults=50,
	        playlistId= args[0]
	)
	response = request.execute()
    elif(len(args)==2):
	request = youtube.playlistItems().list(
	        part="snippet,contentDetails",
	        maxResults=50,
	        playlistId= args[0],
		pageToken= args[1]
	)
	response = request.execute()
    return response

#retrieve Videos Id from the requested PL
def getVideosID(plID):
    nextP = True
    videosIDArr = {}
    
    response = nextPageTokens(plID)
    while nextP == True:
    	for videosID in response["items"]:
		videosIDArr[videosID["snippet"]["position"]+1] = videosID["contentDetails"]["videoId"]

	if("nextPageToken" in response):
		response = nextPageTokens(plID, response["nextPageToken"])
	else:
		nextP = False


    sortedVideosIDArr = {}
    for k in sorted(videosIDArr.keys()):
	sortedVideosIDArr[k] = videosIDArr[k]

    return sortedVideosIDArr

#Retrieve Vidoes Infos from MY OWN created plylist
def retrieveVideosFromPL(plID, file):
    videosIDs = getVideosID(plID)
    #allInfosPerVi = {}
    for videoP in videosIDs:
	position = videoP
	videoID = videosIDs[position]

	#API to retrieve videos infos
	request = youtube.videos().list(
        	part="snippet,contentDetails",
        	id= videoID
    	)
	response = request.execute()

	if(response["items"] is not None):
		title = response["items"][0]["snippet"]["title"]
	#print title.encode('utf-32').decode('utf-32')
		channel = response["items"][0]["snippet"]["channelTitle"]
	#print channel
		duration = response["items"][0]["contentDetails"]["duration"]
	#print duration
		line = (str(position)+". "+title.encode('utf-8').decode('utf-8')+" -> "+channel.encode('utf-8').decode('utf-8')+" %> "+transformDuration(duration)+" #> "+videoID+"\n") 
		print(line)
		file.write(line.encode("utf-8"))

    print "COPY DONE!!"

#Retrieves from my LIKED PL
#https://developers.google.com/youtube/v3/docs/videos/list?refresh=1
#def retrieveFromLiked():

def main():

    connection()

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    global youtube

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "csf2.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_console()

	# API preparation
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

	#API receiving lists 
    request = youtube.playlists().list(
        part="snippet",
        maxResults=25,
	mine=True
    )
    response = request.execute()
 # the response contains the list infos ^^

	# seting up list
    availableListsDico = {"Liked Videos": "LL", "Watch Later":"WL"}

    for element in response["items"]:
	availableListsDico[str(element["snippet"]["title"])] = str(element["id"])
    
    ### Entering the big loop of chooices
    sel = 9999 # infinit choice
    maxChoices = len(availableListsDico)
    #print maxChoices
    while sel != -1:
	listCounter = 1
	print("\n Select the play list (as a number) from the selection below or type -1 to exit \n")
	#displaying choices
	for key, value in availableListsDico.items():
		print (str(listCounter)+". "+key)
		listCounter += 1
	print "-1. Exit \n"
	sel = input("Playlist -> ")

	# EXIT
	if(sel == -1):
		print("Program EXITED")

	# Lists exists
	elif(sel <= maxChoices and sel >= 1):
		
		#file Name
		defaultFileName = availableListsDico.keys()[sel-1]+"_"+str(date.today())+".txt"
		print("Please the file Name, DEFAULT:"+defaultFileName+" (press enter)")
		fileName = checkIfFileNameIsEmpty(str(raw_input("File name -> ")), str(defaultFileName))
		
		#file Path
		filePath = checkIfFPandFexists(raw_input("Please enter a path to save the file with no '/' at the end \n (DEFAULT: ./BK) -> "), fileName)

		# Real Deal, not i does the core of the idea
		print "Sure, a moment please ..."

		# create the empty file
		file = open(filePath+"/"+fileName, 'a')
		file.write("Playlist: -> "+availableListsDico.keys()[sel-1]+"\n\n PO. Title -> OriginateChanel  %> Duration  #> videoID \n\n")

		# copies the playlist in the file with the infos
		retrieveVideosFromPL(availableListsDico.values()[sel-1], file)
		file.close()

	# List does not exist
	else:
		print("Not in the choices, slect again or type -1 to exit!")











if __name__ == "__main__":
    main()
