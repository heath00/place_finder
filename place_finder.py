import requests
import json
from email_helper import check_newmail, send_newmail
import csv
import important_info
import city_reader

key = important_info.key
separator = "*&*"

# takes data returned from the places list search and performs a detailed
# search on the google places API.
# returns a list of all info for businesses in a given city
def detail_finder(data, p_api, state=None):
	details_api = "https://maps.googleapis.com/maps/api/place/details/json?"

	the_list = []
	print ('Number of places returned from api is: ' + str(len(data['results'])))

	#for every place returned by the general search, perform a detailed search 
	#to get name, phone, website
	for place in data['results']:
		this_placeid = place['place_id']
		details_params = {'placeid':  this_placeid,
						  'key': key
		}
		details_reponse = requests.get(details_api, params = details_params)
		details_data = details_reponse.json()
		new_entry = ""
		try:
			name = details_data['result']['name']
			print(name)
			new_entry += name + separator
		except KeyError:
			#if no name
			print('No name given')
			new_entry += 'X' + separator
		try:
			phone = details_data['result']['formatted_phone_number']
			print(phone)
			new_entry += phone + separator
		except KeyError:
			#if no phone
			print('No phone number given')
			new_entry += 'X' + separator
		try:
			site = details_data['result']['website']
			print(site + "\n")
			new_entry += site
		except KeyError:
			#if no website
			print('No website given')
			new_entry += 'X'
		if state:
			#if searching statewide, append the state for clarity
			new_entry += separator + state

		# the_list.append(new_entry)
		the_list.append(new_entry)

	return the_list

# # **for single city search**
# # takes a full us postal location and turns it into a geocode
def get_single_geocode(g_api, full_location):
	response = requests.get(g_api + full_location + '&key=' + key)
	data = response.json()
	return data

# **for multiple city/state searches**
# takes a city and state and turns it into a geocode using google's geocoding 
# to be used in the google places API search
def get_state_city_geocode(g_api, city, state):
	full_location = city + ',+' + state
	response = requests.get(g_api + full_location + '&key=' + key)
	data = response.json()
	return data

# gives the geocode for a given place to the google place API,
# along with radius and keyword to be used in the search
# returns the list of just place_id's, which don't have business name or website
def get_full_places_list(p_api, g_data, rad, keywd):

	location = g_data['results'][0]['geometry']['location']
	places_params = {'location': str(location['lat']) + ',' + str(location['lng']),
					 'radius': rad,
					 'keyword': keywd,
					 'key': key

	}

	response = requests.get(p_api, params = places_params)

	data = response.json()
	return data



def main():

	geocode_api = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	places_api = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?'

	manual_input = True
	state_search = False

	if manual_input:
		if input("Do you want to perform a statewide search? (Enter Y or N): ") == 'Y':
			state_search = True
			desiredLocation = input("Enter state or states to search. If multiple, separate them by a space: ").split()
		else:
			desiredLocation = input("What city do you want to view? (Type in US postal format): ")
			desiredLocation = desiredLocation.replace(' ', '+')
		radius = input("How broad should the search be? (In meters): ")
		keyword = input("What should the keyword be?: ")
			# print(desiredLocation)
	else:
		the_params = check_newmail()

		if the_params == None:
			print('No new mail')
			return None
		elif the_params[0] == 1:
			#indicates a state search is to be performed
			state_search = True
			desiredLocation = the_params[1]
			radius = the_params[2]
			keyword = the_params[3]
			sender = the_params[4]
		else:
			desiredLocation = the_params[0]
			radius = the_params[1]
			keyword = the_params[2]
			sender = the_params[3]



	master_list = []
	if state_search == True:
		for state in desiredLocation:
			print("Performing state searches:")
			cities = city_reader.get_cities(state)
			for city in cities:
				if city:
					print("\nSearching with city: " + city)
					geocode_data = get_state_city_geocode(geocode_api, city, state)
					places_data = get_full_places_list(places_api, geocode_data, radius, keyword)
					master_list += detail_finder(places_data, places_api, state)



	else:
		geocode_data = get_single_geocode(geocode_api, desiredLocation)
		places_data = get_full_places_list(places_api, geocode_data, radius, keyword)

		master_list.extend(detail_finder(places_data, places_api))

	##SUPER HACKY NEED TO FIX THIS ISSUE
	master_list = list(set(master_list))
	ml_length = len(master_list)
	print(master_list)
	print("Length of list is: ", ml_length)
	with open('out.csv', 'w') as out:
		writer = csv.writer(out)
		for item in master_list:
			writer.writerow(item.split(separator))
	if manual_input == True:
		print("Check the new out.csv in this same directory.")
	else:
		if state_search == True:
			send_newmail(', '.join(the_params[1]), ml_length, sender)
		else:
			send_newmail(the_params[0], ml_length, sender)

if __name__ == "__main__":
	main()