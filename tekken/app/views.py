import glob
import os
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect


class IndexView(View):
    def __init__(self):
        self.characters = {}
        self.buttons = []

    template_name = 'app/index.html'
    static_path = "app\\static\\app\\"
    context = {}

    

    def get(self, request, *args, **kwargs):
        self.get_context(request)

        return render(request, self.template_name, self.context)
    

    def post(self, request, *args, **kwargs):
        if request.POST:
            button_color = request.POST.get("button_colors")
            if button_color and button_color != request.session.get("button_type"):
                request.session["button_type"] = button_color

            user_character = request.POST.get("character")
            if user_character:
                request.session["user_character"] = user_character

            clear_combo = request.POST.get("clear")
            if clear_combo:
                request.session["combo"] = []

            undo = request.POST.get("undo")
            if undo:
                move_list = request.session.get("combo")
                if move_list:
                    move_list.pop()
                request.session["combo"] = move_list

            move = request.POST.get("move-value")
            if move:
                if not request.session.get("combo"):
                    request.session["combo"] = [move]
                else:
                    move_list = request.session.get("combo")
                    move_list.append(move)
                    request.session["combo"] = move_list

        return redirect(reverse("index"), args=[self.context])

    def get_characters(self):
        characters_path = self.static_path  + "characters"
        characters =  {}
        for item in os.listdir(characters_path):
            name = item.split(".")[0]
            characters[name] = f"characters\\{item}"
        self.characters = characters
        
    def get_buttons(self, request):
        image_dir = request.session.get("button_type")
        button_path = self.static_path + image_dir
        buttons = []
        for filename in os.listdir(button_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"{image_dir}\\{filename}"
                buttons.append(image_url)

        self.buttons = buttons

    def get_context(self, request):
        request.session["button_type"] = request.session.get("button_type", "default")
        self.get_buttons(request)
        self.get_characters()
        self.context["characters"] = self.characters
        self.context["buttons"] = self.buttons
        self.context["button_colors"] = ["default", "playstation", "xbox"]
