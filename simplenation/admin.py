from django.contrib import admin
from simplenation.models import Term, Definition, Author, Picture, Notification, Favourite, Like, Report, Challenge, Session


class TermAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

class AuthorAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('user',)}

class DefinitionAdmin(admin.ModelAdmin):
	list_display = ('author', 'term','post_date','times_reported')

class PictureAdmin(admin.ModelAdmin):
	list_display = ('definition', 'created_at')

class NotificationAdmin(admin.ModelAdmin):
	list_display = ('typeof', 'sender','receiver','term')

class FavouriteAdmin(admin.ModelAdmin):
	list_display = ('favoror', 'favoree','added')

class ChallengeAdmin(admin.ModelAdmin):
	list_display = ('challenger', 'challengee','subject','added')

class SessionAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at')

admin.site.register(Term, TermAdmin)
admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Session, SessionAdmin)