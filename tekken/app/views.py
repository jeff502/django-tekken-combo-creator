import glob
import os
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'index.html'
    BASE = "C:/Users/jeffm/VSC projects/tekken-8-web-app/tekken/app/static/app/"
    assets = BASE + "assets"
    ps = BASE + "assets_ps"
    xbox = BASE + "assets_xbox"
    chars = BASE + "char"
    buttons = None

    template_name = 'app/index.html'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Home'
    #     return context

    def get(self, request, *args, **kwargs):
        if self.buttons is None:
            self.buttons = self.ps
        context = {}
        characters =  {}
        for item in os.listdir(self.chars):
            name = item.split(".")[0]
            characters[name] = item
                
        context['characters'] = characters
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        pass