'''
python3, only runnable on joinquant.com due to the data API
'''

import pandas as pd
import datetime as dt
import os
import numpy as np
import jqdata
import bisect
import matplotlib.pyplot as plt
from pyecharts import Page,online,Line,Grid
import warnings
warnings.filterwarnings('ignore')

online()

origin = '2005-01-01'
today = dt.datetime.strftime(pd.datetime.today()-dt.timedelta(1),'%Y-%m-%d')

def convert_code(code):
    if code.endswith('XSHG'):
        return 'sh' + code[0:6]
    elif code.endswith('XSHE'):
        return 'sz' + code[0:6] 

def get_ff(index_code,date=today):
    stock_list = get_index_stocks(index_code, date)
    if len(stock_list)>0:
        q = query(valuation).filter(valuation.code.in_(list(stock_list)))
        df = get_fundamentals(q, date)
    else:
        df = pd.DataFrame()
    return df

def get_ff_w(index_code,date=today,weight='C'):
    result = get_ff(index_code,date)
    if result.empty:
        return result
    result=result.loc[:,['code','pe_ratio','pb_ratio','market_cap']]
    num = len(result.iloc[:,0])
    if weight == 'E': #equal weight
        return result.assign(weight=pd.Series([1/float(num) for _ in range(num)]))
    elif weight == 'C': #based on capital
        total = sum([result.iloc[i].market_cap for i in range(num)])
        wei = [result.iloc[i].market_cap for i in range(num)]/total
        return result.assign(weight=pd.Series(wei))
    else:
        wei = weight(result)
        return result.assign(weight=pd.Series(wei))


def get_pepb(index_code,date=today,weight='C'):
    result = get_ff_w(index_code,date,weight)
    if result.empty:
        return [0,0]
    num = len(result.iloc[:,0])
    if num>0:
        pede = np.array([result.iloc[i,4]/result.iloc[i,1] for i in range(num)])
        pbde = np.array([result.iloc[i,4]/result.iloc[i,2] for i in range(num)])
        pede =pede[pede<100]
        pbde =pbde[pbde<100]
        return [1/sum(pede),1/sum(pbde)]
    else:
        return [0,0]
    
    
def get_pepb_range(index_code,start=origin,end=today,weight='C'):
    pebs = pd.DataFrame()
    for date in pd.DatetimeIndex(jqdata.get_trade_days(start_date=start,end_date=end)):
        s = get_pepb(index_code, dt.datetime.strftime(date,'%Y-%m-%d'), weight)
        if s != [0,0]:
            pebs[dt.datetime.strftime(date,'%Y-%m-%d')]=pd.Series(s,index=['pe','pb'])
    return pebs.dropna()




class index:
    
    def __init__(self,code,start=origin,end=today,weight='C'):
        self.code, self.start, self.end, self.weight = code, dt.datetime.strptime(start,'%Y-%m-%d'), dt.datetime.strptime(end,'%Y-%m-%d'), weight
        self.datapath = '%s%spepb.csv'%(convert_code(self.code),self.weight)
        if (self.start-dt.datetime.strptime(origin,'%Y-%m-%d')).total_seconds()<0 or (self.end-self.start).total_seconds()<0 or (self.end-pd.datetime.today()+dt.timedelta(1)).total_seconds()>0:
            raise Exception('date range error')
    
    def __repr__(self):
        return self.code
    __str__ = __repr__

    def update_pepbs(self):
        if os.path.exists(self.datapath):
            cps = pd.DataFrame.from_csv(self.datapath)
            start_date = dt.datetime.strptime(cps.iloc[:,-1].name,'%Y-%m-%d') + dt.timedelta(1)
            origin_date = dt.datetime.strptime(cps.iloc[:,0].name,'%Y-%m-%d')
            omit = (self.end-start_date).days
            omitb = (origin_date-self.start).days
            if omit>=-1:
                self.pepbs = pd.concat([cps, get_pepb_range(self.code,start_date,self.end,self.weight)],axis=1) 
                self.pepbs.to_csv(self.datapath)
            else:
                self.pepbs = cps.loc[:,:dt.datetime.strftime(self.end,'%Y-%m-%d')]
            if omitb>=0:
                self.start = origin_date
            else:
                self.pepbs = self.pepbs.loc[:,dt.datetime.strftime(self.start,'%Y-%m-%d'):]
        else:
            self.pepbs = get_pepb_range(self.code,self.start,self.end,self.weight)
            if self.start-dt.datetime.strptime(origin,'%Y-%m-%d') == dt.timedelta(0):
                self.pepbs.to_csv(self.datapath)
            self.start = self.pepbs.iloc[:,0].name
    
    def img_line(self):
        all_index = get_all_securities(['index'])
        name = all_index.ix[self.code].display_name
        line = Line(name,"PB chart")
        ref=[self.pepbs.iloc[1].quantile(i/10.0) for i in range(11)]
        for i in range(11):
            line.add('ref',list(self.pepbs.iloc[0].index),[ref[i] for _ in self.pepbs.iloc[1].index],is_symbol_show=False,line_opacity=0,mark_line=['average'],mark_line_symbolsize=0)
        line.add('pb',list(self.pepbs.iloc[0].index),list(self.pepbs.iloc[1].values),is_symbol_show=True,is_smooth=True,is_more_utils=True)
#         page.add(line)
        line2 = Line(name,"PE chart")
        ref=[self.pepbs.iloc[0].quantile(i/10.0) for i in range(11)]
        for i in range(11):
            line2.add('ref',list(self.pepbs.iloc[0].index),[ref[i] for _ in self.pepbs.iloc[0].index],is_symbol_show=False,line_opacity=0,mark_line=['average'],mark_line_symbolsize=0)
        line2.add('pe',list(self.pepbs.iloc[0].index),list(self.pepbs.iloc[0].values),is_symbol_show=True,is_smooth=True,is_more_utils=True)
        line2
#         page.add(line2)
        return [line,line2]
    def img_page(self):
        page=Page()
        line = self.img_line()
        page.add(line[0])
        page.add(line[1])
        return page

def pos(pepbs,pe,pb):
    idx = bisect.bisect(sort(list(pepbs.loc['pe'])),pe)
    idy = bisect.bisect(sort(list(pepbs.loc['pb'])),pb)
    return [idx/float(len(pepbs.iloc[0])),idy/float(len(pepbs.iloc[0]))]
def pos_hist(pepbs,date):
    pepbs=pepbs.loc[:,:date]
    pe=pepbs.loc['pe',date]
    pb=pepbs.loc['pb',date]
    return pos(pepbs,pe,pb)
def hist_line(pepbs,start=origin):
    h = pd.DataFrame()
    for date in pd.DatetimeIndex(jqdata.get_trade_days(start_date=start)):
        h[date]=pd.Series(pos_hist(pepbs,dt.datetime.strftime(date,'%Y-%m-%d')),index=['pe','pb'])
    return h.transpose()

'''
# visualization on any index you are interested: its pe, pb history line
page=Page()
for code in ['000016.XSHG','000300.XSHG','000905.XSHG','399006.XSHE','399971.XSHE','399975.XSHE','000932.XSHG'
             ,'000925.XSHG','000992.XSHG','000852.XSHG','000931.XSHG','399967.XSHE','000935.XSHG']:
    demo=index(code)
    demo.update_pepbs()
    a=demo.img_line()
    page.add(a[0])
    page.add(a[1])
for code in ['000922.XSHG','000831.XSHG','000827.XSHG','000978.XSHG','399812.XSHE']:
    demo=index(code,weight='E')
    demo.update_pepbs()
    a=demo.img_line()
    page.add(a[0])
    page.add(a[1])
page.render('graph.html')
# page

'''

'''

def score(code, weight='C', peweight=0.6):
    demo=index(code, weight=weight)
    demo.update_pepbs()
    peb=demo.pepbs
    hp=pos(peb,peb.iloc[0,-1],peb.iloc[1,-1])
    return hp[0]*peweight+hp[1]*(1-peweight)
def tomoney(score, base=50, lower=0):
    money = 0
    if score>=0.35:
        money = 0
    elif score<0.35 and score>=0.27:
        money = 1 - lower
    elif score<0.27 and score>=0.2:
        money = 2 -lower
    elif score<0.2 and score>=0.12:
        money = 3 -lower
    elif score<0.12 and score>=0.07:
        money = 4 -lower
    elif score<=0.07 and score>=0.03:
        money = 5 - lower*1.2
    elif score<0.03 and score>=0.01:
        money = 6 - lower*1.4
    elif score<0.01:
        money = 7 -lower*1.6
    if money<0:
        money = 0
    money*=base
    return money

# print the input value the system recommend based on the pe, pb history
# examples:
# print('上证50：%s'%tomoney(score('000016.XSHG', weight='C'), base = 50, lower = 0.5))
# print('证券公司：%s'%tomoney(score('399975.XSHE', peweight=0, weight='C'), base = 40, lower = 2))
'''