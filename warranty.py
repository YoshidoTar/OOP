from db import DB
class Warranty:
    def __init__(self):
        self.db = DB()

    def make_report(self, days=30):
        r = self.db.report(days)
        text = f"Report ({days} days):\nClaims: {r['count']}\nRepair: ${r['repair']}\nReplace: ${r['replace']}\nTotal: ${r['total']}"

        with open("report.txt", "w") as f:
            f.write(text)

        return text

    def get_all_claims(self):
        data = self.db.load()
        return data["claims"]