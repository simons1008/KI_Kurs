"""
Generiert Testmuster (konzentrische Ringe, wie eine Zielscheibe) mit
zufälligen Farbreihenfolgen. Praktisch, um einen Farberkennungs-Algorithmus
gegen bekannte Ground-Truth-Daten zu testen.

Abhängigkeit: Pillow  ->  pip install pillow

Quelle: Claude (Anthropic)
"""

import json
import random
from pathlib import Path
from PIL import Image, ImageDraw

# Referenz-Farbpalette (RGB) - kann erweitert/angepasst werden
DEFAULT_PALETTE = {
    "green":  (0, 255, 0),
    "black":  (0, 0, 0),
    "red":    (255, 0, 0),
    "blue":   (0, 255, 255),
    "yellow": (255, 255, 0),
    "white":  (255, 255, 255),
}


def generate_test_patterns(
    n: int,
    output_dir: str = "test_patterns",
    n_rings: int = 5,
    size: int = 512,
    palette: dict = None,
    allow_repeats: bool = True,
    background: str = "white",
    add_noise: bool = False,
    seed: int = None,
) -> list:
    """
    Erzeugt n Testbilder mit konzentrischen Ringen in zufälliger Farbreihenfolge.

    Args:
        n: Anzahl der zu generierenden Bilder.
        output_dir: Zielordner für PNG-Dateien + ground_truth.json.
        n_rings: Anzahl der Ringe (von außen nach innen).
        size: Bildkantenlänge in Pixel (quadratisch).
        palette: dict {name: (r,g,b)}. Default = DEFAULT_PALETTE.
        allow_repeats: Ob Farben mehrfach im selben Muster vorkommen dürfen.
        background: Farbname aus der Palette für den Bildhintergrund.
        add_noise: Falls True, wird leichtes Bildrauschen hinzugefügt
                   (realistischere Testbedingungen).
        seed: Optionaler Zufalls-Seed für Reproduzierbarkeit.

    Returns:
        Liste von dicts: [{"file": "...", "colors": [...]}, ...]
        (von außen nach innen), gleichzeitig als ground_truth.json gespeichert.
    """
    if seed is not None:
        random.seed(seed)

    palette = palette or DEFAULT_PALETTE
    color_names = [c for c in palette if c != background]

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    records = []

    for i in range(n):
        # Farbreihenfolge (außen -> innen) auswählen
        if allow_repeats:
            sequence = [random.choice(color_names) for _ in range(n_rings)]
        else:
            sequence = random.sample(color_names, k=min(n_rings, len(color_names)))

        img = Image.new("RGB", (size, size), palette[background])
        draw = ImageDraw.Draw(img)

        center = size // 2
        max_r = int(size * 0.45)
        step = max_r / n_rings

        # von außen nach innen zeichnen (größter Ring zuerst)
        for ring_idx, color_name in enumerate(sequence):
            r = int(max_r - ring_idx * step)
            bbox = [center - r, center - r, center + r, center + r]
            draw.ellipse(bbox, fill=palette[color_name])

        if add_noise:
            img = _add_noise(img, amount=8)

        filename = f"pattern_{i:04d}.png"
        img.save(out_path / filename)

        records.append({"file": filename, "colors": sequence})

    with open(out_path / "ground_truth.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    return records


def _add_noise(img: Image.Image, amount: int = 8) -> Image.Image:
    """Fügt leichtes Gauß-artiges Rauschen hinzu (grobe Annäherung ohne numpy-Zwang)."""
    import random as _r
    pixels = img.load()
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x, y]
            noise = _r.randint(-amount, amount)
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )
    return img


if __name__ == "__main__":
    results = generate_test_patterns(
        n=10,
        output_dir="test_patterns",
        n_rings=5,
        size=210,
        allow_repeats=True,
        seed=42,
    )
    for r in results:
        print(r["file"], "->", r["colors"])
