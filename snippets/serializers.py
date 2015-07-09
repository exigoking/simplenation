from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, User


class UserSerializer(serializers.ModelSerializer):
	snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

	class Meta:
		model = User
		fields = ('id','username','snippets')

class SnippetSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	
	class Meta:
		model = Snippet
		fields = ('id', 'title', 'code', 'linenos', 'language', 'style','owner')