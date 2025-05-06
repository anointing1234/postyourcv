from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 


urlpatterns = [ 
    path('auth_login/',views.auth_login_view,name='auth_login'),
    path('auth_signup/',views.auth_signup_view,name='auth_signup'),
    path('login_view/',views.login_view,name='login_view'),
    path('register/',views.register,name='register'),
    path('auth_logout/',views.logout_view,name='auth_logout'),
    path("update_profile_picture/",views.update_profile_picture, name="update_profile_picture"),
    path('update-bio/', views.update_bio, name='update_bio'),
    path('update-profile-info/', views.update_profile_info, name='update_profile_info'),
    path('football_job/',views.football_job,name='football_job'),
    path('jobs/<int:job_id>/apply/',views.apply_for_job, name='apply_for_job'),
    path('contact_form/',views.contact_player_view, name='contact_form'),
    path('send_reset_code/',views.send_reset_code_view, name='send_reset_code'),
    path('reset_password/',views.reset_password_view, name='reset_password'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

