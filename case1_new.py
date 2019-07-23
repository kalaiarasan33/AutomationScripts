import pandas as pd
from fuzzywuzzy import fuzz

f = open("match.txt","a")
p = open("partial_match.txt","a")
sp = open("semipartial_match.txt","a")


df = pd.read_excel("Construction_Code_Mockathon Data file.xlsx",sheet_name="Train Data" )
df=df.drop_duplicates()
tf = pd.read_excel("Construction_Code_Mockathon Data file.xlsx",sheet_name="Test Data")

cdes=[x for x in df["construction Description"]]
cid=[y for y in df["constructionCode"]]

traindata=dict(zip(cdes,cid))

testdes=[x for x in tf["construction description"]]
tdes = list(dict.fromkeys(testdes))

for key,value in traindata.items():         
    for i in range(0,len(tdes)):           
        try:
                if fuzz.ratio(key, tdes[i]) ==100:
                    f.write("\n  construction Description: {}  ,  constructionCode: {}".format(tdes[i], traindata[key]))
                elif fuzz.ratio(key, tdes[i]) >=70 and fuzz.ratio(key, tdes[i]) <100:
                    p.write("\n  construction Description: {}  ,  constructionCode: {}".format(tdes[i], traindata[key]))
                elif fuzz.ratio(key, tdes[i]) >=50 and fuzz.ratio(key, tdes[i]) <70:
                    sp.write("\n  construction Description: {}  ,  constructionCode: {}".format(tdes[i], traindata[key]))
        except:
                pass
f.close()
p.close()
sp.close()