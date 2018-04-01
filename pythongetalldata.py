from pymongo import MongoClient
import pymongo
import json, requests
import datetime
import re


result = re.findall('"pk":(\d+),"ID"', open("./data.htm","r").read())
#result = ["255501"]
client = MongoClient('mongodb://localhost:27017')
db = client.max_api
listing = db.listings
for item in result:
    print("Check => " + str(item))
    url = "https://www.ultracasas.com/api/app/inmuebles/publicaciones/detail?pk=" + item
    result = requests.get(url)
    data = json.loads(result.text)
    information = {
        "active": True,
        "description" : data["oProperty"]["descripcion"],
        "type_home":data["oProperty"]["tipo"],
        "mlsId" : str(data["oProperty"]["ID"]),
        "additionalRooms" : "",
        "area" : data["oProperty"]["supconstruida"] if data["oProperty"]["supconstruida"] != None else 0,
        "bathsFull" : data["oProperty"]["numBanios"] if data["oProperty"]["numBanios"] != None else 0,
        "bathsHalf" : data["oProperty"]["numBanios"] if data["oProperty"]["numBanios"] != None else 0,
        "bedrooms" : data["oProperty"]["numDormitorios"],
        "city" : data["oProperty"]["region"],
        "closePrice" : float(data["oProperty"]["precioSinFormato"]),
        "country" : "Bolivia",
        "directions" : data["oProperty"]["direccion"],
        "disclaimer" : "Los datos dispuestos en este sitio fueron obtenidos de otros sitios inmoviliarios",
        "exteriorFeatures" : "Dog Run,Patio-Uncovered,Sidewalk",
        "foundation" : "Slab",
        "services" : data["oProperty"]["servicios"],
        "heating" : "Central Heat,Natural Gas",
        "interiorFeatures" : "",
        "simply_rets_lat" : data["oProperty"]["latitud"],
        "listPrice" : float(data["oProperty"]["precioSinFormato"]),
        "listingId" : data["oProperty"]["pk"],
        "simply_rets_lng" : data["oProperty"]["longitud"],
        "lotDescription" : "Both Cats & Dogs",
        "marketArea" : data["oProperty"]["supterreno"],
        "elevator": data["oProperty"]["elevador"],
        "baulera": "No",
        "pool": data["oProperty"]["piscina"],
        "estado" : data["status"],
        "status" : "Closed",
        "zona" : data["oProperty"]["zona"],
        "streetName" : data["oProperty"]["direccion"],
        "style" : "Family,Formal Living,Pantry,Utility",
        "tax" : "04123406170000",
        "oferta": data["oProperty"]["oferta"],
        "view" : "Greenbelt,Woods",
        "water" : "0",
        "parking" : data["oProperty"]["numParqueos"],
        "yearBuilt" : data["oProperty"]["anioconstruccion"],
        "agentLastName" : data["oContact"]["lastname"],
        "agentFirstName" : data["oContact"]["name"],
        "movil" : data["oContact"]["movil"],
        "phone" : data["oContact"]["phone"] if data["oContact"]["phone"] != None else "",
        "email" : data["oContact"]["email"],
        "foto_broker" : data["oContact"]["foto"],
        "agentId" : -1,
        "district" : data["oProperty"]["region"],
        "highSchool" : "Austin",
        "updated" : True,
        "furniture" :data["oProperty"]["amoblado"],
        "google_lat" : float(data["oProperty"]["latitud"]),
        "lat" : float(data["oProperty"]["latitud"]),
        "google_lng" : float(data["oProperty"]["longitud"]),
        "lng" : float(data["oProperty"]["longitud"]),
        "customGeo" : True,
        "closed" : True,
        "featured_listing": True,
        "geo_ids" : [
            "-1"
            ]
        }
    #tipo de oferta
    if data["oProperty"]["oferta"] == "Alquiler":
        information["type"] = "RNT"
    else if data["oProperty"]["oferta"] == "Anticretico":
        information["type"] = "ANT"
    else:
        information["type"] = "RES"
    if data["oProperty"]["tipo"] == "Terreno":
        information["type"] = "L"
    #"full" : data["oProperty"]["ogTitle"] + data["oProperty"]["region"],
    if data["oProperty"]["ogTitle"] == None:
        information["full"] = "%s %s"%(data["oProperty"]["direccion"], data["oProperty"]["region"])
    else:
        information["full"] = "%s %s %s"%(data["oProperty"]["ogTitle"], data["oProperty"]["direccion"], data["oProperty"]["region"])
    date_p = data["oProperty"]["fecpublicacion"].split("/")
    dateFormat = "%s-%s-%s%s"%(date_p[2], date_p[1], date_p[0], "T10:53:53.000Z")
    dateFormat = datetime.datetime.strptime(dateFormat, "%Y-%m-%dT%H:%M:%S.000Z")
    information["updated_at"] = dateFormat
    information["created_at"] = dateFormat
    if  len(data["oProperty"]["images"]) > 0:
        try:
            information["primary_photo"] = data["oProperty"]["images"][0]["real"]
        except KeyError:
            print "Error With the main Image in real key in " + str(data["oProperty"]["pk"])
            information["primary_photo"] = "None"
    else:
        information["primary_photo"] = "none"
    information["pictures"] = []
    for item in data["oProperty"]["images"]:
        try:
            information["pictures"].append(item["real"])
        except KeyError:
            print "Error With the images in " + str(data["oProperty"]["pk"])
            information["pictures"].append("None")
    try:
        listing.insert(information)
    except pymongo.errors.WriteError:
        print "Error In the insert Please Check the PK " + str(data["oProperty"]["pk"])
