import os
import sys
import re
import pdb
import pandas as pd

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import argparser,run_flow,_CLIENT_SECRETS_MESSAGE
from IPython.core.debugger import Tracer



#Project Details
#inner-strategy-185000
#AIzaSyAkao6fA1KfBqgYvbpF7gbhKnwc6WTMgbA


DEVELOPER_KEY = "AIzaSyAaGXsmSdaHwDC8WGNoHFoYNVtu6vJOcMM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

argparser.add_argument("--max-results", help="Max results", default=50)
argparser.add_argument("--q", help="Search term", default="Attention Charlie Puth")
args = argparser.parse_args()

options = args

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#Tracer()()
search_response = youtube.search().list(
 q=options.q,
 type="video",
 part="id,snippet",
 maxResults=options.max_results
).execute()

#pdb.set_trace()
#Tracer()()

videos = {}
for search_result in search_response["items"]:
	if search_result["id"]["kind"] == "youtube#video":
		videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]


s = ','.join(videos.keys())

video_list_response  = youtube.videos().list(id=s, part= 'id,statistics').execute()
res = []
for i in video_list_response['items']:
	temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
	temp_res.update(i['statistics'])
	res.append(temp_res) 
	
pd.DataFrame.from_dict(res)




