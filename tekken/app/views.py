from django.shortcuts import render
from django.views.generic import View
from .templates.app


class IndexView(View):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        pass