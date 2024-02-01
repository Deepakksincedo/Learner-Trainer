from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum,Count,Q
from django.urls import reverse
from social_django.models import UserSocialAuth

@login_required    
def trainer_dashboard_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            notification = LXPModel.TrainerNotification.objects.all().filter(trainer_id = request.user.id,status = False)
            mco = LXPModel.Exam.objects.filter(questiontpye='MCQ').count()
            short = LXPModel.Exam.objects.filter(questiontpye='ShortAnswer').count()
            mcqques= LXPModel.McqQuestion.objects.all().count()
            sques= LXPModel.ShortQuestion.objects.all().count()
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0, 
            'total_question':0,
            'total_short':0,
            'total_learner':0,
            'notifications':notification,
            }
            return render(request,'trainer/trainer_dashboard.html',context=dict)
        else:
            return render(request,'loginrelated/diffrentuser.html')
    #except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_add_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                materialForm=LXPFORM.MaterialForm(request.POST)
                subject = request.POST.get('subject')
                chapter = request.POST.get('chapter')
                mtype = request.POST.get('mtype')
                topic = request.POST.get('topic')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                material = LXPModel.Material.objects.create(subject_id = subject,chapter_id = chapter,topic = topic,mtype = mtype,urlvalue = urlvalue,description = description)
                material.save()
                
            materialForm=LXPFORM.MaterialForm()
            return render(request,'trainer/material/trainer_add_material.html',{'materialForm':materialForm})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def trainer_update_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            materialForm=LXPFORM.MaterialForm(request.POST)
            if request.method=='POST':
                subject = request.POST.get('subject')
                chapter = request.POST.get('chapter')
                mtype = request.POST.get('mtype')
                topic = request.POST.get('topic')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                
                material = LXPModel.Material.objects.get(id=pk)
                material.subject_id = subject
                material.chapter_id = chapter
                material.topic = topic
                material.mtype = mtype
                material.urlvalue = urlvalue
                material.description = description
                material.save()
                materials = LXPModel.Material.objects.all()
                return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
            return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_material_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            materials = LXPModel.Material.objects.all()
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            material=LXPModel.Material.objects.get(id=pk)
            material.delete()
            materials = LXPModel.Material.objects.all()
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_show_material_view(request,materialtype,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            details= LXPModel.Material.objects.all().filter(id=pk)
            if materialtype == 'HTML':
                return render(request,'trainer/material/trainer_material_htmlshow.html',{'details':details})
            if materialtype == 'URL':
                return render(request,'trainer/material/trainer_material_urlshow.html',{'details':details})
            if materialtype == 'PDF':
                return render(request,'trainer/material/trainer_material_pdfshow.html',{'details':details})
            if materialtype == 'Video':
                return render(request,'trainer/material/trainer_material_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_material_upload_file_view(request):
    subjects = LXPModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_material_upload_file.html',context)

from django.conf import settings
from datetime import datetime
import boto3, botocore
ALLOWED_EXTENSIONS = set(['pdf'])
def allowed_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_EXTENSIONS
# Connect to the s3 service
s3 = boto3.client(
    "s3",
    aws_access_key_id='AKIATZQFG2PZIUPD23GA',
    aws_secret_access_key='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'
)
#upload file to s3 w/ acl as public

@login_required  
def upload_material_file_to_s3(request,file, bucket_name, acl="public-read"):
    try:
        filename = datetime.now().strftime("%Y%m%d%H%M%S.pdf")
        print("intered in function")
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Unexpected Happened: ", e)
        return e
    # returns the webling to file upload to view
    url=settings.AWS_DOMAIN + '' + filename
    subject = request.POST.getlist('subject')
    chapter = request.POST.getlist('chapters')
    mtype = '3'
    description = 'file uploaded'
    for x in subject:
        subject = x
    for x in chapter:
        chapter = x
    for x in mtype:
        mtype = x
    if subject == 'Choose your Subject':
        messages.info(request, 'Please Select Subject')
    if chapter == 'Choose your Chapter':
        messages.info(request, 'Please Select Chapter')
    if mtype == 'Choose your Type':
        messages.info(request, 'Please Select Material Type')
    if description is None:
        messages.info(request, 'Please Enter Description')

    if description is not None and subject !='Choose your Subject' and  chapter !='Choose your Chapter' and mtype !='Choose your Type' :
        material = LXPModel.Material.objects.create(
            subject_id = subject,
            chapter_id = chapter,
            mtype = mtype,
            urlvalue=url,
            description=description
        ).save()
    
    subjects = LXPModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_material_upload_file.html',context)

@login_required
def trainer_material_start_upload_file_view(request):
    if request.method=="POST":
        file=request.FILES["select_file"]
        if file == "":
            return "Please return to previous page and select a file"
        if file:
            output = upload_material_file_to_s3(request, file, settings.AWS_BUCKET_NAME)
            return output
        else:
            return redirect("/")

@login_required
def trainer_upload_material_details_csv_view(request):
    if request.method=='POST':
        if request.POST.get('select_file') == '':
            messages.info(request, 'Please select CSV file for upload')
        else:
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            mat_type =''
            mat_url =''
            mat_desc =''
            oldsub =''
            oldchap=''
            top=''
            subid =0
            chapid=0
            topid=0
            tochk=''
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    mat_type = str(fields[3]).replace('///',',').replace('\r','')
                    mat_url = str(fields[4]).replace('///',',').replace('\r','')
                    mat_desc = str(fields[5]).replace('///',',').replace('\r','')
                    tochk = str(fields[0]).replace('///',',').replace('\r','')
                    if tochk != oldsub:
                        oldsub = tochk
                        sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                        if not sub:
                            sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                            sub.save()
                            subid=sub.id
                        else:
                            for x in sub:
                                subid=x.id  
                    tochk = str(fields[1]).replace('///',',').replace('\r','')
                    if tochk != oldchap:
                        oldchap = tochk
                        chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,subject_id=subid)
                        if not chap:
                            chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,subject_id=subid)
                            chap.save()
                            chapid=chap.id
                        else:
                            for x in chap:
                                chapid=x.id 
                    top = str(fields[2]).replace('///',',').replace('\r','')
                    
                    mat = LXPModel.Material.objects.create(
                                subject_id=subid,
                                chapter_id=chapid,
                                topic =top,
                                mtype = mat_type,
                                urlvalue = mat_url,
                                description = mat_desc
                                )
                    mat.save()
    return render(request,'trainer/material/trainer_upload_material_details_csv.html')

@login_required
def trainer_upload_material_folder_view(request):
    return render(request,'trainer/material/trainer_Upload_material_folder.html')


import os
from pathlib import Path
def upload_folder_to_s3(path, bucket_name):
    s3 = boto3.client(
    "s3",
    aws_access_key_id='AKIAVV2TMMSHQ46LTJ6R',
    aws_secret_access_key='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'
)
    oldsub =''
    oldchap=''
    tochk=''
    subid =0
    chapid=0
    filelist = []
    folder = ''
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            s3.upload_file(file_path, bucket_name, file_path)
            aws_link = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_path}, ExpiresIn=604800) # 1 week
            fullfolderpath = os.path.dirname(file_path)
            path=os.path.dirname(file_path)
            onlyFoldername = os.path.basename(path)
            onlyfilenamewithoutextension = Path(file_path).stem
            onlyfilenamewithextension = os.path.basename(file_path)
            file_extension = Path(onlyfilenamewithextension).suffix
            subname = os.path.abspath(os.path.join(fullfolderpath, os.pardir))
            tochk = os.path.basename(subname)
            if tochk != oldsub:
                oldsub = tochk
            sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
            if not sub:
                sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                sub.save()
                subid=sub.id
            else:
                for x in sub:
                    subid=x.id  
            Srno = 0
            tochk = onlyFoldername
            if tochk != oldchap:
                oldchap = tochk
                Srno = 1
                chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,subject_id=subid)
                if not chap:
                    chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,subject_id=subid)
                    chap.save()
                    chapid=chap.id
                else:
                    Srno = Srno + 1
                    for x in chap:
                        chapid=x.id
            topic = onlyfilenamewithoutextension
            doctype = ''
            file_extension = file_extension.replace('.','')
            if str(file_extension).upper() == 'VIDEO':
                doctype = 'Video'
            else :
                doctype = str(file_extension).upper()
            desc = topic
            data = LXPModel.Material.objects.create(
                    serial_number = Srno,
                    topic = topic,
                    mtype = doctype,
                    urlvalue = aws_link,
                    description = desc,
                    chapter_id = chapid,
                    subject_id = subid
            )
            data.save()

def trainer_start_upload_material_folder_view(request):
    if request.method=="POST":
        folder=request.POST["select_folder"]
        folder = str.replace(folder,'/','\\')
        path ='D:\\upload\\iLMS'
        path =folder
        AWS_BUCKET_NAME='nubeera-study'
        upload_folder_to_s3(path, AWS_BUCKET_NAME)
        return  redirect("/")
@login_required
def trainer_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/sessionmaterial/trainer_sessionmaterial.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                sessionmaterialForm=LXPFORM.SessionMaterialForm(request.POST)
                playlist = request.POST.get('playlist')
                video = request.POST.get('video')
                mtype = request.POST.get('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                sessionmaterial = LXPModel.SessionMaterial.objects.create(playlist_id = playlist,video_id = video,mtype = mtype,urlvalue = urlvalue,description = description)
                sessionmaterial.save()
                
            sessionmaterialForm=LXPFORM.SessionMaterialForm()
            return render(request,'trainer/sessionmaterial/trainer_add_sessionmaterial.html',{'sessionmaterialForm':sessionmaterialForm})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def trainer_update_sessionmaterial_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            sessionmaterialForm=LXPFORM.SessionMaterialForm(request.POST)
            if request.method=='POST':
                playlist = request.POST.get('playlist')
                video = request.POST.get('video')
                mtype = request.POST.get('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                
                sessionmaterial = LXPModel.SessionMaterial.objects.get(id=pk)
                sessionmaterial.playlist_id = playlist
                sessionmaterial.video_id = video
                sessionmaterial.mtype = mtype
                sessionmaterial.urlvalue = urlvalue
                sessionmaterial.description = description
                sessionmaterial.save()
                sessionmaterials = LXPModel.SessionMaterial.objects.all()
                return render(request,'trainer/sessionmaterial/trainer_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
            return render(request,'trainer/sessionmaterial/trainer_update_sessionmaterial.html',{'sessionmaterialForm':sessionmaterialForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            sessionmaterials = LXPModel.SessionMaterial.objects.all()
            return render(request,'trainer/sessionmaterial/trainer_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_sessionmaterial_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            sessionmaterial=LXPModel.SessionMaterial.objects.get(id=pk)
            sessionmaterial.delete()
            sessionmaterials = LXPModel.SessionMaterial.objects.all()
            return render(request,'trainer/sessionmaterial/trainer_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_show_sessionmaterial_view(request,sessionmaterialtype,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            details= LXPModel.SessionMaterial.objects.all().filter(id=pk)
            if sessionmaterialtype == 'HTML':
                return render(request,'trainer/sessionmaterial/trainer_sessionmaterial_htmlshow.html',{'details':details})
            if sessionmaterialtype == 'URL':
                return render(request,'trainer/sessionmaterial/trainer_sessionmaterial_urlshow.html',{'details':details})
            if sessionmaterialtype == 'PDF':
                return render(request,'trainer/sessionmaterial/trainer_sessionmaterial_pdfshow.html',{'details':details})
            if sessionmaterialtype == 'Video': 
                return render(request,'trainer/sessionmaterial/trainersessionmaterial_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

def load_videos(request):
    try:
        playlist_id = request.GET.get('playlist')
        videos = LXPModel.PlaylistItem.objects.raw('SELECT  lxpapp_video.id as id,lxpapp_video.id as pk, lxpapp_video.name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) WHERE  lxpapp_playlistitem.playlist_id = ' + str(playlist_id) + ' ORDER BY  lxpapp_video.name')
        context = {'videos': videos}
        return render(request, 'hr/video_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/exam/trainer_exam.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_add_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            form = LXPFORM.ExamForm(request.POST or None)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../trainer/trainer-dashboard'
            breadcrumblink.append(btrnr)

            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../trainer/trainer-view-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Active'
            btrnr["link"]='Add Exam'
            breadcrumblink.append(btrnr)
            
            context = {
                'form': form,
                'breadcrumbsetting':breadcrumblink,
                'page_title': 'Add Exam'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('exam_name')
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = name)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('trainer-add-exam'))
                    try:
                        qtype = form.cleaned_data.get('questiontpye')
                        batch = form.cleaned_data.get('batch').pk
                        exam = LXPModel.Exam.objects.create(
                                                    exam_name = name,questiontpye=qtype,batch_id=batch)
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('trainer-add-exam'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'trainer/exam/add_edit_exam.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            instance = get_object_or_404(LXPModel.Exam, id=pk)
            form = LXPFORM.ExamForm(request.POST or None, instance=instance)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../trainer/trainer-dashboard'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Add Exam'
            btrnr["link"]='../../../../trainer/trainer-add-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../trainer/trainer-view-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Active'
            btrnr["link"]='Update Exam'
            breadcrumblink.append(btrnr)
            
            context = {
                'form': form,
                'exam_id': pk,
                'breadcrumbsetting':breadcrumblink,
                'page_title': 'Update Exam'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('exam_name')
                    batch = form.cleaned_data.get('batch').pk
                    qtype = form.cleaned_data.get('questiontpye')
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = name).exclude(id=pk)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('trainer-update-exam', args=[pk]))
                    try:
                        exam = LXPModel.Exam.objects.get(id=pk)
                        exam.exam_name = name
                        exam.batch_id = batch
                        exam.questiontpye = qtype
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        exams = LXPModel.Exam.objects.all()
                        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")

            return render(request, 'trainer/exam/add_edit_exam.html', context,{'a':'imran'})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_upload_exam_csv_view(request):
    if request.method=='POST':
        file=request.FILES["select_file"]
        examtext=request.POST.get('exam_name')
        batch=request.POST.get('batch')
        qtype=request.POST.get('examtype')
        exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = examtext)
        if exam:
            messages.info(request, 'Exam Name Already Exist')
        else:
            if qtype=='0':
                qtype = 'MCQ'
            else:
                qtype = 'ShortAnswer'
            exam = LXPModel.Exam.objects.create(batch_id = batch,exam_name = examtext,questiontpye = qtype)
            exam.save()   
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    if qtype == 'MCQ':
                        question = LXPModel.McqQuestion.objects.create(
                            question = fields[0],
                            option1 = fields[1],
                            option2 = fields[2],
                            option3 = fields[3],
                            option4 = fields[4],
                            answer = fields[5],
                            marks = fields[6],
                            exam_id = exam.id
                        )
                        question.save()
                    elif qtype == 'ShortAnswer':
                        question = LXPModel.ShortQuestion.objects.create(
                            question = fields[0],
                            marks = fields[1],
                            exam_id = exam.id
                        )
                        question.save()
    batch = LXPModel.Batch.objects.all()
    context = {'batch': batch}
    return render(request,'trainer/exam/trainer_upload_exam_csv.html',context)

def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "myapp/upload_csv.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		file_data = csv_file.read().decode("utf-8")		
		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:						
			fields = line.split(",")
			data_dict = {}
			data_dict["name"] = fields[0]
			data_dict["start_date_time"] = fields[1]
			data_dict["end_date_time"] = fields[2]
			data_dict["notes"] = fields[3]
			

	except Exception as e:
		messages.error(request,"Unable to upload file. "+repr(e))

@login_required
def trainer_view_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all())
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

def trainer_view_filter_exam_view(request,type):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all(),questiontpye = type)
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            exam=LXPModel.Exam.objects.get(id=pk)
            exam.delete()
            return HttpResponseRedirect('/trainer/trainer-view-exam')
        exams = LXPModel.Exam.objects.all()
        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/mcqquestion/trainer_mcqquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            storage = messages.get_messages(request)
            storage.used = True
            if request.method=='POST':
                mcqquestionForm=LXPFORM.McqQuestionForm(request.POST)
                if mcqquestionForm.is_valid(): 
                    questiontext = mcqquestionForm.cleaned_data["question"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(question__iexact = questiontext)
                    if mcqquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        mcqquestionForm=LXPFORM.McqQuestionForm()
                        return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        mcqquestion = LXPModel.McqQuestion.objects.create(exam_id = exam.id,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        mcqquestion.save()
                        messages.info(request, 'Mcq Question added')
                else:
                    print("form is invalid")
            mcqquestionForm=LXPFORM.McqQuestionForm()
            return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestion = LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestionForm=LXPFORM.McqQuestionForm(request.POST,instance=mcqquestion)
            if request.method=='POST':
                if mcqquestionForm.is_valid(): 
                    mcqquestiontext = mcqquestionForm.cleaned_data["mcqquestion_name"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(mcqquestion_name__iexact = mcqquestiontext).exclude(id=pk)
                    if mcqquestion:
                        messages.info(request, 'McqQuestion Name Already Exist')
                        return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
                    else:
                        mcqquestionForm.save()
                        mcqquestions = LXPModel.McqQuestion.objects.all()
                        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
            return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm,'ex':mcqquestion.mcqquestion_name,'sub':mcqquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_exams_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(questiontpye='MCQ')
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion_exams.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_view(request,examid):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestions = LXPModel.McqQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all().filter(id=examid))
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            mcqquestion=LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-mcqquestion')
        mcqquestions = LXPModel.McqQuestion.objects.all()
        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/shortquestion/trainer_shortquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                shortquestionForm=LXPFORM.ShortQuestionForm(request.POST)
                if shortquestionForm.is_valid(): 
                    questiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = questiontext)
                    if shortquestion:
                        messages.info(request, 'Short Question Already Exist')
                        shortquestionForm=LXPFORM.ShortQuestionForm()
                        return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        shortquestion = LXPModel.ShortQuestion.objects.create(exam_id = exam.id,question = questiontext,marks=request.POST.get('marks'))
                        shortquestion.save()
                else:
                    print("form is invalid")
            shortquestionForm=LXPFORM.ShortQuestionForm()
            return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestion = LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestionForm=LXPFORM.ShortQuestionForm(request.POST,instance=shortquestion)
            if request.method=='POST':
                if shortquestionForm.is_valid(): 
                    shortquestiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = shortquestiontext).exclude(id=pk)
                    if shortquestion:
                        messages.info(request, 'ShortQuestion Name Already Exist')
                        return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm})
                    else:
                        examid = LXPModel.Exam.objects.all().filter(id=request.POST['examID'])
                        shortquestionForm.examID=examid
                        shortquestionForm.save()
                        shortquestions = LXPModel.ShortQuestion.objects.all()
                        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
            return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm,'ex':shortquestion.question})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestions = LXPModel.ShortQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all())
            return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            shortquestion=LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-shortquestion')
        shortquestions = LXPModel.ShortQuestion.objects.all()
        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_pending_short_exam_result_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            pending = LXPModel.ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = LXPModel.Exam.objects.all(),status = False)
            return render(request,'trainer/shortexam/trainer_pending_short_exam_reuslt.html',{'pending':pending})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
            return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_save_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=="POST":
                feedback=request.POST['newfeedback']
                marks=request.POST['newmarks']
                rid=request.POST['newid']
                qid=request.POST['newqid']
                answer=request.POST['newanswer']
                mainid=request.POST['newmainid']
                resupdate = LXPModel.ShortResultDetails.objects.all().filter(id=pk)
                resupdate.delete()
                resupdate = LXPModel.ShortResultDetails.objects.create(id=pk,marks=marks,feedback=feedback,question_id=qid,answer=answer,shortresult_id=mainid)
                resupdate.save()
                
                totmarks=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Sum('marks'))['stars']
                maintbl=LXPModel.ShortResult.objects.get(id=mainid)
                tot=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Count('marks'))['stars']
                totgiven=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid,marks__gt=0).aggregate(stars=Count('marks'))['stars']
                if tot == totgiven:
                    maintbl.status=True
                maintbl.marks = totmarks
                maintbl.save()
                if tot == totgiven:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
                else:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = mainid)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def trainer_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/ytexamquestion/trainer_ytexamquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                ytexamquestionForm=LXPFORM.YTExamQuestionForm(request.POST)
                if ytexamquestionForm.is_valid(): 
                    questiontext = ytexamquestionForm.cleaned_data["question"]
                    ytexamquestion = LXPModel.YTExamQuestion.objects.all().filter(question__iexact = questiontext)
                    if ytexamquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        ytexamquestionForm=LXPFORM.YTExamQuestionForm()
                        return render(request,'trainer/ytexamquestion/trainer_add_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})                  
                    else:
                        playlist=LXPModel.Playlist.objects.get(id=ytexamquestionForm.cleaned_data["playlistID"].pk)
                        video=LXPModel.Video.objects.get(id=ytexamquestionForm.cleaned_data["videoID"].pk)
                        ytexamquestion = LXPModel.YTExamQuestion.objects.create(
                            playlist_id = playlist.id,
                            video_id = video.id,
                            question = questiontext,
                            option1=request.POST.get('option1'),
                            option2=request.POST.get('option2'),
                            option3=request.POST.get('option3'),
                            option4=request.POST.get('option4'),
                            answer=request.POST.get('answer'),
                            marks=request.POST.get('marks'))
                        ytexamquestion.save()
                else:
                    print("form is invalid")
            ytexamquestionForm=LXPFORM.YTExamQuestionForm()
            return render(request,'trainer/ytexamquestion/trainer_add_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_ytexamquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            ytexamquestion = LXPModel.YTExamQuestion.objects.get(id=pk)
            ytexamquestionForm=LXPFORM.YTExamQuestionForm(request.POST,instance=ytexamquestion)
            if request.method=='POST':
                if ytexamquestionForm.is_valid(): 
                    ytexamquestiontext = ytexamquestionForm.cleaned_data["ytexamquestion_name"]
                    ytexamquestion = LXPModel.YTExamQuestion.objects.all().filter(ytexamquestion_name__iexact = ytexamquestiontext).exclude(id=pk)
                    if ytexamquestion:
                        messages.info(request, 'Question Already Exist')
                        return render(request,'trainer/ytexamquestion/trainer_update_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})
                    else:
                        ytexamquestionForm.save()
                        ytexamquestions = LXPModel.YTExamQuestion.objects.all()
                        return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
            return render(request,'trainer/ytexamquestion/trainer_update_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm,'ex':ytexamquestion.ytexamquestion_name,'sub':ytexamquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            ytexamquestions = LXPModel.YTExamQuestion.objects.all().filter(playlist_id__in = LXPModel.Playlist.objects.all())
            return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_ytexamquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            ytexamquestion=LXPModel.YTExamQuestion.objects.get(id=pk)
            ytexamquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-ytexamquestion')
        ytexamquestions = LXPModel.YTExamQuestion.objects.all()
        return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_learner_video_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            learner = UserSocialAuth.objects.raw('SELECT social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, social_auth_usersocialauth.pic, auth_user.first_name, auth_user.last_name, GROUP_CONCAT(DISTINCT lxpapp_playlist.name) AS courseset_name, lxpapp_learnerdetails.mobile FROM social_auth_usersocialauth LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) LEFT OUTER JOIN lxpapp_batchlearner ON (auth_user.id = lxpapp_batchlearner.learner_id) LEFT OUTER JOIN lxpapp_batchrecordedvdolist ON (lxpapp_batchlearner.batch_id = lxpapp_batchrecordedvdolist.batch_id) LEFT OUTER JOIN lxpapp_playlist ON (lxpapp_batchrecordedvdolist.playlist_id = lxpapp_playlist.id) LEFT OUTER JOIN lxpapp_learnerdetails ON (auth_user.id = lxpapp_learnerdetails.learner_id) WHERE (social_auth_usersocialauth.utype = 0 OR social_auth_usersocialauth.utype = 2) AND social_auth_usersocialauth.status = 1 GROUP BY social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, auth_user.first_name, auth_user.last_name, lxpapp_learnerdetails.mobile ')
            return render(request,'trainer/learnervideo/trainer_view_learner_video.html',{'learner':learner})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_video_Course_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'trainer':
            videos1 = LXPModel.BatchCourseSet.objects.raw('SELECT DISTINCT lxpapp_courseset.id,  lxpapp_courseset.courseset_name,lxpapp_batchcourseset.batch_id FROM  lxpapp_batchcourseset   INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(user_id))
            return render(request,'trainer/learnervideo/trainer_learner_video_course.html',{'videos':videos1,'userfirstname':userfirstname,'userlastname':userlastname,'user_id':user_id})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_video_Course_subject_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'trainer':
            
            subject = LXPModel.Playlist.objects.raw('SELECT ID AS id, NAME, VTOTAL, Mtotal, SUM(VWATCHED) AS VWatched,((100*VWATCHED)/VTOTAL) as per, THUMBNAIL_URL FROM (SELECT YYY.ID, YYY.NAME, YYY.THUMBNAIL_URL, ( SELECT COUNT(XX.ID) FROM LXPAPP_PLAYLISTITEM XX WHERE XX.PLAYLIST_ID = YYY.ID ) AS Vtotal, ( SELECT COUNT(zz.ID) FROM LXPAPP_sessionmaterial zz WHERE zz.PLAYLIST_ID = YYY.ID ) AS Mtotal, (SELECT COUNT (LXPAPP_VIDEOWATCHED.ID) AS a FROM LXPAPP_PLAYLISTITEM GHGH LEFT OUTER JOIN LXPAPP_VIDEOWATCHED ON ( GHGH.VIDEO_ID = LXPAPP_VIDEOWATCHED.VIDEO_ID ) WHERE GHGH.PLAYLIST_ID = YYY.ID AND LXPAPP_VIDEOWATCHED.LEARNER_ID = ' + str( user_id) + ') AS VWatched FROM LXPAPP_BATCHLEARNER INNER JOIN LXPAPP_BATCH ON (LXPAPP_BATCHLEARNER.BATCH_ID = LXPAPP_BATCH.ID) INNER JOIN LXPAPP_BATCHRECORDEDVDOLIST ON (LXPAPP_BATCH.ID = LXPAPP_BATCHRECORDEDVDOLIST.BATCH_ID) INNER JOIN LXPAPP_PLAYLIST YYY ON (LXPAPP_BATCHRECORDEDVDOLIST.PLAYLIST_ID = YYY.ID) WHERE LXPAPP_BATCHLEARNER.LEARNER_ID = ' + str(user_id) + ') GROUP BY ID, NAME, VTOTAL ORDER BY NAME')
            videocount = LXPModel.LearnerPlaylistCount.objects.all().filter(learner_id = user_id)
            countpresent =False
            if videocount:
                countpresent = True
            per = 0
            tc = 0
            wc = 0
            for x in subject:
                if not videocount:
                    countsave = LXPModel.LearnerPlaylistCount.objects.create(playlist_id = x.id, learner_id = user_id,count =x.Vtotal )
                    countsave.save()
                tc += x.Vtotal
                wc += x.VWatched
            try:
                per = (100*int(wc))/int(tc)
            except:
                per =0
            dif = tc- wc
            return render(request,'trainer/learnervideo/trainer_learner_video_course_subject.html',{'user_id':user_id,'subject':subject,'userfirstname':userfirstname,'userlastname':userlastname,'dif':dif,'per':per,'wc':wc,'tc':tc})
 #   except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_learner_video_list_view(request,subject_id,user_id):
    try:     
        if str(request.session['utype']) == 'trainer':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.PlaylistItem.objects.raw('SELECT DISTINCT mainvid.id, mainvid.name, IFNULL((SELECT lxpapp_videowatched.video_id FROM lxpapp_videowatched WHERE lxpapp_videowatched.learner_id = ' + str(user_id) + ' AND lxpapp_videowatched.video_id = mainvid.id), 0) AS watched, IFNULL((SELECT lxpapp_videotounlock.video_id FROM lxpapp_videotounlock WHERE lxpapp_videotounlock.learner_id = ' + str(user_id) + ' AND lxpapp_videotounlock.video_id = mainvid.id), 0) AS unlocked FROM lxpapp_video mainvid INNER JOIN lxpapp_playlistitem ON (mainvid.id = lxpapp_playlistitem.video_id) WHERE lxpapp_playlistitem.playlist_id = ' + str (subject_id) + ' AND mainvid.name <> "Deleted video"')  
            return render(request,'trainer/learnervideo/trainer_learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'user_id':user_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_approve_video(request,pk,studid):
    try:
        if str(request.session['utype']) == 'trainer':
            unlock = LXPModel.VideoToUnlock.objects.create(learner_id=studid,video_id=pk)
            unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def trainer_learner_approveall_video(request,userid,subject_id):
    try:
        if str(request.session['utype']) == 'trainer':
            videos=LXPModel.Playlist.objects.raw('SELECT   lxpapp_video.id FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) where lxpapp_playlistitem.playlist_id = ' + str (subject_id))
            for x in videos:
                unlock = LXPModel.VideoToUnlock.objects.create(learner_id=userid,video_id=x.id)
                unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_show_video_view(request,subject_id,video_id):
    try:    
        if str(request.session['utype']) == 'trainer':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
            return render(request,'trainer/learnervideo/trainer_learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_chapterquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            storage = messages.get_messages(request)
            storage.used = True
            if request.method=='POST':
                chapterquestionForm=LXPFORM.ChapterQuestionForm(request.POST)
                if chapterquestionForm.is_valid(): 
                    questiontext = chapterquestionForm.cleaned_data["question"]
                    chapterquestion = LXPModel.ChapterQuestion.objects.all().filter(question__iexact = questiontext)
                    if chapterquestion:
                        messages.info(request, 'Chapter Question Name Already Exist')
                        chapterquestionForm=LXPFORM.ChapterQuestionForm()
                        return render(request,'trainer/chapterquestion/trainer_add_chapterquestion.html',{'chapterquestionForm':chapterquestionForm})                  
                    else:
                        chapterquestion = LXPModel.ChapterQuestion.objects.create(subject_id = chapterquestionForm.cleaned_data["subject"].pk,chapter_id = chapterquestionForm.cleaned_data["chapter"].pk,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        chapterquestion.save()
                        messages.info(request, 'Chapter  Question added')
                else:
                    print("form is invalid")
            chapterquestionForm=LXPFORM.ChapterQuestionForm()
            return render(request,'trainer/chapterquestion/trainer_add_chapterquestion.html',{'chapterquestionForm':chapterquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_chapterquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            chapterquestion = LXPModel.ChapterQuestion.objects.get(id=pk)
            chapterquestionForm=LXPFORM.ChapterQuestionForm(request.POST,instance=chapterquestion)
            if request.method=='POST':
                if chapterquestionForm.is_valid(): 
                    chapterquestiontext = chapterquestionForm.cleaned_data["chapterquestion_name"]
                    chapterquestion = LXPModel.ChapterQuestion.objects.all().filter(chapterquestion_name__iexact = chapterquestiontext).exclude(id=pk)
                    if chapterquestion:
                        messages.info(request, 'ChapterQuestion Name Already Exist')
                        return render(request,'trainer/chapterquestion/trainer_update_chapterquestion.html',{'chapterquestionForm':chapterquestionForm})
                    else:
                        chapterquestionForm.save()
                        chapterquestions = LXPModel.ChapterQuestion.objects.all()
                        return render(request,'trainer/chapterquestion/trainer_view_chapterquestion.html',{'chapterquestions':chapterquestions})
            return render(request,'trainer/chapterquestion/trainer_update_chapterquestion.html',{'chapterquestionForm':chapterquestionForm,'ex':chapterquestion.chapterquestion_name,'sub':chapterquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_chapterquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            chapterquestions = LXPModel.ChapterQuestion.objects.raw('SELECT DISTINCT  lxpapp_chapter.id,  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name FROM  lxpapp_chapterquestion  INNER JOIN lxpapp_chapter ON (lxpapp_chapterquestion.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_subject ON (lxpapp_chapterquestion.subject_id = lxpapp_subject.id)')
            return render(request,'trainer/chapterquestion/trainer_view_chapterquestion.html',{'chapterquestions':chapterquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_chapterquestion_chapter_view(request,chapter_id):
    try:
        if str(request.session['utype']) == 'trainer':
            chapterquestions = LXPModel.ChapterQuestion.objects.all().filter(chapter_id__in = LXPModel.Chapter.objects.all().filter(id=chapter_id))
            chapter_name = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name

            return render(request,'trainer/chapterquestion/trainer_view_chapterquestion_chapter.html',{'chapterquestions':chapterquestions,'chapter_name':chapter_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_chapterquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            chapterquestion=LXPModel.ChapterQuestion.objects.get(id=pk)
            chapterquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-chapterquestion')
        chapterquestions = LXPModel.ChapterQuestion.objects.all()
        return render(request,'trainer/chapterquestion/trainer_view_chapterquestion.html',{'chapterquestions':chapterquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/labs/k8sterminal/trainer_k8sterminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                k8sterminalForm=LXPFORM.K8STerminalForm(request.POST)
                learner_id = request.POST['user_name']
                usagevalue = request.POST.get('usagevalue')
                password1 = request.POST.get("password")
                password2 = request.POST.get("confirmpassword")
                if password1 and password2 and password1 != password2:
                    messages.info(request, 'password_mismatch')
                else:
                    k8sterminal = LXPModel.K8STerminal.objects.create(
                        trainer_id = request.user.id,
                        learner_id = learner_id,
                        Password = password1,
                        usagevalue = usagevalue)
                    k8sterminal.save()
                    messages.info(request, 'Record Saved')
            k8sterminalForm=LXPFORM.K8STerminalForm()
            users = User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.password,  auth_user.is_superuser,  auth_user.username,  auth_user.last_name,  auth_user.email,  auth_user.first_name,  social_auth_usersocialauth.utype,  social_auth_usersocialauth.status,  social_auth_usersocialauth.uid FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.status = 1 AND   (social_auth_usersocialauth.utype = 0 OR  social_auth_usersocialauth.utype = 2 ) ORDER BY auth_user.first_name, auth_user.last_name')
            return render(request,'trainer/labs/k8sterminal/trainer_add_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            k8sterminal = LXPModel.K8STerminal.objects.get(id=pk)
            k8sterminalForm=LXPFORM.K8STerminalForm(request.POST,instance=k8sterminal)
            if request.method=='POST':
                if k8sterminalForm.is_valid(): 
                    k8sterminaltext = k8sterminalForm.cleaned_data["k8sterminal_name"]
                    chaptertext = k8sterminalForm.cleaned_data["chapterID"]
                    subjecttext = k8sterminalForm.cleaned_data["subjectID"]
                    k8sterminal = LXPModel.K8STerminal.objects.all().filter(k8sterminal_name__iexact = k8sterminaltext).exclude(id=pk)
                    if k8sterminal:
                        messages.info(request, 'K8STerminal Name Already Exist')
                        return render(request,'trainer/labs/k8sterminal/trainer_update_k8sterminal.html',{'k8sterminalForm':k8sterminalForm})
                    else:
                        chapter = LXPModel.Video.objects.get(chapter_name=chaptertext)
                        subject = LXPModel.Playlist.objects.get(subject_name=subjecttext)
                        k8sterminal = LXPModel.K8STerminal.objects.get(id=pk)
                        k8sterminal.k8sterminal_name = k8sterminaltext
                        k8sterminal.subject_id = subject.id
                        k8sterminal.chapter_id = chapter.id
                        k8sterminal.save()
                        c_list = LXPModel.K8STerminal.objects.filter(chapter_id__in=LXPModel.Video.objects.all())
                        return render(request,'trainer/labs/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':c_list})
            return render(request,'trainer/labs/k8sterminal/trainer_update_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'sub':k8sterminal.k8sterminal_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_k8sterminal_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            k8sterminals = LXPModel.K8STerminal.objects.all().filter(learner_id__in = User.objects.all().order_by('first_name').filter(id__in=UserSocialAuth.objects.all()))
            return render(request,'trainer/labs/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            k8sterminal=LXPModel.K8STerminal.objects.get(id=pk)
            k8sterminal.delete()
            return HttpResponseRedirect('/trainer/trainer-view-k8sterminal')
        k8sterminals = LXPModel.K8STerminal.objects.all()
        return render(request,'trainer/labs/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_python_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/labs/python/trainer_python_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/labs/linux/trainer_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_cloudshell_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/labs/cloudshell/trainer_cloudshell_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')