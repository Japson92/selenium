import urllib.request, urllib.error
import sqlite3
import json
import firstUse
import ssl

#
# startDate = input("Podaj date początkową wyszukiwanych ogłoszeń w formacie YYYY-MM-DD. ")
# endDate = input("Podaj date końcową wyszukiwanych ogłoszeń w formacie YYYY-MM-DD. ")


def gov_serch(startDate, endDate):
    url = "https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&CpvCode=34971000&CpvCode=45000000&OrganizationProvince=PL26&PublicationDateFrom={}T00:00:00&PublicationDateTo={}T23:59:59&PageSize={}"\
        .format(startDate, endDate, "10")
    # url = "https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&CpvCode=34971000&CpvCode=45000000&OrganizationProvince=PL26&PublicationDateFrom={}T00:00:00&PublicationDateTo={}T23:59:59&PageSize={}"\
    #     .format(startDate, endDate, "10")

    # Additional detail for urllib
    # http.client.HTTPConnection.debuglevel = 1

    conn = sqlite3.connect('Noticedatabase.sqlite')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Notice")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Notice (id INTEGER UNIQUE,noticeType TEXT, noticeNumber TEXT, bzpNumber TEXT, 
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

    count = 0
    for line in js:
        cur.execute('''INSERT INTO Notice (id, noticeType, noticeNumber, bzpNumber, publicationDate,
            orderObject, cpvCode, submittingOffersDate, organizationName, organizationCity, 
            organizationProvince) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (count + 1, js[count]["noticeType"], js[count]["noticeNumber"], js[count]["bzpNumber"],
                     js[count]["publicationDate"], js[count]["orderObject"], js[count]["cpvCode"],
                     js[count]["submittingOffersDate"], js[count]["organizationName"],
                     js[count]["organizationCity"], js[count]["organizationProvince"]))
        count += 1
    conn.commit()

    count = 0
    for line in js:
        print((count + 1), js[count]["orderObject"])
        count += 1

    searchId = input("Podaj który numer przetargu chcesz wyszukać? ")

    cur.execute("""SELECT bzpNumber FROM Notice WHERE
                id={}""".format(searchId))

    for row in cur:
        firstUse.searching_notice_gov(row)
