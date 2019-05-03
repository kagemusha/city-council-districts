# Needed for package:
# brew install spatialindex

from opencage.geocoder import OpenCageGeocode
import rtree
import shapely
import shapely.geometry
import fiona
import pandas as pd
import csv
import json

class CityCouncilDistrictLookup:


  def __init__(self):
    self.geocoder = self.init_geocoder()
    district_shapefile = 'data/geo_export_6ca8bf69-89f9-4f50-9f4e-6d8a38fd1527.shp'
    self.cd_rtree, self.cd_shape = self.get_district_rtree(district_shapefile)
    self.district_reps = self.get_district_reps()


  def init_geocoder(self):
    key = '4a64e6ab9b60437f9f09966cbcdbb032'
    return OpenCageGeocode(key)

  def get_district_reps(self):
    reader = csv.DictReader(open('data/city_council_districts.csv', 'r'))
    district_reps = {}
    for district in reader:
      district_reps[district['district']] = json.dumps(district)
    return district_reps

  def get_district_rtree(self, shapefile):
    shapes = {}
    district_rtree = rtree.index.Index()
    for i, district_shape in enumerate(fiona.open(shapefile)):
      district = int(district_shape['properties']['coun_dist'])
      shapes[district] = shapely.geometry.asShape(district_shape['geometry'])
      district_rtree.insert(
        district, shapely.geometry.asShape(district_shape['geometry']).bounds)
    return district_rtree, shapes

  def get_district_for_point(self, lat, lng):
    if pd.isnull(lat) or pd.isnull(lng):
      return 'unknown'
    point = shapely.geometry.Point(lng, lat)
    containing_districts = [
      d for d in self.cd_rtree.intersection((lng, lat))
      if self.cd_shape[d].contains(point)]
    district_count = len(containing_districts)
    if district_count > 1:
      raise Exception(
        'Found multiple council districts for point (' + str(lat) + ', ' + str(lng) + '): ' +
        str(containing_districts))
    elif district_count == 0:
      return 'not found'
    else:
      return self.district_reps[str(containing_districts[0])]


  def addr_to_district(self, addr):
    results = self.geocoder.geocode(addr)
    geom = results[0]['geometry']
    return self.get_district_for_point(geom['lat'], geom['lng'])


def __main__():
  district_lookup = CityCouncilDistrictLookup()
  addrs = [
    u'60 Wall St, 10005',
    u'43 E 19th St, New York, NY 10003',
    u'111 8th Ave, New York, NY 10011',
    u'444 W 19th St, 10011',
    u'29 E 39th St, New York, NY 10016',
    u'5 Bryant Park, 10018',
    u'10-0-10-98 46th Ave Long Island City, NY 11101',
    u'61 Grove St, New York, NY 10014',
    u'15 Stuyvesant Oval, NY 10009',
    u'1378 3rd Ave,New York, NY 10075',
    u'601 W. 57th St, New York, NY 10019',
    u'68 Dean St. 11201'

  ]
  for addr in addrs:
    print(district_lookup.addr_to_district(addr), addr)

if __name__ == "__main__":
  __main__()

