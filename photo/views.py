from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .models import Photo
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model =Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            #올바르다면
            # form : 모델폼
            form.instance.save()
            return redirect('/')
        else:
            #올바르지 않다면
            return self.render_to_response({'form':form})    

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *arg, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            message.warning(request, '수정 권한이 없습니다.')
            return HttpResponseRedirect('/')

        else:
            return super(PhotoUpdate, self).dispatch(request, *arg, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *arg, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            message.warning(request, '삭제 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *arg, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

class PhotoLike(View):
    def get(self, request, *arg, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PhotoFavorite(View):
    def get(self, request, *arg, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)