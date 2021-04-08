import json
import requests
import random
from datetime import date
from geopy.geocoders import Nominatim
import json
import urllib,base64

#get API credential given API name and attribute 
def getAPI_credential(api_name, api_attribute):
    data = json.load (open('API_credentials.json',))
    return data[api_name][api_attribute]
#this function encode consumer_key, consumer_secret according to the HERE API requirement
def encodeBase64(consumer_key, consumer_secret):
    # 1. URL encode the consumer key and the consumer secret according to RFC 1738.
    dummy_param_name = 'bla'
    key_url_encoded = urllib.parse.urlencode({dummy_param_name: consumer_key})[len(dummy_param_name) + 1:]
    secret_url_encoded = urllib.parse.urlencode({dummy_param_name: consumer_secret})[len(dummy_param_name) + 1:]

    # 2. Concatenate the encoded consumer key, a colon character “:”, and the encoded consumer secret into a single string.
    credentials = '{}:{}'.format(key_url_encoded, secret_url_encoded)

    # 3. Base64 encode the string from the previous step.
    bytes_base64_encoded_credentials = base64.encodebytes(credentials.encode('utf-8'))

    return bytes_base64_encoded_credentials.decode('utf-8').replace('\n', '')
def get_latitude_longitude(City):
    
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(City)
    #print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))
    Geo_adress={'Latitude':location.latitude,'Longitude': location.longitude}
    return Geo_adress
def invoke_api(fulfillment, slots_values_list):
    print("\n\n\n\n\n=========> CALL API ",fulfillment)
    if fulfillment == "SearchBusiness_fulfillment":
        url = 'https://api.yelp.com/v3/businesses/search?term=[%term%]&location=[%location%]&limit=1'
        headers = {}
        term = ''
        for slot in slots_values_list:
            url = url.replace('[%{}%]'.format(slot['name']),
                              slot['value'] if not isinstance(slot['value'], list) else '+'.join(slot['value']))
            if slot['name'] == 'term':
                term = slot['value']
        Authorization=getAPI_credential('api.yelp','Authorization')
        headers.update({'Authorization': Authorization})
        result = requests.get(url, headers=headers)
        jsonResult = result.json()
        if result.status_code == 200:
            try:
                businesses = []
                for business in jsonResult['businesses']:
                    businesses.append({'name': business['name'], 'phone': business['phone'],'address': business['location']['address1'] + ' ' + business['location']['city'],'id': business['id']})
                reply = " {}".format(' ** \n '.join(
                    ['{} Restaurant, Phone: {}, address : {}, Business id: {} '.format(business['name'], business['phone'], business['address'], business['id']) for business
                     in businesses]))
                return "This one serves "+str(term[0])+" food:" + reply
            except Exception as e:
                return e.message
        else:
            try:
                return jsonResult['message']
            except KeyError as error:
                return "Something went wrong in the third-party API"
    if fulfillment == "GetWeather_fulfillment":
        appid=getAPI_credential('api.openweathermap','appid')
        url = 'http://api.openweathermap.org/data/2.5/weather?q=[%q%]&appid='+appid
        for slot in slots_values_list:
            url = url.replace('[%{}%]'.format(slot['name']),
                              ' '.join(slot['value']) if isinstance(slot['value'], list) else slot['value'])
        result = requests.get(url)
        jsonResult = result.json()
        if result.status_code == 200:
            weatherCondition = jsonResult['weather'][0]['description']
            reply = "There is {} in there.".format(weatherCondition)
            print(reply)
            return reply
        else:
            #print(jsonResult['message'])
            return "There is light rain in there."

    if fulfillment == "BookDoctorAppointment_fulfillment":
         reply = "Done! Your appointment with Dr. [%doctorname%] on [%Appointmentdate%] is scheduled. You will receive a confirmation email shortly"
         for slot in slots_values_list:
            if slot['name'] == "Appointmentdate": 
                slot['value']=slot['value'].split('T')[0]
            reply = reply.replace('[%{}%]'.format(slot['name']), slot['value'])
            print(reply)
         return reply

    if fulfillment=="SearchCinema_fulfillment":
        location = ''
        apikey=''
        for slot in slots_values_list:
            if slot['name'] == 'location':
                location = slot['value']  
        apikey = getAPI_credential('here','apikey')
        print('****')
        print ('location', location)
      #  print('apikey', apikey)
        ## transformation from location to geo coordinates Latitude and Longitude
        Geocoordinates=get_latitude_longitude(location)
        url='https://places.ls.hereapi.com/places/v1/discover/search?at='+str(Geocoordinates['Latitude'])+','+str(Geocoordinates['Longitude'])+'&q=cinema&size=1&apiKey='+apikey

        result = requests.get(url)
        json_Result = result.json()
        
        #print(json_Result)
        if result.status_code == 200:
            if  json_Result['results']['items']:
                items=json_Result['results']['items']
                Cinema_list=[]
                for  Cinema in items:
                    Cinema_list.append({'name':  Cinema['title'], 'rating': Cinema['averageRating'], 'address':  Cinema['vicinity']})

               
                reply = "I found: {}".format(' ** '.join(['{} Cinema, address: {}, rating: {}'.format(Cinema['name'], Cinema['address'],Cinema['rating']) for Cinema in  Cinema_list]))
                return reply
               
            else:
                reply = "Sorry, there is no cinema that matches your request"
                return reply

    if fulfillment == "BookTaxi_fulfillment":
        reply = "Done! I booked a taxi on [%pickupDate%] at [%pickupTime%] from [%pickupAddress%] to [%dropoffAddress%]."
        for slot in slots_values_list:
            if slot['name'] == "pickupDate":
                slot['value']=slot['value'].split('T')[0]
            elif slot['name'] == "pickupTime":
                slot['value']=slot['value'].split('T')[1].split('+')[0]

            reply = reply.replace('[%{}%]'.format(slot['name']),
                              slot['value'] if not isinstance(slot['value'], list) else '+'.join(slot['value']))
        return reply
    if fulfillment=="FindDoctor_fulfillment":
        City = ''
        Dtype = ''
        apikey=''
        for slot in slots_values_list:
            if slot['name'] == 'City':
                City = slot['value']   
            elif slot['name'] =='Type'and slot['value']=='Dentist':
                 Dtype = slot['value']
            else: 
                 Dtype = 'Doctor'
       
        apikey = getAPI_credential('here','apikey')     
        print("Type : ", Dtype)
        print("City : ", City)
        print("apikey : ", apikey)

        ## transformation from city to geo coordinates Latitude and Longitude 
        Geocoordinates=get_latitude_longitude(City)
        url='https://places.ls.hereapi.com/places/v1/discover/search?at='+str(Geocoordinates['Latitude'])+','+str(Geocoordinates['Longitude'])+'&q='+Dtype+'&apiKey='+apikey

        result = requests.get(url)
        json_Result = result.json()
       
        #print(json_Result)
        if result.status_code == 200: 
            if  json_Result['results']['items']:
                items=json_Result['results']['items']
                Doctors_list=[]
                for Doctor in items: 
                   Doctors_list.append({'name': Doctor['title'], 'rating':Doctor['averageRating'], 'address': Doctor['vicinity']})

                print (Doctors_list)
                reply = "Here what I found:\n {}".format(', \n'.join(['doctor_name/Center: {}\n address: {}\n rating: {}'.format(Doctor['name'], Doctor['address'],Doctor['rating']) for Doctor in  Doctors_list]))
                return reply
                
            else:
                reply = "Sorry, there is no doctor that matches your request"
                return reply
                
        else:
            return jsonResult['message'] 
    if fulfillment == "CheckDoctorAvailabilities_fulfillment":
        free_days = [['Monday', 'Wednesday', ' and Thursday'], ['Tuesday','Friday',' and Saturday'], ['Thursday','Friday',' and Sunday'], ['Tuesday',' and Friday']]
        dr_free_days = random.choice(free_days)
        result  = '{"DRCalendar": {"date": "['+''.join(dr_free_days)+']"}}'
        jsonResult = json.loads(result)
        for slot in slots_values_list:
            if slot['name'] == 'doctor':
                dr = slot['value']
        res = ''
        for day in dr_free_days:
            res += day + " "
        result = 'The doctor will be available on: '+ res
        return result
 
    if fulfillment == "ReserveRoundtripFlights_fulfillment":
        reply="Done! I have booked your flight tickets for [%departureDate%] to [%returnDate%], flying from [%originLocation%] to [%destinationLocation%]."
        for slot in slots_values_list:
            if slot['name'] in {'departureDate','returnDate'}:
                slot['value']=slot['value'].split('T')[0]
            reply = reply.replace('[%{}%]'.format(slot['name']), slot['value'])
        print(reply)
        return reply
    if fulfillment == "ReserveHotel_fulfillment":
        reply="Done! Your booking in [%city%] for [%checkInDate%] to [%checkOutDate%] is confirmed."
        for slot in slots_values_list:
            if slot['name'] in {'checkInDate','checkOutDate'}:
                slot['value']=slot['value'].split('T')[0]
            reply = reply.replace('[%{}%]'.format(slot['name']), slot['value'])
        print(reply)
        return reply

   # if fulfillment == "Reviews": (to be completed by you)
        
   
      
        
