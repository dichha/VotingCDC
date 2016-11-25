from django.conf.urls import url
from vote.views import (landing_view, login_view, register_view, logout_view, post_candidates, candidates_detail, staff_view, user_view, candidates, candidates_update, candidate_deleted,candidate_delete_confirmation,user_info,user_info_update, )
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', landing_view, name='landing'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^admin/staff/(?P<username>[a-z]+)/$', staff_view, name="welcome_staff"),
	url(r'user/(?P<u_id>\d+)/$', user_view, name="welcome_user"),
	url(r'^register/$', register_view, name='register'),
	url(r'^admin/post_candidates/$',post_candidates, name='post_candidates'),
	url(r'^candidates_detail/(?P<c_id>\d+)/', candidates_detail, name='candidates_detail'),
	url(r'^admin/candidates_list/$', candidates, name="candidates_list" ),
	url(r'^admin/candidates/(?P<c_id>\d+)/edit/$', candidates_update , name="candidates_update"),
	url(r'^admin/candidates/(?P<c_id>\d+)/delete/$', candidate_delete_confirmation , name="candidate_delete_confirmation"),
	url(r'^admin/candidates/(?P<c_id>\d+)/delete_success/$', candidate_deleted , name="candidate_deleted"),
	url(r'^user/(?P<u_id>\d+)/profile/$', user_info, name="user_info"),
	url(r'^user/(?P<u_id>\d+)/edit/$', user_info_update, name="user_info_update"),


]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)