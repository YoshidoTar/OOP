import json
from warranty import Warranty


def save_claims_to_txt(claims, filename="claims_report.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Total claims: {len(claims)}\n")

        for claim in claims:
            f.write(f"Claim ID: #{claim['id']}\n")
            f.write(f"Product: {claim['product']}\n")
            f.write(f"Client: {claim['client']}\n")
            f.write(f"Decision: {claim['decision']}\n")
            f.write(f"Cost: ${claim['cost']}\n")
            f.write(f"Date: {claim['date']}\n")


def main():
    w = Warranty()

    try:
        with open("db.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            all_claims = data["claims"]
            claims = all_claims[:5]

            print(f" WORKING WITH FIRST 5 CLAIMS ONLY")
            print(f"Total claims in database: {len(all_claims)}")
            print(f"Processing only first: {len(claims)}\n")

            repair_count = sum(1 for c in claims if c["decision"] == "repair")
            replace_count = sum(1 for c in claims if c["decision"] == "replace")
            total_cost = sum(c["cost"] for c in claims)

            print(f" Repair claims: {repair_count}")
            print(f" Replace claims: {replace_count}")
            print(f" Total cost: ${total_cost}\n")

            products = {}
            for claim in claims:
                product = claim["product"]
                if product not in products:
                    products[product] = {"count": 0, "total_cost": 0}
                products[product]["count"] += 1
                products[product]["total_cost"] += claim["cost"]

            print(" Products Statistics:")
            for product, stats in products.items():
                print(f"  {product}: {stats['count']} claims, total cost: ${stats['total_cost']}")

            clients = {}
            for claim in claims:
                client = claim["client"]
                if client not in clients:
                    clients[client] = {"count": 0, "total_cost": 0}
                clients[client]["count"] += 1
                clients[client]["total_cost"] += claim["cost"]

            print("\n Clients Statistics:")
            for client, stats in clients.items():
                print(f"  {client}: {stats['count']} claims, total cost: ${stats['total_cost']}")

            save_claims_to_txt(claims) #сохраняем первые 5 заявок
            print(f"\n Report saved to 'claims_report.txt' (first 5 claims only)")

            with open("claims_report.txt", "r", encoding="utf-8") as report_file:
                lines = report_file.readlines()[:10]
                print("\n Report preview:")
                print("".join(lines))
                print("... (full report in claims_report.txt)")

            db = w.db
            if db.is_full():
                print("\n Database is full (5 records maximum). Cannot add new claims.")
            else:
                print(f"\n Can add {5 - len(all_claims)} more claims")

    except FileNotFoundError:
        print(" Error: db.txt file not found")
        print("Please ensure db.txt exists with the warranty claims data")
    except json.JSONDecodeError:
        print(" Error: Invalid JSON format in db.txt")
    except Exception as e:
        print(f" Error: {e}")


if __name__ == "__main__": #запуск основной программы
    main()