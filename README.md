# place_finder

This app uses the Google Places API and the Google Geocoding API to allow someone to perform a radius search on any location and it will return a .csv with all of the places that match the search, each place having a name, phone number, and website associated with it. 

It can be used in 2 ways: manual input mode, where the user runs the file from a cli and manually inputs places to be searched, or email mode, where a user can email theplacefinder123 <at> gmail <dot> com. After sending that email, the place finder will respond with an attached .csv with all the desired information. An example of the format for this email is below:

# state wide search

(no subject)

State: OH NY CA#
Radius: 500#
Keyword: advertising#

# specific location search

(no subject)

Location: New York, New York#
Radius: 500#
Keyword: burgers#

The app could be useful in anything from marketing to trying to find the best burger joint in town.
