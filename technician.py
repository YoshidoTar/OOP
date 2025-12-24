class Technician: # создание класса техника
    def fix_cost(self, problem):
        if "not work" in problem.lower():
            return 2000
        return 1000