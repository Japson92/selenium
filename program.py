import sqlite3
import ted
import firstUse


print("Welcome! Type initial data! ")
while True:
    # startDate = input("Insert notice start date of searching in YYYY-MM-DD format. ")
    # endDate = input("Insert notice end date of searching in YYYY-MM-DD format. ")
    startDate = "2023-04-18"
    endDate = "2023-04-27"
    while True:
        web = input("Which website You want to search through? eZamowienia / TED ").lower()
        if web == "ezamowienia":
            ted.gov_search(startDate, endDate)
            conn = sqlite3.connect('Noticedatabase.sqlite')
            cur = conn.cursor()
            cur.execute("""SELECT id, orderObject FROM Notice""")
            for line in cur:
                print(line[0], line[1])

            searchId = input("Select number of notice You want to search? ")

            cur.execute("""SELECT bzpNumber FROM Notice WHERE
                        id={}""".format(searchId))

            for row in cur:
                firstUse.searching_notice_gov(row)
            break

        elif web == "ted":
            replaceStartDate = startDate.replace("-", "")
            ted.ted_search(replaceStartDate)

            conn = sqlite3.connect('teddatabase.sqlite')
            cur = conn.cursor()
            cur.execute("""SELECT id, noticeNumber FROM Notice""")
            for line in cur:
                print(line[0], line[1])

            searchId = input("Select number of notice You want to search? ")

            cur.execute("""SELECT noticeNumber FROM Notice WHERE
                            id={}""".format(searchId))

            for row in cur:
                firstUse.searching_notice_ted(row)

            break
        else:
            print("Please type correctly name of website.")
            continue
    break
