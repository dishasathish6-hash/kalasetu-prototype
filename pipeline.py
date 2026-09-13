import io
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestRegressor

# Train ML Pricing Model on startup
df = pd.read_csv("artisan_dataset_60.csv")
X = df[["material_cost", "labor_hours", "craft_tier"]]
y = df["fair_price_inr"]
pricing_model = RandomForestRegressor(n_estimators=50, random_state=42)
pricing_model.fit(X, y)

def clean_artisan_image(image_bytes: bytes) -> bytes:
    """Removes background lazily to prevent startup hangs."""
    input_img = Image.open(io.BytesIO(image_bytes))
    
    try:
        from rembg import remove
        output_img = remove(input_img)
    except Exception:
        output_img = input_img

    if output_img.mode != "RGBA":
        output_img = output_img.convert("RGBA")

    bg = Image.new("RGBA", output_img.size, (255, 255, 255, 255))
    bg.paste(output_img, (0, 0), output_img)
    
    out_buffer = io.BytesIO()
    bg.convert("RGB").save(out_buffer, format="JPEG", quality=95)
    return out_buffer.getvalue()

def parse_voice_and_extract_wisdom(spoken_transcript: str):
    text_lower = spoken_transcript.lower()
    
    category = "Handicrafts & Decor"
    if "pot" in text_lower or "clay" in text_lower or "mitti" in text_lower:
        category = "Terracotta Pottery"
    elif "toy" in text_lower or "wood" in text_lower or "channapatna" in text_lower:
        category = "Channapatna Toys"
    elif "paint" in text_lower or "canvas" in text_lower or "madhubani" in text_lower:
        category = "Madhubani Painting"

    wisdom = "Traditional generational knowledge passed down without synthetic additives."
    if "thandak" in text_lower or "cool" in text_lower:
        wisdom = "Riverbed clay selected for natural micro-porosity, keeping water cool naturally without electricity."
    elif "bache" in text_lower or "safe" in text_lower or "vegetable" in text_lower:
        wisdom = "Wrightia tinctoria wood dyed with turmeric and natural resin so it remains 100% non-toxic for infants."

    return {
        "title_en": f"Artisan Handcrafted {category}",
        "title_hi": f"हस्तनिर्मित पारंपरिक {category}",
        "category": category,
        "extracted_transcript": spoken_transcript,
        "wisdom_layer": wisdom,
        "suggested_tags": [category, "TraditionalCraft", "EcoFriendly", "VocalForLocal"]
    }

def calculate_dynamic_price(material_cost: float, labor_hours: float, craft_tier: int):
    pred = pricing_model.predict([[material_cost, labor_hours, craft_tier]])[0]
    fair_price = round(pred, -1)
    return {
        "fair_price_inr": fair_price,
        "suggested_range": [round(fair_price * 0.95), round(fair_price * 1.15)],
        "middleman_comparison_inr": round(fair_price * 0.45)
    }