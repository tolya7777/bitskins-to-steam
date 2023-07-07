import pyotp
import requests
import json
import os

my_secret = 'AUUYOMBDK3BEGANK'
my_token = pyotp.TOTP(my_secret)
my_key = 'ae905244-4e8a-401a-9b29-eb90780dee0c'
itemName = "Operation Hydra Case"

os.chdir('c:/Users/Tolya/Desktop/bitskins')

r = requests.get('https://bitskins.com/api/v1/get_steam_price_data/?api_key=' + my_key + '&code=' + my_token.now() + '&market_hash_name=' + itemName + '&app_id=APP_ID')
r1 = r.json()

#creating jsons of all bitskins and steam items
r = requests.get('https://bitskins.com/api/v1/get_all_item_prices/?api_key=ae905244-4e8a-401a-9b29-eb90780dee0c&app_id=730&code=' + my_token.now())
steam_items = r.json()

r = requests.get('https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key=' + my_key + '&code=' + my_token.now() + '&app_id=APP_ID')
bitskins_items = r.json()


#Writing list of bitskins and steam items
file = open("list_of_steam_items.txt", "w",encoding = "utf-8")
file.write(str(steam_items))
file.close()

file = open("list_of_bitskins_items.txt", "w",encoding = "utf-8")
file.write(str(bitskins_items))
file.close() 

file = open("prices.txt", "w", encoding = "utf-8")

listOfItems = []

class ItemPricePair:
    name = 'N/A'
    price = 0
    def __init__(self, n, p):
        self.name = n
        self.price = p
    def __str__(self):
        s = self.name + " | " + str(self.price) + "\n"
        return s
           
    

y = 0
highest_ratio_item = "null"
for steam_object in steam_items['prices']:
    steam_price = steam_object['price']
    bitskins_price = 0
    

    for bitskins_object in bitskins_items['data']['items']:
        if(bitskins_object['market_hash_name'] == steam_object['market_hash_name']):
            bitskins_price = bitskins_object['lowest_price']
            break

    if (float(bitskins_price) != 0.00):
        
        new_ratio = float(steam_price) / float(bitskins_price)

        
        listOfItems.append(ItemPricePair(steam_object['market_hash_name'], new_ratio))


        #file.write(str(item))
        
        if (new_ratio > y):
            y = new_ratio
            highest_ratio_item = steam_object['market_hash_name']
        
print("Ratio: ", y , "Item: ", highest_ratio_item)
listOfItems.sort(key = lambda x: x.price, reverse = True)

for item in listOfItems:
    file.write(str(item))

file.close()
