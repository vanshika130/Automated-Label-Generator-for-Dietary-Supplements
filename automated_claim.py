import os
import json
import requests
import google.generativeai as genai

# Load API Key from environment
api_key = os.getenv("GOOGLE_API_KEY")  
if not api_key:
    raise ValueError("❌ API key not found. Set GOOGLE_API_KEY in your environment variables!")

# **Step 1: Test API Key using a cURL equivalent in Python**
def test_gemini_api():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": "Explain how AI works"}]
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✅ API Test Passed: ", response.json()["candidates"][0]["content"]["parts"][0]["text"])
    else:
        print(f"❌ API Test Failed: {response.text}")
        return False
    return True

# **Step 2: Generate Health Claims for Ingredients**
def generate_health_claims():
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Load product data
    with open("product_data.json", "r") as file:
        product_data = json.load(file)

    ingredients = product_data.get("ingredients", [])
    claims = {}

    for ingredient in ingredients:
        print(f"📝 Generating claim for {ingredient}...")
        try:
            response = model.generate_content(f"Write a short health claim for {ingredient}.")
            claims[ingredient] = response.text
            print(f"✅ Claim for {ingredient}: {response.text}")
        except Exception as e:
            print(f"❌ Error generating claim for {ingredient}: {e}")

    # Save updated claims back to JSON
    product_data["claims"] = claims
    with open("product_data.json", "w") as file:
        json.dump(product_data, file, indent=4)

    print("🎉 Health claims saved successfully!")

# **Run the script**
if test_gemini_api():
    generate_health_claims()
