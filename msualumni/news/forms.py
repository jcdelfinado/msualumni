from django.forms import ModelForm, Textarea, TextInput
from models import Article

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'content']
		labels = {
			'title' : '',
			'content' : ''
		}
		widgets = {
			'title' : TextInput(attrs={'placeholder':'Headline', 'class':'input-lg'}),
			'content' : Textarea(attrs={'rows': 32, 'id':'editor'})
		}