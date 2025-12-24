class Manager:
    def decide(self, product, cost):
        return "replace" if cost > product.price * 0.4 else "repair"