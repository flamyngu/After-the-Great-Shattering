import numpy as np
import json
import random
from noise import pnoise2
import os
# Use your target resolution here or pass it as args
map_width = 1920
map_height = 1080

scale = 200.0  # noise scale factor, tweak to get good noise frequency
octaves = 6
persistence = 0.5
lacunarity = 2.0
sea_level = 0.4
variation_scale = 0.3
num_civs = 15

def generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed=0):
    noise_map = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            nx = x / scale
            ny = y / scale
            noise_map[y][x] = pnoise2(nx, ny, octaves=octaves, persistence=persistence,
                                      lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
    # Normalize to [0,1]
    noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min())
    return noise_map.tolist()

def classify_biome(h, t, m):
    if h < sea_level:
        return 'Ocean'
    elif h < sea_level + 0.05:
        return 'Beach'
    else:
        if t > 0.7:
            if m < 0.3:
                return 'Desert'
            elif m > 0.7:
                return 'Swamp'
            else:
                return 'Grassland'
        elif t > 0.4:
            if m < 0.3:
                return 'Grassland'
            else:
                return 'Forest'
        else:
            if h > 0.8:
                return 'Snow'
            elif m > 0.5:
                return 'Taiga'
            else:
                return 'Tundra'

# Biome colors and traits same as before...

import numpy as np
import json
import random
from noise import pnoise2

# (Your existing code here...)

def main():
    seed = random.randint(0, 80)
    print(f"Generating world with seed: {seed}")

    height_map = np.array(generate_noise_map(map_width, map_height, scale, octaves, persistence, lacunarity, seed=seed))
    temp_map = np.array(generate_noise_map(map_width, map_height, scale*2, octaves, persistence, lacunarity, seed=seed))
    moist_map = np.array(generate_noise_map(map_width, map_height, scale*1.5, octaves, persistence, lacunarity, seed=seed))

    # Latitude temperature adjustment
    for y in range(map_height):
        lat_factor = 1 - abs((y / map_height) * 2 - 1)
        temp_map[y, :] *= lat_factor

    biome_map = []
    for y in range(map_height):
        row = []
        for x in range(map_width):
            biome = classify_biome(height_map[y, x], temp_map[y, x], moist_map[y, x])
            row.append(biome)
        biome_map.append(row)

    # Example biome colors dictionary
    biome_colors = {
        'Ocean': [0, 0, 128],
        'Beach': [238, 214, 175],
        'Desert': [210, 180, 140],
        'Swamp': [47, 79, 47],
        'Grassland': [124, 252, 0],
        'Forest': [34, 139, 34],
        'Snow': [255, 250, 250],
        'Taiga': [0, 100, 0],
        'Tundra': [176, 196, 222],
    }

    # Generate placeholder resources (food, wood, minerals) as arrays of floats, example:
    food_map = np.clip(height_map * 10, 0, 10).tolist()
    wood_map = np.clip(temp_map * 10, 0, 10).tolist()
    minerals_map = np.clip(moist_map * 10, 0, 10).tolist()

    # Spawn civs randomly on land tiles:
    civs = []
    attempts = 0
    while len(civs) < 15 and attempts < 10000:
        x = random.randint(0, map_width-1)
        y = random.randint(0, map_height-1)
        if biome_map[y][x] != 'Ocean':
            civs.append({"x": x, "y": y})
        attempts += 1

    # Compose data dict for export
    export_data = {
        "map_width": map_width,
        "map_height": map_height,
        "height_map": height_map.tolist(),      # optional, for other uses
        "temp_map": temp_map.tolist(),          # optional
        "moist_map": moist_map.tolist(),        # optional
        "biome_map": biome_map,
        "biome_colors": biome_colors,
        "food_map": food_map,
        "wood_map": wood_map,
        "minerals_map": minerals_map,
        "civs": civs
    }

    print("Current working directory:", os.getcwd())
    print("Saving to:", os.path.abspath('backend/data/world_data.json'))

    print("Writing JSON now...")
    with open('backend/data/world_data.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f)
    print("Write complete.")

if __name__ == "__main__":
    main()

