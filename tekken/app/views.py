import glob
import os
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    def __init__(self):
        self.characters = {}
        self.buttons = []

    template_name = 'app/index.html'
    static_path = "app\\static\\app\\"
    context = {}

    

    def get(self, request, *args, **kwargs):
        if not self.context:
            self.get_context()

        return render(request, self.template_name, self.context)
    

    def post(self, request, *args, **kwargs):
        if request.POST:
            user_character = request.POST.get("character")
            request.session["user_character"] = user_character

            clear_combo = request.POST.get("clear")
            if clear_combo:
                request.session["combo"] = []

            move = request.POST.get("move-value")
            if move:
                if not request.session.get("combo"):
                    request.session["combo"] = [move]
                else:
                    move_list = request.session.get("combo")
                    move_list.append(move)
                    request.session["combo"] = move_list

        return render(request, self.template_name, self.context)

    def get_characters(self):
        characters_path = self.static_path  + "characters"
        characters =  {}
        for item in os.listdir(characters_path):
            name = item.split(".")[0]
            characters[name] = f"characters\\{item}"
        self.characters = characters
        
    def get_buttons(self, image_dir="xbox"):
        button_path = self.static_path + image_dir
        buttons = []
        for filename in os.listdir(button_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"xbox\\{filename}"
                buttons.append(image_url)

        self.buttons = buttons

    def get_context(self):
        self.get_buttons()
        self.get_characters()
        self.context["characters"] = self.characters
        self.context["buttons"] = self.buttons
        self.context["button_type"] = "default"
