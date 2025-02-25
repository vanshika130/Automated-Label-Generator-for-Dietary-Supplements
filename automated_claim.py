import json
import time
from transformers import pipeline

# Load AI model
print("🚀 Initializing AI Model...")
generator = pipeline("text-generation", model="distilgpt2")

# Load product data
try:
    with open("product_data.json", "r") as file:
        product_data = json.load(file)
        print("📂 Loaded product_data.json successfully.")
except json.JSONDecodeError:
    print("❌ Error: JSON file is empty or corrupt!")
    exit(1)

# Check if 'ingredients' exist
if "ingredients" not in product_data:
    print("❌ Error: 'ingredients' key not found in product_data.json!")
    exit(1)

print(f"🍀 Ingredients found: {product_data['ingredients']}")

# Generate claims
product_claims = {}
for ingredient in product_data["ingredients"]:
    print(f"📝 Generating claim for {ingredient}...")

    start_time = time.time()  # Start timer
    prompt = f"Generate a short and FSSAI-compliant health claim for {ingredient}."
    result = generator(prompt, max_length=50, truncation=True, pad_token_id=50256)
    end_time = time.time()  # End timer

    elapsed_time = round(end_time - start_time, 2)
    print(f"✅ Generated claim: {result[0]['generated_text']} (Time taken: {elapsed_time} sec)")

    product_claims[ingredient] = result[0]["generated_text"]

# Save claims back to JSON
product_data["health_claims"] = product_claims
with open("product_data.json", "w") as file:
    json.dump(product_data, file, indent=4)

print("🎉 Health claims generated and saved successfully in product_data.json!")
