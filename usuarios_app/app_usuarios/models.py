from django.db import models

# Create your models here.


class Usuario(models.Model):
  
    uuid = models.CharField(max_length=100, primary_key=True)
    nombre_completo = models.CharField(max_length=150)
    email = models.EmailField()
    genero = models.CharField(max_length=20)
    edad = models.IntegerField()
    ciudad = models.CharField(max_length=100)
    imagen_large = models.URLField()
    imagen_medium = models.URLField()
    imagen_thumbnail = models.URLField()
    fecha_registro = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_completo
