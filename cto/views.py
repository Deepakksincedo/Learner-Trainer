import os
import google_auth_oauthlib.flow
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from youtubemanager import PlaylistManager
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.conf import settings
from github import Github

@login_required    
def cto_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortCourse':0,
            'total_question':0,
            'total_learner':0,
            'final':'final'
            }
        return render(request,'cto/cto_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/passionateskill/cto_passionateskill.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                passionateskillForm=LXPFORM.PassionateSkillForm(request.POST)
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = LXPModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext)
                    if passionateskill:
                        messages.info(request, 'PassionateSkill Name Already Exist')
                        passionateskillForm=LXPFORM.PassionateSkillForm()
                        return render(request,'cto/passionateskill/cto_add_passionateskill.html',{'passionateskillForm':passionateskillForm})                  
                    else:
                        passionateskillForm.save()
                else:
                    print("form is invalid")
            passionateskillForm=LXPFORM.PassionateSkillForm()
            return render(request,'cto/passionateskill/cto_add_passionateskill.html',{'passionateskillForm':passionateskillForm})
            #return HttpResponseRedirect('/cto/cto-add-passionateskill')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_passionateskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            passionateskill = LXPModel.PassionateSkill.objects.get(id=pk)
            passionateskillForm=LXPFORM.PassionateSkillForm(request.POST,instance=passionateskill)
            if request.method=='POST':
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = LXPModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext).exclude(id=pk)
                    if passionateskill:
                        messages.info(request, 'PassionateSkill Name Already Exist')
                        return render(request,'cto/passionateskill/cto_update_passionateskill.html',{'passionateskillForm':passionateskillForm})
                    else:
                        passionateskillForm.save()
                        passionateskills = LXPModel.PassionateSkill.objects.all()
                        return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
            return render(request,'cto/passionateskill/cto_update_passionateskill.html',{'passionateskillForm':passionateskillForm,'sub':passionateskill.passionateskill_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            passionateskills = LXPModel.PassionateSkill.objects.all()
            return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_passionateskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            passionateskill=LXPModel.PassionateSkill.objects.get(id=pk)
            passionateskill.delete()
            return HttpResponseRedirect('/cto/passionateskill/cto-view-passionateskill')
        passionateskills = LXPModel.PassionateSkill.objects.all()
        return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/knownskill/cto_knownskill.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                knownskillForm=LXPFORM.KnownSkillForm(request.POST)
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = LXPModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext)
                    if knownskill:
                        messages.info(request, 'KnownSkill Name Already Exist')
                        knownskillForm=LXPFORM.KnownSkillForm()
                        return render(request,'cto/knownskill/cto_add_knownskill.html',{'knownskillForm':knownskillForm})                  
                    else:
                        knownskillForm.save()
                else:
                    print("form is invalid")
            knownskillForm=LXPFORM.KnownSkillForm()
            return render(request,'cto/knownskill/cto_add_knownskill.html',{'knownskillForm':knownskillForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_knownskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            knownskill = LXPModel.KnownSkill.objects.get(id=pk)
            knownskillForm=LXPFORM.KnownSkillForm(request.POST,instance=knownskill)
            if request.method=='POST':
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = LXPModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext).exclude(id=pk)
                    if knownskill:
                        messages.info(request, 'KnownSkill Name Already Exist')
                        return render(request,'cto/knownskill/cto_update_knownskill.html',{'knownskillForm':knownskillForm})
                    else:
                        knownskillForm.save()
                        knownskills = LXPModel.KnownSkill.objects.all()
                        return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
            return render(request,'cto/knownskill/cto_update_knownskill.html',{'knownskillForm':knownskillForm,'sub':knownskill.knownskill_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            knownskills = LXPModel.KnownSkill.objects.all()
            return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_knownskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            knownskill=LXPModel.KnownSkill.objects.get(id=pk)
            knownskill.delete()
            return HttpResponseRedirect('/cto/knownskill/cto-view-knownskill')
        knownskills = LXPModel.KnownSkill.objects.all()
        return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_mainhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.MainHeadForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Main Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('mainhead_name')
                    mainhead = LXPModel.MainHead.objects.all().filter(mainhead_name__iexact = name)
                    if mainhead:
                        messages.info(request, 'Main Head Name Already Exist')
                        return redirect(reverse('cto-add-mainhead'))
                    try:
                        mainhead = LXPModel.MainHead.objects.create(
                                                    mainhead_name = name)
                        mainhead.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-mainhead'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/mainhead/add_edit_mainhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_mainhead_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.MainHead, id=pk)
            form = LXPFORM.MainHeadForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'mainhead_id': pk,
                'page_title': 'Edit Main Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('mainhead_name')
                    mainhead = LXPModel.MainHead.objects.all().filter(mainhead_name__iexact = name).exclude(id=pk)
                    if mainhead:
                        messages.info(request, 'Main Head Name Already Exist')
                        return redirect(reverse('cto-update-mainhead', args=[pk]))
                    try:
                        mainhead = LXPModel.MainHead.objects.get(id=pk)
                        mainhead.mainhead_name = name
                        mainhead.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-update-mainhead', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/mainhead/add_edit_mainhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_mainhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            mainheads = LXPModel.MainHead.objects.all()
            return render(request,'cto/mainhead/cto_view_mainhead.html',{'mainheads':mainheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_mainhead_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            mainhead=LXPModel.MainHead.objects.get(id=pk)
            mainhead.delete()
            return HttpResponseRedirect('/cto/mainhead/cto-view-mainhead')
        mainheads = LXPModel.MainHead.objects.all()
        return render(request,'cto/mainhead/cto_view_mainhead.html',{'mainheads':mainheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_subhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.SubHeadForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Sub Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subhead_name')
                    mainid = form.cleaned_data.get('mainhead').pk
                    subhead = LXPModel.SubHead.objects.all().filter(subhead_name__iexact = name)
                    if subhead:
                        messages.info(request, 'Sub Head Name Already Exist')
                        return redirect(reverse('cto-add-subhead'))
                    try:
                        subhead = LXPModel.SubHead.objects.create(mainhead_id =mainid,
                                                    subhead_name = name)
                        subhead.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-subhead'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subhead/add_edit_subhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_subhead_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.SubHead, id=pk)
            form = LXPFORM.SubHeadForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'subhead_id': pk,
                'page_title': 'Edit Sub Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subhead_name')
                    mainid = form.cleaned_data.get('mainhead').pk
                    subhead = LXPModel.SubHead.objects.all().filter(subhead_name__iexact = name).exclude(id=pk)
                    if subhead:
                        messages.info(request, 'Sub Head Name Already Exist')
                        return redirect(reverse('cto-update-subhead', args=[pk]))
                    try:
                        subhead = LXPModel.SubHead.objects.get(id=pk)
                        subhead.mainhead_id = mainid
                        subhead.subhead_name = name
                        subhead.save()
                        messages.success(request, "Successfully Updated")
                        subheads = LXPModel.SubHead.objects.all()
                        return render(request,'cto/subhead/cto_view_subhead.html',{'subheads':subheads})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subhead/add_edit_subhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_subhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subheads = LXPModel.SubHead.objects.all()
            return render(request,'cto/subhead/cto_view_subhead.html',{'subheads':subheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_subhead_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subhead=LXPModel.SubHead.objects.get(id=pk)
            subhead.delete()
            subheads = LXPModel.SubHead.objects.all()
            return render(request,'cto/subhead/cto_view_subhead.html',{'subheads':subheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.SubjectForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Subject'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subject_name')
                    subject = LXPModel.Subject.objects.all().filter(subject_name__iexact = name)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return redirect(reverse('cto-add-subject'))
                    try:
                        subject = LXPModel.Subject.objects.create(
                                                    subject_name = name)
                        subject.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-subject'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subject/add_edit_subject.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_subject_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Subject, id=pk)
            form = LXPFORM.SubjectForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'subject_id': pk,
                'page_title': 'Edit Subject'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subject_name')
                    subject = LXPModel.Subject.objects.all().filter(subject_name__iexact = name).exclude(id=pk)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return redirect(reverse('cto-update-subject', args=[pk]))
                    try:
                        subject = LXPModel.Subject.objects.get(id=pk)
                        subject.subject_name = name
                        subject.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-update-subject', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subject/add_edit_subject.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = LXPModel.Subject.objects.all()
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=LXPModel.Subject.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/subject/cto-view-subject')
        subjects = LXPModel.Subject.objects.all()
        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_subject_details_csv_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                    file=request.FILES["select_file"]
                    csv_file = request.FILES["select_file"]
                    file_data = csv_file.read().decode("utf-8")		
                    lines = file_data.split("\n")
                    oldsub =''
                    oldchap=''
                    subid =0
                    chapid=0
                    no = 0
                    for line in lines:						
                        no = no + 1
                        if no > 1:
                            fields = line.split(",")
                            if fields[0] != oldsub:
                                oldsub = fields[0]
                                sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                                if not sub:
                                    sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                                    sub.save()
                                    subid=sub.id
                                else:
                                    for x in sub:
                                        subid=x.id  
                            if fields[1] != oldchap:
                                oldchap = fields[1] 
                                chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,subject_id=subid)
                                if not chap:
                                    chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,subject_id=subid)
                                    chap.save()
            return render(request,'cto/subject/cto_upload_subject_details_csv.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.ChapterForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Chapter'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('chapter_name')
                    subject = form.cleaned_data.get('subject').pk
                    chapter = LXPModel.Chapter.objects.all().filter(chapter_name__iexact = name)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return redirect(reverse('cto-add-chapter'))
                    try:
                        chapter = LXPModel.Chapter.objects.create(
                                                    chapter_name = name,
                                                    subject_id = subject)
                        chapter.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-chapter'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/chapter/add_edit_chapter.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_chapter_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Chapter, id=pk)
            form = LXPFORM.ChapterForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'chapter_id': pk,
                'page_title': 'Edit Chapter'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('chapter_name')
                    subject = form.cleaned_data.get('subject').pk
                    chapter = LXPModel.Chapter.objects.all().filter(chapter_name__iexact = name).exclude(id=pk)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return redirect(reverse('cto-update-chapter', args=[pk]))
                    try:
                        chapter = LXPModel.Chapter.objects.get(id=pk)
                        chapter.chapter_name = name
                        chapter.subject_id = subject
                        chapter.save()
                        messages.success(request, "Successfully Updated")
                        chapters = LXPModel.Chapter.objects.all()
                        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':chapters})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/chapter/add_edit_chapter.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_view_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Chapter.objects.all()
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_chapter_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            chapter=LXPModel.Chapter.objects.get(id=pk)
            chapter.delete()
            chapters = LXPModel.Chapter.objects.all()
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':chapters})
    except:
        return render(request,'lxpapp/404page.html')
    return render(request,'lxpapp/404page.html')
    

@login_required
def cto_add_module_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.ModuleForm(request.POST or None)
            clist = LXPModel.Subject.objects.raw('SELECT  Distinct  lxpapp_subject.id as id,  lxpapp_chapter.id as chapter_id, lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name  FROM  lxpapp_chapter  INNER JOIN lxpapp_subject ON (lxpapp_chapter.subject_id = lxpapp_subject.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name')
            sub = ''
            oldsub = ''
            js = '[{' 
            a = 1
            for x in clist:
                sub = x.subject_name
                if sub != oldsub:
                    if a != 1:
                        js = js[:len(js)-1]
                        js += ']},{'    
                    oldsub = sub
                    a = 2
                    js += 'id: "s___' + str(x.id) + '", text: "' + str(sub).replace('\r','') + '", expanded: false, items: ['
                
                js += ' { id: "c___' + str(x.chapter_id) + '", text: "' + str(x.chapter_name).replace('\r','') + '" },'
            js = js[:len(js)-1]
            js += ']}]' 
            bchapter = []

            context = {
                'form': form,
                'js': js,
                'page_title': 'Add Module',
                'chapterlistbyid' : bchapter
            }
            if request.method == 'POST':
                name = request.POST.get('module_name')
                module = LXPModel.Module.objects.all().filter(module_name__iexact = name)
                if module:
                    messages.info(request, 'Module Name Already Exist')
                    return redirect(reverse('cto-add-module'))
                try:
                    mainhead = request.POST.get('mainhead')
                    subhead = request.POST.get('subhead')
                    description = request.POST.get('description')
                    whatlearn = request.POST.get('whatlearn')
                    includes = request.POST.get('includes')
                    themecolor = request.POST.get('themecolor')
                    tags = request.POST.get('tag-output')
                    tags = str(tags).replace('<span class="close">x</span>','')
                    if ',' not in tags:
                        tags = tags + '<span class="close">x</span>'
                    image = request.POST.get ('image')
                    banner = request.POST.get ('banner')
                    price = request.POST.get ('price')
                    chapterlist = request.POST.get ('chapterlist')
                    module = LXPModel.Module.objects.create(
                                                module_name = name,
                                                mainhead_id = mainhead,
                                                subhead_id = subhead,
                                                description = description,
                                                whatlearn = whatlearn,
                                                themecolor = themecolor,
                                                includes = includes,
                                                image = image,
                                                banner = banner,
                                                price = price,
                                                tags = tags)
                    module.save()
                    fields = chapterlist.split(",")
                    for x in fields:
                        if x[0:4] != "s___":
                           ch = LXPModel.ModuleChapter.objects.create(
                                    module_id = module.id,
                                    chapter_id = x[4:])
                           ch.save()
                    messages.success(request, "Successfully Updated")
                    return redirect(reverse('cto-add-module'))
                except Exception as e:
                    messages.error(request, "Could Not Add " + str(e))
            return render(request, 'cto/module/add_edit_module.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_update_module_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            module_name = ''
            description = ''
            whatlearn = ''
            includes = ''
            image = ''
            price = ''
            tags = ''
            banner = ''
            instance = get_object_or_404(LXPModel.Module, id=pk)
            modbyid = LXPModel.Module.objects.all().filter(id=pk)
            

            for x in modbyid:
                module_name = x.module_name
                description = x.description
                whatlearn = x.whatlearn
                includes = x.includes
                image = x.image
                price = x.price
                tags = x.tags
                banner = x.banner
            tags = tags.replace(', ','<span class="close">x</span>, ')
            tags += '<span class="close">x</span>'
            form = LXPFORM.ModuleForm(request.POST or None, instance=instance)
            clist = LXPModel.Subject.objects.raw('SELECT    lxpapp_subject.id as id,  lxpapp_chapter.id as chapter_id, lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name  FROM  lxpapp_chapter  INNER JOIN lxpapp_subject ON (lxpapp_chapter.subject_id = lxpapp_subject.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name')
            chapbyid= list(LXPModel.ModuleChapter.objects.raw('SELECT 1 as id,  lxpapp_chapter.chapter_name FROM  lxpapp_modulechapter  INNER JOIN lxpapp_chapter ON (lxpapp_modulechapter.chapter_id = lxpapp_chapter.id)  WHERE lxpapp_modulechapter.module_id = ' + str(pk)))

            bchapter = []
            for c in chapbyid:
                btrnr={}
                btrnr["name"]=str(c.chapter_name).replace('\r','')
                bchapter.append(btrnr)
            sub = ''
            oldsub = ''
            js = '[{' 
            a = 1
            for x in clist:
                sub = x.subject_name
                if sub != oldsub:
                    if a != 1:
                        js = js[:len(js)-1]
                        js += ']},{'    
                    oldsub = sub
                    a = 2
                    js += 'id: "s___' + str(x.id) + '", text: "' + str(sub).replace('\r','') + '", expanded: false, items: ['
                
                js += ' { id: "c___' + str(x.chapter_id) + '", text: "' + str(x.chapter_name).replace('\r','') + '" },'
            js = js[:len(js)-1]
            js += ']}]' 
            context = {
                'form': form,
                'js': js,
                'module_id': pk,
                'page_title': 'Edit Module',
                'chapterlistbyid' : bchapter,
                'mod_name' : module_name,
                'description' : description,
                'whatlearn' : whatlearn,
                'includes' : includes,
                'image' : image,
                'banner' : banner,
                'price' : price,
                'tags' : tags
            }
            if request.method == 'POST':
                name = request.POST.get('module_name')
                module = LXPModel.Module.objects.all().filter(module_name__iexact = name).exclude(id=pk)
                if module:
                    messages.info(request, 'Module Name Already Exist')
                    return redirect(reverse('cto-update-module', args=[pk]))
                try:
                    module = LXPModel.Module.objects.get(id=pk)
                    mainhead = request.POST.get('mainhead')
                    subhead = request.POST.get('subhead')
                    description = request.POST.get('description')
                    whatlearn = request.POST.get('whatlearn')
                    includes = request.POST.get('includes')
                    themecolor = request.POST.get('themecolor')
                    tags = request.POST.get('tag-output')
                    tags = str(tags).replace('<span class="close">x</span>','')
                    if ',' not in tags:
                        tags = tags + '<span class="close">x</span>'
                    image = request.POST.get ('image')
                    banner = request.POST.get ('banner')
                    price = request.POST.get ('price')
                    chapterlist = request.POST.get ('chapterlist')
                    module.module_name = name
                    module.mainhead_id = mainhead
                    module.subhead_id = subhead
                    module.description = description
                    module.whatlearn = whatlearn
                    module.themecolor = themecolor
                    module.includes = includes
                    module.image = image
                    module.banner = banner
                    module.price = price
                    module.tags = tags
                    module.save()
                    c_list = LXPModel.Module.objects.raw('SELECT    lxpapp_module.id,  lxpapp_module.module_name,  lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name,  COunt(lxpapp_material.topic) AS lessons FROM  lxpapp_module  LEFT OUTER JOIN lxpapp_mainhead ON (lxpapp_module.mainhead_id = lxpapp_mainhead.id)  LEFT OUTER JOIN lxpapp_subhead ON (lxpapp_module.subhead_id = lxpapp_subhead.id)  LEFT OUTER JOIN lxpapp_modulechapter ON (lxpapp_module.id = lxpapp_modulechapter.module_id)  LEFT OUTER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id) GROUP BY  lxpapp_module.id,  lxpapp_module.module_name,  lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name')
                    return render(request,'cto/module/cto_view_module.html',{'modules':c_list})
                except Exception as e:
                    messages.error(request, "Could Not Add " + str(e))
            return render(request, 'cto/module/add_edit_module.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_view_module_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Module.objects.raw('SELECT    lxpapp_module.id,  lxpapp_module.module_name,  lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name,  COunt(lxpapp_material.topic) AS lessons FROM  lxpapp_module  LEFT OUTER JOIN lxpapp_mainhead ON (lxpapp_module.mainhead_id = lxpapp_mainhead.id)  LEFT OUTER JOIN lxpapp_subhead ON (lxpapp_module.subhead_id = lxpapp_subhead.id)  LEFT OUTER JOIN lxpapp_modulechapter ON (lxpapp_module.id = lxpapp_modulechapter.module_id)  LEFT OUTER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id) GROUP BY  lxpapp_module.id,  lxpapp_module.module_name,  lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name')
            return render(request,'cto/module/cto_view_module.html',{'modules':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_module_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            module=LXPModel.Module.objects.get(id=pk)
            module.delete()
        c_list = LXPModel.Module.objects.raw('SELECT    lxpapp_module.id,  lxpapp_module.module_name,  lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name,  COunt(lxpapp_material.topic) AS lessons FROM  lxpapp_module  LEFT OUTER JOIN lxpapp_mainhead ON (lxpapp_module.mainhead_id = lxpapp_mainhead.id)  LEFT OUTER JOIN lxpapp_subhead ON (lxpapp_module.subhead_id = lxpapp_subhead.id)  LEFT OUTER JOIN lxpapp_modulechapter ON (lxpapp_module.id = lxpapp_modulechapter.module_id)  LEFT OUTER JOIN lxpapp_material ON (lxpapp_modulechapter.chapter_id = lxpapp_material.chapter_id) GROUP BY  lxpapp_module.id,  lxpapp_module.module_name,  lxpapp_module.description,  lxpapp_module.whatlearn,  lxpapp_module.includes,  lxpapp_module.themecolor,  lxpapp_module.tags,  lxpapp_module.image,  lxpapp_module.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name')
        return render(request,'cto/module/cto_view_module.html',{'modules':c_list})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/topic/cto_topic.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.TopicForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Topic'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('topic_name')
                    chapter = form.cleaned_data.get('chapter').pk
                    topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return redirect(reverse('cto-add-topic'))
                    try:
                        topic = LXPModel.Topic.objects.create(
                                                    topic_name = name,
                                                    chapter_id = chapter)
                        topic.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-topic'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/topic/add_edit_topic.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_update_topic_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Topic, id=pk)
            form = LXPFORM.TopicForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'topic_id': pk,
                'page_title': 'Edit Topic'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('topic_name')
                    chapter = form.cleaned_data.get('chapter').pk
                    topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name).exclude(id=pk)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return redirect(reverse('cto-update-topic', args=[pk]))
                    try:
                        topic = LXPModel.Topic.objects.get(id=pk)
                        topic.topic_name = name
                        topic.chapter_id = chapter
                        topic.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-update-topic', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/topic/add_edit_topic.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_view_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Topic.objects.all()
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_topic_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            topic=LXPModel.Topic.objects.get(id=pk)
            topic.delete()
            return HttpResponseRedirect('/cto/topic/cto-view-topic')
        topics = LXPModel.Topic.objects.all()
        return render(request,'cto/topic/cto_view_topic.html',{'topics':topics})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/course/cto_course.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                courseForm=LXPFORM.CourseForm(request.POST)
                coursetext = request.POST.get('course_name')
                course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                    courseForm=LXPFORM.CourseForm()
                    return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm})                  
                else:
                    course_name = request.POST.get('course_name')
                    course = LXPModel.Course.objects.create(course_name = course_name)
                    course.save()
                    import json
                    json_data = json.loads(request.POST.get('myvalue'))
                    for cx in json_data:
                        a=json_data[cx]['subject']
                        b=json_data[cx]['module']
                        c=json_data[cx]['chapter']
                        d=json_data[cx]['topic']
                        x = a.split("-")
                        subid = x[0]
                        x = b.split("-")
                        modid = x[0]
                        x = c.split("-")
                        chapid = x[0]
                        x = d.split("-")
                        topid = x[0]
                        coursedet = LXPModel.CourseDetails.objects.create(
                                course_id = course.id,
                                subject_id = subid,
                                module_id = modid,
                                chapter_id = chapid,
                                topic_id = topid
                                )
                        coursedet.save()
            courseForm=LXPFORM.CourseForm()
            return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_course_view(request,coursename,pk):
    try:
        if str(request.session['utype']) == 'cto':
            course = LXPModel.Course.objects.get(id=pk)
            if request.method=='POST':
                courseForm=LXPFORM.CourseForm(request.POST,instance=course)
                coursetext = courseForm.data["course_name"]
                course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext).exclude(id=pk)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                    return render(request,'cto/course/cto_update_course.html',{'courseForm':courseForm})
                else:
                    courseForm.save()
                    coursedet = LXPModel.CourseDetails.objects.all().filter(course_id=pk).delete()

                import json
                json_data = json.loads(request.POST.get('myvalue'))
                for cx in json_data:
                    a=json_data[cx]['subject']
                    b=json_data[cx]['module']
                    c=json_data[cx]['chapter']
                    d=json_data[cx]['topic']
                    x = a.split("-")
                    subid = x[0]
                    x = b.split("-")
                    modid = x[0]
                    x = c.split("-")
                    chapid = x[0]
                    x = d.split("-")
                    topid = x[0]
                    coursedet = LXPModel.CourseDetails.objects.create(
                            course_id = pk,
                            subject_id = subid,
                            module_id = modid,
                            chapter_id = chapid,
                            topic_id = topid
                            )
                    coursedet.save()
                courses = LXPModel.Course.objects.all()
                return render(request,'cto/course/cto_view_course.html',{'courses':courses})
            courseForm = LXPFORM.CourseForm()
            courses = LXPModel.CourseDetails.objects.raw("SELECT   1 AS id,  LXPAPP_SUBJECT.id || '-' || LXPAPP_SUBJECT.SUBJECT_NAME  AS SUBJECT_NAME,  LXPAPP_MODULE.id || '-' || LXPAPP_MODULE.MODULE_NAME  AS MODULE_NAME,  LXPAPP_CHAPTER.id || '-' || LXPAPP_CHAPTER.CHAPTER_NAME  AS CHAPTER_NAME,  LXPAPP_TOPIC.id || '-' || LXPAPP_TOPIC.TOPIC_NAME  AS TOPIC_NAME FROM  LXPAPP_COURSEDETAILS  INNER JOIN LXPAPP_COURSE ON (LXPAPP_COURSEDETAILS.COURSE_ID = LXPAPP_COURSE.ID)  INNER JOIN LXPAPP_SUBJECT ON (LXPAPP_COURSEDETAILS.SUBJECT_ID = LXPAPP_SUBJECT.ID)  INNER JOIN LXPAPP_MODULE ON (LXPAPP_COURSEDETAILS.MODULE_ID = LXPAPP_MODULE.ID)  INNER JOIN LXPAPP_CHAPTER ON (LXPAPP_COURSEDETAILS.CHAPTER_ID = LXPAPP_CHAPTER.ID)  INNER JOIN LXPAPP_TOPIC ON (LXPAPP_COURSEDETAILS.TOPIC_ID = LXPAPP_TOPIC.ID)    WHERE lxpapp_coursedetails.course_id = " + str(pk) + " ORDER BY  LXPAPP_SUBJECT.SUBJECT_NAME,  LXPAPP_MODULE.MODULE_NAME,  LXPAPP_CHAPTER.CHAPTER_NAME,  LXPAPP_TOPIC.TOPIC_NAME")

            qry ="SELECT   1 AS id,  LXPAPP_SUBJECT.id || '-' || LXPAPP_SUBJECT.SUBJECT_NAME  AS SUBJECT_NAME,  LXPAPP_MODULE.id || '-' || LXPAPP_MODULE.MODULE_NAME  AS MODULE_NAME,  LXPAPP_CHAPTER.id || '-' || LXPAPP_CHAPTER.CHAPTER_NAME  AS CHAPTER_NAME,  LXPAPP_TOPIC.id || '-' || LXPAPP_TOPIC.TOPIC_NAME  AS TOPIC_NAME FROM  LXPAPP_COURSEDETAILS  INNER JOIN LXPAPP_COURSE ON (LXPAPP_COURSEDETAILS.COURSE_ID = LXPAPP_COURSE.ID)  INNER JOIN LXPAPP_SUBJECT ON (LXPAPP_COURSEDETAILS.SUBJECT_ID = LXPAPP_SUBJECT.ID)  INNER JOIN LXPAPP_MODULE ON (LXPAPP_COURSEDETAILS.MODULE_ID = LXPAPP_MODULE.ID)  INNER JOIN LXPAPP_CHAPTER ON (LXPAPP_COURSEDETAILS.CHAPTER_ID = LXPAPP_CHAPTER.ID)  INNER JOIN LXPAPP_TOPIC ON (LXPAPP_COURSEDETAILS.TOPIC_ID = LXPAPP_TOPIC.ID)    WHERE lxpapp_coursedetails.course_id = " + str(pk) + " ORDER BY  LXPAPP_SUBJECT.SUBJECT_NAME,  LXPAPP_MODULE.MODULE_NAME,  LXPAPP_CHAPTER.CHAPTER_NAME,  LXPAPP_TOPIC.TOPIC_NAME"

            import json
            from django.core.serializers import serialize
            
           # Convert the dictionary to a JSON object
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute(qry)
            rows = cursor.fetchall()
            result = []
            keys = ('id','subject_name', 'module_name', 'chapter_name', 'topic_name',)
            for row in rows:
                result.append(dict(zip(keys,row)))
            json_data = json.dumps(result)
            json_data = json_data.replace('\\r','')

            return render(request,'cto/course/cto_update_course.html',{'courses':json_data,'courseForm':courseForm,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            courses = LXPModel.Course.objects.all()
            return render(request,'cto/course/cto_view_course.html',{'courses':courses})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_course_details_view(request,coursename,pk):
    try:
        if str(request.session['utype']) == 'cto':
            courses = LXPModel.Course.objects.raw('SELECT 1 as id,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) WHERE lxpapp_coursedetails.course_id = ' + str(pk) + ' ORDER BY lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            return render(request,'cto/course/cto_view_course_details.html',{'courses':courses,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_course_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            coursedet=LXPModel.CourseDetails.objects.filter(course_id=pk).delete()
            course=LXPModel.Course.objects.filter(id=pk).delete()
        courses = LXPModel.Course.objects.all()
        return render(request,'cto/course/cto_view_course.html',{'courses':courses})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_course_details_csv_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                coursetext=request.POST.get('course_name')
                course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                elif coursetext == '':
                    messages.info(request, 'Please enter Course Name')
                elif request.POST.get('select_file') == '':
                    messages.info(request, 'Please select CSV file for upload')
                else:
                    course = LXPModel.Course.objects.create(course_name = coursetext)
                    course.save()     
                    csv_file = request.FILES["select_file"]
                    file_data = csv_file.read().decode("utf-8")		
                    lines = file_data.split("\n")
                    oldsub =''
                    oldmod=''
                    oldchap=''
                    oldtop=''
                    subid =0
                    modid=0
                    chapid=0
                    topid=0
                    no = 0
                    for line in lines:						
                        no = no + 1
                        if no > 1:
                            fields = line.split(",")
                            if str(fields[0]).replace('///',',') != oldsub:
                                oldsub = str(fields[0]).replace('///',',')
                                sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                                if not sub:
                                    sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                                    sub.save()
                                    subid=sub.id
                                else:
                                    for x in sub:
                                        subid=x.id  
                            if str(fields[1]).replace('///',',') != oldmod:
                                oldmod = str(fields[1]).replace('///',',')
                                mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                                if not mod:
                                    mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                                    mod.save()
                                    modid=mod.id
                                else:
                                    for x in mod:
                                        modid=x.id 
                            if str(fields[2]).replace('///',',') != oldchap:
                                oldchap = str(fields[2]).replace('///',',')
                                chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                                if not chap:
                                    chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                                    chap.save()
                                    chapid=chap.id
                                else:
                                    for x in chap:
                                        chapid=x.id 
                            if str(fields[3]).replace('///',',') != oldtop:
                                oldtop = str(fields[3]).replace('///',',') 
                                top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                                if not top:
                                    top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                                    top.save()
                                    topid1=top.id 
                                else:
                                    for x in top:
                                        topid1=x.id 
                            coursedet = LXPModel.CourseDetails.objects.create(
                                        course_id =course.id,
                                        subject_id=subid,
                                        module_id=modid,
                                        chapter_id=chapid,
                                        topic_id=topid1
                                        )
                            coursedet.save()
            return render(request,'cto/course/cto_upload_course_details_csv.html')
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_courseset_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/courseset/cto_courseset.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_courseset_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                coursesetForm=LXPFORM.CourseSetForm(request.POST)
                coursesettext = request.POST.get('courseset_name')
                courseset = LXPModel.CourseSet.objects.all().filter(courseset_name__iexact = coursesettext)
                if courseset:
                    messages.info(request, 'CourseSet Name Already Exist')
                    coursesetForm=LXPFORM.CourseSetForm()
                    return render(request,'cto/courseset/cto_add_courseset.html',{'coursesetForm':coursesetForm})                  
                else:
                    courseset_name = request.POST.get('courseset_name')
                    courseset = LXPModel.CourseSet.objects.create(courseset_name = courseset_name)
                    courseset.save()
                    import json
                    json_data = json.loads(request.POST.get('myvalue'))
                    for cx in json_data:
                        a=json_data[cx]['subject']
                        b=json_data[cx]['module']
                        c=json_data[cx]['chapter']
                        d=json_data[cx]['topic']
                        x = a.split("-")
                        subid = x[0]
                        x = b.split("-")
                        modid = x[0]
                        x = c.split("-")
                        chapid = x[0]
                        x = d.split("-")
                        topid = x[0]
                        coursesetdet = LXPModel.CourseSetDetails.objects.create(
                                courseset_id = courseset.id,
                                subject_id = subid,
                                module_id = modid,
                                chapter_id = chapid,
                                topic_id = topid
                                )
                        coursesetdet.save()
            coursesetForm=LXPFORM.CourseSetForm()
            return render(request,'cto/courseset/cto_add_courseset.html',{'coursesetForm':coursesetForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_courseset_view(request,coursesetname,pk):
    try:
        if str(request.session['utype']) == 'cto':
            courseset = LXPModel.CourseSet.objects.get(id=pk)
            if request.method=='POST':
                coursesetForm=LXPFORM.CourseSetForm(request.POST,instance=courseset)
                coursesettext = coursesetForm.data["courseset_name"]
                courseset = LXPModel.CourseSet.objects.all().filter(courseset_name__iexact = coursesettext).exclude(id=pk)
                if courseset:
                    messages.info(request, 'CourseSet Name Already Exist')
                    return render(request,'cto/courseset/cto_update_courseset.html',{'coursesetForm':coursesetForm})
                else:
                    coursesetForm.save()
                    coursesetdet = LXPModel.CourseSetDetails.objects.all().filter(courseset_id=pk).delete()

                import json
                json_data = json.loads(request.POST.get('myvalue'))
                for cx in json_data:
                    a=json_data[cx]['subject']
                    b=json_data[cx]['module']
                    c=json_data[cx]['chapter']
                    d=json_data[cx]['topic']
                    x = a.split("-")
                    subid = x[0]
                    x = b.split("-")
                    modid = x[0]
                    x = c.split("-")
                    chapid = x[0]
                    x = d.split("-")
                    topid = x[0]
                    coursesetdet = LXPModel.CourseSetDetails.objects.create(
                            courseset_id = pk,
                            subject_id = subid,
                            module_id = modid,
                            chapter_id = chapid,
                            topic_id = topid
                            )
                    coursesetdet.save()
                coursesets = LXPModel.CourseSet.objects.all()
                return render(request,'cto/courseset/cto_view_courseset.html',{'coursesets':coursesets})
            coursesetForm = LXPFORM.CourseSetForm()
            coursesets = LXPModel.CourseSetDetails.objects.raw("SELECT   1 AS id,  LXPAPP_SUBJECT.id || '-' || LXPAPP_SUBJECT.SUBJECT_NAME  AS SUBJECT_NAME,  LXPAPP_MODULE.id || '-' || LXPAPP_MODULE.MODULE_NAME  AS MODULE_NAME,  LXPAPP_CHAPTER.id || '-' || LXPAPP_CHAPTER.CHAPTER_NAME  AS CHAPTER_NAME,  LXPAPP_TOPIC.id || '-' || LXPAPP_TOPIC.TOPIC_NAME  AS TOPIC_NAME FROM  LXPAPP_COURSEDETAILS  INNER JOIN LXPAPP_COURSE ON (LXPAPP_COURSEDETAILS.COURSE_ID = LXPAPP_COURSE.ID)  INNER JOIN LXPAPP_SUBJECT ON (LXPAPP_COURSEDETAILS.SUBJECT_ID = LXPAPP_SUBJECT.ID)  INNER JOIN LXPAPP_MODULE ON (LXPAPP_COURSEDETAILS.MODULE_ID = LXPAPP_MODULE.ID)  INNER JOIN LXPAPP_CHAPTER ON (LXPAPP_COURSEDETAILS.CHAPTER_ID = LXPAPP_CHAPTER.ID)  INNER JOIN LXPAPP_TOPIC ON (LXPAPP_COURSEDETAILS.TOPIC_ID = LXPAPP_TOPIC.ID)    WHERE lxpapp_coursesetdetails.courseset_id = " + str(pk) + " ORDER BY  LXPAPP_SUBJECT.SUBJECT_NAME,  LXPAPP_MODULE.MODULE_NAME,  LXPAPP_CHAPTER.CHAPTER_NAME,  LXPAPP_TOPIC.TOPIC_NAME")

            qry ="SELECT   1 AS id,  LXPAPP_SUBJECT.id || '-' || LXPAPP_SUBJECT.SUBJECT_NAME  AS SUBJECT_NAME,  LXPAPP_MODULE.id || '-' || LXPAPP_MODULE.MODULE_NAME  AS MODULE_NAME,  LXPAPP_CHAPTER.id || '-' || LXPAPP_CHAPTER.CHAPTER_NAME  AS CHAPTER_NAME,  LXPAPP_TOPIC.id || '-' || LXPAPP_TOPIC.TOPIC_NAME  AS TOPIC_NAME FROM  LXPAPP_COURSEDETAILS  INNER JOIN LXPAPP_COURSE ON (LXPAPP_COURSEDETAILS.COURSE_ID = LXPAPP_COURSE.ID)  INNER JOIN LXPAPP_SUBJECT ON (LXPAPP_COURSEDETAILS.SUBJECT_ID = LXPAPP_SUBJECT.ID)  INNER JOIN LXPAPP_MODULE ON (LXPAPP_COURSEDETAILS.MODULE_ID = LXPAPP_MODULE.ID)  INNER JOIN LXPAPP_CHAPTER ON (LXPAPP_COURSEDETAILS.CHAPTER_ID = LXPAPP_CHAPTER.ID)  INNER JOIN LXPAPP_TOPIC ON (LXPAPP_COURSEDETAILS.TOPIC_ID = LXPAPP_TOPIC.ID)    WHERE lxpapp_coursesetdetails.courseset_id = " + str(pk) + " ORDER BY  LXPAPP_SUBJECT.SUBJECT_NAME,  LXPAPP_MODULE.MODULE_NAME,  LXPAPP_CHAPTER.CHAPTER_NAME,  LXPAPP_TOPIC.TOPIC_NAME"

            import json
            from django.core.serializers import serialize
            
           # Convert the dictionary to a JSON object
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute(qry)
            rows = cursor.fetchall()
            result = []
            keys = ('id','subject_name', 'module_name', 'chapter_name', 'topic_name',)
            for row in rows:
                result.append(dict(zip(keys,row)))
            json_data = json.dumps(result)
            json_data = json_data.replace('\\r','')

            return render(request,'cto/courseset/cto_update_courseset.html',{'coursesets':json_data,'coursesetForm':coursesetForm,'coursesetname':coursesetname})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_courseset_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            coursesets = LXPModel.CourseSet.objects.all()
            return render(request,'cto/courseset/cto_view_courseset.html',{'coursesets':coursesets})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_courseset_details_view(request,coursesetname,pk):
    try:
        if str(request.session['utype']) == 'cto':
            coursesets = LXPModel.CourseSet.objects.raw('SELECT 1 as id,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name FROM  lxpapp_coursesetdetails  INNER JOIN lxpapp_courseset ON (lxpapp_coursesetdetails.courseset_id = lxpapp_courseset.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursesetdetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursesetdetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursesetdetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursesetdetails.topic_id = lxpapp_topic.id) WHERE lxpapp_coursesetdetails.courseset_id = ' + str(pk) + ' ORDER BY lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            return render(request,'cto/courseset/cto_view_courseset_details.html',{'coursesets':coursesets,'coursesetname':coursesetname})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_courseset_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            coursesetdet=LXPModel.CourseSetDetails.objects.filter(courseset_id=pk).delete()
            courseset=LXPModel.CourseSet.objects.filter(id=pk).delete()
        coursesets = LXPModel.CourseSet.objects.all()
        return render(request,'cto/courseset/cto_view_courseset.html',{'coursesets':coursesets})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_courseset_details_csv_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                if request.POST.get('select_file') == '':
                    messages.info(request, 'Please select CSV file for upload')
                else:
                    csv_file = request.FILES["select_file"]
                    file_data = csv_file.read().decode("utf-8")		
                    lines = file_data.split("\n")
                    oldcourse =''
                    oldsub =''
                    oldmod=''
                    oldchap=''
                    oldtop=''
                    corsetid =0
                    subid =0
                    modid=0
                    chapid=0
                    topid=0
                    tochk=''
                    no = 0
                    for line in lines:						
                        no = no + 1
                        if no > 1:
                            fields = line.split(",")
                            tochk = str(fields[4]).replace('///',',').replace('\r','')
                            if tochk != oldcourse:
                                oldcourse = tochk
                                cor = LXPModel.CourseSet.objects.all().filter(courseset_name__exact = oldcourse )
                                if not cor:
                                    cor = LXPModel.CourseSet.objects.create(courseset_name = oldcourse )
                                    cor.save()
                                    corsetid=cor.id
                                else:
                                    for x in cor:
                                        corsetid=x.id
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
                            if tochk != oldmod:
                                oldmod = tochk
                                mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                                if not mod:
                                    mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                                    mod.save()
                                    modid=mod.id
                                else:
                                    for x in mod:
                                        modid=x.id 
                            tochk = str(fields[2]).replace('///',',').replace('\r','')
                            if tochk != oldchap:
                                oldchap = tochk
                                chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                                if not chap:
                                    chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                                    chap.save()
                                    chapid=chap.id
                                else:
                                    for x in chap:
                                        chapid=x.id 
                            tochk = str(fields[3]).replace('///',',').replace('\r','')
                            if tochk != oldtop:
                                oldtop = tochk
                                top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                                if not top:
                                    top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                                    top.save()
                                    topid1=top.id 
                                else:
                                    for x in top:
                                        topid1=x.id 
                            coursesetdet = LXPModel.CourseSetDetails.objects.create(
                                        courseset_id =corsetid,
                                        subject_id=subid,
                                        module_id=modid,
                                        chapter_id=chapid,
                                        topic_id=topid1
                                        )
                            coursesetdet.save()
            return render(request,'cto/courseset/cto_upload_courseset_details_csv.html')
    except:
        return render(request,'lxpapp/404page.html')

def load_subheads(request):
    try:
        mainhead_id = request.GET.get('mainhead')
        subheads = LXPModel.SubHead.objects.filter(mainhead_id=mainhead_id).order_by('subhead_name')
        context = {'subheads': subheads}
        return render(request, 'hr/subhead_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

def load_modules(request):
    try:
        subject_id = request.GET.get('subject')
        modules = LXPModel.Module.objects.filter(subject_id=subject_id).order_by('module_name')
        context = {'modules': modules}
        return render(request, 'hr/module_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
def load_chapters(request):
    try:
        subject_id = request.GET.get('subject')
        chapters = LXPModel.Chapter.objects.filter(subject_id=subject_id).order_by('chapter_name')
        context = {'chapters': chapters}
        return render(request, 'hr/chapter_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

def load_topics(request):
    try:
        chapter_id = request.GET.get('chapter')
        topics = LXPModel.Topic.objects.filter(chapter_id=chapter_id).order_by('topic_name')
        context = {'topics': topics}
        return render(request, 'hr/topic_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def getcredentials(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "GoogleCredV1.json"

    # Get credentials and create an API client
    flow = None
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server()
    credentials = flow.credentials
    return credentials

@login_required
def cto_sync_youtube_view(request):
    try:
        if str(request.session['utype']) == 'cto':
    #pllist = LXPModel.IncludePlaylist.objects.all().filter(playlist_id__in =LXPModel.Playlist.objects.all().order_by('name'))
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def cto_sync_youtube_start_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                pm = PlaylistManager()
                credentials = getcredentials(request)
                
                alllist = pm.initializePlaylist(credentials)
                plcount = 1
                maxcount = alllist.__len__()
                for PL_ID in alllist:
                        PL_NAME = ''#LXPModel.Playlist.objects.values('name').filter(playlist_id = PL_ID)
                        print(str(plcount) + ' ' + PL_NAME)
                        pm.getAllVideosForPlaylist(PL_ID,credentials,maxcount,plcount,PL_NAME)
                        plcount = plcount + 1
                        HttpResponse(loader.get_template('cto/youtube/cto_sync_youtube.html').render(
                            {
                                "plname": PL_NAME,
                                "maxcount": maxcount,
                                "plcount": plcount
                            }
                            ))
                dict={
                'total_learner':0,
                'total_trainer':0,
                'total_exam':0,
                'total_question':0,
                }
                return render(request,'cto/cto_dashboard.html',context=dict)
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})    
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_sync_youtube_byselected_playlist_start_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                if 'dblist' in request.POST:
                    pllist = LXPModel.Playlist.objects.all().order_by('name')
                    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
                elif 'cloudlist' in request.POST:
                    pm = PlaylistManager()
                    credentials = getcredentials(request)
                    pl =  pm.initializePlaylist(credentials)
                    pllist = LXPModel.Playlist.objects.all().order_by('name')
                    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
                elif 'startselected' in request.POST:
                    pm = PlaylistManager()
                    selectedlist = request.POST.getlist('playlist[]')
                    maxcount = selectedlist.__len__()
                    plcount = 1
                    credentials = getcredentials(request)
                    for PL_NAME in selectedlist:
                        print(str(plcount) + ' of ' + str(maxcount))
                        _id = PL_NAME 
                        playlist = LXPModel.Playlist.objects.values_list('playlist_id', flat=True).get(id=PL_NAME)
                        pm.getAllVideosForPlaylist(playlist,credentials,maxcount,plcount,_id)
                        plcount= plcount + 1
            dict={
            'total_learner':0,
            'total_trainer':0,
            'total_exam':0,
            'total_question':0,
            }
            return render(request,'cto/cto_dashboard.html',context=dict)
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def get_message_from_httperror(e):
    return e.error_details[0]['message']
######################################################################


@login_required
def cto_trainernotification_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/trainernotification/cto_trainernotification.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_trainernotification_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                trainernotificationForm=LXPFORM.TrainerNotificationForm(request.POST)
                if trainernotificationForm.is_valid(): 
                    trainernotificationtext = trainernotificationForm.cleaned_data["trainernotification_message"]
                    trainernotification = LXPModel.TrainerNotification.objects.all().filter(trainernotification_message__iexact = trainernotificationtext)
                    if trainernotification:
                        messages.info(request, 'TrainerNotification Name Already Exist')
                        trainernotificationForm=LXPFORM.TrainerNotificationForm()
                        return render(request,'cto/trainernotification/cto_add_trainernotification.html',{'trainernotificationForm':trainernotificationForm})                  
                    else:
                        trainernotification = LXPModel.TrainerNotification.objects.create(
                            trainer_id = trainernotificationForm.cleaned_data["trainerID"].user_id,
                            sender_id = request.user.id,
                            status = False,
                            trainernotification_message =trainernotificationtext
                        )
                        trainernotification.save()
                else:
                    print("form is invalid")
            trainernotificationForm=LXPFORM.TrainerNotificationForm()
            return render(request,'cto/trainernotification/cto_add_trainernotification.html',{'trainernotificationForm':trainernotificationForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_trainernotification_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            trainernotification = LXPModel.TrainerNotification.objects.get(id=pk)
            trainernotificationForm=LXPFORM.TrainerNotificationForm(request.POST,instance=trainernotification)
            if request.method=='POST':
                if trainernotificationForm.is_valid(): 
                    trainernotificationtext = trainernotificationForm.cleaned_data["trainernotification_message"]
                    trainernotification = LXPModel.TrainerNotification.objects.all().filter(trainernotification_message__iexact = trainernotificationtext).exclude(id=pk)
                    if trainernotification:
                        messages.info(request, 'TrainerNotification Name Already Exist')
                        return render(request,'cto/trainernotification/cto_update_trainernotification.html',{'trainernotificationForm':trainernotificationForm})
                    else:
                        trainernotificationForm.save()
                        trainernotifications = LXPModel.TrainerNotification.objects.all()
                        return render(request,'cto/trainernotification/cto_view_trainernotification.html',{'trainernotifications':trainernotifications})
            return render(request,'cto/trainernotification/cto_update_trainernotification.html',{'trainernotificationForm':trainernotificationForm,'sub':trainernotification.trainernotification_message})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_trainernotification_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            trainernotifications = LXPModel.TrainerNotification.objects.all()
            return render(request,'cto/trainernotification/cto_view_trainernotification.html',{'trainernotifications':trainernotifications})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_trainernotification_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            trainernotification=LXPModel.TrainerNotification.objects.get(id=pk)
            trainernotification.delete()
        trainernotifications = LXPModel.TrainerNotification.objects.all()
        return render(request,'cto/trainernotification/cto_view_trainernotification.html',{'trainernotifications':trainernotifications})
    except:
        return render(request,'lxpapp/404page.html')
    
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


@login_required
def cto_lxp_upload_doc_file_view(request):
    if request.method == 'POST' and request.FILES['file']:
        emails = request.POST.get('emails-output')
        emails = str(emails).replace('<span class="close">x</span>','')
        fields = emails.split(",")
        
        
        import googleapiclient.discovery
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        from social_django.models import UserSocialAuth
        from apiclient.discovery import build
        from apiclient.errors import HttpError
        from apiclient.http import MediaFileUpload
        from oauth2client.client import flow_from_clientsecrets
        import datetime
        import pytz
        CLIENT_SECRETS_FILE = "GoogleCredV1.json"
        YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        playlistname = request.POST.get('playlist')  # Get the video ID from the form
        playlist_id = LXPModel.Playlist.objects.only('playlist_id').get(name=playlistname).playlist_id
        video_file = request.FILES.get('video')
        title = request.POST.get('title')
        description = request.POST.get('description')
        channel_id = request.POST.get('channel_id')
        channel_name = request.POST.get('channel_name')

        # youtube = build('youtube', 'v3', developerKey='AIzaSyBRlrfvqZLCXUU8oc19PO4Zg2-hB2QMBrI')
        # flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        #                            scope=YOUTUBE_UPLOAD_SCOPE,
        #                            message="")

        # storage = CLIENT_SECRETS_FILE#os.path.abspath(os.path.join(os.path.dirname(__file__),
        #                             #CLIENT_SECRETS_FILE))
        
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
        flow.run_local_server()
        credentials = flow.credentials
        youtube = googleapiclient.discovery.build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
        # Save the video file to a temporary location
        video_path = os.path.join(settings.MEDIA_ROOT, 'temp_video.mp4')
        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        try:
            # Create a new video resource
            videos_insert_response = youtube.videos().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': title,
                        'description': description,
                    },
                    'status': {
                        'privacyStatus': 'private'  # Set video privacy as public
                    }
                },
                media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
            ).execute()

            video_id = videos_insert_response['id']
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            # Add the video to a playlist
            youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()

            # Optionally, you can delete the temporary video file
            os.remove(video_path)

        except Exception as e:
            # Handle API errors or display an error message
            error_message = str(e)
            return render(request,'lxpapp/404page.html')

        file = request.FILES['file']
        # Connect to the GitHub API
        access_token = settings.GITHUB_ACCESS_TOKEN
        github = Github(access_token)
        # Get the repository
        repo_owner = settings.GITHUB_REPO_OWNER
        repo_name = settings.GITHUB_REPO_NAME
        repo = github.get_repo(f'{repo_owner}/{repo_name}')
        # Create a new file in the repository
        new_file = repo.create_file(
            path=file.name,
            message='Upload file',
            content=file.read(),
            branch='main'  # Replace with your desired branch name
        )
        file_url = new_file['content'].download_url
        file_url = file_url.replace('raw.githubusercontent','github')
        file_url = file_url.replace('/main/','/blob/main/')
        # Get the URL of the newly created file
        #file_url = 'https://raw.githubusercontent.com/' + settings.GITHUB_REPO_OWNER +  '/' + settings.GITHUB_REPO_NAME +  '/main/' + file.name + '?token=A76LNERAQFQXBYUZ77XVTBDEQHWBO'

        video = LXPModel.Video.objects.create(
                            video_id=video_id,
                            published_at=datetime.datetime.now(pytz.utc),
                            name=title,
                            description=description,
                            thumbnail_url = '',
                            channel_id= channel_id,
                            channel_name=channel_name
                        )
        video.save()
        videocount = LXPModel.Playlist.objects.all().count()
        PL_id = LXPModel.Playlist.objects.only('id').get(name=playlistname).id
        plylistitems = LXPModel.PlaylistItem.objects.create(
            playlist_item_id = '',
            video_position = videocount,
            published_at = datetime.datetime.now(pytz.utc),
            channel_id= channel_id,
            channel_name=channel_name,
            is_duplicate = False,
            is_marked_as_watched = False,
            num_of_accesses = 0,
            playlist_id = PL_id,
            video_id = video.id
        )
        plylistitems.save()
        material = LXPModel.SessionMaterial.objects.create(
                mtype = 'PDF',
                urlvalue = file_url,
                description = description,
                playlist_id = PL_id,
                video_id = video.id
        )
        material.save()
        return render(request, 'cto/lxpdocgitupload/success.html', {'file_url': file_url})
    playlist = LXPModel.Playlist.objects.all().order_by('name')
    return render(request, 'cto/lxpdocgitupload/upload_recorded_video_material.html',{'playlist': playlist})


@login_required
def cto_add_playlist_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.PlayListForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Play List'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    playlist = LXPModel.Playlist.objects.all().filter(name__iexact = name)
                    if playlist:
                        messages.info(request, 'PlayList Name Already Exist')
                        return redirect(reverse('cto-add-playlist'))
                    try:
                        channel_id = form.cleaned_data.get('channel_id')
                        channel_name = form.cleaned_data.get('channel_name')
                        playlist_id = form.cleaned_data.get('playlist_id')
                        playlist = LXPModel.Playlist.objects.create(
                                                    name = name,
                                                    channel_id = channel_id,
                                                    channel_name = channel_name,
                                                    playlist_id = playlist_id)
                        playlist.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-playlist'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/playlist/add_edit_playlist.html', context)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_playlist_view(request, pk):
    #try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Playlist, id=pk)
            form = LXPFORM.PlayListForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'playlist_id': pk,
                'page_title': 'Edit Play List'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    playlist = LXPModel.Playlist.objects.all().filter(name__iexact = name).exclude(id=pk)
                    if playlist:
                        messages.info(request, 'PlayList Name Already Exist')
                        return redirect(reverse('cto-update-playlist', args=[pk]))
                    try:
                        playlist = LXPModel.Playlist.objects.get(id=pk)
                        name = form.cleaned_data.get('name')
                        channel_id = form.cleaned_data.get('channel_id')
                        channel_name = form.cleaned_data.get('channel_name')
                        playlist_id = form.cleaned_data.get('playlist_id')

                        playlist.name = name
                        playlist.channel_id = channel_id
                        playlist.channel_name = channel_name
                        playlist.playlist_id = playlist_id
                        playlist.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-playlist', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/playlist/add_edit_playlist.html', context)
    #except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_playlist_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            playlists = LXPModel.Playlist.objects.all()
            return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_playlist_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':  
            playlist=LXPModel.Playlist.objects.get(id=pk)
            playlist.delete()
        playlists = LXPModel.Playlist.objects.all()
        return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_video_list_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.PlaylistItem.objects.raw(' SELECT DISTINCT  lxpapp_playlist.id as id, lxpapp_playlistitem.id as item_id, lxpapp_playlist.name as Pl_Name , lxpapp_video.id as vid_id,  lxpapp_video.name as vid_Name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) ORDER BY  lxpapp_playlist.name,  lxpapp_video.name')
            return render(request,'cto/youtube/cto_view_video_list.html',{'videos':c_list})
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_delete_video_view(request,pk,pl_id,vid_id):
    #try:
        if str(request.session['utype']) == 'cto':  
            delobj = LXPModel.PlaylistItem.objects.all().filter(id = pk).delete()
            delobj = LXPModel.Video.objects.all().filter(id = vid_id).delete()
        c_list = LXPModel.PlaylistItem.objects.raw(' SELECT DISTINCT  lxpapp_playlist.id as id, lxpapp_playlistitem.id as item_id, lxpapp_playlist.name as Pl_Name , lxpapp_video.id as vid_id,  lxpapp_video.name as vid_Name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) ORDER BY  lxpapp_playlist.name,  lxpapp_video.name')
        return render(request,'cto/youtube/cto_view_video_list.html',{'videos':c_list})
    #except:
        return render(request,'lxpapp/404page.html')