import random

civ_profiles = {
    "Emberborn": {
        "affinity": ["Volcanic Zone"],
        "passive_traits": ["Immune to burning rain", "Boosts fire rituals"],
        "active_traits": ["Awaken the Fire Lord"],
        "notes": "Proud, isolated, internally competitive"
    },
    "Sylvar": {
        "affinity": ["Forest"],
        "passive_traits": ["Higher healing and diplomacy when in forest"],
        "active_traits": ["Whispering Web ritual"],
        "notes": "Deep tradition, hesitant to change"
    },
    "Deepforge": {
        "affinity": ["Mountains", "Caves"],
        "passive_traits": ["Forge Tempered (immune to fire damage)", "Mining speed bonus"],
        "active_traits": ["Build mechanical constructs or city-fortresses"],
        "notes": "Resistant to magic, culturally closed"
    },
    "Nymphic Folk": {
        "affinity": ["Lakes", "Rivers"],
        "passive_traits": ["Plague immunity boost", "Faster healing"],
        "active_traits": ["Water Communion"],
        "notes": "Peaceful, avoid conflict unless provoked"
    },
    "Bonebound": {
        "affinity": ["Ruins", "Wastelands"],
        "passive_traits": ["Thrive in death zones", "More likely to find powerful artifacts"],
        "active_traits": ["Raise ancestors during war"],
        "notes": "Feared by others; diplomacy difficult"
    },
    "Fluxkin": {
        "affinity": ["Wastelands", "Deserts"],
        "passive_traits": ["Resistant to change and climate"],
        "active_traits": ["Ignite resource-rich revolts"],
        "notes": "Rebellious, opportunistic"
    },
    "Fallen Gods": {
        "affinity": ["Ruins", "Arcane fields"],
        "passive_traits": ["Access to ancient knowledge (damaged codices)"],
        "active_traits": ["Memory Unlocked"],
        "notes": "Distrusted; can shift blame from the Great Shattering"
    }
}

def random_cultural_stat():
    return round(random.uniform(0.4, 0.9), 2)

def create_civ(profile_name, x, y):
    profile = civ_profiles[profile_name]
    civ = {
        "type": profile_name,
        "x": x,
        "y": y,
        "population": random.randint(100, 300),
        "affinity": profile["affinity"],
        "passive_traits": profile["passive_traits"],
        "active_traits": profile["active_traits"],
        "notes": profile["notes"],
        "culture": {
            "unity": random_cultural_stat(),
            "loyalty": random_cultural_stat(),
            "hygiene": random_cultural_stat(),
            "memory": random_cultural_stat(),
            "openness": random_cultural_stat(),
            "arcane_attunement": random_cultural_stat(),
        },
        "resources": {
            "food": random.randint(100, 200),
            "wood": random.randint(50, 150),
            "minerals": random.randint(50, 150)
        },
        "tech_level": 1,
        "nomadic": False
    }
    return civ

def spawn_civs(biome_map, map_width, map_height, num_civs=15):
    civs = []
    taken = set()

    for civ_id in range(num_civs):
        while True:
            x = random.randint(0, map_width - 1)
            y = random.randint(0, map_height - 1)
            if biome_map[y][x] != 'Ocean' and (x, y) not in taken:
                taken.add((x, y))
                break

        civ = {
            "id": civ_id,
            "name": f"Civ{civ_id}",
            "territory": {(x, y)},
            "cities": [{"location": (x, y), "population": 500}],
        }

        civs.append(civ)

    return civs


def get_adjacent_tiles(x, y, map_width, map_height):
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in deltas:
        nx, ny = x + dx, y + dy
        if 0 <= nx < map_width and 0 <= ny < map_height:
            yield (nx, ny)


def monthly_civ_update(civs, biome_map, map_width, map_height, map_ownership):
    for civ in civs:
        new_tiles = set()

        for (tx, ty) in civ["territory"]:
            for nx, ny in get_adjacent_tiles(tx, ty, map_width, map_height):
                if map_ownership[ny][nx] is None and biome_map[ny][nx] != 'Ocean':
                    if random.random() < 0.2:
                        new_tiles.add((nx, ny))

        for tile in new_tiles:
            civ["territory"].add(tile)
            map_ownership[tile[1]][tile[0]] = civ["id"]

        if len(civ["territory"]) > len(civ["cities"]) * 20 and random.random() < 0.1:
            open_tiles = [t for t in civ["territory"] if all(c["location"] != t for c in civ["cities"])]
            if open_tiles:
                new_city = {
                    "location": random.choice(open_tiles),
                    "population": 200
                }
                civ["cities"].append(new_city)

        for city in civ["cities"]:
            city["population"] = int(city["population"] * random.uniform(1.01, 1.05))

    return civs