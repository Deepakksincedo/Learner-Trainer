from django.shortcuts import render,redirect
from lxpapp import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from social_django.models import UserSocialAuth
from django.contrib.auth import update_session_auth_hash

def login(request):
    return render(request, 'lxpapp/index.html')


@login_required
def user_change_password_view(request):
    try:    
        sub = forms.ContactusForm()
        if request.method == 'POST':
            u = request.user
            u.set_password(request.POST['passid'])
            u.save() # Add this line
            update_session_auth_hash(request, u)
            return HttpResponseRedirect('indexpage')  
        return render(request, 'lxpapp/users/changepassword.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def home(request):
    if request.user.is_authenticated:
        # user = User.objects.raw('SELECT   auth_user.id,  auth_user.password,  auth_user.last_login,  auth_user.is_superuser,  auth_user.username,  auth_user.first_name,  auth_user.email,  auth_user.is_staff,  auth_user.is_active,  auth_user.date_joined,  auth_user.last_name,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  social_auth_usersocialauth.extra_data,  social_auth_usersocialauth.user_id,  social_auth_usersocialauth.utype,  social_auth_usersocialauth.status,  social_auth_usersocialauth.modified,  social_auth_usersocialauth.pic,  social_auth_usersocialauth.usercode,  social_auth_usersocialauth.created FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)')
        # update_session_auth_hash(request, user)
        return HttpResponseRedirect('indexpage')  
    return render(request,'lxpapp/404page.html')

def afterlogin_view(request):
    user = UserSocialAuth.objects.all().filter(user_id = request.user.id)
    if not user:
        request.session['utype'] = 'admin'
        return redirect('admin-dashboard')
    elif user:
        for xx in user:
            if xx.utype == 1:
                if xx.status:
                    request.session['utype'] = 'trainer'
                    notification = models.TrainerNotification.objects.all().filter(trainer_id = request.user.id,status = False)
                    mco = models.Exam.objects.filter(questiontpye='MCQ').count()
                    short = models.Exam.objects.filter(questiontpye='ShortAnswer').count()
                    mcqques= models.McqQuestion.objects.all().count()
                    sques= models.ShortQuestion.objects.all().count()
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
                    send_mail('Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                    return render(request,'loginrelated/wait_for_approval.html')
                
            elif xx.utype == 2  or xx.utype == 0 :
                if xx.status:
                    learnerdetails = models.LearnerDetails.objects.all().filter(learner_id = request.user.id)
                    if learnerdetails:
                        request.session['utype'] = 'learner'
                        return render(request,'learner/learner_dashboard.html')
                    else:
                        if request.method=='POST':
                            learnerdetailsForm=forms.LearnerDetailsForm(request.POST,request.FILES)
                            if learnerdetailsForm.is_valid():
                                user_full_name = learnerdetailsForm.cleaned_data["user_full_name"]
                                mobile = learnerdetailsForm.cleaned_data["mobile"]
                                iswhatsapp = learnerdetailsForm.cleaned_data["iswhatsapp"]
                                whatsappno = learnerdetailsForm.cleaned_data["whatsappno"]
                                learnerdetails=learnerdetailsForm.save(commit=False)

                                learner_id=request.user.id
                                user_full_name= user_full_name
                                mobile=mobile
                                iswhatsapp=iswhatsapp
                                whatsappno=whatsappno
                                
                                learnerdetails.save()
                                
                                obj = models.LearnerDetails.objects.latest('id')
                                selectedlist = request.POST.getlist('listbox1')
                                for x in selectedlist:
                                    knownskillid = str(x)
                                    knownskilltable = models.LearnerDetailsKSkill.objects.create(learnerdetails_id=obj.id,knownskill_id=knownskillid)
                                    knownskilltable.save()
                                selectedlist = request.POST.getlist('listbox3')
                                for x in selectedlist:
                                    passionateskillid = str(x)
                                    passionateskilltable = models.LearnerDetailsPSkill.objects.create(learnerdetails_id=obj.id,passionateskill_id=passionateskillid)
                                    passionateskilltable.save()
                                send_mail('New User Login / Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                            else:
                                print("form is invalid")
                                return render(request,'lxpapp/404page.html')
                            return render(request,'loginrelated/wait_for_approval.html')
                        learnerdetailsForm=forms.LearnerDetailsForm()
                        pskills = models.PassionateSkill.objects.all()
                        kskills = models.KnownSkill.objects.all()
                        
                        user =  User.objects.all().filter(id = request.user.id)
                        username=''
                        for u in user:
                            username = u.first_name + ' ' + u.last_name
                        return render(request,'loginrelated/add_learnerdetails.html',{'learnerdetailsForm':learnerdetailsForm,'pskills':pskills,'kskills':kskills,'username':username})
                else:
                    learnerdetails = models.LearnerDetails.objects.all().filter(learner_id = request.user.id)
                    if learnerdetails:
                        isfirstlogin = models.IsFirstLogIn.objects.all().filter(user_id = request.user.id)
                        if not isfirstlogin:
                            return render(request,'loginrelated/wait_for_approval.html')
                        return render(request,'loginrelated/on_hold.html')
                    else:
                        if request.method=='POST':
                            learnerdetailsForm=forms.LearnerDetailsForm(request.POST)
                            if learnerdetailsForm.is_valid():
                                user_full_name = learnerdetailsForm.cleaned_data["user_full_name"]
                                mobile = learnerdetailsForm.cleaned_data["mobile"]
                                iswhatsapp = learnerdetailsForm.cleaned_data["iswhatsapp"]
                                whatsappno = learnerdetailsForm.cleaned_data["whatsappno"]
                                learnerdetails = models.LearnerDetails.objects.create(learner_id=request.user.id,
                                                                                    user_full_name= user_full_name,
                                                                                    mobile=mobile,
                                                                                    iswhatsapp=iswhatsapp,
                                                                                    whatsappno=whatsappno)
                                learnerdetails.save()
                                
                                obj = models.LearnerDetails.objects.latest('id')
                                selectedlist = request.POST.getlist('listbox1')
                                for x in selectedlist:
                                    knownskillid = str(x)
                                    knownskilltable = models.LearnerDetailsKSkill.objects.create(learnerdetails_id=obj.id,knownskill_id=knownskillid)
                                    knownskilltable.save()
                                selectedlist = request.POST.getlist('listbox3')
                                for x in selectedlist:
                                    passionateskillid = str(x)
                                    passionateskilltable = models.LearnerDetailsPSkill.objects.create(learnerdetails_id=obj.id,passionateskill_id=passionateskillid)
                                    passionateskilltable.save()
                                send_mail('New User Login / Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                            else:
                                print("form is invalid")
                                return render(request,'lxpapp/404page.html')
                            return HttpResponseRedirect('indexpage')
                        learnerdetailsForm=forms.LearnerDetailsForm()
                        pskills = models.PassionateSkill.objects.all()
                        kskills = models.KnownSkill.objects.all()
                        
                        user =  User.objects.all().filter(id = request.user.id)
                        username=''
                        for u in user:
                            username = u.first_name + ' ' + u.last_name
                        return render(request,'loginrelated/add_learnerdetails.html',{'learnerdetailsForm':learnerdetailsForm,'pskills':pskills,'kskills':kskills,'username':username})
            elif xx.utype == 3:
                if xx.status:
                    request.session['utype'] = 'cto'
                    return render(request,'cto/cto_dashboard.html')
                else:
                    send_mail('Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                    return render(request,'cto/cto_wait_for_approval.html')
            elif xx.utype == 4:
                if xx.status:
                    request.session['utype'] = 'cfo'
                    return render(request,'cfo/cfo_dashboard.html')
                else:
                    send_mail('Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                    return render(request,'cfo/cfo_wait_for_approval.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('indexpage')
    return HttpResponseRedirect('userlogin')

@login_required
def admin_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'admin':
            dict={
            'total_learner':0,
            'total_trainer':0,
            'total_exam':0,
            'total_question':0,
            }
            return render(request,'lxpapp/admin_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
def aboutus_view(request):
    return render(request,'lxpapp/aboutus.html')

def contactus_view(request):
    try:    
        if str(request.session['utype']) == 'admin':
            sub = forms.ContactusForm()
            if request.method == 'POST':
                sub = forms.ContactusForm(request.POST)
                if sub.is_valid():
                    email = sub.cleaned_data['Email']
                    name=sub.cleaned_data['Name']
                    message = sub.cleaned_data['Message']
                    send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
                    return render(request, 'lxpapp/contactussuccess.html')
            return render(request, 'lxpapp/contactus.html', {'form':sub})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def getUserTable(request):
    users = UserSocialAuth.objects.raw('SELECT   SOCIAL_AUTH_USERSOCIALAUTH.ID,  SOCIAL_AUTH_USERSOCIALAUTH.USER_ID,  AUTH_USER.FIRST_NAME,  AUTH_USER.LAST_NAME,  LXPAPP_LEARNERDETAILS.MOBILE FROM  SOCIAL_AUTH_USERSOCIALAUTH  LEFT OUTER JOIN AUTH_USER ON (SOCIAL_AUTH_USERSOCIALAUTH.USER_ID = AUTH_USER.ID)  LEFT OUTER JOIN LXPAPP_LEARNERDETAILS ON (AUTH_USER.ID = LXPAPP_LEARNERDETAILS.LEARNER_ID) ORDER BY  AUTH_USER.FIRST_NAME,  AUTH_USER.LAST_NAME')
    return users
@login_required
def admin_view_user_list_view(request):
    try:    
        if str(request.session['utype']) == 'admin':
            users = getUserTable(request)
            return render(request,'lxpapp/users/admin_view_user_list.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

    
@login_required
def admin_view_user_grid_view(request):
    try:    
        if str(request.session['utype']) == 'admin':
            users = getUserTable(request)
            return render(request,'lxpapp/users/admin_view_user_grid.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def update_user_view(request,userfirstname,userlastname,userid,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            if request.method == 'POST':
                course = request.POST.getlist('courses[]')
                active = request.POST.get('active')
                usertype = request.POST.getlist('utype[]')
                users = UserSocialAuth.objects.get(id=pk)
                if active:
                    users.status = True
                else:
                    users.status = False
                users.utype = usertype[0]
                users.save()
                users = getUserTable(request)
                return HttpResponseRedirect('/admin-view-user-list',{'users':users})
            learnercourses = ''
            users = UserSocialAuth.objects.all().filter(id=pk)
            userdetails = models.LearnerDetails.objects.all().filter(learner_id=userid)
            username = userfirstname + ' ' + userlastname
            return render(request,'lxpapp/users/admin_update_user.html',{'users':users,'learnercourses':learnercourses,'username':username,'userdetails':userdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def active_user_view(request,userid,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 1 WHERE id = " + str(pk))
            users = models.User.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(pk))
            isfirstlogin =models.IsFirstLogIn.objects.all().filter(user_id = userid)
            if not isfirstlogin:
                isfirstlogin =models.IsFirstLogIn.objects.create(user_id = userid)
                isfirstlogin.save()
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def inactive_user_view(request,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 0 WHERE id = " + str(pk))
            users = models.User.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def delete_user_view(request,userid,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            # cursor = connection.cursor()
            # cursor.execute("DELETE FROM lxpapp_BatchTrainer WHERE trainer_id = " + str(pk))
            # cursor.execute("DELETE FROM lxpapp_UserPics WHERE user_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_UserCourse WHERE user_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_LearnerDetails WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_IsFirstLogIn WHERE user_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_McqResult WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_ShortResult WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_VideoToUnlock WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_VideoWatched WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_WaringMail WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_K8STerminal WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_K8STerminalLearnerCount WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM social_auth_usersocialauth WHERE id = " + str(pk))
            # cursor.execute("DELETE FROM auth_user WHERE id = " + str(userid))
            users = models.User.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')