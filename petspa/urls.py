from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	
	url(r'^mascotas/$', views.petList, name='mascotas'),
	url(r'^register/pet$', csrf_exempt(views.createPet.as_view()), name='mascotas-register'),
	# url(r'^mascotas/list$', views.petList, name='listado-mascotas'),
	url(r'^mascota/(?P<pk>\d+)/delete$', views.petDelete, name='delete-mascota'),
	url(r'^mascota/(?P<pk>\d+)/detail$', views.petDetail, name='detail-mascota'),
	url(r'^mascota/(?P<pk>\d+)/modify$', views.petModify, name='modify-mascota'),
	url(r'^mascota/(?P<pk>\d+)/update$', csrf_exempt(views.petUpdate), name='update-mascota'),
	
	# servicios
	url(r'^servicios/$', views.serviciosIndex, name='servicios'),
	url(r'^register/service$', csrf_exempt(views.createService.as_view()), name='servicios-register'),
	url(r'^service/(?P<pk>\d+)/delete$', views.serviceDelete, name='delete-service'),
	url(r'^service/(?P<pk>\d+)/detail$', views.serviceDetail, name='detail-service'),
	url(r'^service/(?P<pk>\d+)/modify$', views.serviceModify, name='modify-service'),
	url(r'^service/(?P<pk>\d+)/update$', csrf_exempt(views.serviceUpdate), name='update-service'),

	#aplicacion de servicios
	url(r'^petservice/$', views.petServiceIndex, name='petservices'),
	url(r'^register/petservice$', csrf_exempt(views.createPetService.as_view()), name='petservicios-register'),
	url(r'^petservice/(?P<pk>\d+)/delete$', views.petServiceDelete, name='delete-petservice'),
	url(r'^petservice/(?P<pk>\d+)/detail$', views.petServiceDetail, name='detail-petservice'),
	url(r'^petservice/(?P<pk>\d+)/modify$', views.petServiceModify, name='modify-petservice'),
	url(r'^petservice/(?P<pk>\d+)/update$', csrf_exempt(views.petServiceUpdate), name='update-petservice'),


	# alojamiento
	url(r'^alojamiento/$', views.roomIndex, name='alojamiento'),
	url(r'^register/alojamiento$', csrf_exempt(views.createRoom.as_view()), name='room-register'),
	url(r'^alojamiento/(?P<pk>\d+)/detail$', views.roomDetail, name='detail-room'),
	url(r'^alojamiento/(?P<pk>\d+)/delete$', views.roomDelete, name='delete-room'),
	url(r'^alojamiento/(?P<pk>\d+)/modify$', views.roomModify, name='modify-room'),
	url(r'^alojamiento/(?P<pk>\d+)/update$', csrf_exempt(views.roomUpdate), name='update-room'),

	url(r'^categorias/(?P<pk>\d+)$', views.CategoriaDetailView.as_view(), name='detalle-categoria'),
]