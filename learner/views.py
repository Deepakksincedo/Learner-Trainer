from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages

@login_required
def learner_dashboard_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            dict={
            'total_Video':0,
            'total_exam':0,
            }
            return render(request,'learner/learner_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'MCQ' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
            return render(request,'learner/exam/learner_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.McqQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/exam/learner_take_exam.html',{'exam':exam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                mcqresult = LXPModel.McqResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=LXPModel.McqQuestion.objects.all().filter(exam_id=pk).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = LXPModel.McqQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = LXPModel.McqResultDetails.objects.create(mcqresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
                    resdet.save()
                    if 'option' + q.answer ==  request.POST.get(q.question):
                        score+= q.marks
                        correct+=1
                        
                    else:
                        wrong+=1
                percent = score/(total) *100
                context = {
                    'score':score,
                    'time': request.POST.get('timer'),
                    'correct':correct,
                    'wrong':wrong,
                    'percent':percent,
                    'total':total
                }
                mcqresult.marks = score
                mcqresult.wrong = wrong
                mcqresult.correct = correct
                mcqresult.timetaken = request.POST.get('timer')
                mcqresult.save()
                resdetobj = LXPModel.McqResultDetails.objects.raw("SELECT 1 as id,  lxpapp_mcqquestion.question as q,  lxpapp_mcqquestion.option1 as o1,  lxpapp_mcqquestion.option2 as o2,  lxpapp_mcqquestion.option3 as o3,  lxpapp_mcqquestion.option4 as o4,  lxpapp_mcqquestion.answer AS Correct,  lxpapp_mcqquestion.marks,  lxpapp_mcqresultdetails.selected AS answered  FROM  lxpapp_mcqresultdetails  INNER JOIN lxpapp_mcqresult ON (lxpapp_mcqresultdetails.mcqresult_id = lxpapp_mcqresult.id)  INNER JOIN lxpapp_mcqquestion ON (lxpapp_mcqresultdetails.question_id = lxpapp_mcqquestion.id) WHERE lxpapp_mcqresult.id = " + str(r_id) + " AND lxpapp_mcqresult.learner_id = " + str(request.user.id) + " ORDER BY lxpapp_mcqquestion.id" )
                return render(request,'learner/exam/learner_exam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj})
            else:
                questions=LXPModel.McqQuestion.objects.all()
                context = {
                    'questions':questions
                }
            exam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.McqQuestion.objects.all().filter(exam_id=exam.id).order_by('?')
            return render(request,'learner/exam/learner_start_exam.html',{'exam':exam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            return render(request,'learner/exam/learner_show_exam_reuslt.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResultDetails.objects.all().filter(question_id__in = LXPModel.McqQuestion.objects.all(), mcqresult_id = pk)
            return render(request,'learner/exam/learner_exam_result_details.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_short_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
            return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.ShortQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/shortexam/learner_take_short_exam.html',{'shortexam':shortexam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                shortresult = LXPModel.ShortResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0)
                shortresult.save()
                questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=pk).order_by('?')
                r_id = 0
                q_id = 0
                r_id = shortresult.id
                for q in questions:
                    question = LXPModel.ShortQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    a=request.POST.get(str(q_id))
                    resdet = LXPModel.ShortResultDetails.objects.create(shortresult_id = r_id,question_id =q_id,answer =a,feedback ='',marks=0)
                    resdet.save()
                    
                shortresult.timetaken = request.POST.get('timer')
                shortresult.save()
                
                shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
                return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
            shortexam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=shortexam.id).order_by('?')
            return render(request,'learner/shortexam/learner_start_short_exam.html',{'shortexam':shortexam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_short_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            #shortexams=LXPModel.ShortResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            shortexams=LXPModel.ShortResult.objects.raw("SELECT DISTINCT  lxpapp_exam.exam_name,  lxpapp_shortresult.datecreate,  SUM(DISTINCT lxpapp_shortresult.marks) AS Obtained,  Sum(lxpapp_shortquestion.marks) AS Tot,  lxpapp_shortresult.learner_id,  lxpapp_shortresult.timetaken,  lxpapp_shortresult.status,  lxpapp_shortresult.id FROM  lxpapp_shortquestion  LEFT OUTER JOIN lxpapp_exam ON (lxpapp_shortquestion.exam_id = lxpapp_exam.id)  LEFT OUTER JOIN lxpapp_shortresult ON (lxpapp_exam.id = lxpapp_shortresult.exam_id) WHERE  lxpapp_exam.id = " + str(pk) + " AND  lxpapp_shortresult.learner_id = " + str(request.user.id) + " GROUP BY  lxpapp_exam.exam_name,  lxpapp_shortresult.datecreate,  lxpapp_shortresult.learner_id,  lxpapp_shortresult.timetaken,  lxpapp_shortresult.status,  lxpapp_shortresult.id")
            return render(request,'learner/shortexam/learner_show_short_exam_reuslt.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_short_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.ShortResultDetails.objects.all().filter(question_id__in = LXPModel.ShortQuestion.objects.all(), shortresult_id = pk)
            return render(request,'learner/shortexam/learner_short_exam_result_details.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def learner_video_Course_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            videos1 = LXPModel.BatchCourseSet.objects.raw('SELECT DISTINCT lxpapp_courseset.id,  lxpapp_courseset.courseset_name FROM  lxpapp_batchcourseset   INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(request.user.id))
            return render(request,'learner/video/learner_video_course.html',{'videos':videos1})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_video_Course_subject_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            subject = LXPModel.Playlist.objects.raw('SELECT ID AS id, NAME, VTOTAL, Mtotal, SUM(VWATCHED) AS VWatched,((100*VWATCHED)/VTOTAL) as per, THUMBNAIL_URL FROM (SELECT YYY.ID, YYY.NAME, YYY.THUMBNAIL_URL, ( SELECT COUNT(XX.ID) FROM LXPAPP_PLAYLISTITEM XX WHERE XX.PLAYLIST_ID = YYY.ID ) AS Vtotal, ( SELECT COUNT(zz.ID) FROM LXPAPP_sessionmaterial zz WHERE zz.PLAYLIST_ID = YYY.ID ) AS Mtotal, (SELECT COUNT (LXPAPP_VIDEOWATCHED.ID) AS a FROM LXPAPP_PLAYLISTITEM GHGH LEFT OUTER JOIN LXPAPP_VIDEOWATCHED ON ( GHGH.VIDEO_ID = LXPAPP_VIDEOWATCHED.VIDEO_ID ) WHERE GHGH.PLAYLIST_ID = YYY.ID AND LXPAPP_VIDEOWATCHED.LEARNER_ID = ' + str(request.user.id) + ') AS VWatched FROM LXPAPP_BATCHLEARNER INNER JOIN LXPAPP_BATCH ON (LXPAPP_BATCHLEARNER.BATCH_ID = LXPAPP_BATCH.ID) INNER JOIN LXPAPP_BATCHRECORDEDVDOLIST ON (LXPAPP_BATCH.ID = LXPAPP_BATCHRECORDEDVDOLIST.BATCH_ID) INNER JOIN LXPAPP_PLAYLIST YYY ON (LXPAPP_BATCHRECORDEDVDOLIST.PLAYLIST_ID = YYY.ID) WHERE LXPAPP_BATCHLEARNER.LEARNER_ID = ' + str(request.user.id) + ') GROUP BY ID, NAME, VTOTAL ORDER BY NAME')
            videocount = LXPModel.LearnerPlaylistCount.objects.all().filter(learner_id = request.user.id)
            countpresent =False
            if videocount:
                countpresent = True
            per = 0
            tc = 0
            wc = 0
            for x in subject:
                if not videocount:
                    countsave = LXPModel.LearnerPlaylistCount.objects.create(playlist_id = x.id, learner_id = request.user.id,count =x.Vtotal )
                    countsave.save()
                tc += x.Vtotal
                wc += x.VWatched
            try:
                per = (100*int(wc))/int(tc)
            except:
                per =0
            dif = tc- wc

            return render(request,'learner/video/learner_video_course_subject.html',{'subject':subject,'dif':dif,'per':per,'wc':wc,'tc':tc})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def learner_video_list_view(request,subject_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.PlaylistItem.objects.raw("SELECT DISTINCT MAINVID.ID, MAINVID.NAME, IFNULL((SELECT LXPAPP_VIDEOWATCHED.VIDEO_ID FROM LXPAPP_VIDEOWATCHED WHERE LXPAPP_VIDEOWATCHED.LEARNER_ID = " + str(request.user.id) + " AND LXPAPP_VIDEOWATCHED.VIDEO_ID = MAINVID.ID), 0 ) AS watched, IFNULL((SELECT LXPAPP_VIDEOTOUNLOCK.VIDEO_ID FROM LXPAPP_VIDEOTOUNLOCK WHERE LXPAPP_VIDEOTOUNLOCK.LEARNER_ID = " + str(request.user.id) + " AND LXPAPP_VIDEOTOUNLOCK.VIDEO_ID = MAINVID.ID), 0) AS unlocked, IFNULL((SELECT LXPAPP_SESSIONMATERIAL.ID FROM LXPAPP_SESSIONMATERIAL WHERE LXPAPP_SESSIONMATERIAL.playlist_id = MAINLIST.PLAYLIST_ID AND LXPAPP_SESSIONMATERIAL.VIDEO_ID = MAINVID.ID), 0) AS matid FROM LXPAPP_PLAYLISTITEM MAINLIST INNER JOIN LXPAPP_VIDEO MAINVID ON ( MAINLIST.VIDEO_ID = MAINVID.ID ) WHERE MAINLIST.PLAYLIST_ID = " + str (subject_id) + " AND MAINVID.NAME <> 'Deleted video' ORDER BY MAINVID.NAME")  
            return render(request,'learner/video/learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_video_sesseionmaterial_list_view(request,subject_id,video_id):
    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.SessionMaterial.objects.all().filter(playlist_id = str (subject_id),video_id = str (video_id))  
            return render(request,'learner/video/learner_video_sesseionmaterial_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'video_id':video_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_video_view(request,subject_id,video_id):
    try:    
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            vunlock=LXPModel.VideoToUnlock.objects.all().filter(video_id__gt= video_id, playlist_id = subject_id)
            vunlock=LXPModel.VideoToUnlock.objects.raw('SELECT lxpapp_videotounlock.id FROM  lxpapp_videotounlock  WHERE lxpapp_videotounlock.playlist_id = ' + str(subject_id) + ' and lxpapp_videotounlock.video_id > ' + str(video_id) + ' AND  lxpapp_videotounlock.learner_id = ' + str(request.user.id) )

            nextvalue = LXPModel.PlaylistItem.objects.raw('SELECT  1 AS id,  lxpapp_playlistitem.video_id FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) WHERE  lxpapp_playlistitem.video_id > ' + str(video_id) + ' AND  lxpapp_playlistitem.playlist_id = ' + str(subject_id) + ' ORDER BY  lxpapp_video.name LIMIT 1')
            topicname =''
            url=''
            for x in Videos:
                videocount = LXPModel.VideoWatched.objects.all().filter(video_id = video_id,learner_id=request.user.id)
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
                
            if not videocount:
                for x in Videos:
                    vw=  LXPModel.VideoWatched.objects.create(video_id = video_id,learner_id=request.user.id)
                    vw.save()
                    for x in nextvalue:
                        vu=  LXPModel.VideoToUnlock.objects.create(video_id = x.video_id ,playlist_id = subject_id ,learner_id=request.user.id)
                        vu.save()

            return render(request,'learner/video/learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id,"video_id":video_id})
    except:
        return render(request,'LXPapp/404page.html')

@login_required
def learner_see_sesseionmaterial_view(request,subject_id,video_id,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.SessionMaterial.objects.all().filter(id=pk)
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            chaptername = LXPModel.Video.objects.only('name').get(id=video_id).name

            materialtype = 0
            for x in details:
                materialtype = x.mtype

            if materialtype == "HTML":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_htmlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
            if materialtype == "URL":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_urlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
            if materialtype == "PDF":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'video_id':video_id})
            if materialtype == "Video":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_studymaterial_module_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            modules = LXPModel.Module.objects.raw('SELECT id, module_name, description, whatlearn, includes, themecolor, image , Topiccount, CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END as watchcount, ((CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END)*100)/Topiccount as per FROM ( SELECT mainmod.id, mainmod.module_name, mainmod.description, mainmod.whatlearn, mainmod.includes, mainmod.themecolor, mainmod.image , (SELECT count(chpmod.topic) AS Topiccount FROM lxpapp_modulechapter INNER JOIN lxpapp_material chpmod ON (lxpapp_modulechapter.chapter_id = chpmod.chapter_id) WHERE lxpapp_modulechapter.module_id = mainmod.id ) AS Topiccount, ( SELECT count (lxpapp_learnermaterialwatched.id) as watchcount FROM lxpapp_learnermaterialwatched WHERE lxpapp_learnermaterialwatched.module_id = mainmod.id) as watchcount FROM lxpapp_batchmodule LEFT OUTER JOIN lxpapp_batch ON (lxpapp_batchmodule.batch_id = lxpapp_batch.id) LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id) LEFT OUTER JOIN lxpapp_module mainmod ON (lxpapp_batchmodule.module_id = mainmod.id) WHERE lxpapp_batchlearner.learner_id = ' + str(request.user.id) + ' )')
            if  not modules:
                return render(request,'learner/studymaterial/learner_studymaterial_nomodule.html')
            else:        
                return render(request,'learner/studymaterial/learner_studymaterial_module.html',{'modules':modules})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_studymaterial_module_chapter_view(request,module_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            list = LXPModel.Module.objects.raw("SELECT  id, srno, chapter_name, chapter_id, topic, mtype, urlvalue, description, per, CASE WHEN ROW_NUMBER() OVER (ORDER BY srno) = 1 THEN 'yes' WHEN LAG(per) OVER (ORDER BY srno) > 0 THEN 'yes' ELSE 'no' END AS flag FROM ( SELECT lxpapp_material.id, ROW_NUMBER() OVER (PARTITION BY lxpapp_chapter.chapter_name) AS srno, lxpapp_chapter.chapter_name, lxpapp_chapter.id AS chapter_id, lxpapp_material.topic, lxpapp_material.mtype, lxpapp_material.urlvalue, lxpapp_material.description, ( SELECT per FROM ( SELECT lxpapp_chapterresult.id, lxpapp_chapterresult.correct * 100 / (lxpapp_chapterresult.wrong + lxpapp_chapterresult.correct) AS per FROM lxpapp_chapterresult WHERE lxpapp_chapterresult.module_id = main.module_id AND lxpapp_chapterresult.chapter_id = main.chapter_id AND lxpapp_chapterresult.learner_id = " + str(request.user.id) + " ) a ORDER BY per DESC, 1 ) AS per FROM lxpapp_modulechapter main LEFT OUTER JOIN lxpapp_material ON (main.chapter_id = lxpapp_material.chapter_id) LEFT OUTER JOIN lxpapp_chapter ON (main.chapter_id = lxpapp_chapter.id) WHERE main.module_id = " + str(module_id) + " ) order By chapter_name, id")
            
            #list = LXPModel.Module.objects.raw("SELECT DISTINCT * FROM (SELECT lxpapp_material.id, ROW_NUMBER() OVER(PARTITION BY lxpapp_chapter.chapter_name) as srno,  lxpapp_chapter.chapter_name,  lxpapp_chapter.id as chapter_id,  lxpapp_material.topic,  lxpapp_material.mtype,  lxpapp_material.urlvalue,  lxpapp_material.description FROM  lxpapp_modulechapter  LEFT OUTER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id)  LEFT OUTER JOIN lxpapp_chapter ON (lxpapp_modulechapter.chapter_id = lxpapp_chapter.id) WHERE lxpapp_modulechapter.module_id = " + str(module_id) + ") WHERE id > 0")

            #list = LXPModel.Module.objects.raw("SELECT id, srno, chapter_name, chapter_id, topic, mtype, urlvalue, description, questions, per, CASE WHEN questions = 0 THEN 'yes' WHEN Row_number() OVER ( ORDER BY srno) = 1 THEN 'yes' WHEN Lag(per) OVER ( ORDER BY srno) > 0 THEN 'yes' ELSE 'no' END AS flag FROM (SELECT lxpapp_material.id, Row_number() OVER ( partition BY lxpapp_chapter.chapter_name) AS srno, lxpapp_chapter.chapter_name, lxpapp_chapter.id AS chapter_id, lxpapp_material.topic, lxpapp_material.mtype, lxpapp_material.urlvalue, lxpapp_material.description, (SELECT Count (lxpapp_chapterquestion.id) AS questions FROM lxpapp_chapterquestion WHERE lxpapp_chapterquestion.chapter_id = main.chapter_id) AS questions, (SELECT per FROM (SELECT lxpapp_chapterresult.id, lxpapp_chapterresult.correct * 100 / ( lxpapp_chapterresult.wrong + lxpapp_chapterresult.correct ) AS per FROM lxpapp_chapterresult WHERE lxpapp_chapterresult.module_id = main.module_id AND lxpapp_chapterresult.chapter_id = main.chapter_id AND lxpapp_chapterresult.learner_id = " + str(request.user.id) + ") a ORDER BY per DESC, 1) AS per FROM lxpapp_modulechapter main LEFT OUTER JOIN lxpapp_material ON ( main.chapter_id = lxpapp_material.chapter_id ) LEFT OUTER JOIN lxpapp_chapter ON ( main.chapter_id = lxpapp_chapter.id ) WHERE main.module_id = " + str(module_id) + ") subquery")
            # from django.db.models import F, Max, Case, When, IntegerField, CharField, Value
            # from django.db.models.functions import RowNumber
            # from django.db.models.expressions import Window, Subquery, OuterRef
            # per_subquery = (
            #     LXPModel.ChapterResult.objects.filter(
            #         module_id=module_id,
            #         chapter_id=OuterRef('chapter_id'),
            #         learner_id=request.user.id,
            #     ).annotate(
            #         per=F('correct') * 100 / (F('wrong') + F('correct'))
            #     ).order_by('-per', 'id')
            #     .values('per')[:1]
            # )

            # flag_annotation = Case(
            #     When(
            #         srno=1,
            #         then=Value('yes')
            #     ),
            #     When(
            #         per__gt=0,
            #         then=Value('yes')
            #     ),
            #     default=Value('no'),
            #     output_field=CharField()
            # )

            # list = (
            #     LXPModel.Material.objects.annotate(
            #         srno=Window(
            #             expression=RowNumber(),
            #             partition_by=F('chapter__chapter_name'),
            #         ),
            #         per=Subquery(per_subquery),
            #         flag=flag_annotation,
            #     ).filter(
            #         chapter__modulechapter__module_id=module_id
            #     ).order_by('srno')
            #     .values('id', 'srno', 'chapter__chapter_name', 'chapter_id', 'topic', 'mtype', 'urlvalue', 'description', 'per', 'flag')
            # )

            count = LXPModel.Module.objects.raw('SELECT 1 as id, Topiccount, CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END  as watchcount, ((CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END)*100)/Topiccount as per FROM ( (SELECT count(lxpapp_material.topic) AS Topiccount FROM lxpapp_modulechapter INNER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id) WHERE lxpapp_modulechapter.module_id = ' + str(module_id) + ' ) AS Topiccount, ( SELECT count (lxpapp_learnermaterialwatched.id) as watchcount FROM lxpapp_learnermaterialwatched WHERE lxpapp_learnermaterialwatched.module_id = ' + str(module_id) + ' ) as watchcount )')
            moddet = LXPModel.Module.objects.raw("SELECT lxpapp_module.id, lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name FROM  lxpapp_module  INNER JOIN lxpapp_mainhead ON (lxpapp_module.mainhead_id = lxpapp_mainhead.id)  INNER JOIN lxpapp_subhead ON (lxpapp_module.subhead_id = lxpapp_subhead.id) WHERE lxpapp_module.id = " + str(module_id) )
            Topiccount = 0
            watchcount = 0
            per = 0
            for r in count:
                Topiccount = r.Topiccount
                watchcount= r.watchcount
                per= r.per
            per = 55
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            return render(request,'learner/studymaterial/learner_studymaterial_chapter_topic.html',{'list':list,'modulename':modulename,'module_id':module_id,'moddet':moddet,'Topiccount':Topiccount,'watchcount':watchcount,'per':per})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_studymaterial_chapter_show_view(request,chapter_id,module_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            chapter_name = ''
            topiccount = 0
            Topiccount = 0
            watchcount = 0
            per = 0
            count = LXPModel.Module.objects.raw('SELECT 1 as id, Topiccount, CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END  as watchcount, ((CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END)*100)/Topiccount as per FROM ( (SELECT count(lxpapp_material.topic) AS Topiccount FROM lxpapp_modulechapter INNER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id) WHERE lxpapp_modulechapter.module_id = ' + str(module_id) + ' AND lxpapp_material.chapter_id = ' + str(chapter_id) + ') AS Topiccount, ( SELECT count (lxpapp_learnermaterialwatched.id) as watchcount FROM lxpapp_learnermaterialwatched WHERE lxpapp_learnermaterialwatched.module_id = ' + str(module_id) + ' AND lxpapp_learnermaterialwatched.learner_id = ' + str(request.user.id) + ' AND lxpapp_learnermaterialwatched.chapter_id = ' + str(chapter_id) + ' ) as watchcount )')
            result = LXPModel.Chapter.objects.raw("SELECT 1 as id,   lxpapp_chapter.chapter_name,  Count(lxpapp_material.id) as count FROM  lxpapp_material  INNER JOIN lxpapp_chapter ON (lxpapp_material.chapter_id = lxpapp_chapter.id) WHERE lxpapp_chapter.id = " + str(chapter_id) + " GROUP BY lxpapp_chapter.chapter_name")
            exam = LXPModel.ChapterQuestion.objects.filter(chapter_id = chapter_id).values_list("id").count()
            for r in result:
                chapter_name = r.chapter_name
                topiccount= r.count
            for r in count:
                Topiccount = r.Topiccount
                watchcount= r.watchcount
                per= r.per
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            list = LXPModel.Module.objects.raw("SELECT mat.id, (SELECT COUNT(lxpapp_learnermaterialwatched.id) AS MatCount FROM lxpapp_learnermaterialwatched LEFT OUTER JOIN lxpapp_material matwatch ON (lxpapp_learnermaterialwatched.material_id = matwatch.id) WHERE mat.id = matwatch.id AND lxpapp_learnermaterialwatched.module_id = " + str(module_id) + " ) AS matcount, lxpapp_chapter.chapter_name, lxpapp_chapter.id AS chapter_id, mat.topic, mat.mtype, mat.urlvalue, mat.description FROM lxpapp_material mat INNER JOIN lxpapp_chapter ON (mat.chapter_id = lxpapp_chapter.id) WHERE lxpapp_chapter.id = " + str(chapter_id) )
            return render(request,'learner/studymaterial/learner_studymaterial_chapter_show.html',{'list':list,'chapter_id':chapter_id,'chapter_name':chapter_name,'topiccount':topiccount,'modulename':modulename,'module_id':module_id,'Topiccount':Topiccount,'watchcount':watchcount,'per':per,'exam':exam})
 #   except:
        return render(request,'lxpapp/404page.html')

def save_topic(request):
    try:
        if request.method == 'POST':
            id = request.body
            id = str(id).replace("'",'')
            id = str(id).replace("bid=",'')
            id = str (id).replace("&module_id=",',')
            id = str (id).replace("&chapter_id=",',')
            x = id.split(",")
            matid= x[0]
            modid= x[1]
            chpid= x[2]
            mat =LXPModel.LearnerMaterialWatched.objects.all().filter(learner_id = request.user.id,material_id=matid,module_id = modid,chapter_id = chpid)
            if not mat:
                mat = LXPModel.LearnerMaterialWatched.objects.create(learner_id = request.user.id,material_id=matid,module_id = modid,chapter_id = chpid)
                mat.save()
            nextvalue = LXPModel.Material.objects.raw('SELECT lxpapp_material.id  FROM lxpapp_material where  lxpapp_material.id > ' + str(matid) + ' limit 1')
            a = len(nextvalue)
            if a == 0:
                xyz = LXPModel.LearnerMaterialWatched.objects.all().filter(learner_id = request.user.id,material_id=matid,module_id = modid,chapter_id = chpid)
                a = len(xyz)
                if a == 1:
                    mat = LXPModel.LearnerMaterialWatched.objects.create(learner_id = request.user.id,material_id=matid,module_id = modid,chapter_id = chpid)
                    mat.save()
            for c in nextvalue:
                mat =LXPModel.LearnerMaterialWatched.objects.all().filter(learner_id = request.user.id,material_id=c.id,module_id = modid,chapter_id = chpid)
                if not mat:
                    mat = LXPModel.LearnerMaterialWatched.objects.create(learner_id = request.user.id,material_id=c.id,module_id = modid,chapter_id = chpid)
                    mat.save()
            return JsonResponse({'status': 'success'})    
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def learner_show_studymaterial_view(request,studymaterialtype,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.Material.objects.raw('SELECT lxpapp_material.id,  lxpapp_material.topic,  lxpapp_material.mtype,  lxpapp_material.urlvalue,  lxpapp_material.description FROM  lxpapp_material WHERE  lxpapp_material.id = ' + str(pk))
            if studymaterialtype == 'HTML':
                return render(request,'learner/studymaterial/learner_studymaterial_htmlshow.html',{'details':details})
            if studymaterialtype == 'URL':
                return render(request,'learner/studymaterial/learner_studymaterial_urlshow.html',{'details':details})
            if studymaterialtype == 'PDF':
                return render(request,'learner/studymaterial/learner_studymaterial_pdfshow.html',{'details':details})
            if studymaterialtype == 'Video':
                return render(request,'learner/studymaterial/learner_studymaterial_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_availablecourse_module_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            modules = LXPModel.Module.objects.all().order_by('module_name')
            return render(request,'learner/availablecourse/learner_availablecourse_module.html',{'modules':modules})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def learner_availablecourse_module_chapter_view(request,modulename,module_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            list = LXPModel.Module.objects.raw("SELECT lxpapp_material.id, ROW_NUMBER() OVER(PARTITION BY lxpapp_chapter.chapter_name) as srno,  lxpapp_chapter.chapter_name,  lxpapp_chapter.id as chapter_id,  lxpapp_material.topic,  lxpapp_material.mtype,  lxpapp_material.urlvalue,  lxpapp_material.description FROM  lxpapp_modulechapter  LEFT OUTER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id)  LEFT OUTER JOIN lxpapp_chapter ON (lxpapp_modulechapter.chapter_id = lxpapp_chapter.id) WHERE lxpapp_modulechapter.module_id = " + str(module_id) )
            moddet = LXPModel.Module.objects.raw("SELECT lxpapp_module.id, lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name FROM  lxpapp_module  INNER JOIN lxpapp_mainhead ON (lxpapp_module.mainhead_id = lxpapp_mainhead.id)  INNER JOIN lxpapp_subhead ON (lxpapp_module.subhead_id = lxpapp_subhead.id) WHERE lxpapp_module.id = " + str(module_id) )
            return render(request,'learner/availablecourse/learner_availablecourse_chapter_topic.html',{'list':list,'modulename':modulename,'module_id':module_id,'moddet':moddet})
 #   except:
        return render(request,'lxpapp/404page.html')



@login_required
def learner_chapterexam_view(request,chapter_id,module_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            chapterexams=LXPModel.Chapter.objects.all().filter(id =  chapter_id) 
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            return render(request,'learner/studymaterial/chapterexam/learner_chapterexam.html',{'chapterexams':chapterexams,'modulename':modulename,'module_id':module_id,'chaptername':chaptername,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_chapterexam_view(request,chapter_id,module_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            
            mcqquestion= LXPModel.ChapterQuestion.objects.filter(chapter_id=chapter_id)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/studymaterial/chapterexam/learner_take_chapterexam.html',{'modulename':modulename,'chaptername':chaptername,'total_questions':total_questions,'total_marks':total_marks,'module_id':module_id,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_chapterexam_view(request,chapter_id,module_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            if request.method == 'POST':
                mcqresult = LXPModel.ChapterResult.objects.create(learner_id = request.user.id,module_id =module_id,chapter_id =chapter_id,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=LXPModel.ChapterQuestion.objects.all().filter(chapter_id=chapter_id).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = LXPModel.ChapterQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = LXPModel.ChapterResultDetails.objects.create(chapterresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
                    resdet.save()
                    if 'option' + q.answer ==  request.POST.get(q.question):
                        score+= q.marks
                        correct+=1
                        
                    else:
                        wrong+=1
                percent = score/(total) *100
                context = {
                    'score':score,
                    'time': request.POST.get('timer'),
                    'correct':correct,
                    'wrong':wrong,
                    'percent':percent,
                    'total':total
                }
                mcqresult.marks = score
                mcqresult.wrong = wrong
                mcqresult.correct = correct
                mcqresult.timetaken = request.POST.get('timer')
                mcqresult.save()
                resdetobj = LXPModel.ChapterResultDetails.objects.raw("SELECT 1 as id,  lxpapp_chapterquestion.question as q,  lxpapp_chapterquestion.option1 as o1,  lxpapp_chapterquestion.option2 as o2,  lxpapp_chapterquestion.option3 as o3,  lxpapp_chapterquestion.option4 as o4,  lxpapp_chapterquestion.answer AS Correct,  lxpapp_chapterquestion.marks,  lxpapp_chapterresultdetails.selected AS answered  FROM  lxpapp_chapterresultdetails  INNER JOIN lxpapp_chapterresult ON (lxpapp_chapterresultdetails.chapterresult_id = lxpapp_chapterresult.id)  INNER JOIN lxpapp_chapterquestion ON (lxpapp_chapterresultdetails.question_id = lxpapp_chapterquestion.id) WHERE lxpapp_chapterresult.id = " + str(r_id) + " AND lxpapp_chapterresult.learner_id = " + str(request.user.id) + " ORDER BY lxpapp_chapterquestion.id" )
                return render(request,'learner/studymaterial/chapterexam/learner_chapterexam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj,'modulename':modulename,'module_id':module_id,'chaptername':chaptername,'chapter_id':chapter_id})
            else:
                questions=LXPModel.ChapterQuestion.objects.all()
                context = {
                    'questions':questions
                }
            questions=LXPModel.ChapterQuestion.objects.all().filter(chapter_id=chapter_id).order_by('?')
            
            return render(request,'learner/studymaterial/chapterexam/learner_start_chapterexam.html',{'questions':questions,'modulename':modulename,'module_id':module_id,'chaptername':chaptername,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_chapterexam_reuslt_view(request,chapter_id,module_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            chapterexams=LXPModel.ChapterResult.objects.all().filter(chapter_id = chapter_id,learner_id=request.user.id)
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            return render(request,'learner/studymaterial/chapterexam/learner_show_chapterexam_reuslt.html',{'chapterexams':chapterexams,'modulename':modulename,'module_id':module_id,'chaptername':chaptername,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_chapterexam_reuslt_details_view(request,result_id,attempt,chapter_id,module_id):
    try:    
        if str(request.session['utype']) == 'learner':
            modulename = LXPModel.Module.objects.only('module_name').get(id=module_id).module_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            chapterexams=LXPModel.ChapterResultDetails.objects.all().filter(question_id__in = LXPModel.ChapterQuestion.objects.all(), chapterresult_id = result_id)
            return render(request,'learner/studymaterial/chapterexam/learner_chapterexam_result_details.html',{'chapterexams':chapterexams,'attempt':attempt,'modulename':modulename,'module_id':module_id,'chaptername':chaptername,'chapter_id':chapter_id})
    except:
        return render(request,'lxpapp/404page.html')


def save_cart(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            # id = str(id).replace("'",'')
            # id = str(id).replace("bid=",'')
            # id = str (id).replace("&module_id=",',')
            # id = str (id).replace("&chapter_id=",',')
            
            cart =LXPModel.LearnerCart.objects.all().filter(learner_id = request.user.id,module_id=id)
            if not cart:
                 cart = LXPModel.LearnerCart.objects.create(learner_id = request.user.id,module_id=id)
                 cart.save()
            return JsonResponse({'status': 'success'})    
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_check_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':
            if request.method=='POST':
                password = request.POST.get("password")
                if password == '' or password is None:
                    messages.info(request, 'Please Enter password')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                usage = LXPModel.K8STerminal.objects.all().filter(learner_id= request.user.id)
                if not usage:
                    messages.info(request, 'Invalid password or Terminal Setting not found, please contact to your trainer')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                totcount = 0
                passwordmain=''
                for x in usage:
                    totcount += x.usagevalue
                    passwordmain = x.Password
                usagecount = LXPModel.K8STerminalLearnerCount.objects.all().filter(learner_id= request.user.id)
                count = 0
                for x in usagecount:
                    count += x.usedvalue
                if password != passwordmain:
                    messages.info(request, 'Invalid password or Terminal Setting not found, please contact to your trainer')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                if count > totcount:
                    messages.info(request, 'Terminal usage permission exceed, please contact to your trainer')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                
                count += 1
                usagecount = LXPModel.K8STerminalLearnerCount.objects.create(
                            learner_id = request.user.id,
                            usedvalue = 1
                ).save()
                return render(request,'learner/labs/k8sterminal/learner_launch_k8sterminal.html')
            return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
    except: 
        return render(request,'lxpapp/404page.html')

@login_required
def learner_python_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/labs/python/learner_python_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/labs/linux/learner_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_cloudshell_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/labs/cloudshell/learner_cloudshell_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')