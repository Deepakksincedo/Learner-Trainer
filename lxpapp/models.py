from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Sum
import requests
import humanize
import datetime

class UserLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    login =  models.DateTimeField(default=datetime.datetime.now)
    logout = models.DateTimeField(default=datetime.datetime.now)
    dur = models.CharField(default='',max_length=200)
    session_id = models.CharField(default='',max_length=200)

class UserPics(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    picpath = models.TextField(default='')
    pic = models.ImageField()

class PassionateSkill(models.Model):
   passionateskill_name = models.CharField(max_length=200)
   def __str__(self):
        return self.passionateskill_name

class KnownSkill(models.Model):
   knownskill_name = models.CharField(max_length=200)
   def __str__(self):
        return self.knownskill_name

class LearnerDetails(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    user_full_name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    iswhatsapp = models.BooleanField(default=False)
    whatsappno = models.IntegerField(default=0)
    
class LearnerDetailsPSkill(models.Model):
    learnerdetails=models.ForeignKey(LearnerDetails,on_delete=models.SET_NULL, null=True)
    passionateskill=models.ForeignKey(PassionateSkill,on_delete=models.SET_NULL, null=True)

class LearnerDetailsKSkill(models.Model):
    learnerdetails=models.ForeignKey(LearnerDetails,on_delete=models.SET_NULL, null=True)
    knownskill=models.ForeignKey(KnownSkill,on_delete=models.SET_NULL, null=True)

class IsFirstLogIn(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.user

#Need to del
class Subject(models.Model):
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        try:
            return self.subject_name
        except:
            return self
class Chapter(models.Model):
    chapter_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.chapter_name
    
# class Module(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
#     module_name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.module_name

class MainHead(models.Model):
    mainhead_name = models.CharField(max_length=200)

    def __str__(self):
        try:
            return self.mainhead_name
        except:
            return self

class SubHead(models.Model):
    mainhead = models.ForeignKey(MainHead, on_delete=models.SET_NULL, null=True)
    subhead_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subhead_name
class Module(models.Model):
    mainhead = models.ForeignKey(MainHead, on_delete=models.SET_NULL, null=True)
    subhead = models.ForeignKey(SubHead, on_delete=models.SET_NULL, null=True)
    module_name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,default='')
    whatlearn = models.CharField(max_length=1000,default='')
    includes = models.CharField(max_length=1000,default='')
    cat=(('1','Red'),('2','Green'),('3','Blue'),('4','Orange'))
    themecolor=models.CharField(max_length=200,choices=cat,default='Green')
    tags = models.CharField(max_length=10000,default='')
    image = models.CharField(max_length=1000,default='')
    banner = models.CharField(max_length=1000,default='')
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.module_name

class ModuleChapter(models.Model):
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.chapter.chapter_name


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.topic_name

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True,blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True,blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.course_name

class CourseDetails(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True,blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True,blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.course
    def to_dict(c):
            if isinstance(c, CourseDetails):
                dict = {
                    "id": c.id,
                    "course_name": c.course.course_name,
                    "subject_name": c.subject.subject_name,
                    "module_name": c.module.module_name,
                    "chapter_name": c.chapter.chapter_name,
                    "topic_name": c.topic.topic_name
                }
                return dict
            else:
                type_name = c.__class__.__name__
                raise TypeError("Unexpected type {0}".format(type_name))
    
class CourseSet(models.Model):
    courseset_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True,blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True,blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.courseset_name

class CourseSetDetails(models.Model):
    courseset = models.ForeignKey(CourseSet, on_delete=models.SET_NULL, null=True,blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True,blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True,blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.courseset
    def to_dict(c):
            if isinstance(c, CourseSetDetails):
                dict = {
                    "id": c.id,
                    "courseset_name": c.courseset.courseset_name,
                    "subject_name": c.subject.subject_name,
                    "module_name": c.module.module_name,
                    "chapter_name": c.chapter.chapter_name,
                    "topic_name": c.topic.topic_name
                }
                return dict
            else:
                type_name = c.__class__.__name__
                raise TypeError("Unexpected type {0}".format(type_name))
    

###################################
def getHumanizedTimeString(seconds):
      return humanize.precisedelta(
         datetime.timedelta(seconds=seconds)).upper(). \
         replace(" month".upper(), "m.").replace(" months".upper(), "m.").replace(" days".upper(), "d.").replace(
         " day".upper(), "d.").replace(" hours".upper(), "hrs.").replace(" hour".upper(), "hr.").replace(
         " minutes".upper(), "mins.").replace(" minute".upper(), "min.").replace(
         "and".upper(), "").replace(" seconds".upper(), "secs.").replace(" second".upper(), "sec.").replace(",", "")

SECRETS = {"SECRET_KEY": 'django-insecure-ycs22y+20sq67y(6dm6ynqw=dlhg!)%vuqpd@$p6rf3!#1h$u=',
           "YOUTUBE_V3_API_KEY": 'AIzaSyCBOucAIJ5PdLeqzTfkTQ_6twsjNaMecS8',
           "GOOGLE_OAUTH_CLIENT_ID": "699466001074-biu4pjifnphoh1raipgi5mm5bf72h1ot.apps.googleusercontent.com",
           "GOOGLE_OAUTH_CLIENT_SECRET": "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",
           "GOOGLE_OAUTH_SCOPES": ['https://www.googleapis.com/auth/youtube']}
class Tag(models.Model):
    name = models.CharField(max_length=69)
    created_by = models.ForeignKey(User, related_name="playlist_tags", on_delete=models.SET_NULL, null=True)

    times_viewed = models.IntegerField(default=0)
    times_viewed_per_week = models.IntegerField(default=0)
    # type = models.CharField(max_length=10)  # either 'playlist' or 'video'

    last_views_reset = models.DateTimeField(default=datetime.datetime.now)

class Video(models.Model):
    # video details
    video_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    duration_in_seconds = models.BigIntegerField(default=0)
    thumbnail_url = models.TextField(blank=True)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField(default="")
    has_cc = models.BooleanField(default=False, blank=True, null=True)
    liked = models.BooleanField(default=False)  # whether this video liked on YouTube by user or not

    # video stats
    public_stats_viewable = models.BooleanField(default=True)
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    dislike_count = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)

    yt_player_HTML = models.TextField(blank=True)

    # video is made by this channel
    # channel = models.ForeignKey(Channel, related_name="videos", on_delete=models.SET_NULL, null=True)
    channel_id = models.TextField(blank=True)
    channel_name = models.TextField(blank=True)

    # which playlist this video belongs to, and position of that video in the playlist (i.e ALL videos belong to some pl)
    # playlist = models.ForeignKey(Playlist, related_name="videos", on_delete=models.SET_NULL, null=True)

    # (moved to playlistItem)
    # is_duplicate = models.BooleanField(default=False)  # True if the same video exists more than once in the playlist
    # video_position = models.IntegerField(blank=True)

    # NOTE: For a video in db:
    # 1.) if both is_unavailable_on_yt and was_deleted_on_yt are true,
    # that means the video was originally fine, but then went unavailable when updatePlaylist happened
    # 2.) if only is_unavailable_on_yt is true and was_deleted_on_yt is false,
    # then that means the video was an unavaiable video when initPlaylist was happening
    # 3.) if both is_unavailable_on_yt and was_deleted_on_yt are false, the video is fine, ie up on Youtube
    is_unavailable_on_yt = models.BooleanField(
        default=False)  # True if the video was unavailable (private/deleted) when the API call was first made
    was_deleted_on_yt = models.BooleanField(default=False)  # True if video became unavailable on a subsequent API call

    is_planned_to_watch = models.BooleanField(default=False)  # mark video as plan to watch later
    is_marked_as_watched = models.BooleanField(default=False)  # mark video as watched
    is_favorite = models.BooleanField(default=False, blank=True)  # mark video as favorite
    num_of_accesses = models.IntegerField(default=0)  # tracks num of times this video was clicked on by user
    user_label = models.CharField(max_length=100, blank=True)  # custom user given name for this video
    user_notes = models.TextField(blank=True)  # user can take notes on the video and save them

    # for new videos added/modified/deleted in the playlist
    video_details_modified = models.BooleanField(
        default=False)  # is true for videos whose details changed after playlist update
    def __str__(self):
        return str(self.name)

class Playlist(models.Model):
    tags = models.ManyToManyField(Tag, related_name="playlists")
    # playlist is made by this channel
    channel_id = models.TextField(blank=True)
    channel_name = models.TextField(blank=True)

    # playlist details
    is_yt_mix = models.BooleanField(default=False)
    playlist_id = models.CharField(max_length=150)
    name = models.CharField(max_length=150, blank=True)  # YT PLAYLIST NAMES CAN ONLY HAVE MAX OF 150 CHARS
    thumbnail_url = models.TextField(blank=True)
    description = models.TextField(default="No description")
    video_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    is_private_on_yt = models.BooleanField(default=False)
    videos = models.ManyToManyField(Video, related_name="playlists")

    # eg. "<iframe width=\"640\" height=\"360\" src=\"http://www.youtube.com/embed/videoseries?list=PLFuZstFnF1jFwMDffUhV81h0xeff0TXzm\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>"
    playlist_yt_player_HTML = models.TextField(blank=True)

    playlist_duration = models.CharField(max_length=69, blank=True)  # string version of playlist dureation
    playlist_duration_in_seconds = models.BigIntegerField(default=0)

    # watch playlist details
    # watch_time_left = models.CharField(max_length=150, default="")
    started_on = models.DateTimeField(default=datetime.datetime.now, null=True)
    last_watched = models.DateTimeField(default=datetime.datetime.now, null=True)

    # manage playlist
    user_notes = models.TextField(default="")  # user can take notes on the playlist and save them
    user_label = models.CharField(max_length=100, default="")  # custom user given name for this playlist
    marked_as = models.CharField(default="none",
                                 max_length=100)  # can be set to "none", "watching", "on-hold", "plan-to-watch"
    is_favorite = models.BooleanField(default=False, blank=True)  # to mark playlist as fav
    num_of_accesses = models.IntegerField(default="0")  # tracks num of times this playlist was opened by user
    last_accessed_on = models.DateTimeField(default=datetime.datetime.now)
    is_user_owned = models.BooleanField(default=True)  # represents YouTube playlist owned by user

    # set playlist manager
    #objects = PlaylistManager()

    # playlist settings (moved to global preferences)
    # hide_unavailable_videos = models.BooleanField(default=False)
    # confirm_before_deleting = models.BooleanField(default=True)
    auto_check_for_updates = models.BooleanField(default=False)

    # for import
    is_in_db = models.BooleanField(default=False)  # is true when all the videos of a playlist have been imported
    
    # for updates
    has_playlist_changed = models.BooleanField(default=False)  # determines whether playlist was modified online or not
    has_new_updates = models.BooleanField(default=False)  # meant to keep track of newly added/unavailable videos

    def __str__(self):
        return str(self.name)

    def has_unavailable_videos(self):
        if self.playlist_items.filter(Q(video__is_unavailable_on_yt=True) & Q(video__was_deleted_on_yt=False)).exists():
            return True
        return False

    def has_duplicate_videos(self):
        if self.playlist_items.filter(is_duplicate=True).exists():
            return True
        return False

    def get_channels_list(self):
        channels_list = []
        num_channels = 0
        for video in self.videos.all():
            channel = video.channel_name
            if channel not in channels_list:
                channels_list.append(channel)
                num_channels += 1

        return [num_channels, channels_list]

    def generate_playlist_thumbnail_url(self):
        """
        Generates a playlist thumnail url based on the playlist name
        """
        
        pl_name = self.name
        response = requests.get(
            f'https://api.unsplash.com/search/photos/?client_id={SECRETS["UNSPLASH_API_ACCESS_KEY"]}&page=1&query={pl_name}')
        image = response.json()["results"][0]["urls"]["small"]

        print(image)

        return image

    def get_playlist_thumbnail_url(self):
        playlist_items = self.playlist_items.filter(
            Q(video__was_deleted_on_yt=False) & Q(video__is_unavailable_on_yt=False))
        if playlist_items.exists():
            return playlist_items.first().video.thumbnail_url
        else:
            return "https://i.ytimg.com/vi/9219YrnwDXE/maxresdefault.jpg"

    def get_unavailable_videos_count(self):
        return self.video_count - self.get_watchable_videos_count()

    def get_duplicate_videos_count(self):
        return self.playlist_items.filter(is_duplicate=True).count()

    # return count of watchable videos, i.e # videos that are not private or deleted in the playlist
    def get_watchable_videos_count(self):
        return self.playlist_items.filter(
            Q(is_duplicate=False) & Q(video__is_unavailable_on_yt=False) & Q(video__was_deleted_on_yt=False)).count()

    def get_watched_videos_count(self):
        return self.playlist_items.filter(Q(is_duplicate=False) &
                                          Q(video__is_marked_as_watched=True) & Q(
            video__is_unavailable_on_yt=False) & Q(video__was_deleted_on_yt=False)).count()

    # diff of time from when playlist was first marked as watched and playlist reached 100% completion
    def get_finish_time(self):
        return self.last_watched - self.started_on

    

    def get_watch_time_left(self):
        unwatched_playlist_items_secs = self.playlist_items.filter(Q(is_duplicate=False) &
                                                                   Q(video__is_marked_as_watched=False) &
                                                                   Q(video__is_unavailable_on_yt=False) &
                                                                   Q(video__was_deleted_on_yt=False)).aggregate(
            Sum('video__duration_in_seconds'))['video__duration_in_seconds__sum']

        watch_time_left =  getHumanizedTimeString(
            unwatched_playlist_items_secs) if unwatched_playlist_items_secs is not None else getHumanizedTimeString(0)

        return watch_time_left

    # return 0 if playlist empty or all videos in playlist are unavailable
    def get_percent_complete(self):
        total_playlist_video_count = self.get_watchable_videos_count()
        watched_videos = self.playlist_items.filter(Q(is_duplicate=False) &
                                                    Q(video__is_marked_as_watched=True) & Q(
            video__is_unavailable_on_yt=False) & Q(video__was_deleted_on_yt=False))
        num_videos_watched = watched_videos.count()
        percent_complete = round((num_videos_watched / total_playlist_video_count) * 100,
                                 1) if total_playlist_video_count != 0 else 0
        return percent_complete

    def all_videos_unavailable(self):
        all_vids_unavailable = False
        if self.videos.filter(
                Q(is_unavailable_on_yt=True) | Q(was_deleted_on_yt=True)).count() == self.video_count:
            all_vids_unavailable = True
        return all_vids_unavailable

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, related_name="playlist_items",
                                 on_delete=models.SET_NULL, null=True)  # playlist this pl item belongs to
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)

    # details
    playlist_item_id = models.CharField(max_length=100)  # the item id of the playlist this video beo
    video_position = models.IntegerField(blank=True)  # video position in the playlist
    published_at = models.DateTimeField(default=datetime.datetime.now)  # snippet.publishedAt - The date and time that the item was added to the playlist
    channel_id = models.CharField(null=True,
                                  max_length=250)  # snippet.channelId - The ID that YouTube uses to uniquely identify the user that added the item to the playlist.
    channel_name = models.CharField(null=True,
                                    max_length=250)  # snippet.channelTitle -  The channel title of the channel that the playlist item belongs to.

    # video_owner_channel_id = models.CharField(max_length=100)
    # video_owner_channel_title = models.CharField(max_length=100)
    is_duplicate = models.BooleanField(default=False)  # True if the same video exists more than once in the playlist
    is_marked_as_watched = models.BooleanField(default=False, blank=True)  # mark video as watched
    num_of_accesses = models.IntegerField(default=0)  # tracks num of times this video was clicked on by user

    # for new videos added/modified/deleted in the playlist
    # video_details_modified = models.BooleanField(
    #    default=False)  # is true for videos whose details changed after playlist update
    # video_details_modified_at = models.DateTimeField(default=datetime.datetime.now)  # to set the above false after a day
   

class Pin(models.Model):
    kind = models.CharField(max_length=100)  # "playlist", "video"
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    
##############################################################################

class TrainerNotification(models.Model):
    trainernotification_message = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    trainer = models.ForeignKey(User, related_name="trainers",
                                 on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(User, related_name="senders",
                                 on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.trainernotification_message

class Material(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField(default=0)
    topic = models.CharField(max_length=200)
    cat = (('PDF', 'PDF'), ('HTML', 'HTML'), ('Video', 'Video'), ('URL', 'URL'))
    mtype = models.CharField(max_length=200, choices=cat, default='PDF')
    urlvalue = models.CharField(max_length=2000)
    description = models.CharField(max_length=200)

    class Meta:
        ordering = ['subject', 'chapter', 'serial_number']

    def save(self, *args, **kwargs):
        if not self.serial_number:
            last_material = Material.objects.filter(
                subject=self.subject,
                chapter=self.chapter
            ).order_by('-serial_number').first()
            if last_material:
                self.serial_number = last_material.serial_number + 1
            else:
                self.serial_number = 1
        super(Material, self).save(*args, **kwargs)



class CourseType(models.Model):
    coursetype_name = models.CharField(max_length=200)

    def __str__(self):
        return self.coursetype_name

class Batch(models.Model):
   batch_name = models.CharField(max_length=50)
   coursetype=models.ForeignKey(CourseType,on_delete=models.SET_NULL, null=True)
   stdate = models.DateField()
   enddate = models.DateField()
   def __str__(self):
      return self.batch_name

class BatchModule(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.SET_NULL, null=True)
   module=models.ForeignKey(Module,on_delete=models.SET_NULL, null=True)

class BatchRecordedVDOList(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.SET_NULL, null=True)
   playlist=models.ForeignKey(Playlist,on_delete=models.SET_NULL, null=True)

class BatchTrainer(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.SET_NULL, null=True)
   trainer=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class Batchlearner(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.SET_NULL, null=True)
   learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
   fee = models.IntegerField(default=0)


class Exam(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.SET_NULL, null=True)
   exam_name = models.CharField(max_length=50)
   cat=(('MCQ','MCQ'),('ShortAnswer','ShortAnswer'))
   questiontpye=models.CharField(max_length=200,choices=cat,default='')
   def __str__(self):
        return self.exam_name

class McqQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=0)

class McqResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class McqResultDetails(models.Model):
    mcqresult=models.ForeignKey(McqResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(McqQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class ShortQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   marks=models.IntegerField(default=0)

class ShortResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    datecreate = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=False)
    timetaken = models.CharField(max_length=200)

class ShortResultDetails(models.Model):
    shortresult=models.ForeignKey(ShortResult,on_delete=models.SET_NULL, null=True)
    question=models.ForeignKey(ShortQuestion,on_delete=models.SET_NULL, null=True)
    marks=models.PositiveIntegerField()
    answer=models.CharField(max_length=200)
    feedback=models.CharField(max_length=200,default='')


class YTExamQuestion(models.Model):
   playlist=models.ForeignKey(Playlist,on_delete=models.SET_NULL, null=True)
   video=models.ForeignKey(Video,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=1)

class YTExamResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    ytexamquestion = models.ForeignKey(YTExamQuestion,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class YTExamResultDetails(models.Model):
    ytexamresult=models.ForeignKey(YTExamResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(YTExamQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class VideoToUnlock(models.Model):
    playlist=models.ForeignKey(Playlist,on_delete=models.SET_NULL, null=True)
    video=models.ForeignKey(Video,on_delete=models.SET_NULL, null=True)
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class VideoWatched(models.Model):
    video=models.ForeignKey(Video,on_delete=models.SET_NULL, null=True)
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class LearnerPlaylistCount(models.Model):
    playlist=models.ForeignKey(Playlist,on_delete=models.SET_NULL, null=True)
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField(default=0)

class SessionMaterial(models.Model):
    playlist=models.ForeignKey(Playlist,on_delete=models.SET_NULL, null=True)
    video=models.ForeignKey(Video,on_delete=models.SET_NULL, null=True)
    cat=(('PDF','PDF'),('HTML','HTML'),('Video','Video'),('URL','URL'))
    mtype=models.CharField(max_length=200,choices=cat, default= 'PDF')
    urlvalue=models.CharField(max_length=200)
    description=models.CharField(max_length=200)

class LearnerMaterialWatched(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    module=models.ForeignKey(Module,on_delete=models.SET_NULL, null=True)
    chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    material=models.ForeignKey(Material,on_delete=models.SET_NULL, null=True)

class LastUserLogin(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)


class ChapterQuestion(models.Model):
   subject=models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
   chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=0)

class ChapterResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module,on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    def get_percentage(self):
        try:
            perc = self.correct * 100 / (self.wrong + self.correct)
        except:
            perc = self.correct * 100 / 1
        return perc

class ChapterResultDetails(models.Model):
    chapterresult=models.ForeignKey(ChapterResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(ChapterQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=2048)
    method = models.CharField(max_length=16)
    status_code = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} accessed {self.url} ({self.status_code})'


class ErrorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField(max_length=2048)
    exception = models.TextField()
    traceback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Error occurred while processing {self.url}'

class LearnerCart(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module,on_delete=models.SET_NULL, null=True)
    status=models.IntegerField(default=0)

class K8STerminal(models.Model):
    trainer=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_requests_trainer')
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_requests_learner')
    Password=models.TextField()
    usagevalue=models.PositiveIntegerField(default=0)

class K8STerminalLearnerCount(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    usedvalue=models.PositiveIntegerField(default=0)