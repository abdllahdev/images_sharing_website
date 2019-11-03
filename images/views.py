from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from django.views import generic as generic_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Image
from .forms import ImageCreateForm
from common.decorators import ajax_required

from actions.utils import create_action


class ImageCreateView(LoginRequiredMixin, generic_views.FormView):
    form_class = ImageCreateForm
    template_name = 'images/image_create.html'

    def form_valid(self, form):
        image = form.save(commit=False)
        image.user = self.request.user
        image.save()
        messages.success(self.request, 'Image created successfully')
        self.success_url = image.get_absolute_url()
        return super(ImageCreateView, self).form_valid(form)


class ImageListView(generic_views.ListView):
    model = Image
    template_name = 'images/image_list.html'

    def get_queryset(self):
        return Image.objects.all().order_by('-created')


class ImageDetailView(generic_views.DetailView):
    model = Image
    template_name = 'images/image_detail.html'


class LikeView(LoginRequiredMixin, generic_views.View):
    def post(self, request):
        if request.is_ajax():
            image_id = request.POST.get('id')
            action = request.POST.get('action')
            if image_id and action:
                try:
                    image = Image.objects.get(id=image_id)
                    if action == 'like':
                        image.user_likes.add(request.user)
                        create_action(request.user, 'likes', target=image)
                    elif action == 'dislike':
                        image.user_likes.remove(request.user)
                    return JsonResponse({'status': True})
                except:
                    pass
        else:
            return HttpResponseBadRequest()

