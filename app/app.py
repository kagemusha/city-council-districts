# docker run -d -p 5000:5000 app
from flask import Flask, request
from city_council_lookup import CityCouncilDistrictLookup
from urllib.parse import unquote

app = Flask(__name__)
district_lookup = CityCouncilDistrictLookup()
@app.route('/')
def addr_to_city_council_member():
  addr = request.args.get('addr')
  if not addr:
    return "Need an address"
  addr = unquote(addr)
  return str(district_lookup.addr_to_district(addr))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')