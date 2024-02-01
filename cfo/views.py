from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.shortcuts import render, redirect
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
import json

@login_required    
def cfo_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'cfo/cfo_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
 

@login_required
def cfo_add_coursetype_view(request):
    form = LXPFORM.CourseTypeForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course Type'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('coursetype_name')
            coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = name)
            if coursetype:
                messages.info(request, 'Course Type Name Already Exist')
                return redirect(reverse('cfo-add-coursetype'))
            try:
                coursetype = LXPModel.CourseType.objects.create(
                                            coursetype_name = name)
                coursetype.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cfo-add-coursetype'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cfo/coursetype/add_edit_coursetype.html', context)

@login_required
def cfo_update_coursetype_view(request, pk):
    instance = get_object_or_404(LXPModel.CourseType, id=pk)
    form = LXPFORM.CourseTypeForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'coursetype_id': pk,
        'page_title': 'Edit CourseType'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('coursetype_name')
            coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = name).exclude(id=pk)
            if coursetype:
                messages.info(request, 'Course Type Name Already Exist')
                return redirect(reverse('cfo-update-coursetype', args=[pk]))
            try:
                coursetype = LXPModel.CourseType.objects.get(id=pk)
                coursetype.coursetype_name = name
                coursetype.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cfo-update-coursetype', args=[pk]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cfo/coursetype/add_edit_coursetype.html', context)


@login_required
def cfo_view_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            coursetypes = LXPModel.CourseType.objects.all()
            return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_coursetype_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            coursetype=LXPModel.CourseType.objects.get(id=pk)
            coursetype.delete()
            return HttpResponseRedirect('/cfo/coursetype/cfo-view-coursetype')
        coursetypes = LXPModel.CourseType.objects.all()
        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')
    
from django.db import transaction
@login_required
def cfo_add_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                batchForm=LXPFORM.BatchForm(request.POST)
                batchtext = batchForm.data["batch_name"]
                batch = LXPModel.Batch.objects.all().filter(batch_name__iexact = batchtext)
                if batch:
                    messages.info(request, 'Batch Name Already Exist')
                    batchForm=LXPFORM.BatchForm()
                    return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm})                  
                else:
                    coursetypeid = batchForm.data["coursetypeID"]
                    batchtable = LXPModel.Batch.objects.create(batch_name=batchtext,stdate=batchForm.data["stdate"],enddate=batchForm.data["enddate"],coursetype_id=coursetypeid)
                    batchtable.save()
                    selectedlist = request.POST.getlist('listbox1')
                    for x in selectedlist:
                        trainerid = str(x)
                        batchtrainertable = LXPModel.BatchTrainer.objects.create(batch_id=batchtable.id,trainer_id=trainerid)
                        batchtrainertable.save()
                    import json
                    json_data = json.loads(request.POST.get('myvalue'))
                    for cx in json_data:
                        a=json_data[cx]['id']
                        b=json_data[cx]['fee']
                        batchlearnertable = LXPModel.Batchlearner.objects.create(batch_id=batchtable.id,learner_id=a,fee=b)
                        batchlearnertable.save()
                    selectedlist = request.POST.getlist('listbox3')
                    for x in selectedlist:
                        modid = str(x)
                        batchmodtable = LXPModel.BatchModule.objects.create(batch_id=batchtable.id,module_id=modid)
                        batchmodtable.save()
                    selectedlist = request.POST.getlist('vdolist')
                    for x in selectedlist:
                        PLid = str(x)
                        batchvdotable = LXPModel.BatchRecordedVDOList.objects.create(batch_id=batchtable.id,playlist_id=PLid)
                        batchvdotable.save()
            batchForm=LXPFORM.BatchForm()
            trainers =  User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 1 AND  social_auth_usersocialauth.status = true')
            learners =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 2 AND  social_auth_usersocialauth.status = true ORDER BY auth_user.first_name, auth_user.last_name'))
            modules =  LXPModel.Module.objects.all()
            PList =  LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm,'trainers':trainers,'learners':learners,'modules':modules,'PList':PList})
    except:
        return render(request,'lxpapp/404page.html')
import json
@login_required
def cfo_update_batch_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cfo':
            batch = LXPModel.Batch.objects.get(id=pk)
            batchForm=LXPFORM.BatchForm(request.POST,instance=batch)
            if request.method=='POST':
                if batchForm.is_valid(): 
                    batchtext = batchForm.cleaned_data["batch_name"]
                    batch = LXPModel.Batch.objects.all().filter(batch_name__iexact = batchtext).exclude(id=pk)
                    if batch:
                        messages.info(request, 'Batch Name Already Exist')
                        return render(request,'cfo/batch/cfo_update_batch.html',{'batchForm':batchForm})
                    else:
                        batchForm.save()
                        selectedlist = request.POST.getlist('listbox1')
                        det = LXPModel.BatchTrainer.objects.all().filter(batch_id=pk)
                        det.delete()
                        for x in selectedlist:
                            trainerid = str(x)
                            batchtrainertable = LXPModel.BatchTrainer.objects.create(batch_id=pk,trainer_id=trainerid)
                            batchtrainertable.save()
                        det = LXPModel.Batchlearner.objects.all().filter(batch_id=pk)
                        det.delete()
                        json_data = json.loads(request.POST.get('myvalue'))
                        for cx in json_data:
                            a=json_data[cx]['id']
                            b=json_data[cx]['fee']
                            batchlearnertable = LXPModel.Batchlearner.objects.create(batch_id=pk,learner_id=a,fee=b)
                            batchlearnertable.save()
                        selectedlist = request.POST.getlist('listbox3')
                        det = LXPModel.BatchModule.objects.all().filter(batch_id=pk)
                        det.delete()
                        for x in selectedlist:
                            moduleid = str(x)
                            batchcoursetable = LXPModel.BatchModule.objects.create(batch_id=pk,module_id=moduleid)
                            batchcoursetable.save()
                        det = LXPModel.BatchRecordedVDOList.objects.all().filter(batch_id=pk)
                        det.delete()
                        selectedlist = request.POST.getlist('vdolist')
                        for x in selectedlist:
                            PLid = str(x)
                            batchvdotable = LXPModel.BatchRecordedVDOList.objects.create(batch_id=pk,playlist_id=PLid)
                            batchvdotable.save()
                        batchs = LXPModel.Batch.objects.all()
                        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
            trainers =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 1 AND  social_auth_usersocialauth.status = true'))
            learners =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 2 AND  social_auth_usersocialauth.status = true ORDER BY auth_user.first_name, auth_user.last_name'))
            batchtrainers =  list(User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.first_name , auth_user.last_name ,  auth_user.email FROM  lxpapp_batchtrainer  INNER JOIN auth_user ON (lxpapp_batchtrainer.trainer_id = auth_user.id)   WHERE lxpapp_batchtrainer.batch_id = ' + str (pk)))
            PList =  list(LXPModel.Playlist.objects.all().order_by('name'))

            bPList = []
            for c in PList:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["name"]=c.name
                bPList.append(btrnr)
            bPList = json.dumps(bPList)
            
            btrainer = []
            for c in batchtrainers:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["first_name"]=c.first_name
                btrnr["last_name"]=c.last_name
                btrnr["email"]=c.email
                btrainer.append(btrnr)
            batchlearners =  list(User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.first_name , auth_user.last_name ,  auth_user.email,lxpapp_batchlearner.fee FROM  lxpapp_batchlearner  INNER JOIN auth_user ON (lxpapp_batchlearner.learner_id = auth_user.id)   WHERE lxpapp_batchlearner.batch_id = ' + str (pk)))
            blearner = []
            for c in batchlearners:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["first_name"]=c.first_name
                btrnr["last_name"]=c.last_name
                btrnr["email"]=c.email
                btrnr["fee"]=c.fee
                blearner.append(btrnr)
            courses =  LXPModel.Course.objects.all()
            btrainer = json.dumps(btrainer)
            blearner = json.dumps(blearner)
            query = LXPModel.Batch.objects.get(id=pk)
            stdate = (query.stdate).strftime('%Y-%m-%d')
            enddate = (query.enddate).strftime('%Y-%m-%d')
            coursetype = query.coursetype
            dict={
            'batchForm':batchForm,
            'sub':batch.batch_name,
            'trainers':trainers,
            'learners':learners,
            'batchtrainers':batchtrainers,
            'batchlearners':batchlearners,
            'courses':courses,
            'btrainer':btrainer,
            'blearner':blearner,
            'stdate':stdate,
            'enddate':enddate,
            'coursetype':coursetype,
            'bPList':bPList,
            'PList':PList}
            
            return render(request,'cfo/batch/cfo_update_batch.html',context=dict)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = LXPModel.Batch.objects.all()
            return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_batch_details_view(request,batchname,pk):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = LXPModel.Batch.objects.raw("SELECT lxpapp_batch.id, GROUP_CONCAT(DISTINCT lxpapp_module.module_name) AS module_name, GROUP_CONCAT(DISTINCT lxpapp_playlist.name) AS video_name, lxpapp_batch.stdate, lxpapp_batch.enddate, GROUP_CONCAT(DISTINCT trainer.first_name || ' ' || trainer.last_name) AS trainer_name, GROUP_CONCAT(DISTINCT learner.first_name || ' ' || learner.last_name) AS learner_name FROM lxpapp_batch LEFT OUTER JOIN lxpapp_batchmodule ON (lxpapp_batchmodule.batch_id = lxpapp_batch.id) LEFT OUTER JOIN lxpapp_batchrecordedvdolist ON (lxpapp_batchrecordedvdolist.batch_id = lxpapp_batch.id) LEFT OUTER JOIN lxpapp_playlist ON (lxpapp_batchrecordedvdolist.playlist_id = lxpapp_playlist.id) LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id) LEFT OUTER JOIN lxpapp_batchtrainer ON (lxpapp_batch.id = lxpapp_batchtrainer.batch_id) LEFT OUTER JOIN auth_user trainer ON (lxpapp_batchtrainer.trainer_id = trainer.id) LEFT OUTER JOIN lxpapp_module ON (lxpapp_batchmodule.module_id = lxpapp_module.id) LEFT OUTER JOIN auth_user learner ON (lxpapp_batchlearner.learner_id = learner.id) WHERE lxpapp_batch.id = " + str(pk))
            return render(request,'cfo/batch/cfo_view_batch_details.html',{'batchs':batchs,'batchname':batchname})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_batch_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            batch=LXPModel.Batch.objects.get(id=pk)
            batch.delete()
        batchs = LXPModel.Batch.objects.all()
        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'lxpapp/404page.html')