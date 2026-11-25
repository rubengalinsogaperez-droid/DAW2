from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, type=None
    ):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    #Aqui aparte del abstaractbaseuser se añade le mixin de permisos que trae django
    #para poder acceder posteriormente como admin despues de añadir esto hay que hacer
    #un migrate
class MyUser(AbstractBaseUser, PermissionsMixin):

    #Para hacer que 'Pueda ser nulo' en vez de poner none hay que poner esto:
    #null para que en la base de datos pueda estar vacio y blank para que pueda enviar el formularo sin rellenarlo
    #sin max_lenght dara un error y moriremos todos
    username = models.CharField(max_length=150, null=True, blank=True)


    #campo email
    email = models.EmailField(unique=True)

    #campo fecha con auto now, imagino que add hará que se añada a la hora a la que se a añadido
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    #dos campos booleanos si es estaf y, si esta activado?
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    #REQUIRED FIELDS. Esto sirve para si a parte de username y email necesita mas 
    # campos para la autentificacion del ususario en este caso no 
    # lo vamos a usar pero como tampoco molesta lo dejaré ahí, lo 
    # e sacado de el tercer link de los ejercicios NO ME MATES
    REQUIRED_FIELDS = []
    #Sirve para conectar el MyUserManager con MyUser. Así, Django puede usar sus funciones para crear usuarios
    objects = MyUserManager()