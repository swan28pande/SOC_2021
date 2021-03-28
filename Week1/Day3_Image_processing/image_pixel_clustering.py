"""
Step1: Take any .png image (Use pillow to convert to png to np array)
Step2: Perform kmeans on the pixel intensities
Step3: Visualize the image after clustering with 3,5,10 clusters

Repeat the process but cluster based on pixel intensity & position

Write ur code here
"""

from PIL import Image
import numpy as np
from kmeans import kmeans
import matplotlib.pyplot as plt

image = Image.open("test_image.png")

image_array = np.array(image)
image_shape = image_array.shape

#plt.imshow(image_array)
#plt.show()

numColors = 10
centroids,cluster_ids = kmeans(image_array.reshape((-1,image_shape[2])),numColors)

final_image_array = np.zeros((image_shape[0]*image_shape[1],image_shape[2]))
for pixel_id in range(final_image_array.shape[0]):
    final_image_array[pixel_id,:] = centroids[cluster_ids[pixel_id]]
final_image_array=final_image_array.reshape(image_shape).astype(int)

#plt.imshow(final_image_array)
#plt.show()

print(final_image_array.shape)
final_image = Image.fromarray(final_image_array[:,:,0:3])
new_img.save("final_image.png")