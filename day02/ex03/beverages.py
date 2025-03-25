class HotBeverage:
    price = 0.3
    name = "hot beverage"
    def description(self):
        return "Just some hot water in a cup."
    def __str__(self):
        return "name : " + self.name + "\nprice : " + str(self.price) + "\ndescription : " + self.description()
    
class Coffee(HotBeverage):
    price = 0.4
    name = "coffee"
    def description(self):
        return "A coffee, to stay awake."

class Tea(HotBeverage):
    name = "tea"
    def description(self):
        return "Just some hot water in a cup."

class Chocolate(HotBeverage):
    price = 0.5
    name = "chocolate"
    def description(self):
        return "Chocolate, sweet chocolate..."

class Cappuccino(HotBeverage):
    price = 0.45
    name = "cappuccino"
    def description(self):
        return "Un po’ di Italia nella sua tazza!"

if __name__ == '__main__':
    a = HotBeverage()
    print(a)
    b = Coffee()
    print(b)
    c = Tea()
    print(c)
    d = Chocolate()
    print(d)
    e = Cappuccino()
    print(e)