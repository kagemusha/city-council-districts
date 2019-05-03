import requests
from bs4 import BeautifulSoup
import csv
import re

start_district = 1
end_district = 51 #51
contact_sel = ["[aria-label='Legislative office contact information'] p",
               "[aria-label='District office contact information'] p",
               ]
phone_re = re.compile("\d{3}(.*?)\d{3}(.*?)\d{4}", re.MULTILINE)

def scrape():
  districts = [district_scrape(i) for i in range(start_district, end_district+1)]
  write_to_csv(districts)

def district_scrape(district):
  url = f"https://council.nyc.gov/district-{district}"
  print("---------------")
  print(url)
  hdr = {'User-Agent': 'Mozilla/5.0'}
  page = requests.get(url, headers=hdr)
  content = BeautifulSoup(page.content, 'html.parser')
  name = content.select('h4.district-member a')[0].get_text()

  contact_info = None
  phone = ''
  for sel in contact_sel:
    contact_info = content.select(sel)
    if contact_info:
      contact_info = contact_info[0].get_text()
      phone_match = phone_re.search(contact_info).group(0)
      phone = re.sub('[^0-9]', '', phone_match)
      phone = phone[0:3]+"-"+phone[3:6]+"-"+phone[6:]
      break

  email_elem = content.select(".callout a")
  email = ''
  if email_elem:
    email = email_elem[0].get_text()[11:]
  return {
    'url': url,
    'district': district,
    'name': name,
    'phone': phone,
    'email': email
  }

def write_to_csv(districts):
  try:
    with open("city_council_districts.csv", 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=["district","name","phone","email","url"])
      writer.writeheader()
      for data in districts:
        writer.writerow(data)
  except IOError:
    print("I/O error")

def __main__():
  scrape()

if __name__ == '__main__':
  __main__()
