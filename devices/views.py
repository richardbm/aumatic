from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.template.exceptions import TemplateDoesNotExist
# Create your views here.


class TemplatePageView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        self.template_name = self.kwargs["slug"]
        return kwargs





