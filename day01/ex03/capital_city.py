import sys

def find_capital_city(state,capital):
    if state in states:
        print(capital[states[state]])
    else:
        print("Unknown state")
    return

if __name__ == '__main__':
    capital_cities = { "OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver" }
    states = { "Oregon" : "OR", "Alabama" : "AL", "New Jersey": "NJ", "Colorado" : "CO" } 
    if len(sys.argv) == 2:
        find_capital_city(sys.argv[1],capital_cities)
    else:
        sys.exit(0)
    sys.exit(0)