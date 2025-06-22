# test_noise_issue.py
from noise import pnoise2
import sys

print(f"Python version: {sys.version}")
try:
    import noise
    print(f"Noise library version: {getattr(noise, '__version__', 'unknown')}")
except ImportError:
    print("Noise library not found.")
    sys.exit()

x_coord, y_coord = 0, 0 # Simuliert die ersten x, y Werte in deiner Schleife
scale = 200.0
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = 68959 # Der Seed aus deinem Absturzprotokoll

nx = x_coord / scale
ny = y_coord / scale

print(f"Calling pnoise2 with: nx={nx}, ny={ny}, octaves={octaves}, persistence={persistence}, lacunarity={lacunarity}, repeatx=1024, repeaty=1024, base={seed}")
try:
    value = pnoise2(nx, ny,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024, # Standardwerte, explizit für Klarheit
                    repeaty=1024, # Standardwerte, explizit für Klarheit
                    base=seed)
    print(f"pnoise2 returned: {value}")
except Exception as e:
    # Dieser Block fängt nur Python-Exceptions, kein 0xC0000005
    print(f"Python-level exception during pnoise2 call: {e}")
    import traceback
    traceback.print_exc()

print("Test finished.")