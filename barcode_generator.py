import barcode
from barcode.writer import ImageWriter

# .venv\Scripts\Activate === to actiate the environment


def generate_barcode(product_data):
    """Generates a barcode for the product and updates the JSON data."""
    
    barcode_data = product_data["product_name"].replace(" ", "").upper()
    barcode_filename = f"static/barcode_{barcode_data}"

    # ✅ Generate Barcode (EAN-13 format)
    try:
        ean = barcode.get("ean13", barcode_data[:12], writer=ImageWriter())
        ean.save(barcode_filename)
        product_data["barcode"] = f"{barcode_filename}.png"
        print(f"✅ Barcode saved as {barcode_filename}.png")
    except Exception as e:
        print(f"❌ Error generating barcode: {e}")
        product_data["barcode"] = "Error generating barcode"

# ✅ Run the function if this script is executed directly
if __name__ == "__main__":
    import json

    # ✅ Load product data for testing
    try:
        with open("product_data.json", "r") as file:
            product_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("❌ Error: JSON file is missing or corrupt!")
        product_data = {}

    if product_data:
        generate_barcode(product_data)

        # ✅ Save updated JSON
        with open("product_data.json", "w") as file:
            json.dump(product_data, file, indent=4)
