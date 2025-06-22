// Top-level declarations for shared variables
let worldData = null;
let frame = 0;
const totalFrames = 2400; // 200 years * 12 months (for JS simulation, if intended)

let canvas; // Main canvas for civs
let ctx;    // Context for main canvas
let info;   // Element to display information

let biomeCanvas; // Offscreen canvas for biomes
let biomeCtx;    // Context for biome canvas

const DEBUG_DRAW_SCALE_TERRITORY = 3; // Make territory tiles 3x3 for visibility
const DEBUG_DRAW_SCALE_CITY = 5;     // Make city radius 5 for visibility

async function loadData() {
  console.log('loadData: Attempting to load world data...');
  if (info) info.textContent = 'Loading world data...';
  try {
    const response = await fetch('../backend/backend/data/world_data.json');
    if (!response.ok) {
      console.error('loadData: Failed to load world data HTTP error:', response.status, response.statusText);
      if (info) info.textContent = `Failed to load world data: ${response.status}`;
      return;
    }
    worldData = await response.json();
    console.log('loadData: World data JSON loaded and parsed.');

    if (!worldData || !worldData.map_width || !worldData.map_height) {
        console.error('loadData: World data is invalid or incomplete (missing map_width/map_height).');
        if (info) info.textContent = 'Error: World data is invalid.';
        return;
    }
    console.log(`loadData: Map dimensions: ${worldData.map_width}x${worldData.map_height}`);

    canvas.width = Math.floor(worldData.map_width);
    canvas.height = Math.floor(worldData.map_height);

    createBiomeCanvas(); // This seems to work as biomes are visible

    if (!worldData.civs || !Array.isArray(worldData.civs)) {
        console.warn('loadData: worldData.civs is missing or not an array.');
        worldData.civs = []; // Ensure it's an array to prevent errors later
    }

    console.log(`loadData: Number of civs from JSON: ${worldData.civs.length}`);

    for (let i = 0; i < worldData.civs.length; i++) {
      let civ = worldData.civs[i];
      civ.id = civ.id !== undefined ? civ.id : `CivUnknown_${i}`; // Ensure ID for logging
      civ.js_population = 10; // JS simulation population, distinct from Python's city.population
      civ.color = getRandomColor();

      console.log(`loadData: Initializing civ ID ${civ.id} (index ${i}). Color: ${civ.color}`);
      console.log(`  Civ ${civ.id} territory from JSON:`, civ.territory ? `Array with ${civ.territory.length} tiles` : 'MISSING/NULL');
      if (civ.territory && civ.territory.length > 0) console.log(`    First territory tile: [${civ.territory[0].join(',')}]`);
      console.log(`  Civ ${civ.id} cities from JSON:`, civ.cities ? `Array with ${civ.cities.length} cities` : 'MISSING/NULL');
      if (civ.cities && civ.cities.length > 0) console.log(`    First city location: [${civ.cities[0].location ? civ.cities[0].location.join(',') : 'N/A'}]`);


      // Initialize civ.x and civ.y for JS simulation (updateCivs)
      // These are NOT directly used for drawing territory/cities from Python output
      if (typeof civ.x === 'undefined' || typeof civ.y === 'undefined') {
        if (civ.cities && civ.cities.length > 0 && civ.cities[0].location && civ.cities[0].location.length === 2) {
          civ.x = civ.cities[0].location[0];
          civ.y = civ.cities[0].location[1];
        } else if (civ.territory && civ.territory.length > 0 && civ.territory[0] && civ.territory[0].length === 2) {
          civ.x = civ.territory[0][0];
          civ.y = civ.territory[0][1];
        } else {
          console.warn(`loadData: Civ ID ${civ.id} has no cities or territory in JSON to derive x,y for JS sim. Defaulting position to center.`);
          civ.x = Math.floor(worldData.map_width / 2);
          civ.y = Math.floor(worldData.map_height / 2);
        }
        console.log(`  Civ ID ${civ.id} JS sim coords (x,y) set to: ${civ.x}, ${civ.y}`);
      }
    }

    if (worldData.civs.length === 0) {
        console.warn("loadData: No civilizations were loaded from the JSON. Nothing to draw for civs.");
    }


    if (info) info.textContent = 'Simulation started';
    requestAnimationFrame(drawFrame);
  } catch (e) {
    console.error('loadData: CRITICAL ERROR loading or processing world data:', e);
    if (info) info.textContent = 'Error loading or processing world data. Check console.';
  }
}

function createBiomeCanvas() {
  // ... (this function seems to be working correctly, keep as is)
  biomeCanvas = document.createElement('canvas');
  biomeCtx = biomeCanvas.getContext('2d');
  const width = Math.floor(worldData.map_width);
  const height = Math.floor(worldData.map_height);

  biomeCanvas.width = width;
  biomeCanvas.height = height;
  const imgData = biomeCtx.createImageData(width, height);

  const data = imgData.data;
  for (let y = 0; y < worldData.map_height; y++) {
    for (let x = 0; x < worldData.map_width; x++) {
      const biome = worldData.biome_map[y][x];
      const color = worldData.biome_colors[biome] || [0, 0, 0];
      const idx = (y * worldData.map_width + x) * 4;
      data[idx] = color[0];
      data[idx + 1] = color[1];
      data[idx + 2] = color[2];
      data[idx + 3] = 255;
    }
  }
  biomeCtx.putImageData(imgData, 0, 0);
  console.log("createBiomeCanvas: Biome canvas created and rendered.");
}

function drawCivs() {
  if (!worldData || !worldData.civs || worldData.civs.length === 0) {
    // console.log("drawCivs: No civs to draw."); // Can be noisy, enable if needed
    return;
  }

  // console.log("drawCivs: Starting to draw civs. Count:", worldData.civs.length);

  for (let civ of worldData.civs) {
    ctx.fillStyle = civ.color; // Base color for the civ

    // Draw Territory
    if (Array.isArray(civ.territory) && civ.territory.length > 0) {
      // console.log(`drawCivs: Drawing territory for Civ ID ${civ.id}. Tiles: ${civ.territory.length}. Color: ${civ.color}`);
      for (const tile of civ.territory) {
        if (Array.isArray(tile) && tile.length === 2) {
          const [x, y] = tile;
          if (typeof x === 'number' && typeof y === 'number') {
            ctx.fillRect(x, y, DEBUG_DRAW_SCALE_TERRITORY, DEBUG_DRAW_SCALE_TERRITORY);
          } else {
            console.warn(`drawCivs: Invalid tile [${x},${y}] in territory for civ ID ${civ.id}`);
          }
        } else {
           console.warn(`drawCivs: Malformed tile data in territory for civ ID ${civ.id}:`, tile);
        }
      }
    } else {
      // console.log(`drawCivs: Civ ID ${civ.id} has no territory to draw or territory is not an array.`);
    }

    // Draw Cities
    if (Array.isArray(civ.cities) && civ.cities.length > 0) {
      // console.log(`drawCivs: Drawing cities for Civ ID ${civ.id}. Count: ${civ.cities.length}.`);
      for (const city of civ.cities) {
        if (city && city.location && Array.isArray(city.location) && city.location.length === 2) {
          const [cx, cy] = city.location;
           if (typeof cx === 'number' && typeof cy === 'number') {
            ctx.fillStyle = shadeColor(civ.color, -40); // Darker color for city
            ctx.beginPath();
            ctx.arc(cx, cy, DEBUG_DRAW_SCALE_CITY, 0, 2 * Math.PI);
            ctx.fill();
          } else {
            console.warn(`drawCivs: Invalid city location [${cx},${cy}] for civ ID ${civ.id}`);
          }
        } else {
          console.warn(`drawCivs: Malformed city data or missing location for civ ID ${civ.id}:`, city);
        }
      }
    } else {
      // console.log(`drawCivs: Civ ID ${civ.id} has no cities to draw or cities is not an array.`);
    }
  }
}

function updateCivs() {
  if (!worldData || !worldData.civs) return;

  for (let civ of worldData.civs) {
    let currentX = Math.floor(civ.x);
    let currentY = Math.floor(civ.y);

    if (currentX < 0 || currentX >= worldData.map_width || currentY < 0 || currentY >= worldData.map_height) {
      currentX = Math.max(0, Math.min(worldData.map_width - 1, currentX));
      currentY = Math.max(0, Math.min(worldData.map_height - 1, currentY));
    }

    if (!worldData.food_map || !worldData.food_map[currentY] || worldData.food_map[currentY][currentX] === undefined) {
      continue;
    }

    const food = worldData.food_map[currentY][currentX];
    const wood = worldData.wood_map[currentY][currentX];
    const minerals = worldData.minerals_map[currentY][currentX];
    const totalResources = food + wood + minerals;

    if (totalResources > 3) {
      // Population growth
      civ.js_population += civ.js_population * 0.02;

      // Resource consumption
      worldData.food_map[currentY][currentX] = Math.max(0, food - civ.js_population * 0.1);
      worldData.wood_map[currentY][currentX] = Math.max(0, wood - civ.js_population * 0.05);
      worldData.minerals_map[currentY][currentX] = Math.max(0, minerals - civ.js_population * 0.05);

      // TERRITORY EXPANSION - chance to expand if population is growing
      if (Math.random() < 0.1 && civ.territory && Array.isArray(civ.territory)) {
        const expandChance = 0.3;
        const newTiles = [];

        for (const tile of civ.territory) {
          if (Array.isArray(tile) && tile.length === 2) {
            const [tx, ty] = tile;
            // Check adjacent tiles
            const adjacent = [
              [tx-1, ty], [tx+1, ty], [tx, ty-1], [tx, ty+1]
            ];

            for (const [ax, ay] of adjacent) {
              if (ax >= 0 && ax < worldData.map_width && ay >= 0 && ay < worldData.map_height) {
                if (worldData.biome_map[ay][ax] !== 'Ocean') {
                  // Check if tile is not already owned by this civ
                  const alreadyOwned = civ.territory.some(t =>
                    Array.isArray(t) && t[0] === ax && t[1] === ay
                  );
                  if (!alreadyOwned && Math.random() < expandChance) {
                    newTiles.push([ax, ay]);
                  }
                }
              }
            }
          }
        }

        // Add new tiles to territory
        for (const newTile of newTiles) {
          civ.territory.push(newTile);
        }
      }

      // CITY FOUNDING - chance to found new city if population is high enough
      if (civ.js_population > 50 && Math.random() < 0.05 && civ.cities && Array.isArray(civ.cities)) {
        if (civ.territory && civ.territory.length > civ.cities.length * 10) {
          // Find a territory tile that doesn't have a city
          const availableTiles = civ.territory.filter(tile => {
            if (!Array.isArray(tile) || tile.length !== 2) return false;
            return !civ.cities.some(city =>
              city.location && city.location[0] === tile[0] && city.location[1] === tile[1]
            );
          });

          if (availableTiles.length > 0) {
            const newCityLocation = availableTiles[Math.floor(Math.random() * availableTiles.length)];
            civ.cities.push({
              location: newCityLocation,
              population: 100 + Math.floor(Math.random() * 200)
            });
            console.log(`New city founded by civ ${civ.id} at [${newCityLocation.join(',')}]`);
          }
        }
      }

    } else {
      // Resource scarcity - population decline and migration
      civ.js_population *= 0.95;

      // Migration logic (existing code)
      let bestScore = -1;
      let bestPos = { x: currentX, y: currentY };
      for (let dx = -5; dx <= 5; dx++) {
        for (let dy = -5; dy <= 5; dy++) {
          const nx = currentX + dx;
          const ny = currentY + dy;
          if (nx < 0 || ny < 0 || nx >= worldData.map_width || ny >= worldData.map_height) continue;
          if (worldData.biome_map[ny][nx] === 'Ocean') continue;
          if (!worldData.food_map[ny] || worldData.food_map[ny][nx] === undefined) continue;

          const r = worldData.food_map[ny][nx] + worldData.wood_map[ny][nx] + worldData.minerals_map[ny][nx];
          const habit = (() => {
            switch (worldData.biome_map[ny][nx]) {
              case 'Grassland': return 0.8; case 'Forest': return 0.7;
              case 'Beach': return 0.5; case 'Taiga': return 0.5;
              case 'Swamp': return 0.4; case 'Tundra': return 0.3;
              case 'Desert': return 0.1; case 'Snow': return 0.1;
              default: return 0.5;
            }
          })();
          const score = r * habit;
          if (score > bestScore) {
            bestScore = score;
            bestPos = { x: nx, y: ny };
          }
        }
      }
      civ.x = bestPos.x;
      civ.y = bestPos.y;
    }

    if (civ.js_population < 1) civ.js_population = 1;
  }
}

function drawFrame() {
  if (!ctx || !canvas || !worldData) {
    console.log("drawFrame: Canvas or worldData not ready. Aborting frame.");
    return;
  }
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (biomeCanvas) {
    ctx.drawImage(biomeCanvas, 0, 0);
  } else {
    console.warn("drawFrame: biomeCanvas not available to draw.");
  }

  drawCivs();   // Draws current state of worldData.civs (Python output + JS modifications to non-geometric props)

  updateCivs(); // This function modifies worldData for the *next* JS frame.
                // It simulates civ behavior in JS, separate from Python's sim.
                // Call it if you intend for a JS-based simulation to run using Python's output as a starting point.

  frame++;
  if (info) {
    // Show current JS frame and effective year of JS simulation
    info.textContent = `Month: ${frame} | Year: ${Math.floor(frame / 12)} / ${Math.floor(totalFrames / 12)}`;
  }

  if (frame < totalFrames) { // totalFrames is for the JS simulation
    requestAnimationFrame(drawFrame);
  } else {
    if (info) info.textContent = `JS Simulation finished after ${Math.floor(totalFrames/12)} years.`;
    console.log("drawFrame: JS simulation totalFrames reached.");
  }
}

function getRandomColor() {
  const colors = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#00FFFF', '#FF00FF', '#FFC0CB', '#90EE90', '#ADD8E6', '#FA8072', '#EE82EE', '#D2B48C', '#87CEEB'];
  return colors[Math.floor(Math.random() * colors.length)];
}

function shadeColor(hexColor, percent) {
    // Ensure hexColor is a string and starts with #
    if (typeof hexColor !== 'string' || !hexColor.startsWith('#')) {
        console.warn("shadeColor: Invalid hexColor input", hexColor, "defaulting to gray.");
        return "#808080"; // Default color if input is bad
    }
    let R = parseInt(hexColor.substring(1,3),16);
    let G = parseInt(hexColor.substring(3,5),16);
    let B = parseInt(hexColor.substring(5,7),16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = Math.max(0, Math.min(255, R));
    G = Math.max(0, Math.min(255, G));
    B = Math.max(0, Math.min(255, B));

    const RR = R.toString(16).padStart(2, '0');
    const GG = G.toString(16).padStart(2, '0');
    const BB = B.toString(16).padStart(2, '0');

    return "#"+RR+GG+BB;
}

window.onload = () => {
  canvas = document.getElementById('worldCanvas');
  info = document.getElementById('info');

  if (!canvas) {
    console.error("CRITICAL: Canvas element with ID 'worldCanvas' not found.");
    if(info) info.textContent = "Error: Canvas element 'worldCanvas' not found. Check console.";
    return;
  }
  ctx = canvas.getContext('2d');
  if (!ctx) {
    console.error("CRITICAL: Failed to get 2D context from canvas.");
    if(info) info.textContent = "Error: Failed to get canvas context. Check console.";
    return;
  }
  console.log("window.onload: Canvas and context obtained successfully.");

  if (!info) {
    console.warn("Info element with ID 'info' not found. Status messages will not be displayed on the page.");
  }

  loadData();
};