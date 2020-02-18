from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)    
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self.db)
        
        return user
    def create_superuser(self, email, name, password):
        """Crate and save a new super user with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user
        

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    # Email column on the user profile database table with a max lenght of 255 chars
    #  and to be uinique in the system
    email = models.EmailField(max_length=255, unique=True)
    # Name column with max lenght of 255
    name = models.CharField(max_length=255)
    # is_active field of type boolean
    is_active = models.BooleanField(default=True)
    # is_staff field of type boolean with default val of FALSE
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # the username field is specified because the default username field is being overridden by an email field
    USERNAME_FIELD = 'email'
    # lists the additional required fields, NOTE: email field is automatically rquired by default
    REQUIRED_FIELDS = ['name']


    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """String representation of the model, when a user profile object is converted to a string in python"""
        return self.email