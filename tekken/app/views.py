import os
import io
from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect
from PIL import Image
from django.http import HttpResponse


class IndexView(View):
    def __init__(self):
        self.characters = {}
        self.attack_buttons = []
        self.movement_buttons = []
        self.general_buttons = []
        self.stance_buttons = []

    template_name = 'app/index.html'
    static_path = "app\\static\\app\\"
    context = {}

    
    def get(self, request, *args, **kwargs):
        self.get_context(request)
        return render(request, self.template_name, self.context)
    

    def post(self, request, *args, **kwargs):
        if request.POST:
            self.handle_post_request(request)
        return redirect(reverse("index"))

    def handle_post_request(self, request):
        if request.POST.get("button_colors"):
            request.session["button_dir"] = request.POST.get("button_colors")

        if request.POST.get("move-value"):
            move = request.POST.get("move-value")
            if len(request.session.get("combo")) >= 50:
                request.session["max"] = True
            else:
                if not request.session.get("combo"):
                    request.session["combo"] = [move]
                else:
                    move_list = request.session.get("combo")
                    move_list.append(move)
                    request.session["combo"] = move_list
                
        if request.POST.get("character"):
                request.session["user_character"] = request.POST.get("character")

        if request.POST.get("clear"):
            request.session["combo"] = []

        if request.POST.get("undo"):
            move_list = request.session.get("combo", [])
            if move_list:
                move_list.pop()
        
            request.session["combo"] = move_list

        return redirect(reverse("index"))
        


    def get_characters(self):
        characters_path = self.static_path  + "characters"
        characters =  {}
        for item in os.listdir(characters_path):
            name = item.split(".")[0]
            characters[name] = f"characters\\{item}"
        self.characters = characters
        
    def get_attack_buttons(self, request):
        image_dir = request.session.get("button_dir", "default")
        button_path = self.static_path + image_dir
        buttons = []
        for filename in os.listdir(button_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"{image_dir}\\{filename}"
                buttons.append(image_url)

        self.attack_buttons = buttons

    def get_buttons(self):
        image_dirs = {
            "general": self.general_buttons,
            "movement": self.movement_buttons,
            "stances": self.stance_buttons
        }
        for image_dir, buttons in image_dirs.items():
            button_path = self.static_path + image_dir
            for filename in os.listdir(button_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    image_url = f"{image_dir}\\{filename}"
                    buttons.append(image_url)


    def get_context(self, request):
        self.get_attack_buttons(request)
        self.get_buttons()
        self.get_characters()
        request.session["stance_buttons"] = request.session.get("stance_buttons", False)
        self.context["characters"] = self.characters
        self.context["attack_buttons"] = self.attack_buttons
        self.context["movement_buttons"] = self.movement_buttons
        self.context["general_buttons"] = self.general_buttons
        self.context["stance_buttons"] = self.stance_buttons
        self.context["button_colors"] = ["default", "playstation", "xbox"]
        request.session["max"] = len(request.session.get("combo", [])) >= 50


def merge_combo(combo_list, character=None):
    # Characters and images 
    static_path = "app\\static\\app\\"
    image_list = []
    if character.endswith("None") is False and character is not None:
        character_path = static_path + character
        image_list.append(character_path)

    for attack in combo_list:
        image_list.append(f"{static_path}{attack}")
    images = [Image.open(x) for x in image_list]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    return new_im
 

def download_combo(request):
    if request.method == "POST":
        character = request.POST.get("user_character")
        combo = request.POST.get("combo")
        combo = eval(combo)
        
        if combo:
            merged_combo = merge_combo(combo, character)
            headers = {
                    'Content-Type': 'image/png',
                    'Content-Disposition': 'attachment; filename="combo.png"'
                }
            response = HttpResponse(headers=headers)

            with io.BytesIO() as output:
                merged_combo.save(output, format="PNG")
                image_data = output.getvalue()
                response.write(image_data)
                
            return response
    return response


def remove_character(request):
    if request.method == "POST":
        if request.session["user_character"]:
            request.session["user_character"] = None

    return redirect(reverse("index"))


def toggle_stances(request):
    if request.method == "POST":
        request.session["stance_buttons"] = not request.session.get("stance_buttons")

    return redirect(reverse("index"))