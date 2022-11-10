
# Your name: Jianxuan Xu
# Your student id: 42940584
# Your email: jianxux@umich.edu
# Who you worked with on this homework: Fredrick Kusumo
from asyncio.proactor_events import _ProactorDuplexPipeTransport
from types import coroutine
from xml.dom.minidom import Identified
from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest


def get_listings_from_search_results(html_file):
    """
    Write a function that creates a BeautifulSoup object on html_file. Parse
    through the object and return a list of tuples containing:
     a string of the title of the listing,
     an int of the cost to rent for one night,
     and a string of the listing id number
    in the format given below. Make sure to turn costs into ints.

    The listing id is found in the url of a listing. For example, for
        https://www.airbnb.com/rooms/1944564
    the listing id is 1944564.
.

    [
        ('Title of Listing 1', 'Cost 1', 'Listing ID 1'),  # format
        ('Loft in Mission District', 210, '1944564'),  # example
    ]
    """
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir,html_file)
    file = open(full_path,'r')
    file_handle = file.read()
    file.close()

    soup = BeautifulSoup(file_handle,'html.parser')
    title = soup.find_all('div',class_="t1jojoys dir dir-ltr")
    name_list = [i.text for i in title]
    price = soup.find_all('span',class_="_tyxjp1")
    price_list_process = [i.text for i in price]
    price_list = []
    for price in price_list_process:
        price_list.append(int(price.strip("$ ")))
    list_num = soup.find_all('a',class_="ln2bl2p dir dir-ltr")
    num_list = []
    for i in list_num:
        link = i.get('href',None)
        regex = r"\/(\d+)\?.+"
        temp = re.findall(regex,link)
        num_list.extend(temp)

    info_list = []
    for i in range(len(title)):
        info_list.append((name_list[i],price_list[i],num_list[i]))
    return (info_list)

    


def get_listing_information(listing_id):
    """
    Write a function to return relevant information in a tuple from an Airbnb listing id.
    NOTE: Use the static files in the html_files folder, do NOT send requests to the actual website.
    Information we're interested in:
        string - Policy number: either a string of the policy number, "Pending", or "Exempt"
            This field can be found in the section about the host.
            Note that this is a text field the lister enters, this could be a policy number, or the word
            "pending" or "exempt" or many others. Look at the raw data, decide how to categorize them into
            the three categories.
        string - Place type: either "Entire Room", "Private Room", or "Shared Room"
            Note that this data field is not explicitly given from this page. Use the
            following to categorize the data into these three fields.
                "Private Room": the listing subtitle has the word "private" in it
                "Shared Room": the listing subtitle has the word "shared" in it
                "Entire Room": the listing subtitle has neither the word "private" nor "shared" in it
        int - Number of bedrooms
.
    (
        policy number,
        place type,
        number of bedrooms
    )
    """
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir,f'html_files/listing_{listing_id}.html')
    file = open(full_path,'r')
    file_handle = file.read()
    file.close()

    soup = BeautifulSoup(file_handle,'html.parser')
    pl1 = soup.find('li',class_="f19phm7j dir dir-ltr")
    poli_num = pl1.find('span',class_="ll4r2nl dir dir-ltr")
    poli_list= []
    for i in poli_num:
        if "pending" in i or 'Pending' in i:
            poli_list.append('Pending')
        elif "exempt" in i or 'not needed' in i:
            poli_list.append('Exempt')
        else:
            poli_list.append(i.text)


    sub_list=[]
    sub_title = soup.find('h2',class_="_14i3z6h")
    for i in sub_title:
        if "private" in i or "Private" in i:
            sub_list.append("Private Room")
        elif "shared" in i or "Shared" in i:
            sub_list.append("Shared Room")
        else:
            sub_list.append("Entire Room")


    room_list=[]
    li_list = soup.find_all('li',class_="l7n4lsf dir dir-ltr")
    temp = li_list[1].find_all('span')
    if "studio" and "Studio" in temp[2].text:
        room_list.append(int(1))
    else:
        room_list.append(int((temp[2].text)[0]))

    for i in range(len(poli_list)):
            info_tup= (poli_list[i],sub_list[i],room_list[i])
    return (info_tup)




def get_detailed_listing_database(html_file):
    """
    Write a function that calls the above two functions in order to return
    the complete listing information using the functions you’ve created.
    This function takes in a variable representing the location of the search results html file.
    The return value should be in this format:


    [
        (Listing Title 1,Cost 1,Listing ID 1,Policy Number 1,Place Type 1,Number of Bedrooms 1),
        (Listing Title 2,Cost 2,Listing ID 2,Policy Number 2,Place Type 2,Number of Bedrooms 2),
        ...
    ]
    """
    value_1 = get_listings_from_search_results(html_file)
    title_list =[]
    price_list =[]
    id_list=[]
    for i in value_1:
        title_list.append(i[0])
        price_list.append(i[1])
        id_list.append(i[2])
    # print("title_list", title_list)
    # print("price_list",price_list)
    # print("id_list",id_list)
    pl_num_list = []
    platp_list = []
    numRoom_list = []
    for id in id_list:
        value_2 = get_listing_information(id)
        pl_num_list.append(value_2[0])
        platp_list.append(value_2[1])
        numRoom_list.append(value_2[2])
    # print("pl_num_list",pl_num_list)
    # print("platp_list",platp_list)
    # print("numRoom_list",numRoom_list)

    info_list = []
    for i in range(len(title_list)):
        info_list.append((title_list[i],price_list[i],id_list[i],pl_num_list[i],platp_list[i],numRoom_list[i]))
    return (info_list)
    

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_detailed_listing_database()), sorts the tuples in
    ascending order by cost, writes the data to a csv file, and saves it
    to the passed filename. The first row of the csv should contain
    "Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms",
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Listing Title,Cost,Listing ID,Policy Number,Place Type,Number of Bedrooms
    title1,cost1,id1,policy_number1,place_type1,num_bedrooms1
    title2,cost2,id2,policy_number2,place_type2,num_bedrooms2
    title3,cost3,id3,policy_number3,place_type3,num_bedrooms3
    ...

    In order of least cost to most cost.

    This function should not return anything.
    """
    first_row = ["Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms"]
    data = sorted(data, key= lambda x:x[1])
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)
        writer.writerows(data)


def check_policy_numbers(data):
    """
    Write a function that takes in a list of tuples called data, (i.e. the one that is returned by
    get_detailed_listing_database()), and parses through the policy number of each, validating the
    policy number matches the policy number format. Ignore any pending or exempt listings.
    Return the listing numbers with respective policy numbers that do not match the correct format.
        Policy numbers are a reference to the business license San Francisco requires to operate a
        short-term rental. These come in two forms, where # is a number from [0-9]:
            20##-00####STR
            STR-000####
    .
    Return value should look like this:
    [
        listing id 1,
        listing id 2,
        ...
    ]

    """
    invalid_list = []

    for i in data:
        policy_number = i[3]

        def policy_number_valid(policy_number):
            regex = r"(?:20\d\d-00\d\d\d\dSTR)|(?:STR-000\d\d\d\d)"
            if "Pending" in policy_number or "Exempt" in policy_number:
                return True
            if re.search(regex,policy_number):
                return True
            else:
                return False
        if not policy_number_valid(policy_number):
            invalid_list.append(i[2])
    return invalid_list

def extra_credit(listing_id):
    """
    There are few exceptions to the requirement of listers obtaining licenses
    before listing their property for short term leases. One specific exception
    is if the lister rents the room for less than 90 days of a year.

    Write a function that takes in a listing id, scrapes the 'reviews' page
    of the listing id for the months and years of each review (you can find two examples
    in the html_files folder), and counts the number of reviews the apartment had each year.
    If for any year, the number of reviews is greater than 90 (assuming very generously that
    every reviewer only stayed for one day), return False, indicating the lister has
    gone over their 90 day limit, else return True, indicating the lister has
    never gone over their limit.
    """
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir,f'html_files/listing_{listing_id}_reviews.html')
    file = open(full_path,'r')
    file_handle = file.read()
    file.close()

    soup = BeautifulSoup(file_handle,'html.parser')
    reviews = soup.find_all('li',class_="_1f1oir5")
    review_list = [i.text for i in reviews]

    dic = {}
    for i in review_list:
        key = i[-4:]
        dic[key] = dic.get(key,0)+1
    dic = sorted(dic.items(),key=lambda x:x[1],reverse=True)
    for i in dic:
        if i[1] > 90:
            return False
        else:
            return True

class TestCases(unittest.TestCase):

    def test_get_listings_from_search_results(self):
        # call get_listings_from_search_results("html_files/mission_district_search_results.html")
        # and save to a local variable
        listings = get_listings_from_search_results("html_files/mission_district_search_results.html")
        # check that the number of listings extracted is correct (20 listings)
        self.assertEqual(len(listings), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)
        # check that each item in the list is a tuple
        for i in range(0,(len(listings))):
            self.assertEqual(type(listings[i]), tuple)
        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)
        self.assertEqual((listings[0][0]), 'Loft in Mission District')
        self.assertEqual((listings[0][1]), 210)
        self.assertEqual((listings[0][2]), '1944564')
        # check that the last title is correct (open the search results html and find it)
        self.assertEqual((listings[-1][0]), 'Guest suite in Mission District')

    def test_get_listing_information(self):
        html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081"]
        # call get_listing_information for i in html_list:
        listing_informations = [get_listing_information(id) for id in html_list]
        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
        # check that the first listing in the html_list has policy number 'STR-0001541'
        #    print('test: ',listing_information)
        self.assertEqual(listing_informations[0][0], 'STR-0001541')
        # check that the last listing in the html_list is a "Private Room"
        self.assertEqual(listing_informations[-1][1], 'Private Room')
        # check that the third listing has one bedroom
        self.assertEqual(listing_informations[2][2], 1)


    def test_get_detailed_listing_database(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save it to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # check that we have the right number of listings (20)
        self.assertEqual(len(detailed_database), 20)
        for item in detailed_database:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6
            self.assertEqual(len(item), 6)
        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1
        self.assertEqual(detailed_database[0], ('Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1))
        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1
        self.assertEqual(detailed_database[-1], ('Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1))
        

    def test_write_csv(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call write csv on the variable you saved
        write_csv(detailed_database, "test.csv")
        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Listing Title', 'Cost', 'Listing ID', 'Policy Number', 'Place Type', 'Number of Bedrooms'])
        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1
        self.assertEqual(csv_lines[1], ['Private room in Mission District', '82', '51027324', 'Pending', 'Private Room', '1'])
        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2
        self.assertEqual(csv_lines[-1], ['Apartment in Mission District', '399', '28668414', 'Pending', 'Entire Room', '2'])       

    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that there is exactly one element in the string
        self.assertEqual(len(invalid_listings), 1)
        # check that the element in the list is a string
        self.assertEqual(type(invalid_listings[0]), str)
        # check that the first element in the list is '16204265'
        self.assertEqual(invalid_listings[0], '16204265')
    
    def test_extra_credit(self):
        self.assertEqual(extra_credit(1944564),True) 
        self.assertEqual(extra_credit(16204265),False)


if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)
    

#a.
# I think we could adopt a new system where new users are asked to enter their business license's number when they upload their home on airbnb. Once the license number has been received by the user, airbnb can first quickly check whether the license number conforms to the basic formatting specifications via regex; once this step is passed, it should take some time to go to the San Francisco Planning Office to check the number. Airbnb will only list the home after the license has been found and verified. However, the difficulty that this new system may cause is that, from the airbnb side, the new system not only extends the waiting time for users, but also adds additional workload to the system. And if you need to get the data of SFPO reasonably and legally also need to put effort. And for SFPO, they may need to share their database to airbnb. this may be met with data confidentiality agreement issues.

#b.
# I think we can use airbnb's data to study whether Americans have enough housing, because houses are marked on airbnb whether they are whole houses or individual rooms. We can roughly assume that detached room homeowners only have mobile homes, while whole house homeowners have at least 2 or more residences. From there, we can make a rough judgment with this information.

#c.
# It is undeniable that when a programmer is trying to crawl information from a website, it can cause a sudden increase in the amount of computation on the website's server. Occupying a lot of CPU utilization, CPU utilization reaches 100%, the user access to the site is: access speed is very slow, often can not brush out. In serious cases, it will lead to the website crash. If the website is a website selling items, this may cause the website to be unable to sell items as originally planned. Resulting in financial loss. So I think we should think about whether our actions will affect the normal operation of the website when we are scraping the website information.

#d.
# When scraping public data, we should think about the following guide lines in order to protect the privacy of users' information.
# Is this data allowed to be scraped by the data collector (contributor)?
# Are we allowed to use this data for our profit or non-profit purposes?
# Is there a risk of violating anyone's privacy issues if the data is used?


