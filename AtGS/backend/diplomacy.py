import random

# Simple diplomacy states
DIPLOMACY_STATES = ["Neutral", "Allied", "At War", "Truce"]

def init_diplomacy(civs):
    """Initialize a diplomacy matrix between civs as Neutral."""
    n = len(civs)
    relations = {}
    for i in range(n):
        for j in range(i+1, n):
            relations[(i, j)] = "Neutral"
    return relations

def update_diplomacy(civs, relations):
    """
    Basic diplomacy logic per tick:
    - Closer civs may become allied or at war based on random chance
    - Further civs remain Neutral or form Truce
    """
    for (i, j), state in relations.items():
        civ_a = civs[i]
        civ_b = civs[j]

        dist = abs(civ_a["x"] - civ_b["x"]) + abs(civ_a["y"] - civ_b["y"])

        if dist < 50:  # Close proximity
            if state == "Neutral":
                if random.random() < 0.05:
                    relations[(i,j)] = random.choice(["Allied", "At War"])
            elif state == "Allied":
                if random.random() < 0.02:
                    relations[(i,j)] = "Neutral"
            elif state == "At War":
                if random.random() < 0.01:
                    relations[(i,j)] = "Truce"
        else:
            # Far civs tend to be neutral or truce
            if state == "Neutral" and random.random() < 0.01:
                relations[(i,j)] = "Truce"
            elif state == "Truce" and random.random() < 0.005:
                relations[(i,j)] = "Neutral"
    return relations
