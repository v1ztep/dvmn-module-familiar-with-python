from PIL import Image

image = Image.open('monro.jpg')
red, green, blue = image.split()

offset = 50
transparency = 0.3

coordinates_red_left = (offset, 0, image.width, image.height)  
coordinates_edges = (offset/2, 0, (image.width - offset/2), image.height)


cropped_red_1 = red.crop(coordinates_red_left) 
cropped_red_2 = red.crop(coordinates_edges)
overlay_red = Image.blend(cropped_red_1, cropped_red_2, transparency)


coordinates_blue_right = (0, 0, (image.width - offset), image.height)

cropped_blue_1 = blue.crop(coordinates_blue_right) 
cropped_blue_2 = blue.crop(coordinates_edges)
overlay_blue = Image.blend(cropped_blue_1, cropped_blue_2, transparency)


cropped_green = green.crop(coordinates_edges)

result = Image.merge('RGB', (overlay_red, cropped_green, overlay_blue))

result.thumbnail((80, 80))

result.save('result.jpg')
