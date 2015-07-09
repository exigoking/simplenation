from django.contrib import admin
from simplenation.models import Term, Definition, Author
# Register your models here.


class TermAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
	list_display = ('name', 'tags')

class AuthorAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('user',)}

class DefinitionAdmin(admin.ModelAdmin):
	list_display = ('author', 'term','post_date','times_reported')

admin.site.register(Term, TermAdmin)
admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Author, AuthorAdmin)
