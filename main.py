import json
from warranty import Warranty
def save_claims_to_txt(claims, filename="claims_report.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== WARRANTY CLAIMS REPORT ===\n\n")
        f.write(f"Total claims: {len(claims)}\n")
        f.write("=" * 50 + "\n\n")

        for claim in claims:
            f.write(f"Claim ID: #{claim['id']}\n")
            f.write(f"Product: {claim['product']}\n")
            f.write(f"Client: {claim['client']}\n")
            f.write(f"Decision: {claim['decision']}\n")
            f.write(f"Cost: ${claim['cost']}\n")
            f.write(f"Date: {claim['date']}\n")
            f.write("-" * 30 + "\n")


def main():
    w = Warranty()

    try:
        with open("db.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            claims = data["claims"]

            print("=== Warranty Claims Analysis ===")
            print(f"Total claims in database: {len(claims)}\n")

            repair_count = sum(1 for c in claims if c["decision"] == "repair")
            replace_count = sum(1 for c in claims if c["decision"] == "replace")
            total_cost = sum(c["cost"] for c in claims)

            print(f"Repair claims: {repair_count}")
            print(f"Replace claims: {replace_count}")
            print(f"Total cost: ${total_cost}\n")

            print("=== Claims by Product ===")
            products = {}
            for claim in claims:
                product = claim["product"]
                if product not in products:
                    products[product] = {"count": 0, "total_cost": 0}
                products[product]["count"] += 1
                products[product]["total_cost"] += claim["cost"]

            for product, stats in products.items():
                print(f"{product}: {stats['count']} claims, total cost: ${stats['total_cost']}")

            print("\n=== Claims by Client ===")
            clients = {}
            for claim in claims:
                client = claim["client"]
                if client not in clients:
                    clients[client] = {"count": 0, "total_cost": 0}
                clients[client]["count"] += 1
                clients[client]["total_cost"] += claim["cost"]

            for client, stats in clients.items():
                print(f"{client}: {stats['count']} claims, total cost: ${stats['total_cost']}")

            save_claims_to_txt(claims)
            print(f"\nReport saved to 'claims_report.txt'")

            print("\n=== Sample from claims_report.txt ===")
            with open("claims_report.txt", "r", encoding="utf-8") as report_file:
                lines = report_file.readlines()[:15]
                print("".join(lines))
                print("... (full report in claims_report.txt)")

    except FileNotFoundError:
        print("Error: db.txt file not found")
        print("Please ensure db.txt exists with the warranty claims data")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in db.txt")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()