import json
from datetime import datetime, timedelta
import os
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


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.sold = datetime.now() - timedelta(days=100)

    def is_valid(self):
        return datetime.now() <= self.sold + timedelta(days=365)

class Receiver:
    def check(self, product):
        return product.is_valid()

class Technician:
    def fix_cost(self, problem):
        if "not work" in problem.lower():
            return 2000
        return 1000
class Manager:
    def decide(self, product, cost):
        return "replace" if cost > product.price * 0.4 else "repair"

class Warranty:
    def __init__(self):
        self.db = DB()
        self.receiver = Receiver()
        self.tech = Technician()
        self.manager = Manager()
        self.products = {
            1: Product("CPU", 25000),
            2: Product("GPU", 50000),
            3: Product("SSD", 7000)
        }
    def claim(self, pid, client, problem):
        if pid not in self.products:
            return "No product"
        p = self.products[pid]
        if not self.receiver.check(p):
            return "No warranty"
        cost = self.tech.fix_cost(problem)
        decision = self.manager.decide(p, cost)
        cid = self.db.add(p.name, client, decision, cost)

        return f"#{cid}: {decision} (${cost})"
    def make_report(self, days=30):
        r = self.db.report(days)
        text = f"Report ({days} days):\nClaims: {r['count']}\nRepair: ${r['repair']}\nReplace: ${r['replace']}\nTotal: ${r['total']}"

        with open("report.txt", "w") as f:
            f.write(text)

        return text
def main():
    w = Warranty()

    cases = [
        (1, "Ivan", "Not working"),
        (2, "Petr", "Overheat"),
        (3, "Alex", "Slow"),
        (1, "Max", "Broken")
    ]
    for pid, client, problem in cases:
        print(f"{client}: {w.claim(pid, client, problem)}")

    print("\n" + w.make_report())
if __name__ == "__main__":
    main()