from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from profiles.models import Alum
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import random, string
from django.core.mail import send_mail
from profiles.models import STATUS

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, alumni_id,
                     is_staff, is_superuser, is_active, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        code = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          activation_code=code,
                          alumni_id = alumni_id,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def _create_staff(self, email, password,
                     is_staff, is_superuser, is_active, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        code = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          activation_code=code,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, True,
                                 **extra_fields)
                                 
    def create_inactive_user(self, alumni_id, email, password=None, **extra_fields):
        return self._create_user(email, password, alumni_id, False, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_staff(email, password, True, True, True,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

  alumni_id = models.ForeignKey(Alum, null=True, blank=True)
  email = models.EmailField(_('email address'), unique=True)
  name = models.CharField(_('username'), max_length=32, unique=True)
  is_staff = models.BooleanField(_('staff status'), default=False,
      help_text=_('Designates whether the user can log into this admin '
                  'site.'))
  is_active = models.BooleanField(_('active'), default=True,
      help_text=_('Designates whether this user should be treated as '
                  'active. Unselect this instead of deleting accounts.'))
  status = models.CharField(max_length=1, choices=STATUS)
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
  activation_code = models.CharField(max_length=8, null=True, blank=True)
  #username = models.CharField(max_length=16, unique=True)
  #last_name = models.CharField(max_length=64, null=True, blank=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  
  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
    db_table="user"

  def __unicode__(self):
    return self.name
  
  def get_absolute_url(self):
    return "/users/%s/" % urlquote(self.username)
  
  def get_full_name(self):
    """
    Returns the first_name plus the last_name, with a space in between.
    """
    #alum = Alum.objects.get(alumni_id=self.alumni_id)
    #full_name = '%s %s' % (alum.first_name, alum.last_name)
    #return full_name.strip()
    return self.alumni_id
  
  def get_short_name(self):
    "Returns the short name for the user."
    return self.name

  def send_email(self, subject, message, from_email=None):
    """
    Sends an email to this User.
    """
    send_mail(subject, message, from_email, [self.email])

  def get_profile(self):
    """
    Returns site-specific profile for this user. Raises
    SiteProfileNotAvailable if this site does not allow profiles.
    """
    warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
        DeprecationWarning, stacklevel=2)
    if not hasattr(self, '_profile_cache'):
        from django.conf import settings
        if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
            raise SiteProfileNotAvailable(
                'You need to set AUTH_PROFILE_MODULE in your project '
                'settings')
        try:
            app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        except ValueError:
            raise SiteProfileNotAvailable(
                'app_label and model_name should be separated by a dot in '
                'the AUTH_PROFILE_MODULE setting')
        try:
            model = models.get_model(app_label, model_name)
            if model is None:
                raise SiteProfileNotAvailable(
                    'Unable to load the profile model, check '
                    'AUTH_PROFILE_MODULE in your project settings')
            self._profile_cache = model._default_manager.using(
                               self._state.db).get(user__id__exact=self.id)
            self._profile_cache.user = self
        except (ImportError, ImproperlyConfigured):
            raise SiteProfileNotAvailable
    return self._profile_cache
    
    
    
    