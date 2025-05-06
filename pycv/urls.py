from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 


urlpatterns = [ 
    path('',views.home_view,name='home'),
    path('contact/',views.contact_view,name='contact'),
    path('players_data/',views.players_data,name='players_data'),
    path('events/',views.events_view,name='events'),
    path('player_account/',views.player_view,name='player_account'),
    path('send_message/',views.send_message_view,name='send_message'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

