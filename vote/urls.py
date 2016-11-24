from django.conf.urls import url
from vote.views import (landing_view, login_view, register_view, logout_view, post_candidates, candidates_detail, staff_view, user_view, candidates)
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', landing_view, name='landing'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^admin/staff/(?P<username>[a-z]+)/$', staff_view, name="welcome_staff"),
	url(r'user/(?P<username>[a-z]+)/$', user_view, name="welcome_user"),
	url(r'^register/$', register_view, name='register'),
	url(r'^admin/post_candidates/$',post_candidates, name='post_candidates'),
	url(r'^candidates_detail/(?P<c_id>\d+)/', candidates_detail, name='candidates_detail'),
	url(r'^admin/candidates_list/$', candidates, name="candidates_list" )


]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)