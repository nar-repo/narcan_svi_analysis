import json
import pandas as pd

# Load JSON file
with open("narcan_sites_mn.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Navigate to the list of locations
locations = data.get("results", {}).get("locations", [])

# Extract relevant fields into a list of dicts
records = []
for loc in locations:
    record = {
        "id": loc.get("id"),
        "name": loc.get("name"),
        "latitude": loc.get("lat"),
        "longitude": loc.get("lng"),
        "address": loc.get("address"),
        "city": loc.get("city"),
        "state": loc.get("state"),
        "postcode": loc.get("postcode"),
        "country": loc.get("country"),
        "url": loc.get("url"),
        "phone": loc.get("phone"),
        "email": loc.get("email"),
        "location_type": loc.get("location_type_name"),
        "distance": loc.get("distance"),
        # Add more fields as needed
    }
    records.append(record)

# Convert to DataFrame
df = pd.DataFrame(records)

# Save to CSV
df.to_csv("narcan_sites_mn.csv", index=False)
print("✅ Saved narcan_sites_mn.csv")
