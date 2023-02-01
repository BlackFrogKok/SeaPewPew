from PIL import Image

image_path = 'Victory.png'

img = Image.open(image_path)
# изменяем размер
new_image = img.resize((960, 225))
#new_image.show()
# сохранение картинки
new_image.save('Victory2.png')
