import requests
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

f = open("case2.txt","a")


df = pd.read_excel('Company_Address_Mockathon.xlsx')

compname=[x for x in df['Company']]
zipc=[x for x in df['Zipcode']]


l = [',','.',',','.']
cname = []
for x in compname:
    for i in l : 
        c = x.replace(i, '')
    cname.append(c)

print(cname)






api_key = 'AIzaSyCT1E68r6gr6YhcTAEoz9ID-RauCI09WFM'
  
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"


def location(k,v):  
    #for k,v in cz.items():
        query = "{},{}".format(k,v)  
        r = requests.get(url + 'query=' + query +'&key=' + api_key) 
        ss=json.dumps(json.loads(r.content))
        for ad in json.loads(ss)['results']:
             print("{} , {} ".format(k,ad['formatted_address']))            
        return
             

def main(cz):
        executor =  ThreadPoolExecutor(max_workers=5)
        futures = [executor.submit(location, k,v) for k,v in cz.items()]
        for future in as_completed(futures):
            f.write(future.result())   


if __name__=="__main__":
    cz=dict(zip(cname,zipc))
    main(cz)
    f.close()
