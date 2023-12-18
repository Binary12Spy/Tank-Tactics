import base64
import numpy as np
import random
from noise import snoise2

def generate_perlin_noise_image(width, height):
    vector = np.zeros((height, width), dtype=int)
    scale = 10.0  # Adjust this value to control the noise frequency

    # Generate random offsets
    x_offset = random.uniform(0, 1000)
    y_offset = random.uniform(0, 1000)

    for y in range(height):
        for x in range(width):
            noise_value = snoise2((x + x_offset) / scale, (y + y_offset) / scale)
            if noise_value < -0.6:
                sprite_value = 0
            if noise_value >= -0.6 and noise_value < 0.6:
                sprite_value = 1
            if noise_value >= 0.6:
                sprite_value = 2
            vector[y][x] = sprite_value

    return vector

array = np.ravel(generate_perlin_noise_image(80,50))
print(base64.b64encode(array))