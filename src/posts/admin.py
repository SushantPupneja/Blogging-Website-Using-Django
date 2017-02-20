from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp","updated","image"]
	list_editable = ["title"]
	list_display_links = ['timestamp']
	list_filter = ['timestamp']
	search_fields = ["title"]
	class Meta:
		model = Post
		
admin.site.register(Post, PostModelAdmin)