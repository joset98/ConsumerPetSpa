from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse 
from django.views.generic import TemplateView, View, ListView, UpdateView
from django.views import generic
from .forms import *
from django.contrib import messages
import requests
import json

# Create your views here.
GLOBAL_IP_SERVER = 'http://192.168.1.5:8000' #ip de la pc en que se proba la aplicacion en red


from .models import Curso, Categoria


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    context = {}
    
    context['form_to_Pet'] = formPet()

    return render(
        request,
        'index.html',
        context,
    )


# class MascotasListView(ListView):
#     model = Curso
#     paginate_by = 10
# #     # context_object_name = 'my_book_list'   # your own name for the list as a template variable
# #     # queryset = Book.objects.filter(title__icontains='Musi')[:5] # Get 5 books containing the title war
#     template_name = 'mascotas.html'  # Specify your own template name/location

class ServiciosListView(ListView):
    model = Categoria
    template_name = 'servicios.html'  # Specify your own template name/location

class CategoriaDetailView(generic.DetailView):
    model = Categoria
#     # context_object_name = 'my_book_list'   # your own name for the list as a template variable
#     # queryset = Book.objects.filter(title__icontains='Musi')[:5] # Get 5 books containing the title war
    template_name = 'detalle-categoria.html'  # Specify your own template name/location



def petList (request ):
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/')
	# raise Exception(response.json())
	
	context = {'mascota_list':response.json()}
	context['form_to_Pet'] = formPet()
	
	# return HttpResponse(context['mascota_list'][5])

	return render(request,
	'mascotas.html',
	context,
	)
    
def petDelete (request,pk):
	
	response = requests.delete(GLOBAL_IP_SERVER+'/api/v1/pets/{}'.format(pk) )
	# raise Exception(response.json())
	

	return HttpResponseRedirect(reverse('mascotas'))

def petDetail (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/{}'.format(pk) )
	# raise Exception(response.json())
	context = {'petdetail':response.json()}
	# return HttpResponse(context['mascota_detail'])

	return render(request,
	'detalle_mascota.html',
	context,
	)

def petModify (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/{}'.format(pk) ).json()
	# raise Exception(response.json())
	context = {'petdetail':response}
	# return HttpResponse(context['mascota_detail'])

	context['form_to_Pet'] = formPet(initial={'name': response['name'],
						'gender': response['gender'],'age': response['age'],
						'race': response['race'],'weight': response['weight'],	})
	
	return render(request,
	'mascota_modif.html',
	context,
	)
    
def petUpdate (request,pk):
	# raise Exception(request.POST)
	formp = formPet(request.POST)
	response = {}
	if formp.is_valid():
		# raise Exception(request.POST)
		response = requests.put(GLOBAL_IP_SERVER+'/api/v1/pets/{}/'.format(pk),
			data={'name':request.POST['name'],
				'race':request.POST['race'],
				'gender':request.POST['gender'],
				'age':request.POST['age'],
				'weight':request.POST['weight'],
				}).json()
				
	messages.add_message(request, messages.SUCCESS, 'Modificado exitosamente la mascota '+str(response['id']))
	# context = {'petdetail':response.json()}
	return HttpResponseRedirect(reverse('detail-mascota',args=[pk]))


class createPet(View):

	def post(self, request, *args, **kwargs):

		formt = formPet(request.POST)
		if formt.is_valid():
			

			response = requests.post(GLOBAL_IP_SERVER+'/api/v1/pets/', data={'name':request.POST['name'],
			'race':request.POST['race'],
			'gender':request.POST['gender'],
			'age':request.POST['age'],
			'weight':request.POST['weight'],
			})
			# return HttpResponse({response})
		messages.add_message(request, messages.SUCCESS, 'Guardado exitosamente')

		return HttpResponseRedirect(reverse('mascotas'))




# creacion de servicios


def serviciosIndex(request):
	"""
    Función vista para la página de servicios del sitio.
    """
	context = {}
	context['form_to_Service'] = formService()
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/services/')
	context['service_list'] = response.json()

	return render(
		request,
		'servicios.html',
		context,
	)



    
def serviceDelete (request,pk):
	
	response = requests.delete(GLOBAL_IP_SERVER+'/api/v1/services/{}'.format(pk) )
	# raise Exception(response.json())
	

	# return HttpResponse(response)
	return HttpResponseRedirect(reverse('servicios'))


def serviceDetail (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/services/{}'.format(pk) )
	# raise Exception(response.json())
	context = {'servicio':response.json()}
	# return HttpResponse(context['mascota_detail'])

	return render(request,
	'detalle_servicio.html',
	context,
	)
    
def serviceModify (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/services/{}'.format(pk) ).json()
	# raise Exception(response.json())
	context = {'servicedetail':response}
	# return HttpResponse(context['mascota_detail'])

	context['form_to_Service'] = formService(initial={'name': response['name'],
						'description': response['description'],})
	
	return render(request,
	'service_modif.html',
	context,
	)
    
def serviceUpdate (request,pk):
	# raise Exception(request.POST)
	forms = formService(request.POST)
	response = {}
	if forms.is_valid():
		# raise Exception(request.POST)
		response = requests.put(GLOBAL_IP_SERVER+'/api/v1/services/{}/'.format(pk),
			data={'name':request.POST['name'],
				'description':request.POST['description'],
				}).json()
	
	return HttpResponseRedirect(reverse('detail-service',args=[pk]))
	
class createService(View):



	def post(self, request, *args, **kwargs):

		forms = formService(request.POST)
		if forms.is_valid():
			objPet = {}
			
			response = requests.post(GLOBAL_IP_SERVER+'/api/v1/services/', data={'name':request.POST['name'],
			'description':request.POST['description'],
			})
			# return HttpResponse({response})

		return HttpResponseRedirect(reverse('servicios'))

    	



# asociacion de servicios


def petServiceIndex(request):
	"""
    Función vista para la página de servicios del sitio.
    """
	# request.GET
	context = {}
	context['form_to_PetService'] = formPetService()
	responsePet = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/').json()# mascotas del sistema
	responseAllo = requests.get(GLOBAL_IP_SERVER+'/api/v1/lodgement/').json()#mascotas alojadas
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/service/petservices/').json()
	responseService = requests.get(GLOBAL_IP_SERVER+'/api/v1/services/').json()#mascotas alojadas
	
	result = list()

	for pet in response:
		pet['pet'] = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/{}'.format(pet['idPet'])).json()
		pet['service'] = requests.get(GLOBAL_IP_SERVER+'/api/v1/services/{}'
								.format(pet['idService'])).json()


	for i in range (len(responseAllo)):
		for j in range (len(responsePet)):
			if responsePet[j]['id'] == responseAllo[i]['idPet']:
				result.append(responsePet[j])
				continue
	context['petservice_list'] = response
	context['pet_allocated'] = result
	context['servicios'] = responseService
	return render(
		request,
		'pet_service.html',
		context,
	)



    
def petServiceDelete (request,pk):
	
	response = requests.delete(GLOBAL_IP_SERVER+'/api/v1/service/petservices/{}'.format(pk) )
	
	return HttpResponseRedirect(reverse('petservices'))


def petServiceDetail (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/service/petservices/{}'.format(pk) )
	# raise Exception(response.json())
	context = {'servicio':response.json()}
	# return HttpResponse(context['mascota_detail'])

	return render(request,
	'detalle_servicio.html',
	context,
	)
    
def petServiceModify (request,pk):
	
	context = {}

	responsePet = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/').json()# mascotas del sistema
	responseAllo = requests.get(GLOBAL_IP_SERVER+'/api/v1/lodgement/').json()#mascotas alojadas
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/service/petservices/{}'.format(pk)).json()
	responseService = requests.get(GLOBAL_IP_SERVER+'/api/v1/services/').json()#mascotas alojada
	result = list()

	context['form_to_PetService'] = formPetService(initial={'idPet': response['idPet'],
				'idService': response['idService'],'hora': response['hora'],
				'fecha': response['fecha'],	})

	for i in range (len(responseAllo)):
		for j in range (len(responsePet)):
			if responsePet[j]['id'] == responseAllo[i]['idPet']:
				result.append(responsePet[j])
				continue
	# raise Exception ()
	context['petservice'] = response
	context['pet_allocated'] = result
	context['servicios'] = responseService
	
	# raise Exception (result)
	return render(request,
	'petservice_modif.html',
	context,
	)
    
def petServiceUpdate (request,pk):
	formps = formPetService(request.POST)
	response = {}
	if formps.is_valid():
		response = requests.put(GLOBAL_IP_SERVER+'/api/v1/service/petservices/{}/'.format(pk),
			data={'idPet':request.POST['pet'],
				'idService':request.POST['service'],
				'hora':request.POST['hora'],
				'fecha':request.POST['date'],
				}).json()
	
	return HttpResponseRedirect(reverse('detail-petservice',args=[pk]))

    	
class createPetService(View):

	def post(self, request, *args, **kwargs):

		forms = formPetService(request.POST)
		
		if forms.is_valid():
			# raise Exception (request.POST)	
			
			response = requests.post(GLOBAL_IP_SERVER+'/api/v1/service/petservices/', 
			data={'idPet':request.POST['pet'],
			'idService':request.POST['service'],
			'fecha':request.POST['date'],
			'hora':request.POST['hora'],
			})
        
		return HttpResponseRedirect(reverse('petservices'))







# Habitaciones-alojamiento

def roomIndex(request):
	"""
    Función vista para la página de servicios del sitio.
    """
	context = {}
	context['form_to_Room'] = formRoom()#initial={'description': 'Hi there!'}
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/lodgement/').json()#mascotas alojadas
	responsePets = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/')#mascotas
	responseList = responsePets.json()
	result = list()
	flag = 0

	for pet in response:
		pet['pet'] = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/{}'.format(pet['idPet'])).json()

	for i in range (len(responseList)):
		flag = 0
		for j in range (len(response)):
			if response[j]['idPet'] == responseList[i]['id']:
				flag = 1
				continue
		if flag == 0:
			result.append(responseList[i])
	
	context['room_list'] = response
	context['pet_list'] = result

	return render(
		request,
		'alojamiento.html',
		context,
	)
    
def roomDelete (request,pk):
	
	response = requests.delete(GLOBAL_IP_SERVER+'/api/v1/lodgement/{}'.format(pk) )
	# raise Exception(response.json())
	

	return HttpResponseRedirect(reverse('alojamiento'))

def roomDetail (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/lodgement/{}'.format(pk) ).json()
	# raise Exception(response.json())
	response['pet'] = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/{}'.format(response['idPet'])).json() 

	context = {'roomdetail':response}
	# return HttpResponse(context['mascota_detail'])

	return render(request,
	'detalle_room.html',
	context,
	)
    
def roomModify (request,pk):
	
	response = requests.get(GLOBAL_IP_SERVER+'/api/v1/lodgement/{}'.format(pk) ).json()
	responseAllo = requests.get(GLOBAL_IP_SERVER+'/api/v1/lodgement/').json()#mascotas alojadas
	responsePets = requests.get(GLOBAL_IP_SERVER+'/api/v1/pets/').json()#mascotas
	result = list()
	context = {'roomdetail':response}
	flag = 0
	context['form_to_Room'] = formRoom(initial={'idPet': response['idPet'],
				'roomNumber': response['roomNumber'],'floor': response['floor'],
				'description': response['description'],	})#
	for i in range (len(responsePets)):
		flag = 0
		for j in range (len(responseAllo)):
			if responseAllo[j]['idPet'] == responsePets[i]['id']:
				if(int(pk) == int(responseAllo[j]['id'])):
					result.append(responsePets[i])
				flag = 1
				continue
		if flag == 0:
			result.append(responsePets[i])
	context['pet_list'] = result

	# raise Exception (result)
	return render(request,
	'room_modif.html',
	context,
	)
    
def roomUpdate (request,pk):
	forms = formRoom(request.POST)
	response = {}
	if forms.is_valid():
		response = requests.put(GLOBAL_IP_SERVER+'/api/v1/lodgement/{}/'.format(pk),
			data={'idPet':request.POST['pet'],
				'roomNumber':request.POST['roomNumber'],
				'floor':request.POST['floor'],
				'description':request.POST['description'],
				}).json()
	
	return HttpResponseRedirect(reverse('alojamiento'))


class createRoom(View):



	def post(self, request, *args, **kwargs):
		formr = formRoom(request.POST)

		if formr.is_valid():
			objPet = {}
			response = requests.post(GLOBAL_IP_SERVER+'/api/v1/lodgement/', 
			data={'idPet':request.POST['pet'],
			'roomNumber':request.POST['roomNumber'],
			'floor':request.POST['floor'],
			'description':request.POST['description'],
			})
			# return HttpResponse({response})

		return HttpResponseRedirect(reverse('alojamiento'))




# objt = formt.save(commit = False)

# datef = datetime.datetime.strptime(request.POST['final'].replace('T',' ').replace('-','/'), '%Y/%m/%d')
# datei = datetime.datetime.strptime(request.POST['inicio'].replace('T',' ').replace('-','/'), '%Y/%m/%d')
