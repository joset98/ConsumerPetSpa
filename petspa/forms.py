from django.forms import ModelForm
from django.forms import Form
from django import forms
from .models import *
from datetime import datetime
from django.contrib.admin import widgets

currentTime = datetime.now()



class formPet(ModelForm):

	class Meta:
		model = Pet
		fields = '__all__'
		labels = { 'name':'Nombre',
				'gender':'Genero',
				'race':'raza',
				'age':'Edad',
				'weight':'Peso',}


class formService(ModelForm):

	class Meta:
		model = Service
		fields = '__all__'
		labels = { 'name':'nombre del servicio',
				'description':'descripcion del servicio', }


class formPetService(Form):

	class Meta:
		model = PetService
		idPet = forms.ChoiceField(label='pet')
		idService = forms.ChoiceField(label='service')
		fecha = forms.DateField(label='date')
		hora = forms.TimeField(label='hora')


class formRoom(Form):

	class Meta:
		model = Room
		description = forms.CharField(label='description', max_length=100)
		idPet = forms.ChoiceField(label='pet')
		floor = forms.IntegerField(label='floor')
		roomNumber = forms.IntegerField(label='roomnumber')
		# fields = {'idPet','description','roomNumber','floor',}
		# labels = { 'floor':'piso',
		# 		'description':'descripcion de la habitacion', }


#fin modelos spa