from PIL import Image

image_path = 'table.png'

img = Image.open(image_path)
# изменяем размер
new_image = img.resize((400, 400))
#new_image.show()
# сохранение картинки
new_image.save('table2.png')
