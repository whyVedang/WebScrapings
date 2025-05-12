from bs4 import BeautifulSoup
import requests
import pandas as pd

# Scrape eBay listings
searchkey=input("Enter the search query: ")
url=f"https://www.ebay.com/sch/i.html?_nkw=${searchkey}&_sacat=0&_from=R40&rt=nc&LH_PrefLoc=98"
res=requests.get(url).text
soup=BeautifulSoup(res,"html.parser")
# print(soup.prettify())
result=[]
listings=soup.find_all("div",class_="s-item__info clearfix")
for listing in listings[2:40]:
    title=listing.find("span",role="heading").text
    price=listing.find("div",class_="s-item__detail s-item__detail--primary").text
    link=listing.find("a",class_="s-item__link")["href"]
    # print(link)
    # print(title)
    # print(price)
    result.append([title, price, link])
df=pd.DataFrame(result,columns=["Title","Price","Link"])
print(df)
df.to_csv(f"ebay_{searchkey}.csv",sep='\t',index=False)