import json
import os
from world_generation import generate_world
from civ import spawn_civs, monthly_civ_update


def convert_keys_to_str(d):
    if isinstance(d, dict):
        new_d = {}
        for k, v in d.items():
            if isinstance(k, tuple):
                k = ",".join(str(i) for i in k)
            new_d[k] = convert_keys_to_str(v)
        return new_d
    elif isinstance(d, list):
        return [convert_keys_to_str(i) for i in d]
    else:
        return d


def init_map_ownership(width, height):
    return [[None for _ in range(width)] for _ in range(height)]


def main():
    world = generate_world()
    map_width = world["map_width"]
    map_height = world["map_height"]
    biome_map = world["biome_map"]

    map_ownership = init_map_ownership(map_width, map_height)
    civs = spawn_civs(biome_map, map_width, map_height, num_civs=15)

    for civ in civs:
        for (x, y) in civ["territory"]:
            map_ownership[y][x] = civ["id"]

    for month in range(30 * 12):
        civs = monthly_civ_update(civs, biome_map, map_width, map_height, map_ownership)
        if month % 12 == 0:
            print(f"Year {month // 12} simulation running...")

    export_data = world.copy()
    export_data.update({
        "civs": civs,
        "map_ownership": map_ownership,
    })

    # Process civs to make them JSON serializable
    processed_civs = []
    for civ_dict in civs:  # civs is the list of civ dictionaries
        processed_civ = civ_dict.copy()  # Make a copy to avoid modifying original during iteration
        if "territory" in processed_civ and isinstance(processed_civ["territory"], set):
            # Convert the set of (x,y) tuples to a list of [x,y] lists
            processed_civ["territory"] = [list(tile_tuple) for tile_tuple in processed_civ["territory"]]
        processed_civs.append(processed_civ)

    export_data.update({
        "civs": processed_civs,  # Use the processed list of civs
        "map_ownership": map_ownership,
    })

    # Your existing convert_keys_to_str might still be useful for other parts of export_data,
    # or if any dictionary keys are tuples (e.g., in diplomacy if you used tuple keys directly).
    # However, for civ["territory"], we've handled it above.
    # If convert_keys_to_str was *only* for territory sets, you might not need it anymore
    # or it needs to be adapted.

    # Let's assume convert_keys_to_str is still needed for other things:
    export_data = convert_keys_to_str(export_data)

    # ... (your path setup and file writing logic) ...
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_output_dir = os.path.join(script_dir, 'backend', 'data')
    os.makedirs(absolute_output_dir, exist_ok=True)
    path = os.path.join(absolute_output_dir, 'world_data.json')

    print("Current working directory:", os.getcwd())
    print("Saving to:", os.path.abspath('backend/data/world_data.json'))

    print("Writing JSON now...")
    with open('backend/data/world_data.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)
    print("Write complete.")


if __name__ == "__main__":
    main()
