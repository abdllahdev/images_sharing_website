from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'url')

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('Invalid URL')
        return url

    def save(self, commit=True):
        image = super(ImageCreateForm, self).save(commit)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        try:
            response = request.urlopen(image_url)
            image.image.save(image_name,
                             ContentFile(response.read()),
                             save=False)
        except:
            raise forms.ValidationError('Error while downloading the image. This might happen because of the copy rights')

        if commit:
            image.save()
        return image
