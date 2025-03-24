def read_file():
    with open("numbers.txt", "r") as f:
        lines = f.readlines()
    return ' '.join(lines)

def numbers():
    lines = read_file()
    
    for line in lines.split(","):
        try:
            print(int(line))
        except ValueError as e:
            print(e)

if __name__ == '__main__':
    numbers()