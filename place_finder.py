import requests
import json
from email_helper import check_newmail, send_newmail
import csv
import important_info

def detail_finder(m_list, data):

	for place in data['results']:
		this_placeid = place['place_id']
		details_params = {'placeid':  this_placeid,
						  'key': key
		}
		details_reponse = requests.get("https://maps.googleapis.com/maps/api/place/details/json?", params = details_params)
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
	if 'next_page_token' in data.keys():
		response_params = {'pagetoken': data['next_page_token'],
							'key': key}
		response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params = response_params)
		data = response.json()
		m_list.extend(detail_finder(m_list, data))

	return m_list


key = important_info.key

manual_input = False



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


response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + desiredLocation + "&key=" + key)
data = response.json()

# print(data['results'][0]['geometry']['location']['lat'])
location = data['results'][0]['geometry']['location']
places_params = {'location': str(location['lat']) + ',' + str(location['lng']),
				 'radius': radius,
				 'keyword': keyword,
				 'key': key

}
response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params = places_params)

data = response.json()
master_list = []
master_list = detail_finder(master_list, data)

print(master_list)
with open('out.csv', 'w') as out:
	writer = csv.writer(out)
	for item in master_list:
		writer.writerow(item.split("&"))

send_newmail(the_params[0])

