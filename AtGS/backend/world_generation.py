import numpy as np
import json
import random
from opensimplex import OpenSimplex

map_width = 1920
map_height = 1080

scale = 200.0
octaves = 6
persistence = 0.5
lacunarity = 2.0
sea_level = 0.4


def generate_noise_map(width, height, scale, seed=0, octaves_simplex=6, persistence_simplex=0.5,
                       lacunarity_simplex=2.0):  # Parameter für FBM hinzugefügt
    print(f"generate_noise_map (opensimplex): START - w:{width}, h:{height}, sc:{scale}, seed:{seed}")
    simplex = OpenSimplex(seed=seed)
    noise_map = np.zeros((height, width))
    print(f"generate_noise_map: np.zeros created")

    for y in range(height):
        if y % (height // 10 if height >= 10 else 1) == 0:  # Print progress
            print(f"generate_noise_map: Processing row {y}/{height}")
        for x in range(width):
            # Fractional Brownian Motion (FBM)
            current_amplitude = 1.0
            current_frequency = 1.0
            total_value = 0.0

            for i in range(octaves_simplex):
                nx = x / scale * current_frequency
                ny = y / scale * current_frequency
                try:
                    # OpenSimplex noise2 gibt Werte im Bereich [-1, 1] zurück
                    noise_val = simplex.noise2(nx, ny)
                    total_value += noise_val * current_amplitude
                except Exception as e:
                    print(f"ERROR in OpenSimplex noise2 at x={x}, y={y}, nx={nx}, ny={ny}: {e}")
                    # Hier sollte kein C-Crash passieren, eher eine Python Exception

                current_amplitude *= persistence_simplex
                current_frequency *= lacunarity_simplex

            noise_map[y][x] = total_value

    print(f"generate_noise_map: noise generation loop finished")

    # Normalisieren auf [0,1]
    min_val = noise_map.min()
    max_val = noise_map.max()
    if max_val == min_val:  # Verhindert Division durch Null, falls alle Werte gleich sind
        noise_map.fill(0.5)  # oder einen anderen Standardwert
    else:
        noise_map = (noise_map - min_val) / (max_val - min_val)

    print(f"generate_noise_map: Normalization complete")
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

def generate_world():
    seed = random.randint(0, 99999)
    print("generate_world: Generating height_map...")
    height_map = np.array(
        generate_noise_map(map_width, map_height, scale,  # Positionale Argumente: width, height, scale
                           seed=seed,  # Schlüsselwortargument für seed
                           octaves_simplex=octaves,
                           # Schlüsselwortargument für octaves_simplex (verwendet die globale Variable 'octaves')
                           persistence_simplex=persistence,
                           # Schlüsselwortargument für persistence_simplex (verwendet globale 'persistence')
                           lacunarity_simplex=lacunarity)
        # Schlüsselwortargument für lacunarity_simplex (verwendet globale 'lacunarity')
    )
    print("generate_world: height_map generated.")

    print("generate_world: Generating temp_map...")
    temp_map = np.array(
        generate_noise_map(map_width, map_height, scale * 2,  # Positionale Argumente, beachte scale * 2
                           seed=seed,
                           octaves_simplex=octaves,
                           persistence_simplex=persistence,
                           lacunarity_simplex=lacunarity)
    )
    print("generate_world: temp_map generated.")

    print("generate_world: Generating moist_map...")
    moist_map = np.array(
        generate_noise_map(map_width, map_height, scale * 1.5,  # Positionale Argumente, beachte scale * 1.5
                           seed=seed,
                           octaves_simplex=octaves,
                           persistence_simplex=persistence,
                           lacunarity_simplex=lacunarity)
    )

    for y_idx in range(map_height):
        lat_factor = 1 - abs((y_idx / map_height) * 2 - 1)
        temp_map[y_idx, :] *= lat_factor

    biome_map = []
    for y in range(map_height):
        row = []
        for x in range(map_width):
            biome = classify_biome(height_map[y, x], temp_map[y, x], moist_map[y, x])
            row.append(biome)
        biome_map.append(row)

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

    food_map = np.clip(height_map * 10, 0, 10).tolist()
    wood_map = np.clip(temp_map * 10, 0, 10).tolist()
    minerals_map = np.clip(moist_map * 10, 0, 10).tolist()

    return {
        "map_width": map_width,
        "map_height": map_height,
        "height_map": height_map.tolist(),
        "temp_map": temp_map.tolist(),
        "moist_map": moist_map.tolist(),
        "biome_map": biome_map,
        "biome_colors": biome_colors,
        "food_map": food_map,
        "wood_map": wood_map,
        "minerals_map": minerals_map,
    }
