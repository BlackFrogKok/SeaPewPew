from PIL import Image

image_path = 'FourDeckShip.png'

img = Image.open(image_path)
# изменяем размер
new_image = img.resize((50, 210))
new_image.show()
# сохранение картинки
new_image.save('FourDeckShip2.png')
