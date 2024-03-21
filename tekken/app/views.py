import glob
import os
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings


class IndexView(View):
    def __init__(self):
        self.characters = self.get_characters()
        self.moves, self.move_type = self.get_buttons(self.xbox)

    template_name = 'index.html'
    BASE = "C:/Users/jeffm/VSC projects/tekken-8-web-app/tekken/app/static/app/"
    assets = "assets/"
    ps = "assets_ps/"
    xbox = "assets_xbox/"

    template_name = 'app/index.html'
    

    def get(self, request, *args, **kwargs):
        context = {}
        context['characters'] = self.characters
        context["moves"] = self.moves
        context["move_type"] = self.move_type
        
        print(self.moves[0])
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        if request.POST:
            user_character = request.POST.get("character")

        return render(request, self.template_name)

    def get_characters(self) -> dict:
        characters_path = self.BASE + "chararacters"
        characters =  {}
        for item in os.listdir(characters_path):
            name = item.split(".")[0]
            characters[name] = item
                
        characters['characters'] = characters
        return characters
        
    def get_buttons(self, image_dir) -> dict:
        static_dir = "static/app/"
        button_path = self.BASE + image_dir
        buttons = []
        for filename in os.listdir(button_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_url = os.path.join(static_dir, image_dir, filename)
                buttons.append(image_url)

        return buttons, image_dir