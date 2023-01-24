from PIL import Image

image_path = 'Explosion.png'

img = Image.open(image_path)
# изменяем размер
new_image = img.resize((50, 50))
new_image.show()
# сохранение картинки
new_image.save('Explosion2.png')
