import sys

def find_capital_city(state,capital):
    if state in states:
        print(capital[state])
        return capital[states[state]]
    else:
        print("Unknown state")
        return None


def find_state(capital):
    capital_cities.get(capital)
    if capital:
        keys = [key for key, val in capital_cities.items() if val == capital]
        for state in states:
            if states[state] == keys[0]:
                print(state)
                return state
    else:
        print("Unknown capital city")
        return None

def handler(input):
    if input in capital_cities.values():
        tmp = find_state(input)
        print(input, "is the capital of", tmp)
    elif input in states:
        print(capital_cities[states[input]], "is the capital of", input)
    else:
        print(input, "is neither a capital city nor a state")


if __name__ == '__main__':
    capital_cities = { "OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver" }
    states = { "Oregon" : "OR", "Alabama" : "AL", "New Jersey": "NJ", "Colorado" : "CO" }
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
           tmp = sys.argv[i].lower().capitalize()
           handler(tmp)
    else:
        sys.exit(0)