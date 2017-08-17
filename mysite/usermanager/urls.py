from django.conf.urls import url, include

from . import views

app_name = "usermanager"
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login_page/$', views.login_page, name='login_page'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^create/$', views.create_user, name='create_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    #url(r'^polls/', include("polls.urls"))
]