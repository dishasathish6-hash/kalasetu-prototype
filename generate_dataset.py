import pandas as pd
import numpy as np

np.random.seed(42)

categories = ["Terracotta Pottery", "Channapatna Toys", "Madhubani Painting", "Dhokra Metal Craft", "Pashmina Shawls"]
materials = {
    "Terracotta Pottery": ["Riverbed Clay", "Natural Oxide Wash"],
    "Channapatna Toys": ["Wrightia Tinctoria (Ivory Wood)", "Vegetable Dyes"],
    "Madhubani Painting": ["Handmade Paper", "Natural Plant Pigments"],
    "Dhokra Metal Craft": ["Recycled Brass", "Beeswax Mold"],
    "Pashmina Shawls": ["Ladakhi Cashmere", "Natural Indigo"]
}

data = []
for i in range(60):
    cat = np.random.choice(categories)
    mat = np.random.choice(materials[cat])
    material_cost = np.random.randint(80, 1500)
    labor_hours = np.random.randint(4, 48)
    craft_tier = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
    
    base_price = (material_cost * 1.25) + (labor_hours * 85 * (1 + 0.3 * craft_tier))
    market_price = round(base_price * np.random.uniform(0.95, 1.1), -1)

    data.append({
        "item_id": f"ART-{1000 + i}",
        "category": cat,
        "primary_material": mat,
        "material_cost": material_cost,
        "labor_hours": labor_hours,
        "craft_tier": craft_tier,
        "fair_price_inr": market_price
    })

df = pd.DataFrame(data)
df.to_csv("artisan_dataset_60.csv", index=False)
print("Dataset created: artisan_dataset_60.csv (60 records)")