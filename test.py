from PIL import Image, ImageDraw, ImageFont

img_path = "../image_animal/3-1F10G12T7.jpg"
path_save = "3-1F10G12T7_new.jpg"

im = Image.open(img_path)
im.thumbnail((900,500),Image.ANTIALIAS)
print(im.format, im.size, im.mode)
im.save(path_save,'JPEG')
