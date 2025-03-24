import sys

def find_state(capital,states):
    capital_cities.get(capital)
    if capital:
        keys = [key for key, val in capital_cities.items() if val == capital]
        for state in states:
            if states[state] == keys[0]:
                print(state)
                return
    else:
        print("Unknown capital city")

if __name__ == '__main__':
    capital_cities = { "OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver" }
    states = { "Oregon" : "OR", "Alabama" : "AL", "New Jersey": "NJ", "Colorado" : "CO" } 
    if len(sys.argv) == 2:
        find_state(sys.argv[1],states)
    else:
        sys.exit(0)
    sys.exit(0)