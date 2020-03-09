from django.db import models
from django.core.files.images import get_image_dimensions
# Create your models here.
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Categoria(models.Model):
	"""
	Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
	"""
	nombre = models.CharField(max_length=50, help_text="Ejemplo: idiomas,programacion")
	
	def __str__(self):
		"""
		Cadena que representa a la instancia particular del modelo (p. ej en el sitio de Administración)
		"""
		return self.nombre

	def get_absolute_url(self):
		"""
		Devuelve el URL a una instancia particular de Book
		"""
		return reverse('detalle-categoria', args=[str(self.id)])

class Curso(models.Model):
	"""
	Modelo que representa un libro (pero no un Ejemplar específico).
	"""

	Nombre = models.CharField(max_length=200)

	Descripcion = models.TextField(max_length=1000, help_text="Descripcion breve del curso")
	
	categoria = models.ManyToManyField(Categoria, help_text="Seleccione la categoria a la que pertenece el curso")
	
	def __str__(self):
		"""
		String que representa al objeto Book
		"""
		return self.Nombre
	
	def display_genre(self):
		"""
		Creates a string for the Genre. This is required to display genre in Admin.
		"""
		return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
	display_genre.short_description = 'Genre'
	
	def get_absolute_url(self):
		"""
		Devuelve el URL a una instancia particular de Book
		"""
		return reverse('book-detail', args=[str(self.id)])


class Pet(models.Model):
    name = models.CharField(max_length = 255)
    race = models.CharField(max_length = 255)
    gender = models.CharField(max_length = 1)
    age = models.IntegerField()
    weight = models.FloatField()
    
    def __str__(self):
        return "%s %s" % (self.name, self.race)

class Service(models.Model):
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)

    def __str__(self):
        return "%s" % (self.name)

class PetService(models.Model):
    fecha = models.DateField(max_length=50)
    idPet = models.ForeignKey(Pet, on_delete=models.CASCADE)    
    idService = models.ForeignKey(Service, on_delete=models.CASCADE)
    hora = models.DurationField(max_length=50)
    # hora = models.DurationField¶(max_length=50, default=get_default_my_hour) 
    # idService = models.IntegerField()
    # idPet = models.IntegerField()


class Room(models.Model):
    floor = models.IntegerField()
    roomNumber = models.IntegerField()
    # idPet = models.IntegerField()
    idPet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    description = models.CharField(max_length = 255)