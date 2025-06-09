from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/tokens", methods=["GET"])
def get_tokens():
    base_url = "https://api.geckoterminal.com/api/v2/networks/solana/pools"
    tokens = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        for page in range(1, 4):
            params = {
                "page": page,
                "dex_name": "pumpfun"
            }

            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            pools = data.get("data", [])
            print(f"✅ DEBUG PAGE {page}: received {len(pools)} pools")

            for pool in pools:
                attributes = pool.get("attributes", {})
                base_token = attributes.get("base_token")
                if not base_token:
                    continue

                name = base_token.get("name")
                address = base_token.get("address")
                if name and address:
                    tokens.append({"name": name, "address": address})

        print(f"✅ DEBUG TOTAL TOKENS: {len(tokens)}")
        return jsonify(tokens)

    except Exception as e:
        print("❌ DEBUG ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
