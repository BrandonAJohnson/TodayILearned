from followers.models import Follower
from django.http import request
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from followers.models import Follower
from .models import Post

class HomePage(TemplateView):
	http_method_names = ["get"]
	template_name = "feed/homepage.html"

	def dispatch(self, request, *args, **kwargs):
		self.request = request
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated:
			following = list(
				Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
			)
			if not following:
				context['posts'] = Post.objects.all().order_by('-id')[0:30]
			else:
				following.append(self.request.user)
				context['posts'] = Post.objects.filter(author__in=following).order_by('-id')[0:60]
		else:
			context['posts'] = Post.objects.all().order_by('-id')[0:30]

		return context

class PostDetailView(LoginRequiredMixin, DetailView):
	http_method_names = ["get"]
	template_name = "feed/detail.html"
	model = Post
	context_object_name = "post"

class CreateNewPost(LoginRequiredMixin, CreateView):
	model = Post
	template_name = "feed/create.html"
	fields = ['text', 'details', 'tag']
	success_url = "/"

	def post(self, request, *args, **kwargs):
		post = Post.objects.create(
			author=request.user,
			text=request.POST.get("text"),
			tag=request.POST.get("tag"),
			details=request.POST.get("details"),
		)
		return render(
			request,
			"includes/post.html",
			{
				"post": post,
			},
			content_type="application/html",
		)

	def dispatch(self, request, *args, **kwargs):
		self.request = request
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.author = self.request.user
		obj.save()
		return super().form_valid(form)