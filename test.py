# import os
# os.environ["OLAMAPS_API_KEY"] = "UkUs3JeMNDj7LCtp5b23WQCZXC6qdoIaxqwCaXhn"
# os.environ["OLAMAPS_CLIENT_ID"] = "f088c41f-7a62-454f-83c7-18dcafa2d769"
# os.environ["OLAMAPS_CLIENT_SECRET"] = "COBQQs6ltCUv7zlkebv2vSXojJ3gPhqM"
# from olamaps import Client

# # Initialize the client
# client = Client()

# # Autocomplete a query
# autocomplete_results = client.autocomplete("Kempe")
# # Geocode a text address
# geocode_results = client.geocode("Chennai")
# print(geocode_results)
# # Reverse geocode a latitude-longitude pair
# reverse_geocode_results = client.reverse_geocode(
#     lat="12.9519408",
#     lng="77.6381845",
# )

# # Get directions
# directions_results = client.directions(
#     origin="12.993103152916301,77.54332622119354",
#     destination="12.972006793201695,77.5800850011884",
# )
# def dosomething2(location):
#     geocode_results = client.geocode("Chennai")
#     print(geocode_results)
#     return geocode_results


import geocoder
g = geocoder.ip('me')
print(g.latlng)
