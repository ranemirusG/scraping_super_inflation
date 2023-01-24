import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import readline


DIR = "history_AGO22-JAN23"

joined_files = os.path.join( DIR , "*")
joined_list = glob.glob(joined_files)
df = pd.concat(map(lambda a : pd.read_csv(a, thousands="."), joined_list), ignore_index=True)
df.dropna(inplace = True)
df.date= pd.to_datetime(df.date, format="%Y-%m-%d")
df = df.set_index('date').sort_values(["date","item"])
PRODUCTS = pd.unique(df.item)
RETAILERS = pd.unique(df.retailer)

def complete(text, state):
    for i in PRODUCTS:
        if re.findall(text,i, flags=re.IGNORECASE):
            if not state:
                return i
            else:
                state -= 1


readline.parse_and_bind("tab: menu-complete") #TODO use arrows
readline.set_completer(complete)

def search():
    x = input('Search for: ')
    if x in PRODUCTS:
        return x
    else:
        print("Invalid product. Try again.")
        return search()


choose = search() #choose = "QUAKER HONEY GRAHAM 190GR"

"""TODO elegir all time o filtrar por fecha
# algo asi: input("Select filter? (y/n)")
# date_from =
# date_to =
# df.query("('2022-09-05' < date) & ('2022-09-15' > date)")
"""


def func(retailer):

    query = df.query("item == @choose & retailer == @retailer") # .copy()
    query.is_copy = False
    query["ch_col"] = ""

    for i in range(len(query)):
        if query.price.iloc[i] != query.price.iloc[(i-1)]:
            query.ch_col.iloc[i] = "change"

    #return query
    x = query.index
    y = query.price
    # query_ch = query.query("ch_col == ('change')")
    # change_label = list(query_ch.index.strftime("%Y-%m-%d"))
    # plt.xticks(ticks=query_ch.index, label=change_label)
    plt.plot(x,y, label=retailer)


for i in RETAILERS:
    func(i)

""" PLOT """
plt.grid(axis = 'y')
plt.title(choose, loc= "left")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend() #muestra a que retailer corresponde cada linea
plt.show()
plt.close()


#TODO porcentaje de aumento
## como comentario en el grafico???

#TODO segunda linea de xticks con la cantidad de dias transcurridos entre cada AUMENTO
