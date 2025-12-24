import json
import os
from datetime import datetime, timedelta


class DB:
    def __init__(self, f="db.txt"):
        self.f = f
        if not os.path.exists(f):
            with open(f, 'w') as file:
                json.dump({"claims": [], "next_id": 1}, file)

    def load(self):
        with open(self.f, 'r') as file:
            return json.load(file)

    def save(self, data):
        with open(self.f, 'w') as file:
            json.dump(data, file, indent=2)

    def add(self, product, client, decision, cost):
        data = self.load()
        data["claims"].append({
            "id": data["next_id"],
            "product": product,
            "client": client,
            "decision": decision,
            "cost": cost,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        data["next_id"] += 1
        self.save(data)
        return data["next_id"] - 1

    def report(self, days):
        data = self.load()
        start = datetime.now() - timedelta(days=days)
        repair = replace = count = 0

        for c in data["claims"]:
            d = datetime.strptime(c["date"], "%Y-%m-%d")
            if d >= start:
                count += 1
                if c["decision"] == "repair":
                    repair += c["cost"]
                else:
                    replace += c["cost"]

        return {"count": count, "repair": repair, "replace": replace, "total": repair + replace}