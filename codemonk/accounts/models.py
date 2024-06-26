from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# CustomUserManager model impleneted using django bult in BaseUserManager,AbstractBaseUser suing django documentation

class MyUserManager(BaseUserManager):
    def create_user(self, email, name,date_of_birth, password=None,password2=None):
        """
        Creates and saves a User with the given email, name,date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth = date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email,name, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            name = name,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# CustomUser model impleneted using django bult in BaseUserManager,AbstractBaseUser suing django documentation

class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40,null=False,blank=False)
    email = models.EmailField(verbose_name="email address",max_length=50,unique=True,)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager() 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name','date_of_birth','created_at','modified_at']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



# paragraph model 
class Paragraph(models.Model):
   id = models.AutoField(primary_key=True)
   user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
   text = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)
   modified_at = models.DateTimeField(auto_now=True)
   
   def __str__(self) -> str:
       return f"paragraph {self.id}"