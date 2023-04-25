import ezamowienia
import ted
# print("2023-01-18".replace("-", ""))

print("Welcome! Type initial data! ")
while True:
    # startDate = input("Insert notice start date of searching in YYYY-MM-DD format. ")
    # endDate = input("Insert notice end date of searching in YYYY-MM-DD format. ")
    startDate = "2023-01-18"
    endDate = "2023-04-19"
    while True:
        web = input("Which website You want to search through? eZamowienia / TED ").lower()
        if web == "ezamowienia":
            ezamowienia.gov_serch(startDate, endDate)
            break
        elif web == "ted":
            replaceStartDate = startDate.replace("-", "")
            ted.ted_search(replaceStartDate)
            break
        else:
            continue
    break
