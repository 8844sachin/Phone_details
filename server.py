from flask import Flask, request, jsonify, render_template
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from phonenumbers.phonenumberutil import number_type, is_valid_number, NumberParseException

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_number():
    data = request.get_json()

    if not data or "phone" not in data:
        return jsonify({"valid": False, "error": "No phone number provided."}), 400

    try:
        phone = phonenumbers.parse(data["phone"])

        if not is_valid_number(phone):
            return jsonify({"valid": False, "error": "Invalid phone number."})

        num_type = number_type(phone)
        type_map = {
            0: "Fixed Line",
            1: "Mobile",
            2: "Fixed Line or Mobile",
            3: "Toll Free",
            4: "Premium Rate",
            5: "Shared Cost",
            6: "VOIP",
            7: "Personal Number",
            8: "Pager",
            9: "Universal Access Number",
            10: "Voicemail",
        }

        result = {
            "valid": True,
            "carrier": carrier.name_for_number(phone, "en"),
            "region": geocoder.description_for_number(phone, "en"),
            "timezone": list(timezone.time_zones_for_number(phone)),
            "type": type_map.get(num_type, "Unknown")
        }

        return jsonify(result)

    except NumberParseException as e:
        return jsonify({"valid": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"valid": False, "error": "Server error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
