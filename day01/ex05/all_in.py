import sys

def find_capital_city(state,capital):
    if state in states:
        print(capital[states[state]])
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


if __name__ == '__main__':
    capital_cities = { "OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver" }
    states = { "Oregon" : "OR", "Alabama" : "AL", "New Jersey": "NJ", "Colorado" : "CO" }
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
           tmp = sys.argv[i].lower().capitalize()
           capitall =  find_capital_city(tmp, states)
           statee =  find_state(tmp)
           print(capitall)
           print(statee)
           if capitall is None and statee is None:
               print(tmp,"is neither a capital city nor a state")
           else:
                print(sys.argv[i],"is the capital of",statee)
    else:
        sys.exit(0)