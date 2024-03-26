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
            if button_color and button_color != request.session.get("button_dir"):
                request.session["button_dir"] = button_color

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
        image_dir = request.session.get("button_dir")
        button_path = self.static_path + image_dir
        buttons = []
        for filename in os.listdir(button_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"{image_dir}\\{filename}"
                buttons.append(image_url)

        self.buttons = buttons

    def get_context(self, request):
        request.session["button_dir"] = request.session.get("button_dir", "default")
        self.get_buttons(request)
        self.get_characters()
        self.context["characters"] = self.characters
        self.context["buttons"] = self.buttons
        self.context["button_colors"] = ["default", "playstation", "xbox"]


def merge_combo(combo_list, character=None):
    # Characters and images 
    static_path = "app\\static\\app\\"
    print(character)
    image_list = []
    if character.endswith("None") is False:
        character_path = static_path + character
        image_list.append(character_path)
        print(image_list)

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
        # print(character)
        combo = request.POST.get("combo")
        combo = eval(combo)
        
        if combo:
            merged_combo = merge_combo(combo, character)
            headers = {
                    'Content-Type': 'image/png',
                    'Content-Disposition': 'attachment; filename="test.png"'
                }
            response = HttpResponse(headers=headers)

            with io.BytesIO() as output:
                merged_combo.save(output, format="PNG")
                image_data = output.getvalue()
                response.write(image_data)
                
            return response

                

def remove_character(request):
    print("cat")
    if request.method == "POST":
        if request.session["user_character"]:
            request.session["user_character"] = None
    print(request.session["user_character"], "cat")
    return redirect(reverse("index"))