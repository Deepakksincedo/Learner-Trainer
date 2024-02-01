import datetime
from lxpapp import models as LXPModel
import requests
from django.contrib.auth.models import User
from util import *
import pytz
from django.db import models
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import timedelta
from googleapiclient.discovery import build
import googleapiclient.errors
from django.db.models import Q, Sum
import os
import google_auth_oauthlib.flow
from urllib.parse import parse_qs, urlparse
from django.http import HttpResponse
from django.template import loader
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_message_from_httperror(e):
    return e.error_details[0]['message']


class PlaylistManager(models.Manager):
    def getCredentials(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "GoogleCredV1.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        flow.run_local_server()
        credentials = flow.credentials

        return credentials

    def getPlaylistId(self, playlist_link):
        if "?" not in playlist_link:
            return playlist_link

        temp = playlist_link.split("?")[-1].split("&")

        for el in temp:
            if "list=" in el:
                return el.split("list=")[-1]
    # Used to check if the user has a vaild YouTube channel
    # Will return -1 if user does not have a YouTube channel
    def getUserYTChannelID(self):
        credentials = self.getCredentials()

        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.channels().list(
                part='id,topicDetails,status,statistics,snippet,localizations,contentOwnerDetails,contentDetails,brandingSettings',
                mine=True  # get playlist details for this user's playlists
            )

            pl_response = pl_request.execute()

            if pl_response['pageInfo']['totalResults'] == 0:
                print("Looks like do not have a channel on youtube. Create one to import all of your playlists. Retry?")
                return -1
        return 0

    # Set pl_id as None to retrive all the playlists from authenticated user. Playlists already imported will be skipped by default.
    # Set pl_id = <valid playlist id>, to import that specific playlist into the user's account
    def initializePlaylist(self,credentials, pl_id=None):
        '''
        Retrieves all of user's playlists from YT and stores them in the Playlist model. Note: only stores
        the few of the columns of each playlist in every row, and has is_in_db column as false as no videos will be
        saved yet.
        :param user: django User object
        :param pl_id:
        :return:
        '''
        result = {"status": 0,
                  "num_of_playlists": 0,
                  "first_playlist_name": "N/A",
                  "error_message": "",
                  "playlist_ids": []}
                  
        playlist_ids = []
        with build('youtube', 'v3', credentials=credentials) as youtube:
            if pl_id is not None:
                pl_request = youtube.playlists().list(
                    part='contentDetails, snippet, id, player, status',
                    id=pl_id,  # get playlist details for this playlist id
                    maxResults=50
                )
            else:
                print("GETTING ALL USER AUTH PLAYLISTS")
                pl_request = youtube.playlists().list(
                    part='contentDetails, snippet, id, player, status',
                    mine=True,  # get playlist details for this playlist id
                    maxResults=50
                )

            # execute the above request, and store the response
            try:
                pl_response = pl_request.execute()
            except googleapiclient.errors.HttpError as e:
                print("YouTube channel not found if mine=True")
                print("YouTube playlist not found if id=playlist_id")
                result["status"] = -1
                result["error_message"] = get_message_from_httperror(e)
                return result

            if pl_response["pageInfo"]["totalResults"] == 0:
                print("No playlists created yet on youtube.")
                result["status"] = -2
                return result

            playlist_items = []

            for item in pl_response["items"]:
                playlist_items.append(item)

            if pl_id is None:
                while True:
                    try:
                        pl_request = youtube.playlists().list_next(pl_request, pl_response)
                        pl_response = pl_request.execute()
                        for item in pl_response["items"]:
                            playlist_items.append(item)
                    except AttributeError:
                        break

        result["num_of_playlists"] = len(playlist_items)
        result["first_playlist_name"] = playlist_items[0]["snippet"]["title"]

        for item in playlist_items:
            playlist_id = item["id"]
            playlist_ids.append(playlist_id)

            # check if this playlist already exists in user's untube collection
            if LXPModel.Playlist.objects.all().filter(playlist_id=playlist_id).exists():
                playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)
                ####print(f"PLAYLIST {playlist.name} ({playlist_id}) ALREADY EXISTS IN DB")

                # POSSIBLE CASES:
                # 1. PLAYLIST HAS DUPLICATE VIDEOS, DELETED VIDS, UNAVAILABLE VIDS

                # check if playlist count changed on youtube
                if playlist.video_count != item['contentDetails']['itemCount']:
                    playlist.has_playlist_changed = True
                    playlist.save(update_fields=['has_playlist_changed'])

                if pl_id is not None:
                    result["status"] = -3
                    return result
            else:  # no such playlist in database
                ####print(f"CREATING {item['snippet']['title']} ({playlist_id})")
                if LXPModel.Playlist.objects.filter(Q(playlist_id=playlist_id) & Q(is_in_db=False)).exists():
                    unimported_playlist = LXPModel.Playlist.objects.filter(Q(playlist_id=playlist_id) & Q(is_in_db=False)).first()
                    unimported_playlist.delete()

                ### MAKE THE PLAYLIST AND LINK IT TO CURRENT_USER
                playlist = LXPModel.Playlist(  # create the playlist and link it to current user
                    playlist_id=playlist_id,
                    name=item['snippet']['title'],
                    description=item['snippet']['description'],
                    published_at=item['snippet']['publishedAt'],
                    thumbnail_url=getThumbnailURL(item['snippet']['thumbnails']),
                    channel_id=item['snippet']['channelId'] if 'channelId' in
                                                               item['snippet'] else '',
                    channel_name=item['snippet']['channelTitle'] if 'channelTitle' in
                                                                    item[
                                                                        'snippet'] else '',
                    video_count=item['contentDetails']['itemCount'],
                    is_private_on_yt=True if item['status']['privacyStatus'] == 'private' else False,
                    playlist_yt_player_HTML=item['player']['embedHtml'],
                    is_user_owned=True if item['snippet']['channelId'] == item['snippet']['channelId'] else False,
                    is_yt_mix=True if ("My Mix" in item['snippet']['title'] or "Mix -" in item['snippet']['title']) and
                                      item['snippet']['channelId'] == "UCBR8-60-B28hp2BmDPdntcQ" else False
                )
                playlist.save()

        result["playlist_ids"] = playlist_ids

        return playlist_ids

    def getAllVideosForPlaylist(self, playlist_id,credentials,maxcount,plcount,plname):
        
        playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)
        
        ### GET ALL VIDEO IDS FROM THE PLAYLIST
        video_ids = []  # stores list of all video ids for a given playlist
        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.playlistItems().list(
                part='contentDetails, snippet, status',
                playlistId=playlist_id,  # get all playlist videos details for this playlist id
                maxResults=50
            )

            # execute the above request, and store the response
            pl_response = pl_request.execute()

            for item in pl_response['items']:
                playlist_item_id = item["id"]
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

                # video DNE in user's untube:
                # 1. create and save the video in user's untube
                # 2. add it to playlist
                # 3. make a playlist item which is linked to the video
                if not LXPModel.Video.objects.filter(video_id=video_id).exists():
                    if item['snippet']['title'] == "Deleted video" or item['snippet'][
                        'description'] == "This video is unavailable." or item['snippet']['title'] == "Private video" or \
                            item['snippet']['description'] == "This video is private.":
                        video = LXPModel.Video(
                            video_id=video_id,
                            name=item['snippet']['title'],
                            description=item['snippet']['description'],
                            is_unavailable_on_yt=True,
                        )
                        video.save()
                    else:
                        video = LXPModel.Video(
                            video_id=video_id,
                            published_at=item['contentDetails']['videoPublishedAt'] if 'videoPublishedAt' in
                                                                                       item[
                                                                                           'contentDetails'] else None,
                            name=item['snippet']['title'],
                            description=item['snippet']['description'],
                            thumbnail_url=getThumbnailURL(item['snippet']['thumbnails']),
                            channel_id=item['snippet']['videoOwnerChannelId'],
                            channel_name=item['snippet']['videoOwnerChannelTitle'],
                        )
                        video.save()

                    playlist.videos.add(video)

                    playlist_item = LXPModel.PlaylistItem(
                        playlist_item_id=playlist_item_id,
                        published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                                                                       item[
                                                                           'snippet'] else None,
                        channel_id=item['snippet']['channelId'],
                        channel_name=item['snippet']['channelTitle'],
                        video_position=item['snippet']['position'],
                        playlist=playlist,
                        video=video
                    )
                    playlist_item.save()
                else:  # video found in user's db
                    if playlist.playlist_items.filter(playlist_item_id=playlist_item_id).exists():
                        ####print("PLAYLIST ITEM ALREADY EXISTS")
                        # video = LXPModel.Video.objects.get(video_id=video_id)
                        # if not LXPModel.PlaylistItem.objects.filter(playlist_id=playlist.id,video_id=video.id).exists():
                        #     playlist_item = LXPModel.PlaylistItem(
                        #     playlist_item_id=playlist_item_id,
                        #     published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                        #                                                 item[
                        #                                                     'snippet'] else None,
                        #     channel_id=item['snippet']['channelId'],
                        #     channel_name=item['snippet']['channelTitle'],
                        #     video_position=item['snippet']['position'],
                        #     playlist=playlist,
                        #     video=video
                        #     ).save()
                        continue

                    video = LXPModel.Video.objects.get(video_id=video_id)

                    # if video already in playlist.videos
                    is_duplicate = False
                    if playlist.videos.filter(video_id=video_id).exists():
                        is_duplicate = True
                    else:
                        playlist.videos.add(video)
                    playlist_item = LXPModel.PlaylistItem(
                        playlist_item_id=playlist_item_id,
                        published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                                                                       item[
                                                                           'snippet'] else None,
                        channel_id=item['snippet']['channelId'] if 'channelId' in
                                                                   item[
                                                                       'snippet'] else None,
                        channel_name=item['snippet']['channelTitle'] if 'channelTitle' in
                                                                        item[
                                                                            'snippet'] else None,
                        video_position=item['snippet']['position'],
                        playlist=playlist,
                        video=video,
                        is_duplicate=is_duplicate

                    )
                    playlist_item.save()
                    # check if the video became unavailable on youtube
                    if not video.is_unavailable_on_yt and not video.was_deleted_on_yt and (
                            item['snippet']['title'] == "Deleted video" or
                            item['snippet'][
                                'description'] == "This video is unavailable.") or (
                            item['snippet']['title'] == "Private video" or item['snippet'][
                        'description'] == "This video is private."):
                        video.was_deleted_on_yt = True
                        video.save(update_fields=['was_deleted_on_yt'])

            while True:
                try:
                    pl_request = youtube.playlistItems().list_next(pl_request, pl_response)
                    pl_response = pl_request.execute()
                    for item in pl_response['items']:
                        playlist_item_id = item["id"]
                        video_id = item['contentDetails']['videoId']
                        video_ids.append(video_id)

                        # video DNE in user's untube:
                        # 1. create and save the video in user's untube
                        # 2. add it to playlist
                        # 3. make a playlist item which is linked to the video
                        if not LXPModel.Video.objects.filter(video_id=video_id).exists():
                            if item['snippet']['title'] == "Deleted video" or item['snippet'][
                                'description'] == "This video is unavailable." or item['snippet'][
                                'title'] == "Private video" or \
                                    item['snippet']['description'] == "This video is private.":
                                video = LXPModel.Video(
                                    video_id=video_id,
                                    name=item['snippet']['title'],
                                    description=item['snippet']['description'],
                                    is_unavailable_on_yt=True,
                                )
                                video.save()
                            else:
                                video = LXPModel.Video(
                                    video_id=video_id,
                                    published_at=item['contentDetails']['videoPublishedAt'] if 'videoPublishedAt' in
                                                                                               item[
                                                                                                   'contentDetails'] else None,
                                    name=item['snippet']['title'],
                                    description=item['snippet']['description'],
                                    thumbnail_url=getThumbnailURL(item['snippet']['thumbnails']),
                                    channel_id=item['snippet']['videoOwnerChannelId'],
                                    channel_name=item['snippet']['videoOwnerChannelTitle'],
                                )
                                video.save()

                            playlist.videos.add(video)

                            playlist_item = LXPModel.PlaylistItem(
                                playlist_item_id=playlist_item_id,
                                published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                                                                               item[
                                                                                   'snippet'] else None,
                                channel_id=item['snippet']['channelId'],
                                channel_name=item['snippet']['channelTitle'],
                                video_position=item['snippet']['position'],
                                playlist=playlist,
                                video=video
                            )
                            playlist_item.save()
                        else:  # video found in user's db
                            video = LXPModel.Video.objects.get(video_id=video_id)

                            # if video already in playlist.videos
                            is_duplicate = False
                            if playlist.videos.filter(video_id=video_id).exists():
                                is_duplicate = True
                            else:
                                playlist.videos.add(video)
                            playlist_item = LXPModel.PlaylistItem(
                                playlist_item_id=playlist_item_id,
                                published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                                                                               item[
                                                                                   'snippet'] else None,
                                channel_id=item['snippet']['channelId'] if 'channelId' in
                                                                           item[
                                                                               'snippet'] else None,
                                channel_name=item['snippet']['channelTitle'] if 'channelTitle' in
                                                                                item[
                                                                                    'snippet'] else None,
                                video_position=item['snippet']['position'],
                                playlist=playlist,
                                video=video,
                                is_duplicate=is_duplicate
                            )
                            playlist_item.save()
                            
                            # check if the video became unavailable on youtube
                            if not video.is_unavailable_on_yt and not video.was_deleted_on_yt and (
                                    item['snippet']['title'] == "Deleted video" or
                                    item['snippet'][
                                        'description'] == "This video is unavailable.") or (
                                    item['snippet']['title'] == "Private video" or item['snippet'][
                                'description'] == "This video is private."):
                                video.was_deleted_on_yt = True
                                video.save(update_fields=['was_deleted_on_yt'])


                except AttributeError:
                    break

            # API expects the video ids to be a string of comma seperated values, not a python list
            video_ids_strings = getVideoIdsStrings(video_ids)

            # store duration of all the videos in the playlist
            vid_durations = []
            for video_ids_string in video_ids_strings:
                # query the videos resource using API with the string above
                vid_request = youtube.videos().list(
                    part="contentDetails,player,snippet,statistics",  # get details of eac video
                    id=video_ids_string,
                    maxResults=50,
                )

                vid_response = vid_request.execute()

                for item in vid_response['items']:
                    duration = item['contentDetails']['duration']
                    vid = playlist.videos.get(video_id=item['id'])

                    if playlist_id == "LL":
                        vid.liked = True

                    vid.name = item['snippet']['title']
                    vid.description = item['snippet']['description']
                    vid.thumbnail_url = getThumbnailURL(item['snippet']['thumbnails'])
                    vid.duration = duration.replace("PT", "")
                    vid.duration_in_seconds = calculateDuration([duration])
                    vid.has_cc = True if item['contentDetails']['caption'].lower() == 'true' else False
                    vid.view_count = item['statistics']['viewCount'] if 'viewCount' in item[
                        'statistics'] else -1
                    vid.like_count = item['statistics']['likeCount'] if 'likeCount' in item[
                        'statistics'] else -1
                    vid.dislike_count = item['statistics']['dislikeCount'] if 'dislikeCount' in item[
                        'statistics'] else -1
                    vid.comment_count = item['statistics']['commentCount'] if 'commentCount' in item[
                        'statistics'] else -1
                    vid.yt_player_HTML = item['player']['embedHtml'] if 'embedHtml' in item['player'] else ''
                    vid.save()
                    HttpResponse(loader.get_template('cto/youtube/cto_sync_youtube.html').render(
                    {
                        "plname": plname,
                        "maxcount": maxcount,
                        "plcount": plcount
                    }
                ))

                    vid_durations.append(duration)

        playlist_duration_in_seconds = calculateDuration(vid_durations)

        playlist.playlist_duration_in_seconds = playlist_duration_in_seconds
        playlist.playlist_duration = getHumanizedTimeString(playlist_duration_in_seconds)

        playlist.is_in_db = True
        playlist.last_accessed_on = datetime.datetime.now(pytz.utc)

        playlist.save()
        
    # Returns True if the video count for a playlist on UnTube and video count on same playlist on YouTube is different
    def checkIfPlaylistChangedOnYT(self, pl_id):
        """
        If full_scan is true, the whole playlist (i.e each and every video from the PL on YT and PL on UT, is scanned and compared)
        is scanned to see if there are any missing/deleted/newly added videos. This will be only be done
        weekly by looking at the playlist.last_full_scan_at

        If full_scan is False, only the playlist count difference on YT and UT is checked on every visit
        to the playlist page. This is done everytime.
        """
        credentials = self.getCredentials()

        playlist = LXPModel.Playlist.objects.get(playlist_id=pl_id)
###to do
        # if its been a week since the last full scan, do a full playlist scan
        # basically checks all the playlist video for any updates
        xc=1
        if xc == 1:
            print("DOING A FULL SCAN")
            current_playlist_item_ids = [playlist_item.playlist_item_id for playlist_item in
                                         playlist.playlist_items.all()]

            deleted_videos, unavailable_videos, added_videos = 0, 0, 0

            ### GET ALL VIDEO IDS FROM THE PLAYLIST
            video_ids = []  # stores list of all video ids for a given playlist
            with build('youtube', 'v3', credentials=credentials) as youtube:
                pl_request = youtube.playlistItems().list(
                    part='contentDetails, snippet, status',
                    playlistId=pl_id,  # get all playlist videos details for this playlist id
                    maxResults=50
                )

                # execute the above request, and store the response
                try:
                    pl_response = pl_request.execute()
                except googleapiclient.errors.HttpError as e:
                    if e.status_code == 404:  # playlist not found
                        return [-1, "Playlist not found!"]

                for item in pl_response['items']:
                    playlist_item_id = item['id']
                    video_id = item['contentDetails']['videoId']

                    if not playlist.playlist_items.filter(
                            playlist_item_id=playlist_item_id).exists():  # if playlist item DNE in playlist, a new vid added to playlist
                        added_videos += 1
                        video_ids.append(video_id)
                    else:  # playlist_item found in playlist
                        if playlist_item_id in current_playlist_item_ids:
                            video_ids.append(video_id)
                            current_playlist_item_ids.remove(playlist_item_id)

                        video = playlist.videos.get(video_id=video_id)
                        # check if the video became unavailable on youtube
                        if not video.is_unavailable_on_yt and not video.was_deleted_on_yt:
                            if (item['snippet']['title'] == "Deleted video" or
                                    item['snippet']['description'] == "This video is unavailable." or
                                    item['snippet']['title'] == "Private video" or item['snippet'][
                                        'description'] == "This video is private."):
                                unavailable_videos += 1

                while True:
                    try:
                        pl_request = youtube.playlistItems().list_next(pl_request, pl_response)
                        pl_response = pl_request.execute()

                        for item in pl_response['items']:
                            playlist_item_id = item['id']
                            video_id = item['contentDetails']['videoId']

                            if not playlist.playlist_items.filter(
                                    playlist_item_id=playlist_item_id).exists():  # if playlist item DNE in playlist, a new vid added to playlist
                                added_videos += 1
                                video_ids.append(video_id)
                            else:  # playlist_item found in playlist
                                if playlist_item_id in current_playlist_item_ids:
                                    video_ids.append(video_id)
                                    current_playlist_item_ids.remove(playlist_item_id)

                                video = playlist.videos.get(video_id=video_id)
                                # check if the video became unavailable on youtube
                                if not video.is_unavailable_on_yt and not video.was_deleted_on_yt:
                                    if (item['snippet']['title'] == "Deleted video" or
                                            item['snippet']['description'] == "This video is unavailable." or
                                            item['snippet']['title'] == "Private video" or item['snippet'][
                                                'description'] == "This video is private."):
                                        unavailable_videos += 1
                    except AttributeError:
                        break

            # playlist.last_full_scan_at = datetime.datetime.now(pytz.utc)

            playlist.save()

            deleted_videos = len(current_playlist_item_ids)  # left out video ids

            return [1, deleted_videos, unavailable_videos, added_videos]
        else:
            print("YOU CAN DO A FULL SCAN AGAIN IN")#,
                  #str(datetime.datetime.now(pytz.utc) - (playlist.last_full_scan_at + datetime.timedelta(minutes=1))))
        """
        print("DOING A SMOL SCAN")

        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.playlists().list(
                part='contentDetails, snippet, id, status',
                id=pl_id,  # get playlist details for this playlist id
                maxResults=50
            )

            # execute the above request, and store the response
            try:
                pl_response = pl_request.execute()
            except googleapiclient.errors.HttpError:
                print("YouTube channel not found if mine=True")
                print("YouTube playlist not found if id=playlist_id")
                return -1

            print("PLAYLIST", pl_response)

            playlist_items = []

            for item in pl_response["items"]:
                playlist_items.append(item)

            while True:
                try:
                    pl_request = youtube.playlists().list_next(pl_request, pl_response)
                    pl_response = pl_request.execute()
                    for item in pl_response["items"]:
                        playlist_items.append(item)
                except AttributeError:
                    break

        for item in playlist_items:
            playlist_id = item["id"]

            # check if this playlist already exists in database
            if LXPModel.Playlist.objects.filter(playlist_id=playlist_id).exists():
                playlist = LXPModel.Playlist.objects.get(playlist_id__exact=playlist_id)
                print(f"PLAYLIST {playlist.name} ALREADY EXISTS IN DB")

                # POSSIBLE CASES:
                # 1. PLAYLIST HAS DUPLICATE VIDEOS, DELETED VIDS, UNAVAILABLE VIDS

                # check if playlist changed on youtube
                if playlist.video_count != item['contentDetails']['itemCount']:
                    playlist.has_playlist_changed = True
                    playlist.save()
                    return [-1, item['contentDetails']['itemCount']]
        """

        return [0, "no change"]

    def updatePlaylist(self, playlist_id):
        credentials = self.getCredentials()

        playlist = LXPModel.Playlist.objects.get(playlist_id__exact=playlist_id)

        current_video_ids = [playlist_item.video.video_id for playlist_item in playlist.playlist_items.all()]
        current_playlist_item_ids = [playlist_item.playlist_item_id for playlist_item in playlist.playlist_items.all()]

        updated_playlist_video_count = 0

        deleted_playlist_item_ids, unavailable_videos, added_videos = [], [], []

        ### GET ALL VIDEO IDS FROM THE PLAYLIST
        video_ids = []  # stores list of all video ids for a given playlist
        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.playlistItems().list(
                part='contentDetails, snippet, status',
                playlistId=playlist_id,  # get all playlist videos details for this playlist id
                maxResults=50
            )

            # execute the above request, and store the response
            try:
                pl_response = pl_request.execute()
            except googleapiclient.errors.HttpError:
                print("Playist was deleted on YouTube")
                return [-1, [], [], []]

            print("ESTIMATED VIDEO IDS FROM RESPONSE", len(pl_response["items"]))
            updated_playlist_video_count += len(pl_response["items"])
            for item in pl_response['items']:
                playlist_item_id = item["id"]
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

                # check if new playlist item added
                if not playlist.playlist_items.filter(playlist_item_id=playlist_item_id).exists():
                    # if video dne in user's db at all, create and save it
                    if not LXPModel.Video.objects.filter(video_id=video_id).exists():
                        if (item['snippet']['title'] == "Deleted video" and item['snippet'][
                            'description'] == "This video is unavailable.") or (item['snippet'][
                                                                                    'title'] == "Private video" and
                                                                                item['snippet'][
                                                                                    'description'] == "This video is private."):
                            video = LXPModel.Video(
                                video_id=video_id,
                                name=item['snippet']['title'],
                                description=item['snippet']['description'],
                                is_unavailable_on_yt=True,
                            )
                            video.save()
                        else:
                            video = LXPModel.Video(
                                video_id=video_id,
                                published_at=item['contentDetails']['videoPublishedAt'] if 'videoPublishedAt' in
                                                                                           item[
                                                                                               'contentDetails'] else None,
                                name=item['snippet']['title'],
                                description=item['snippet']['description'],
                                thumbnail_url=getThumbnailURL(item['snippet']['thumbnails']),
                                channel_id=item['snippet']['videoOwnerChannelId'],
                                channel_name=item['snippet']['videoOwnerChannelTitle'],
                            )
                            video.save()

                    video = LXPModel.Video.objects.get(video_id=video_id)

                    # check if the video became unavailable on youtube
                    if not video.is_unavailable_on_yt and not video.was_deleted_on_yt and (
                            item['snippet']['title'] == "Deleted video" and
                            item['snippet'][
                                'description'] == "This video is unavailable.") or (
                            item['snippet']['title'] == "Private video" and item['snippet'][
                        'description'] == "This video is private."):
                        video.was_deleted_on_yt = True

                    is_duplicate = False
                    if not playlist.videos.filter(video_id=video_id).exists():
                        playlist.videos.add(video)
                    else:
                        is_duplicate = True

                    playlist_item = LXPModel.PlaylistItem(
                        playlist_item_id=playlist_item_id,
                        published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                                                                       item[
                                                                           'snippet'] else None,
                        channel_id=item['snippet']['channelId'] if 'channelId' in
                                                                   item[
                                                                       'snippet'] else None,
                        channel_name=item['snippet']['channelTitle'] if 'channelTitle' in
                                                                        item[
                                                                            'snippet'] else None,
                        video_position=item['snippet']['position'],
                        playlist=playlist,
                        video=video,
                        is_duplicate=is_duplicate
                    )
                    playlist_item.save()
                    video.video_details_modified = True
                    video.save(
                        update_fields=['video_details_modified', 'was_deleted_on_yt'])
                    added_videos.append(video)

                else:  # if playlist item already in playlist
                    current_playlist_item_ids.remove(playlist_item_id)

                    playlist_item = playlist.playlist_items.get(playlist_item_id=playlist_item_id)
                    playlist_item.video_position = item['snippet']['position']
                    playlist_item.save(update_fields=['video_position'])

                    # check if the video became unavailable on youtube
                    if not playlist_item.video.is_unavailable_on_yt and not playlist_item.video.was_deleted_on_yt:
                        if (item['snippet']['title'] == "Deleted video" and
                            item['snippet']['description'] == "This video is unavailable.") or (
                                item['snippet']['title'] == "Private video" and item['snippet'][
                            'description'] == "This video is private."):
                            playlist_item.video.was_deleted_on_yt = True  # video went private on YouTube
                            playlist_item.video.video_details_modified = True
                            playlist_item.video.save(update_fields=['was_deleted_on_yt', 'video_details_modified'])

                            unavailable_videos.append(playlist_item.video)

            while True:
                try:
                    pl_request = youtube.playlistItems().list_next(pl_request, pl_response)
                    pl_response = pl_request.execute()
                    updated_playlist_video_count += len(pl_response["items"])
                    for item in pl_response['items']:
                        playlist_item_id = item["id"]
                        video_id = item['contentDetails']['videoId']
                        video_ids.append(video_id)

                        # check if new playlist item added
                        if not playlist.playlist_items.filter(playlist_item_id=playlist_item_id).exists():
                            # if video dne in user's db at all, create and save it
                            if not LXPModel.Video.objects.filter(video_id=video_id).exists():
                                if (item['snippet']['title'] == "Deleted video" and item['snippet'][
                                    'description'] == "This video is unavailable.") or (item['snippet'][
                                                                                            'title'] == "Private video" and
                                                                                        item['snippet'][
                                                                                            'description'] == "This video is private."):
                                    video = LXPModel.Video(
                                        video_id=video_id,
                                        name=item['snippet']['title'],
                                        description=item['snippet']['description'],
                                        is_unavailable_on_yt=True,
                                    )
                                    video.save()
                                else:
                                    video = LXPModel.Video(
                                        video_id=video_id,
                                        published_at=item['contentDetails']['videoPublishedAt'] if 'videoPublishedAt' in
                                                                                                   item[
                                                                                                       'contentDetails'] else None,
                                        name=item['snippet']['title'],
                                        description=item['snippet']['description'],
                                        thumbnail_url=getThumbnailURL(item['snippet']['thumbnails']),
                                        channel_id=item['snippet']['videoOwnerChannelId'],
                                        channel_name=item['snippet']['videoOwnerChannelTitle'],
                                    )
                                    video.save()

                            video = LXPModel.Video.objects.get(video_id=video_id)

                            # check if the video became unavailable on youtube
                            if not video.is_unavailable_on_yt and not video.was_deleted_on_yt and (
                                    item['snippet']['title'] == "Deleted video" and
                                    item['snippet'][
                                        'description'] == "This video is unavailable.") or (
                                    item['snippet']['title'] == "Private video" and item['snippet'][
                                'description'] == "This video is private."):
                                video.was_deleted_on_yt = True

                            is_duplicate = False
                            if not playlist.videos.filter(video_id=video_id).exists():
                                playlist.videos.add(video)
                            else:
                                is_duplicate = True

                            playlist_item = LXPModel.PlaylistItem(
                                playlist_item_id=playlist_item_id,
                                published_at=item['snippet']['publishedAt'] if 'publishedAt' in
                                                                               item[
                                                                                   'snippet'] else None,
                                channel_id=item['snippet']['channelId'] if 'channelId' in
                                                                           item[
                                                                               'snippet'] else None,
                                channel_name=item['snippet']['channelTitle'] if 'channelTitle' in
                                                                                item[
                                                                                    'snippet'] else None,
                                video_position=item['snippet']['position'],
                                playlist=playlist,
                                video=video,
                                is_duplicate=is_duplicate
                            )
                            playlist_item.save()
                            video.video_details_modified = True
                            video.save(update_fields=['video_details_modified',
                                                      'was_deleted_on_yt'])
                            added_videos.append(video)

                        else:  # if playlist item already in playlist
                            current_playlist_item_ids.remove(playlist_item_id)
                            playlist_item = playlist.playlist_items.get(playlist_item_id=playlist_item_id)
                            playlist_item.video_position = item['snippet']['position']
                            playlist_item.save(update_fields=['video_position'])

                            # check if the video became unavailable on youtube
                            if not playlist_item.video.is_unavailable_on_yt and not playlist_item.video.was_deleted_on_yt:
                                if (item['snippet']['title'] == "Deleted video" and
                                    item['snippet']['description'] == "This video is unavailable.") or (
                                        item['snippet']['title'] == "Private video" and item['snippet'][
                                    'description'] == "This video is private."):
                                    playlist_item.video.was_deleted_on_yt = True  # video went private on YouTube
                                    playlist_item.video.video_details_modified = True
                                    playlist_item.video.save(
                                        update_fields=['was_deleted_on_yt', 'video_details_modified'])

                                    unavailable_videos.append(playlist_item.video)

                except AttributeError:
                    break

            # API expects the video ids to be a string of comma seperated values, not a python list
            video_ids_strings = getVideoIdsStrings(video_ids)

            # store duration of all the videos in the playlist
            vid_durations = []

            for video_ids_string in video_ids_strings:
                # query the videos resource using API with the string above
                vid_request = youtube.videos().list(
                    part="contentDetails,player,snippet,statistics",  # get details of eac video
                    id=video_ids_string,
                    maxResults=50
                )

                vid_response = vid_request.execute()

                for item in vid_response['items']:
                    duration = item['contentDetails']['duration']
                    vid = playlist.videos.get(video_id=item['id'])

                    if (item['snippet']['title'] == "Deleted video" or
                        item['snippet'][
                            'description'] == "This video is unavailable.") or (
                            item['snippet']['title'] == "Private video" or item['snippet'][
                        'description'] == "This video is private."):
                        vid_durations.append(duration)
                        vid.video_details_modified = True
                        vid.save(
                            update_fields=['video_details_modified', 'video_details_modified_at', 'was_deleted_on_yt',
                                           'is_unavailable_on_yt'])
                        continue

                    vid.name = item['snippet']['title']
                    vid.description = item['snippet']['description']
                    vid.thumbnail_url = getThumbnailURL(item['snippet']['thumbnails'])
                    vid.duration = duration.replace("PT", "")
                    vid.duration_in_seconds = calculateDuration([duration])
                    vid.has_cc = True if item['contentDetails']['caption'].lower() == 'true' else False
                    vid.view_count = item['statistics']['viewCount'] if 'viewCount' in item[
                        'statistics'] else -1
                    vid.like_count = item['statistics']['likeCount'] if 'likeCount' in item[
                        'statistics'] else -1
                    vid.dislike_count = item['statistics']['dislikeCount'] if 'dislikeCount' in item[
                        'statistics'] else -1
                    vid.comment_count = item['statistics']['commentCount'] if 'commentCount' in item[
                        'statistics'] else -1
                    vid.yt_player_HTML = item['player']['embedHtml'] if 'embedHtml' in item['player'] else ''
                    vid.save()

                    vid_durations.append(duration)

        playlist_duration_in_seconds = calculateDuration(vid_durations)

        playlist.playlist_duration_in_seconds = playlist_duration_in_seconds
        playlist.playlist_duration = getHumanizedTimeString(playlist_duration_in_seconds)

        playlist.has_playlist_changed = False
        playlist.video_count = updated_playlist_video_count
        playlist.has_new_updates = True
        playlist.save()

        deleted_playlist_item_ids = current_playlist_item_ids  # left out playlist_item_ids

        return [0, deleted_playlist_item_ids, unavailable_videos, added_videos]

    def deletePlaylistFromYouTube(self,  playlist_id):
        """
        Takes in playlist itemids for the videos in a particular playlist
        """
        credentials = self.getCredentials()
        playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)

        # new_playlist_duration_in_seconds = playlist.playlist_duration_in_seconds
        # new_playlist_video_count = playlist.video_count
        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.playlists().delete(
                id=playlist_id
            )
            try:
                pl_response = pl_request.execute()
            except googleapiclient.errors.HttpError as e:  # failed to delete playlist
                # possible causes:
                # playlistForbidden (403)
                # playlistNotFound  (404)
                # playlistOperationUnsupported (400)
                print(e.error_details, e.status_code)
                return [-1, get_message_from_httperror(e), e.status_code]

            # playlistItem was successfully deleted if no HttpError, so delete it from db
            video_ids = [video.video_id for video in playlist.videos.all()]
            playlist.delete()
            for video_id in video_ids:
                video = LXPModel.Video.objects.get(video_id=video_id)
                if video.playlists.all().count() == 0:
                    video.delete()

        return [0]

    def deletePlaylistItems(self,  playlist_id, playlist_item_ids):
        """
        Takes in playlist itemids for the videos in a particular playlist
        """
        credentials = self.getCredentials()
        playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)
        playlist_items = LXPModel.Playlist.objects.get(playlist_id=playlist_id).playlist_items.select_related('video').filter(
            playlist_item_id__in=playlist_item_ids)

        new_playlist_duration_in_seconds = playlist.playlist_duration_in_seconds
        new_playlist_video_count = playlist.video_count
        with build('youtube', 'v3', credentials=credentials) as youtube:
            for playlist_item in playlist_items:
                pl_request = youtube.playlistItems().delete(
                    id=playlist_item.playlist_item_id
                )
                try:
                    pl_response = pl_request.execute()
                    
                except googleapiclient.errors.HttpError as e:  # failed to delete playlist item
                    # possible causes:
                    # playlistItemsNotAccessible (403)
                    # playlistItemNotFound (404)
                    # playlistOperationUnsupported (400)
                    print(e, e.error_details, e.status_code)
                    continue

                # playlistItem was successfully deleted if no HttpError, so delete it from db
                video = playlist_item.video
                playlist_item.delete()

                if not playlist.playlist_items.filter(video__video_id=video.video_id).exists():
                    playlist.videos.remove(video)
                    # if video.playlists.all().count() == 0:  # also delete the video if it is not found in other playlists
                    #    video.delete()

                if playlist_id == "LL":
                    video.liked = False
                    video.save(update_fields=['liked'])

                new_playlist_video_count -= 1
                new_playlist_duration_in_seconds -= video.duration_in_seconds

        playlist.video_count = new_playlist_video_count
        if new_playlist_video_count == 0:
            playlist.thumbnail_url = ""
        playlist.playlist_duration_in_seconds = new_playlist_duration_in_seconds
        playlist.playlist_duration = getHumanizedTimeString(new_playlist_duration_in_seconds)
        playlist.save(
            update_fields=['video_count', 'playlist_duration', 'playlist_duration_in_seconds', 'thumbnail_url'])
        # time.sleep(2)

        playlist_items = playlist.playlist_items.select_related('video').order_by("video_position")
        counter = 0
        videos = []
        for playlist_item in playlist_items:
            playlist_item.video_position = counter

            is_duplicate = False
            if playlist_item.video_id in videos:
                is_duplicate = True
            else:
                videos.append(playlist_item.video_id)

            playlist_item.is_duplicate = is_duplicate
            playlist_item.save(update_fields=['video_position', 'is_duplicate'])
            counter += 1

    def deleteSpecificPlaylistItems(self,  playlist_id, command):
        playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)
        playlist_items = []
        if command == "duplicate":
            playlist_items = playlist.playlist_items.filter(is_duplicate=True)
        elif command == "unavailable":
            playlist_items = playlist.playlist_items.filter(
                Q(video__is_unavailable_on_yt=True) & Q(video__was_deleted_on_yt=False))

        playlist_item_ids = []
        for playlist_item in playlist_items:
            playlist_item_ids.append(playlist_item.playlist_item_id)

        self.deletePlaylistItems( playlist_id, playlist_item_ids)

    def createNewPlaylist(self,  playlist_name, playlist_description):
        """
        Takes in playlist details and creates a new private playlist in the user's account
        """
        credentials = self.getCredentials()
        result = {
            "status": 0,
            "playlist_id": None
        }
        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.playlists().insert(
                part='snippet,status',
                body={
                    "snippet": {
                        "title": playlist_name,
                        "description": playlist_description,
                        "defaultLanguage": "en"
                    },
                    "status": {
                        "privacyStatus": "private"
                    }
                }
            )
            try:
                pl_response = pl_request.execute()
            except googleapiclient.errors.HttpError as e:  # failed to create playlist
                print(e.status_code, e.error_details)
                if e.status_code == 400:  # maxPlaylistExceeded
                    result["status"] = 400
                result["status"] = -1
            result["playlist_id"] = pl_response["id"]

        return result

    def updatePlaylistDetails(self,  playlist_id, details):
        """
        Takes in playlist itemids for the videos in a particular playlist
        """
        credentials = self.getCredentials()
        playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)

        with build('youtube', 'v3', credentials=credentials) as youtube:
            pl_request = youtube.playlists().update(
                part="id,snippet,status",
                body={
                    "id": playlist_id,
                    "snippet": {
                        "title": details["title"],
                        "description": details["description"],
                    },
                    "status": {
                        "privacyStatus": "private" if details["privacyStatus"] else "public"
                    }
                },
            )

            
            try:
                pl_response = pl_request.execute()
            except googleapiclient.errors.HttpError as e:  # failed to update playlist details
                # possible causes:
                # playlistItemsNotAccessible (403)
                # playlistItemNotFound (404)
                # playlistOperationUnsupported (400)
                # errors i ran into:
                # runs into HttpError 400 "Invalid playlist snippet." when the description contains <, >
                print("ERROR UPDATING PLAYLIST DETAILS", e, e.status_code, e.error_details)
                return -1

            playlist.name = pl_response['snippet']['title']
            playlist.description = pl_response['snippet']['description']
            playlist.is_private_on_yt = True if pl_response['status']['privacyStatus'] == "private" else False
            playlist.save(update_fields=['name', 'description', 'is_private_on_yt'])

            return 0

    def moveCopyVideosFromPlaylist(self,  from_playlist_id, to_playlist_ids, playlist_item_ids, action="copy"):
        """
        Takes in playlist itemids for the videos in a particular playlist
        """
        credentials = self.getCredentials()
        playlist_items = LXPModel.Playlist.objects.get(playlist_id=from_playlist_id).playlist_items.select_related('video').filter(
            playlist_item_id__in=playlist_item_ids)

        result = {
            "status": 0,
            "num_moved_copied": 0,
            "playlistContainsMaximumNumberOfVideos": False,
        }

        with build('youtube', 'v3', credentials=credentials) as youtube:
            for playlist_id in to_playlist_ids:
                for playlist_item in playlist_items:
                    pl_request = youtube.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": playlist_id,
                                "position": 0,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": playlist_item.video.video_id,
                                }
                            },
                        }
                    )

                    try:
                        pl_response = pl_request.execute()
                    except googleapiclient.errors.HttpError as e:  # failed to update playlist details
                        # possible causes:
                        # playlistItemsNotAccessible (403)
                        # playlistItemNotFound (404) - I ran into 404 while trying to copy an unavailable video into another playlist
                        # playlistOperationUnsupported (400)
                        # errors i ran into:
                        # runs into HttpError 400 "Invalid playlist snippet." when the description contains <, >
                        print("ERROR UPDATING PLAYLIST DETAILS", e.status_code, e.error_details)
                        if e.status_code == 400:
                            pl_request = youtube.playlistItems().insert(
                                part="snippet",
                                body={
                                    "snippet": {
                                        "playlistId": playlist_id,
                                        "resourceId": {
                                            "kind": "youtube#video",
                                            "videoId": playlist_item.video.video_id,
                                        }
                                    },
                                }
                            )

                            try:
                                pl_response = pl_request.execute()
                            except googleapiclient.errors.HttpError as e:
                                result['status'] = -1
                        elif e.status_code == 403:
                            result["playlistContainsMaximumNumberOfVideos"] = True
                        else:
                            result['status'] = -1
                    result["num_moved_copied"] += 1

        if action == "move":  # delete from the current playlist
            self.deletePlaylistItems( from_playlist_id, playlist_item_ids)

        return result

    def addVideosToPlaylist(self,  playlist_id, video_ids):
        """
        Takes in playlist itemids for the videos in a particular playlist
        """
        credentials = self.getCredentials()

        result = {
            "num_added": 0,
            "playlistContainsMaximumNumberOfVideos": False,
        }

        added = 0
        with build('youtube', 'v3', credentials=credentials) as youtube:

            for video_id in video_ids:
                pl_request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "position": 0,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id,
                            }
                        },
                    }
                )

                try:
                    pl_response = pl_request.execute()
                except googleapiclient.errors.HttpError as e:  # failed to update add video to playlis
                    print("ERROR ADDDING VIDEOS TO PLAYLIST", e.status_code, e.error_details)
                    if e.status_code == 400:  # manualSortRequired - see errors https://developers.google.com/youtube/v3/docs/playlistItems/insert
                        pl_request = youtube.playlistItems().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "playlistId": playlist_id,
                                    "resourceId": {
                                        "kind": "youtube#video",
                                        "videoId": video_id,
                                    }
                                },
                            }
                        )
                        try:
                            pl_response = pl_request.execute()
                        except googleapiclient.errors.HttpError as e:  # failed to update playlist details
                            pass
                    elif e.status_code == 403:
                        result["playlistContainsMaximumNumberOfVideos"] = True
                    continue
                added += 1
        result["num_added"] = added

        try:
            playlist = LXPModel.Playlist.objects.get(playlist_id=playlist_id)
            if added > 0:
                playlist.has_playlist_changed = True
                playlist.save(update_fields=['has_playlist_changed'])
        except:
            pass
        return result


