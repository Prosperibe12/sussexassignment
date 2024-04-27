from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _

class HelperModel(models.Model):
    '''
    Automatically creates these attributes when this class is inherited
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class Users(HelperModel,AbstractBaseUser,PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required.
    """
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    password = models.CharField(_("password"), blank=False, max_length=128)
    username = models.CharField(_("username"), blank=False, null=False, unique=True,max_length=200)
    full_name = models.CharField(_("Full Name"), blank=False, null=False, max_length=200)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"),auto_now_add=True)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.email}"

class UserAccount(HelperModel):
    '''
    User Profile Table
    '''
    status = (
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('USD', 'USD')
    )
    user = models.OneToOneField(Users, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), blank=True, null=True, max_length=14)
    balance = models.IntegerField(_("User Account Balance"), blank=True, null=True)
    pin = models.IntegerField(_("Account secure pin"), blank=False, null=False)
    currency = models.CharField(_("User account currency"), max_length=200, choices=status ,blank=False, null=False)
    address = models.CharField(_("Residential address"), max_length=150, blank=True, null=True)
    profile_pix = models.ImageField(_("profile image"), upload_to='profile_img/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg'])])
    is_updated = models.BooleanField(
        _("updated"),
        default=False,
        help_text=_(
            "This attribute designates whether this user has updated requirements for an account. "
            "User should update account details before using the app"
        ),
    )

    def __str__(self) -> str:
        return f"{self.user}"
