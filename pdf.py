import fitz


def get_customers(document, first_page, last_page):
    document = fitz.open(document)


    num_pages = document.pageCount
    print(num_pages)
    if first_page == None:
        first_page = 1
    count = first_page - 1
    text = ""
    endpage = num_pages
    if last_page != None:
        endpage = last_page

    while count < endpage:
        text += document.loadPage(count).getText("text")
        count += 1


    arr = text.split()

    i = 0
    customers = []
    
    while i < len(arr):
        if arr[i] == "Applied.":
            j = 2
            singleCustomer = []
            while  arr[i-j] != "Applied." and arr[i-j] != "ResponseCode" and arr[i-j] != "ncgvrserver:8081/Dashboard/CollectDueToday" and arr[i-j] != "on":
                singleCustomer.insert(0, arr[i-j])
                j = j + 1            
            if arr[i-j] == "ResponseCode" or arr[i-j] == "ncgvrserver:8081/Dashboard/CollectDueToday" or arr[i-j] == "on":
                singleCustomer.pop(0)
            customers.append(singleCustomer)    
        i += 1

    # print(len(customers))
    # print(customers)
    print(customers[0])
    return customers