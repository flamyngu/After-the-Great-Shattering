# 🌍 Fractured Realms: A Post-Apocalyptic Fantasy World Simulation

**Fractured Realms** is a procedural, autonomous world simulation set in a post-apocalyptic fantasy universe. Civilizations rise, fall, migrate, and interact based on terrain, history, and inner culture. Inspired by *LotR*, *DnD*, *The Bartimaeus Trilogy*, *Game of Thrones*, and *The Alchemyst*, the simulation explores what happens after the world shatters — and how civilizations claw their way back from myth and ruin.

---

## 🧩 Core Concept

Centuries after a magical catastrophe known only as **The Great Shattering**, the world is left scarred. Rain sometimes burns. Magic is unstable. Cities lie buried under ash, sea, or forest. Civilizations born of myth — Elves, Dwarves, Nymphs, and others — must adapt or perish in a fractured, unpredictable world.

There is no central player. The simulation runs **without interference**, but the system supports the possibility of **observer intervention**, such as:
- Granting civilizations relics or knowledge
- Nudging diplomacy
- Awakening ancient threats or saviors

---

## 🌐 World Mechanics

### 🗺 Terrain Types

| Terrain       | Traits |
|---------------|--------|
| **Forest**     | Rich in herbs and wildlife, slows armies, aids stealth and healing. Sylvar affinity. |
| **Mountain**   | High defense, mineral-rich, mining opportunities. Deepforge affinity. |
| **Lake**       | Fertile and mystical. Boosts healing, magic, and Nymphic rituals. |
| **Wasteland**  | Scarred land. Low yield but high ruin/relic chance. |
| **Volcanic Zone** | Heat, danger, and powerful magic nodes. Emberborn affinity. |
| **Ruins**      | Pre-Shattering remnants. Risk and reward. Bonebound and Fallen Gods affinity. |

---

### 🌋 Terrain-Based Behavior

Civs spawning in terrain they don't understand become **nomadic** until they reach a suitable biome:
- Nomads follow terrain logic (e.g. rivers → sea, elevation → mountains)
- Can't grow population or build permanent structures
- Explore and uncover ruins more rapidly

---

## 🏛 Civilizations (Civs)

Each civilization has:
- **Passive Traits**: Persistent bonuses or tendencies
- **Active Traits**: Abilities or effects triggered in specific conditions
- **Cultural Profile**: Determines openness, memory, unity, hygiene, arcane attunement

### Civs Overview

#### 🐉 Emberborn
- **Affinity**: Volcanic zones
- **Passive**: Immune to burning rain; boosts fire rituals
- **Active**: "Awaken the Fire Lord" – Summon a fire avatar during crisis
- **Notes**: Proud, isolated, internally competitive

#### 🧝 Sylvar (Elves)
- **Affinity**: Forests
- **Passive**: Higher healing and diplomacy when in forest
- **Active**: Ritual to unify forests under a "Whispering Web"
- **Notes**: Deep tradition, hesitant to change

#### 🛠 Deepforge (Dwarves)
- **Affinity**: Mountains & caves
- **Passive**: "Forge Tempered" – Immune to fire damage; mining speed bonus
- **Active**: Build mechanical constructs or city-fortresses
- **Notes**: Resistant to magic, culturally closed

#### 🌊 Nymphic Folk
- **Affinity**: Lakes & rivers
- **Passive**: Plague immunity boost, faster healing
- **Active**: "Water Communion" – Redirect river or summon water elemental
- **Notes**: Peaceful, avoid conflict unless provoked

#### 🦴 Bonebound
- **Affinity**: Ruins & wastelands
- **Passive**: Thrive in death zones; more likely to find powerful artifacts
- **Active**: Raise ancestors during war
- **Notes**: Feared by others; diplomacy difficult

#### 🔥 Fluxkin
- **Affinity**: Wastelands and deserts
- **Passive**: Resistant to change and climate
- **Active**: Can ignite resource-rich revolts to seize nearby tiles
- **Notes**: Rebellious, opportunistic

#### 👁 Fallen Gods
- **Affinity**: Ruins, arcane fields
- **Passive**: Access to ancient knowledge (damaged codices)
- **Active**: "Memory Unlocked" – Reveal past tech or rituals
- **Notes**: Distrusted; can use diplomacy to shift blame from the Great Shattering

---

## 🧭 Diplomacy & Proximity Effects

| Civilization | Close Spawn Outcome | Far Spawn Outcome |
|--------------|---------------------|-------------------|
| Elves ↔ Dwarves | Early conflict over trees/mining rights | Mutual indifference, minor trade |
| Nymphs ↔ Emberborn | Drought/flood conflicts | Nymphs purify burned zones |
| Fallen Gods ↔ All | High distrust → conflict | May trade knowledge at distance |
| Bonebound ↔ Elves | Cultural hatred | Avoidance, fear-based diplomacy |
| Fluxkin ↔ Anyone | Raid risk nearby | Peaceful when far, migratory |
| Deepforge ↔ Bonebound | Ally in ruins | Religious/philosophical conflict |

---

## 🧠 Internal Culture System

Each civ tracks:

- **Unity %**
- **Loyalty to Ruler %**
- **Hygiene %**
- **Cultural Memory %**
- **Openness %**
- **Arcane Attunement %**

These influence:
- Civil war risk
- Plague outbreaks
- Hero emergence
- Governance shifts

---

## ⚔ Hero System

Rare individuals who:
- Emerge under specific conditions (e.g. famine, prophecy)
- Shift entire civilizations’ trajectories
- Can replace leaders or cause civil war

**Attributes:**
- Origin, Role, Motivation, Unique Power

**Example:**
- *Glintstone the Enlightened* (Dwarf Hero) — invents golem tech, sparks civil war after king suppresses it

---

## 👑 Leadership System

- Each civ has a leader with:
  - Loyalty, Control, Competence, Ambition, Hero Tolerance
- Can suppress, empower, or be overthrown by heroes
- Leadership style evolves (Monarchy, Theocracy, Council, etc.)

---

## 🗓 Simulation Tick System

Each **year**, the simulation processes:
1. Environmental changes (burning rain, quakes)
2. Civ state updates (population, unity, terrain match)
3. Leader and hero actions
4. Random and triggered events
5. Civ-to-civ diplomacy
6. Migration logic for nomads
7. Culture and resource updates

---

## 🧭 World Generation (WIP)

- Uses **fractal noise + fBM** to generate elevation
- Simulates rivers, erosion, volcanoes
- Assigns terrain types based on height/moisture
- Magic level overlay via secondary noise

---

## 🛠 Dev Status

| Feature                   | Status         |
|---------------------------|----------------|
| Terrain Generation (noise) | ✅ Base done     |
| Civ Traits + Culture       | ❌ Finalized     |
| Diplomacy Table            | ❌ Finalized     |
| Hero System                | ❌ Designed      |
| Leader System              | ❌ Designed      |
| Yearly Simulation Engine   | 🛠 In Progress   |
| Map/Grid Placement Logic   | 🛠 Building      |

---

## 📘 Inspirations

- Fractal Philosophy (YouTube) https://www.youtube.com/@FractalPhilosophy
- LOTR, GoT, DnD
- Bartimaeus Trilogy (Stroud)
- The Alchemyst (Michael Scott)
- Dwarf Fortress
- Old World

---

## 📄 License

MIT License (You’re free to fork and expand — please link back if you release a game or story based on this world.)

---

## 🖊️ How to Run

1. copy the repo with "git copy"
2. make sure you have installed numpy and opensimplex 
3. execute main.py 
4. run  python -m http.server 8000 in your local shell
5. open http://localhost:8000/frontend/index.html in your browser

---
