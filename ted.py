import urllib.request, urllib.error
import sqlite3
import json
import firstUse
import ssl

#
# startDate = input("Podaj date początkową wyszukiwanych ogłoszeń w formacie YYYY-MM-DD. ")
# endDate = input("Podaj date końcową wyszukiwanych ogłoszeń w formacie YYYY-MM-DD. ")


def ted_search(startDate):
    url = "https://ted.europa.eu/api/v3.0/notices/search?pageNum=1&pageSize=100&q=CY%20%3D%20%5BPOL%5D%20AND%20RC%20%3D%20%5BPL72%5D%20AND%20PD%20%3D%20%5B{}%5D%20AND%20TI%20%3D%20%5BPOLAND%5D&scope=3"\
        .format(startDate)
    # Additional detail for urllib
    # http.client.HTTPConnection.debuglevel = 1

    conn = sqlite3.connect('teddatabase.sqlite')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Notice")
    cur.execute('''CREATE TABLE IF NOT EXISTS Notice (id INTEGER UNIQUE, noticeNumber TEXT, publicationDate TEXT, 
                submittingOffersDate TEXT)''')

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
    while count < len(js["results"]):
        # cpvCodes was removed for problem to resolve data
        cur.execute('''INSERT INTO Notice (id, noticeNumber, publicationDate, submittingOffersDate) VALUES ( ?, ?, ?, ?)''',
                    (count + 1, js["results"][count]["ND"], js["results"][count]["PD"], js["results"][count]["DT"][0]))
        count += 1
    conn.commit()
    #
    # count = 0
    # for line in js:
    #     print((count + 1), js[count]["orderObject"])
    #     count += 1
    #
    # searchId = input("Podaj który numer przetargu chcesz wyszukać? ")
    #
    # cur.execute("""SELECT bzpNumber FROM Notice WHERE
    #             id={}""".format(searchId))

    # firstUse.searching_notice_ted("234996-2023")
    # for row in cur:
    #     firstUse.searching_date(row)
