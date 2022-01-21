from bs4 import BeautifulSoup
import requests
import random


def formatter(content:str) -> str:
    """The purpose of this function is to properly reformat URLs pulled from the target site(DiscUdemy)."""

    if content.count("/") == 4:
        try:
            base = [x for x in content.split("https://www.discudemy.com/") if x != ""][0]
        except:
            base=""
        ek = ""
        if "/" in base:
            ek = base.split("/")[1:][0]
        d = "https://www.discudemy.com/"+"go/"+ek

        return d
    elif content.count("/") == 3:
        try:
            base = [x for x in content.split("https://www.discudemy.com/") if x != ""][0]
        except:
            base=""
        return "https://www.discudemy.com/"+"go/"+base

def bs4_r(curl:str) -> list:
    """Link scraping for formatted links founded in DiscUdemy courses page."""
    hs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    req = requests.get(curl, headers=hs)
    bsoup = BeautifulSoup(req.content, "lxml")

    links = [a['href'] for a in bsoup.select('a[href]') if "discudemy" in a["href"]]

    return links

def parse_four_page(page_id:int) -> list[str]:
    soup_object = bs4_r(f"https://www.discudemy.com/all/{page_id}")

    queries = [formatter(query) for query in soup_object]

    def find_url(curl):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
            r = requests.get(curl, headers=headers)

            soup = BeautifulSoup(r.content, "lxml")

            a = soup.find_all("a", attrs={"target":"_blank"})

            return [a[x]["href"] for x in range(len(a)) if a[x]["href"].startswith("https://www.udemy.com")][0]
        except:
            pass
    if queries:
        courses=[]
        for q in queries:
            if find_url(q) != None:
                if "couponCode" in find_url(q):
                    courses.append(find_url(q))
    return courses

def data_export(courses:list, path="courses/", file="courses.txt") -> dict[str, int]:
    """Export all courses with using data_export(courses, path=path, file=file). Please do configure path directory as that -> 'your_directory/target/' and if you want you could to add specific file name."""
    if type(courses) == list and len(courses) > 0:
        fpath = f"{path}{random.randint(12345678, 87654321)}-{file}"
        with open(fpath, "a") as file:
            for x in courses:
                file.write(f"{x}\n")
        return {"file":fpath, "total-courses":len(courses), "status":True}
      
      
"""
Usage of Class:

Udemy = UdemyParser() # Create an object from the class base
Udemy.method(*params) # How can I access to the class methods?
\n
Udemy.parse_four_page(page_id) # If you want to get all last added courses, use that method.\nPage ID must be one to five, five is maximum. Why not greater? Because free courses often not available after page five.
\n
Udemy.data_export(courses, path=path, file=file) # Export all courses with using data_export(courses, path=path, file=file).\nPlease do configure path directory as that -> 'your_directory/target/' and if you want you could to add specific file name.
\nTry looping to fetch all courses, so you'll get it like this:\n
```
datas = []
for x in range(1, 3):
    for i in udemy.parse_four_page(x):
        datas.append(i)\n```
"""
