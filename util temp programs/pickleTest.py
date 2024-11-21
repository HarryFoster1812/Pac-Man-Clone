import json
from PIL import Image

root =  Image.open("assets/Dot.png")


with open("file.json", "wb") as my_file:
    json.dump(root, my_file)