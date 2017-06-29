import requests
import json
from email_helper import check_newmail, send_newmail
import csv
import important_info

def detail_finder(m_list, data, p_api, nby_search):
	details_api = "https://maps.googleapis.com/maps/api/place/details/json?"

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
			new_entry += name + "&"
		except KeyError:
			print('No name given')
			new_entry += "X&"
		try:
			phone = details_data['result']['formatted_phone_number']
			print(phone)
			new_entry += phone + "&"
		except KeyError:
			print('No phone number given')
			new_entry += 'X&'
		try:
			site = details_data['result']['website']
			print(site + "\n")
			new_entry += site
		except KeyError:
			print('No website given')
			new_entry += 'X'

		m_list.append(new_entry)
	if nby_search:
		if 'next_page_token' in data.keys():
			print('\nOpening new page...\n')
			response_params = {'pagetoken': data['next_page_token'],
								'key': key}
			response = requests.get(p_api, params = response_params)
			data = response.json()
			m_list.extend(detail_finder(m_list, data))

	return m_list


def main():
	key = important_info.key
	geocode_api = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	places_api = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?'

	manual_input = True
	nearby_search = 'nearby' in places_api

	if manual_input:
		desiredLocation = input("What city do you want to view? (Type in US postal format): ")
		desiredLocation = desiredLocation.replace(' ', '+')
		radius = input("How broad should the search be? (In meters): ")
		keyword = input("What should the keyword be?: ")
		# print(desiredLocation)
	else:
		the_params = check_newmail()
		desiredLocation = the_params[0]
		desiredLocation = desiredLocation.replace(' ', '+')
		radius = the_params[1]
		keyword = the_params[2]


	response = requests.get(geocode_api + desiredLocation + "&key=" + key)
	data = response.json()

	location = data['results'][0]['geometry']['location']
	places_params = {'location': str(location['lat']) + ',' + str(location['lng']),
					 'radius': radius,
					 'keyword': keyword,
					 'key': key

	}
	response = requests.get(places_api, params = places_params)

	data = response.json()
	master_list = []
	master_list = detail_finder(master_list, data, places_api, nearby_search)

	ml_length = len(master_list)
	print(master_list)
	print("Length of list is: %d", ml_length)
	with open('out.csv', 'w') as out:
		writer = csv.writer(out)
		for item in master_list:
			writer.writerow(item.split("&"))
	if manual_input == True:
		send_newmail(desiredLocation.replace('+', ' '), ml_length)
	else:
		send_newmail(the_params[0], ml_length)

if __name__ == "__main__":
	main()