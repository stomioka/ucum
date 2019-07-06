'''utilities for ucum APIs
Sam Tomioka
May 2019

Updates
* May 25, 2019 convert_unit() is updated to accept mw from LOINC
'''

import re
import os
import pandas as pd
import numpy as np
from tqdm import tqdm, tnrange, tqdm_notebook
import urllib
import xml.etree.ElementTree as ET

# visualizations
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file


import random
def Color(n):
    c_=[]
    for i in range(n):
        r = lambda: random.randint(0,255)
        c='#%02X%02X%02X' % (r(),r(),r())
        c_.append(c)
    return c_

def bar_hm(df,title):
    sns.set(style="white")
    ct = pd.crosstab(df['LBORRESU'], df['LBSTRESU'])
    g=ct.plot.bar(stacked=True)
    plt.legend(title='LBSTRESU',loc=5, bbox_to_anchor=(1.4, .5))
    plt.title(title)
      
    fig2, ax = plt.subplots(figsize=(13, 25))
    fig2.subplots_adjust(top=.965)
    plt.suptitle(title, fontsize=10, fontweight='bold')

    cbar_kws = {'orientation':"horizontal", 'pad':0.08, 'aspect':80}
    return plt, sns.heatmap(ct, annot=True, fmt='d', linewidths=.2, ax=ax, cmap='RdPu', cbar_kws=cbar_kws)



def cleanlist(lst, regex, substitution):
    cleaned_list = [re.sub(regex, substitution, str(line)) for line in lst]
    return cleaned_list

def orresu2ucum(df_,patterns):
    
    
    original=pd.unique(df_[['LBORRESU','LBSTRESU']].values.ravel('K'))
    original=original.tolist()
    ucum=original
# convert to UCUM units
    df=df_.copy()
    for x, sub in patterns:
        ucum=cleanlist(ucum, x, sub)
    patterns2 = [("\^",''),('\Amc','u')]
    for x, sub in patterns2:
        ucum=cleanlist(ucum, x, sub)    
    b = dict(zip(original, ucum))
    df['LBORRESU']=df['LBORRESU'].map(b)
    df['LBSTRESU']=df['LBSTRESU'].map(b)
    
    df=df[df['LBORRESU']!='']
    df=df[df['LBSTRESU']!='']
    


    return df,ucum

def ucumVerify(ucumlist,url):
    '''Verify UCUM units using isValidUCUM'''
    
    url=url+'/isValidUCUM/'
    ucum = filter(None, ucumlist)
    l__=[]
    for i in ucum:
        resp_=urllib.request.urlopen(url+i).read().decode("utf-8")
        l__.append(i+' = '+resp_)
    l__
    return l__

def convert_unit(dfin, url, patterns, loinconly=0):
    '''
    df: input dataframe
    url: RestAPI url
           prod version use -> https://ucum.nlm.nih.gov/ucum-service/v1/ucumtransform/
           test version use -> http://xml4pharmaserver.com:8080/UCUMService2/rest/ucumtransform/
    patterns: regular expressions used to convert input units to UCUM unit representation
    loinconly: 0 if api call should be made for any records, 1 if api call for records with loinc.
    '''
    url=url+'/ucumtransform/'
    df_=dfin.copy()
   #incl=1 for LOINC based api call
    df_['incl'] = df_['LBLOINC'].apply(lambda x: 1 if x!='' else 0 )
    df2=df_.copy() 
    
    # convert to UCUM units
    df3,_=orresu2ucum(df2,patterns)
    
    #  add lbtestcd to tests with % as an unit
    mask = df3['LBORRESU'] =='%'
    df3.loc[mask, 'LBORRESU'] = '%{'+df3['LBTESTCD']+'}'
    mask = df3['LBSTRESU'] =='%'
    df3.loc[mask, 'LBSTRESU'] = '%{'+df3['LBTESTCD']+'}'

    # build url list
    if loinconly==0:
        df3['checklist']=df3.apply(lambda x: url+str(x['LBORRES'])+
                                 "/from/"+str(x['LBORRESU'])+
                                 "/to/"+str(x['LBSTRESU'])+"/LOINC/"+
                                 str(x['LBLOINC']) if x['incl']==1 else url+
                                 str(x['LBORRES'])+
                                 "/from/"+str(x['LBORRESU'])+
                                 "/to/"+str(x['LBSTRESU']), axis=1)
    if loinconly==1:   
        df3=df3[df3['incl']==1]
        df3['checklist']=df3.apply(lambda x: url+str(x['LBORRES'])+
                                 "/from/"+str(x['LBORRESU'])+
                                 "/to/"+str(x['LBSTRESU'])+"/LOINC/"+
                                 str(x['LBLOINC']), axis=1)
    
    df3['checklist'].to_csv('out_2.csv', index=False, header=False)
    checklist=df3['checklist'].tolist()

    # make API call
    response=[]
    for i in tnrange(0,len(checklist), desc='Verification'):
        #print(checklist[i], i)
        try:
            with urllib.request.urlopen(checklist[i]) as res:
                context=ET.fromstring(res.read())

                for child in context:
                    tmp1=[]
                    if child.text==None:
                        for element in child:
                            
                            tmp1.append(element.text)
                            #print(child, tmp1)
                    elif child.text!=None: #error handling ERROR: unexpected result: Invalid UCUM Transformation Expression 
                        #print(child.text)
                        tmp1=[child.text]
                response.append(tmp1)
        except urllib.error.HTTPError as e: # error handling bad request
            tmp1=[e+i,np.nan,np.nan,np.nan]
            response.append(tmp1)
    #updated to get LOINC results
    fromucmc=[]
    for x in range(len(response)):
        #print(response[x])
        if len(response[x])==1:
            tmp2=np.nan
            fromucmc.append(tmp2)
        elif len(response[x])==4:
            tmp2=float(response[x][3])
            fromucmc.append(tmp2)
        elif len(response[x])==5:
            #print(response[x])
            tmp2=float(response[x][4])
            fromucmc.append(tmp2)
            
    rawdata=df3['LBSTRESN'].tolist()
    df3['fromucum']=fromucmc
    df3=df3.drop(columns=['incl'])
    df3.reset_index(drop=True, inplace=True)
    #updated to get LOINC results
    response_=[]
    for x in range(len(response)):
        if len(response[x])==1:
            tmp2=response[x][0]
            response_.append(tmp2)
        elif len(response[x])==4:
            tmp2=np.nan
            response_.append(tmp2)
        elif len(response[x])==5:
            tmp2=np.nan
            response_.append(tmp2)
    
    df3['response']=response_
            
    check=[i!=j for i, j in zip(fromucmc, rawdata)]
    return df3[check],df3,response

def sumstat(test, findings, originaldf, findingspiv):
    check=originaldf[originaldf['LBTESTCD']==test]
    print(test+': Summary stats of LBSTRESN')
    print()
    print(check[['LBSTRESN','LBSTRESU']].groupby(['LBSTRESU']).describe())
    check=findings[findings['LBTESTCD']==test]
    print('--------------------------------------------------------------')
    print(test+': Summary stats of UCUM Conversion')
    print()
    print(check[['fromucum','LBSTRESU']].groupby(['LBSTRESU']).describe())
    print('--------------------------------------------------------------')
    print(test+': Summary stats of Differences between LBSTRESN and UCUM Conversion')
    print()
    print(findingspiv[test].describe())
    return check