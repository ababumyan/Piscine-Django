import random
from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino

class CoffeeMachine:
    def __init__(self):
        self.count = 0
        self.brockenCount = 0
        self.outOfOrder = 10
    class EmptyCup(HotBeverage):
        name = "empty cup"
        price = 0.90
        def description(self):
            return "An empty cup?! Gimme my money back!"
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")
    def repair(self):
        
        self.outOfOrder = 10
        print("Machine repaired.")
    def serve(self, beverage):
        if self.outOfOrder <= 0:
            self.brockenCount += 1
            raise self.BrokenMachineException()
        
        elif random.randint(0, 8) == 0:
            return self.EmptyCup()
        else:
            self.outOfOrder -= 1
            self.count += 1
            return beverage()
        
if __name__ == '__main__':
    machine = CoffeeMachine()
    for i in range(300):
        try:
            print(machine.serve(random.choice([Coffee, Tea, Chocolate, Cappuccino])))
        except machine.BrokenMachineException as e:
            print(e)
            machine.repair()       
    print(machine.count, "drinks served.", machine.brockenCount, "drinks lost.")