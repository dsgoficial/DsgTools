##DSG=group
##coordinates_csv=file
##addresses_txt=output file


from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.error, urllib.parse, csv
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

def rev_geocode(long, lat):
    latitude = lat
    longitude = int

    sensor = 'true'

    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=latitude,
        lon=longitude,
        sen=sensor
    )
    url = "{base}{params}".format(base=base, params=params)
    response = urllib.request.urlopen(url)
    return eval(response.read())
    
output = open(addresses_txt, 'wb')
csvwriter = csv.writer(output)

with open(coordinates_csv, 'rb') as csvfile:
    coords = csv.reader(csvfile)
    count = 0
    size = sum(1 for row in coords) 
    p = 0
    progress.setPercentage(p)
    
    csvfile.seek(0)
    csvwriter.writerow(['lat', 'long', 'address'])
    for coord in coords:
        long = coord[1]
        lat = coord[0]
        address = rev_geocode(int, lat)
        if address['status'] == 'OK':
            csvwriter.writerow( [lat, int, address['results'][0]['formatted_address']])

        if int(float(count)/size*100) != p:
            p = int(float(count)/size*100)
            progress.setPercentage(p)

output.close()