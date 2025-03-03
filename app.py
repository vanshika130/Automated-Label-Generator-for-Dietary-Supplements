from flask import Flask, request, jsonify
import json
from automated_claim import generate_claims
from barcode_generator import generate_codes
# from label_generator import generate_label

app = Flask(__name__)

# ✅ Flask Route to Handle Form Submission
@app.route('/submit-product', methods=['POST'])
def submit_product():
    data = request.json  # Get JSON data from user input

    # ✅ Store product data in JSON format
    product_data = {
        "product_name": data["product_name"],
        "ingredients": data["ingredients"],
        "dosage": data.get("dosage", "N/A"),
        "expiry_date": data.get("expiry_date", "N/A"),
        "health_claims": {},
        "barcode": "",
        "qr_code": "",
        "label": ""
    }

    # ✅ Call functions from respective files
    generate_claims(product_data)
    generate_codes(product_data)
    generate_label(product_data)

    # ✅ Save updated data
    with open("product_data.json", "w") as file:
        json.dump(product_data, file, indent=4)

    return jsonify({
        "message": "Product processed successfully!",
        "product_data": product_data
    })

# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
