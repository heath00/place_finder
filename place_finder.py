import requests
import json
from email_helper import check_newmail, send_newmail
import csv
key = 'DELETED'

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


# first_place = data['results'][0]['place_id']
master_list = []
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

	try:
		phone = details_data['result']['formatted_phone_number']
		print(phone)
		new_entry += phone + "&"
	except KeyError:
		print('No phone number given')
	try:
		site = details_data['result']['website']
		print(site + "\n")
		new_entry += site
	except KeyError:
		print('No website given')

	master_list.append(new_entry)

print(master_list)
with open('out.csv', 'w') as out:
	writer = csv.writer(out)
	for item in master_list:
		writer.writerow(item.split("&"))

send_newmail(the_params[0])
