from django.db import models
from django.utils.translation import ugettext_lazy as _
from alumniadmin.models import User

class Tag(models.Model):

	name = models.CharField(max_length=16, unique=True)

	class Meta:
		db_table="tag"

class Article(models.Model):

	author = models.ForeignKey(User)
	title = models.CharField(max_length=64)
	content = models.TextField()
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	pub_date = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	tag = models.ManyToManyField(Tag)

	class Meta:
		db_table="article"
