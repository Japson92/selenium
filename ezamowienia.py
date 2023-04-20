import urllib.request, urllib.error
import sqlite3
import json
import firstUse
import ssl

url = "https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&PublicationDateFrom=2023-04-18T00:00:00&PublicationDateTo=2023-04-19T23:59:59&PageSize=10"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('Noticedatabase.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Notice")
cur.execute('''
CREATE TABLE IF NOT EXISTS Notice (noticeType TEXT, noticeNumber TEXT, bzpNumber TEXT, 
publicationDate TEXT, orderObject TEXT, cpvCode TEXT, submittingOffersDate TEXT, 
organizationName TEXT, organizationCity TEXT, organizationProvince TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))

js = json.loads(data)
print(json.dumps(js, indent=4))


print(js[0]["orderType"])
count = 0
for line in js: 
    cur.execute('''INSERT INTO Notice (noticeType, noticeNumber, bzpNumber, publicationDate,
        orderObject, cpvCode, submittingOffersDate, organizationName, organizationCity, 
        organizationProvince) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (js[count]["noticeType"], js[count]["noticeNumber"], js[count]["bzpNumber"],
                 js[count]["publicationDate"], js[count]["orderObject"], js[count]["cpvCode"],
                 js[count]["submittingOffersDate"], js[count]["organizationName"],
                 js[count]["organizationCity"], js[count]["organizationProvince"]))
    count += 1
conn.commit()
# searchingNumber = cur.execute("""SELECT bzpNumber FROM Notice WHERE
#             orderObject='Dostawa oprogramowania do wirtualizacji wraz  z dożywotnimi licencjami'""",
#                               )
searchingNumber = "2023/BZP 00179991"
firstUse.searching_date(searchingNumber)
# print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
