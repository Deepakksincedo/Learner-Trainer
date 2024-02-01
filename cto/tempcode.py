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

@login_required
def cto_add_courseset_view(request):
    try:
        if str(request.session['utype']) == 'cto':

            course = LXPModel.CourseDetails.objects.all().filter(
                    course_id__in = LXPModel.Course.objects.all(),
                    subject_id__in = LXPModel.Subject.objects.all(),
                    module_id__in = LXPModel.Module.objects.all(),
                    chapter_id__in = LXPModel.Chapter.objects.all(),
                    topic_id__in = LXPModel.Topic.objects.all()
                    )
            import json
            
            data = list(course.values())
            result = {}
            for item in data:
                current_dict = result
                for key in list(item.keys())[:-1]:
                    current_dict = current_dict.setdefault(key, {})
                current_dict[list(item.keys())[-1]] = item[list(item.keys())[-1]]

            # Convert the dictionary to a JSON object
            json_data = json.dumps(result, indent=4)
            json_data = json_data.replace('\n','')
           # course = LXPModel.Course.objects.raw(' SELECT 1 as id,  ROW_NUMBER () OVER (        PARTITION BY lxpapp_course.course_name    ) CRow , lxpapp_course.course_name ,    ROW_NUMBER () OVER (        PARTITION BY lxpapp_subject.subject_name    ) SRow ,  lxpapp_subject.subject_name,       ROW_NUMBER () OVER (        PARTITION BY lxpapp_module.module_name    ) MRow ,  lxpapp_module.module_name,         ROW_NUMBER () OVER (        PARTITION BY lxpapp_chapter.chapter_name    ) CHRow ,  lxpapp_chapter.chapter_name,     ROW_NUMBER () OVER (        PARTITION BY lxpapp_topic.topic_name    ) TRow ,  lxpapp_topic.topic_name FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
           # course = LXPModel.CourseSetDetails.objects.raw('SELECT   1 as id,lxpapp_course.course_name,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name   FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            courses = LXPModel.Course.objects.raw('SELECT   1 as id,lxpapp_course.course_name,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name   FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            from django.core.serializers import serialize
            people = serialize("json", course)
            import collections
            # data = serialize("json", courses)
            objects_list = []
            for row in courses:
                
                d = collections.OrderedDict()
                d["course_name"] = row.course_name
                d["subject_name"] = row.subject_name
                d["module_name"] = row.module_name
                d["chapter_name"] = row.chapter_name
                d["topic_name"] = row.topic_name
                objects_list.append(d)
            j = json.dumps(objects_list)
            
            import ast
            
            # List Initialization
            Input =  list(course.values())#['12, 454', '15.72, 82.85', '52.236, 25256', '95.9492, 72.906']
            
            # using ast to convert
            Output = [list(ast.literal_eval(x)) for x in Input]
            
            # printing
            print(Output)
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
