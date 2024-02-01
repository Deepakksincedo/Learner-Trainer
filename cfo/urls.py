from django.urls import path
from cfo import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('cfo-dashboard', views.cfo_dashboard_view,name='cfo-dashboard'),

    path('cfo-add-coursetype', views.cfo_add_coursetype_view,name='cfo-add-coursetype'),
    path('cfo-update-coursetype/<int:pk>', views.cfo_update_coursetype_view,name='cfo-update-coursetype'),
    path('cfo-view-coursetype', views.cfo_view_coursetype_view,name='cfo-view-coursetype'),
    path('cfo-delete-coursetype/<int:pk>', views.cfo_delete_coursetype_view,name='cfo-delete-coursetype'),

    path('cfo-add-batch', views.cfo_add_batch_view,name='cfo-add-batch'),
    path('cfo-update-batch/<int:pk>', views.cfo_update_batch_view,name='cfo-update-batch'),
    path('cfo-view-batch', views.cfo_view_batch_view,name='cfo-view-batch'),
    path('cfo-delete-batch/<int:pk>', views.cfo_delete_batch_view,name='cfo-delete-batch'),
    path('cfo-view-batch-details/<batchname>/<int:pk>', views.cfo_view_batch_details_view,name='cfo-view-batch-details'),
]
