from django.contrib.auth.models import User
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from followers.models import Follower

from feed.models import Post

class ProfileDetailView(DetailView):
	http_method_names = ["get"]
	template_name = "profiles/detail.html"
	model = User
	context_object_name ="user"
	slug_field = "username"
	slug_url_kwarg = "username"

	def dispatch(self, request, *args, **kwargs):
		self.request = request
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		user = self.get_object()
		context = super().get_context_data(**kwargs)
		context['total_posts'] = Post.objects.filter(author=user).count
		context['followers'] = Follower.objects.filter(following=user).count
		context['followed_by'] = Follower.objects.filter(followed_by=user).count

		print(context['followers'])

		if self.request.user.is_authenticated:
			context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user)

		return context

class FollowView(LoginRequiredMixin,View):
	http_method_names = ["post"]

	def post(self, request, *args, **kwargs):
		data = request.POST.dict()
		if "action" not in data or "username" not in data:
			return HttpResponseBadRequest({"Missing Data"})

		try:
			other_user = User.objects.get(username=data['username'])
		except User.DoesNotExist:
			return HttpResponseBadRequest("Missing User")

		if data['action'] == "follow":
			follower, created = Follower.objects.get_or_create(
				followed_by=request.user,
				following=other_user,
			)
		else:
			try:
				follower = Follower.objects.get(
					followed_by=request.user,
					following=other_user
				)
			except Follower.DoesNotExist:
				follower = None

			if follower:
				follower.delete()

		return JsonResponse({
			"success": True,
			"wording": "Unfollow" if data['action'] == "follow" else "Follow",
		})
