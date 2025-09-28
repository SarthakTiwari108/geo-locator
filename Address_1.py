from geopy.geocoders import Nominatim

def get_coords_from_address(address_string):
    geolocator=Nominatim(user_agent="my_geocoder")
    try:
        location=geolocator.geocode(address_string)
        if location:
            print(f"Coordinates for '{address_string}':Latitude={location.latitude},Longitude={location.longitude}")
            return location.address
        else:
            return f"Address details not found for '{address_string}'."
    except Exception as e:
        return f"Error: {e}"

def get_address_from_coords(lat,long):
    geolocator=Nominatim(user_agent="my_geocoder")
    try:
        location=geolocator.reverse((lat,long))
        if location:
            print(f"Address for coordinates ({lat},{long}):")
            return location.address
        else:
            return f"Address not found for coordinates ({lat},{long})."
    except Exception as e:
        return f"Error: {e}"
print("Choose an option:")
print("1. Find coordinates from place name")
print("2. Find address from coordinates")
choice=input("Enter 1 or 2: ")
if choice=="1":
    place_name=input("Enter a place name: ")
    address_details=get_coords_from_address(place_name)
    print(f"Full details: {address_details}")

elif choice=="2":
    lat=float(input("Enter latitude: "))
    long=float(input("Enter longitude: "))
    address_details=get_address_from_coords(lat,long)
    print(f"Full details: {address_details}")
else:
    print("Invalid choice. Please run again and enter 1 or 2")
