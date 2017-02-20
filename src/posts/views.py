from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 , redirect , Http404
from .models import Post
from .forms import PostForm
from django.utils import timezone
from urllib import quote_plus
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

# Create your views here.
def post_list(request):
	#queryset = Post.objects.all().order_by("-timestamp") replace by below
	# queryset = Post.objects.all().filter(draft=False).filter(publish__lte=timezone.now()) replace by post manager
	queryset = Post.objects.active().order_by("-timestamp")


	if request.user.is_staff or request.user.is_superuser:
		queryset = Post.objects.all().order_by("-timestamp")
	query = request.GET.get("q")

	if query:
		queryset = queryset.filter(
			Q(title__icontains=query) |
			# Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()

	context = {
		"title": "List",
		"object_all": queryset,
	}
	return render(request, "post_list.html", context)

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404 
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, 'Item Created')
	context = {
		'form': form
	}
	return render(request, "post_create.html", context)

def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	share_string = quote_plus(instance.content)
	context = {
		"instance": instance,
		"title": instance.title,
		"share_string": share_string,
		
	}
	return render(request, "post_detail.html", context)

def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None , instance=instance )
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request , 'Item saved')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"instance": instance,
		"title": instance.title,
		'form': form
	}
	return render(request, "post_update.html", context)

def post_delete(request,id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request , 'Successfully deleted')
	return redirect('posts:list')

