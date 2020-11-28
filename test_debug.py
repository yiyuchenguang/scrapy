from PIL import Image
img_path = "../image_animal/3-1F10G12T7.jpg"
path_save = "3-1F10G12T7_new_resize_2.jpg"
img = Image.open(img_path)

print("初始尺寸",img.size)
IMG = img.resize((900,500),Image.ANTIALIAS)
IMG.save(path_save,'JPEG')
print("ANTIALIAS",IMG.size)