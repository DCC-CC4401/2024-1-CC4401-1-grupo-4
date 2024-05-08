from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage

fsPhotos = FileSystemStorage(location="/media/Fotos_usuarios")
fsMedia = FileSystemStorage(location="/media/Multimedia")

options = [[0, "No anónimo"],
             [1, "Anónimo"]]

class Tag(models.Model):
    nombre=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Rol(models.Model):
    rol=models.CharField(max_length=20)
    def __str__(self):
        return self.rol  

class Usuario(AbstractUser):
    options = [
        ("ES", "Estudiante"),
        ("AU", "Auxiliar"),
        ("PR", "Profesor"),
    ]
    contrasenha=models.CharField(max_length=100)
    tipo=models.CharField(choices=options, max_length=2)
    foto=models.ImageField(storage=fsPhotos, blank=True)
    # rol=models.ForeignKey(Rol,blank=False,null=False,on_delete=models.PROTECT)

class Consulta(models.Model):
    titulo=models.CharField(blank=False, null=False,max_length=100)
    fecha_creacion=models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d"))
    mensaje=models.TextField(blank=False,null=False)
    creador=models.ForeignKey(Usuario, blank=False, null=False,on_delete=models.CASCADE)
    anonimo=models.BooleanField(null=False,default=0)
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    multimedia=models.FileField(storage=fsMedia)
class Respuesta(models.Model):
    mensaje=models.TextField(blank=False,null=False)
    creador=models.ForeignKey(Usuario,blank=False,null=False,on_delete=models.CASCADE)
    fecha_creacion=models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d"))
    consulta=models.ForeignKey(Consulta,null=False,blank=False,on_delete=models.CASCADE)
    multimedia=models.FileField(storage=fsMedia)
    votar=models.IntegerField(default=0)
    
class Consulta_respuesta(models.Model):
    consulta=models.ForeignKey(Consulta,blank=False,null=False,on_delete=models.CASCADE)
    respuesta=models.ForeignKey(Respuesta,blank=True,null=True,on_delete=models.CASCADE)

class Consulta_tag(models.Model):
    consulta=models.ForeignKey(Consulta,blank=False,null=False,on_delete=models.CASCADE)
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
