from django.conf.urls import url
from vote.views import (landing_view, login_view, register_view, logout_view)


urlpatterns = [
	url(r'^$', landing_view, name='landing'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^register/$', register_view, name='register'),
]