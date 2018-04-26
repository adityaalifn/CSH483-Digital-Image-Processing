from PIL import Image 
import numpy as np
image_file = Image.open("./static/img/colorful-ink-water-38259551.jpg") # open colour image
image_file = image_file.convert('1') # convert image to black and white
print(np.asarray(image_file).shape)
image_file.save('result.png')