from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight



class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(default='python', max_length=100)
    style = models.CharField(default='friendly', max_length=100)

    owner = models.ForeignKey(User, related_name='snippets')
    highlighted = models.TextField(blank = True)

    def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""
		lexer = get_lexer_by_name(self.language)
		linenos = self.linenos and 'table' or False
		options = self.title and {'title': self.title} or {}
		formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
		self.highlighted = highlight(self.code, lexer, formatter)
		super(Snippet, self).save(*args, **kwargs)


    class Meta:
    	ordering = ('created',)
	

	