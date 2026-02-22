# backend/app/model_utils.py
import os, json
from PIL import Image
import numpy as np

# Simple perishable set (for PoC)
PERISHABLE = {"biryani","dosa","idli","rice","fish","chicken","meat","curry","salad","milk","bread"}

def parse_text_metadata(text):
    text_low = (text or "").lower()
    qty = None
    hours = None
    tokens = text_low.replace(",", " ").split()
    for i,t in enumerate(tokens):
        if t.isdigit():
            # crude detection
            if i+1 < len(tokens) and tokens[i+1].startswith(("box","boxes","meal","meals","plate","plates")):
                try:
                    qty = int(t)
                except:
                    qty = 1
        if t.endswith("hr") or t.endswith("hrs") or t.endswith("hour") or t.endswith("hours"):
            try:
                hours = int(''.join([c for c in t if c.isdigit()]))
            except:
                pass
    return {"quantity": qty or 1, "hours_since_cooked": hours or 1, "raw_text": text}

def edibility_score(food_type, hours_since_cooked, packaging="open"):
    base = 0.55
    if food_type and any(p in food_type for p in PERISHABLE):
        base -= 0.2
    base -= min(0.35, 0.05 * max(0, hours_since_cooked-1))
    if packaging in ["sealed","vacuum","wrapped","boxed"]:
        base += 0.18
    return float(max(0.0, min(1.0, base)))

# Simple filename heuristic for PoC
def predict_food_from_image(image_path):
    name = os.path.basename(image_path).lower()
    for key in PERISHABLE:
        if key in name:
            return key
    # fallback
    return "mixed_food"

def inference_pipeline(image_path=None, text_metadata=""):
    parsed = parse_text_metadata(text_metadata)
    food = None
    if image_path:
        food = predict_food_from_image(image_path)
    packaging = "open"
    if "sealed" in (text_metadata or "").lower() or "packed" in (text_metadata or "").lower() or "boxed" in (text_metadata or "").lower():
        packaging = "sealed"
    score = edibility_score(food if food else "mixed_food", parsed["hours_since_cooked"], packaging)
    label = "safe" if score>=0.6 else ("urgent" if score>=0.35 else "not_safe")
    return {
        "food_type": food,
        "quantity": parsed["quantity"],
        "hours_since_cooked": parsed["hours_since_cooked"],
        "packaging": packaging,
        "edibility_score": round(score,2),
        "label": label
    }
