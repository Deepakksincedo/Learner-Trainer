from django.urls import path
from learner import views
urlpatterns = [
    path('learner-dashboard', views.learner_dashboard_view,name='learner-dashboard'),
    
    path('learner-exam', views.learner_exam_view,name='learner-exam'),
    path('learner-take-exam/<int:pk>', views.learner_take_exam_view,name='learner-take-exam'),
    path('learner-start-exam/<int:pk>', views.learner_start_exam_view,name='learner-start-exam'),
    path('learner-show-exam-reuslt/<int:pk>', views.learner_show_exam_reuslt_view,name='learner-show-exam-reuslt'),
    path('learner-show-exam-reuslt-details/<int:pk>', views.learner_show_exam_reuslt_details_view,name='learner-show-exam-reuslt-details'),
    
    path('learner-short-exam', views.learner_short_exam_view,name='learner-short-exam'),
    path('learner-take-short-exam/<int:pk>', views.learner_take_short_exam_view,name='learner-take-short-exam'),
    path('learner-start-short-exam/<int:pk>', views.learner_start_short_exam_view,name='learner-start-short-exam'),
    path('learner-show-short-exam-reuslt/<int:pk>', views.learner_show_short_exam_reuslt_view,name='learner-show-short-exam-reuslt'),
    path('learner-show-short-exam-reuslt-details/<int:pk>', views.learner_show_short_exam_reuslt_details_view,name='learner-show-short-exam-reuslt-details'),

    path('learner-video-course', views.learner_video_Course_view,name='learner-video-course'),
    path('learner-video-course-subject', views.learner_video_Course_subject_view,name='learner-video-course-subject'),
    path('learner-video-list/<int:subject_id>', views.learner_video_list_view,name='learner-video-list'),
    path('learner-show-video/<int:subject_id>,/<int:video_id>', views.learner_show_video_view,name='learner-show-video'),
    path('learner-video-sesseionmaterial-list/<subject_id>/<video_id>', views.learner_video_sesseionmaterial_list_view,name='learner-video-sesseionmaterial-list'),
    path('learner-see-sesseionmaterial/<subject_id>/<video_id>/<int:pk>', views.learner_see_sesseionmaterial_view,name='learner-see-sesseionmaterial'),

    path('learner-studymaterial-module', views.learner_studymaterial_module_view,name='learner-studymaterial-module'),
    path('learner-studymaterial-module-chapter/<int:module_id>', views.learner_studymaterial_module_chapter_view,name='learner-studymaterial-module-chapter'),
    path('learner-studymaterial-chapter-show/<int:chapter_id>/<int:module_id>', views.learner_studymaterial_chapter_show_view,name='learner-studymaterial-chapter-show'),
    path('learner-studymaterial-show/<studymaterialtype>/<int:pk>', views.learner_show_studymaterial_view,name='learner-studymaterial-show'),
    path('ajax/save-topic/', views.save_topic, name='ajax_save_topic'),

    path('learner-availablecourse-module', views.learner_availablecourse_module_view,name='learner-availablecourse-module'),
    path('learner-availablecourse-module-chapter/<modulename>/<int:module_id>', views.learner_availablecourse_module_chapter_view,name='learner-availablecourse-module-chapter'),
    
    path('learner-chapterexam/<int:chapter_id>/<int:module_id>', views.learner_chapterexam_view,name='learner-chapterexam'),
    path('learner-take-chapterexam/<int:chapter_id>/<int:module_id>', views.learner_take_chapterexam_view,name='learner-take-chapterexam'),
    path('learner-start-chapterexam/<int:chapter_id>/<int:module_id>', views.learner_start_chapterexam_view,name='learner-start-chapterexam'),
    path('learner-show-chapterexam-reuslt/<int:chapter_id>/<int:module_id>', views.learner_show_chapterexam_reuslt_view,name='learner-show-chapterexam-reuslt'),
    path('learner-show-chapterexam-reuslt-details/<int:result_id>/<int:attempt>/<int:chapter_id>/<int:module_id>', views.learner_show_chapterexam_reuslt_details_view,name='learner-show-chapterexam-reuslt-details'),

    path('learner-check-k8sterminal', views.learner_check_k8sterminal_view,name='learner-check-k8sterminal'),
    path('learner-pyton-terminal', views.learner_python_terminal_view,name='learner-pyton-terminal'),
    path('learner-linux-terminal', views.learner_linux_terminal_view,name='learner-linux-terminal'),
    path('learner-cloudshell-terminal', views.learner_cloudshell_terminal_view,name='learner-cloudshell-terminal'),

    path('ajax/save-cart/', views.save_cart, name='ajax_save_cart'),

]
#<a href="{% url 'learner-studymaterial-subject-chapter' coursename t.subject_name t.id courseset_id %}">Preview</a>