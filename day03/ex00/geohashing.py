import sys
import antigravity

def calculate_geohash(latitude, longitude, datedow):
    try:
        lat = float(latitude)
        lon = float(longitude)
        antigravity.geohash(lat, lon, datedow.encode())  
    except ValueError:
        print("Error: Invalid latitude, longitude, or datedow provided. Please enter valid values.")
        sys.exit(1)

def main():
    if len(sys.argv) < 4:
        print("Usage: python geohashing.py <latitude> <longitude> <datedow>")
        sys.exit(1)
    
    latitude = sys.argv[1]
    longitude = sys.argv[2]
    datedow = sys.argv[3]  

    calculate_geohash(latitude, longitude, datedow)

if __name__ == "__main__":
    main()
