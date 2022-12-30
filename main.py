# Imports
import os
import csv
import pandas as pd
from datetime import timedelta
from datetime import datetime
from tabulate import tabulate
from datetime import date
import typer
from rich.console import Console


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


app = typer.Typer()
console = Console()

# pathnames to respective (csv-)files
fldr = 'superpy'
current = os.getcwd()
file_b = os.path.join(current, fldr, 'bght.csv')
file_s = os.path.join(current, fldr, 'sld.csv')
file_i = os.path.join(current, fldr, 'invntry.csv')
file_t = os.path.join(current, fldr, 'set_dt.txt')


# creating the csv-files
def create_csv():
    if not os.path.exists(file_b):
        with open(file_b, 'w+') as bought:
            headers = ['ID', 'Product Name', 'Buy Date', 'Buy Price', 'Expiration Date', 'Transaction ID']
            writer = csv.DictWriter(bought, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
    if not os.path.exists(file_s):
        with open(file_s, 'w+') as sold:
            headers = ['Sell Date', 'Sell Price', 'Expiration Date']
            writer = csv.DictWriter(sold, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
    if not os.path.exists(file_i):
        with open(file_i, 'w+') as inv:
            headers = ['ID', 'Product Name', 'Buy Date', 'Buy Price', 'Expiration Date', 'Transaction ID']
            writer = csv.DictWriter(inv, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
    return


@app.command()
def main():
    action()
    reset()
    return


def reset():
    app()


def action():
    create_csv()
    action = console.input("""\n[b blue]Choose your action. Type [b u]'help'[/b u] (or 'h') for all options or [b u]'exit'[/b u] (or 'x') to quit:\n\n[/b blue]""").lower()
    if action == 'help' or action == 'h':
        console.print("""\n[u b]Choose one of the following actions:[/u b]\n
        [b green]products[/b green] = shows all the avaiable products [b green](p)[/b green]
        [b green]buy[/b green] = adds a product to your inventory [b green](b)[/b green]
        [b green]sell[/b green] = lets you sell an item (if it's in stock) [b green](s)[/b green]
        [b green]stock[/b green] = shows the amount in stock of the desired product [b green](st)[/b green]
        [b green]full stock[/b green] = shows all products in stock [b green](all)[/b green]
        [b green]check[/b green] = checks for potential expired dates (and auto-removes those expired) [b green](c)[/b green]
        [b green]custom date[/b green] = create a specific date in time (+ or - a specific number of days) [b green](cd)[/b green]
        [b green]reset[/b green] = resets the date to the present time [b green](r)[/b green]
        [b green]today[/b green] = shows the given date (reset or not) [b green](d)[/b green]
        [b green]profit[/b green] = shows today's profit (or loss) [b green](w)[/b green]
        [b green]profit yesterday[/b green] = shows yesterdays profit (or loss) [b green](py)[/b green]
        [b red]exit[/b red] = quit the hell outta here! [b red](x)[/b red]""")
    if action == 'products' or action == 'p':
        console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
    if action == 'buy' or action == 'b':
        buy_product()
    if action == 'sell' or action == 's':
        sell_product()
    if action == 'stock' or action == 'st':
        console.print(report_item())
    if action == 'full stock' or action == 'all':
        console.print(products_in_stock())
    if action == 'check' or action == 'c':
        check_inventory()
    if action == 'custom date' or action == 'cd':
        custom_date()
    if action == 'reset' or action == 'r':
        reset_to_today()
    if action == 'today' or action == 'd':
        console.print("\n[b green]Today it is: [/b green]", today().strftime("%Y-%m-%d"))
    if action == 'profit' or action == 'w':
        profit()
    if action == 'profit yesterday' or action == 'py':
        profit_yesterday()
    if action == 'exit' or action == 'x':
        quit()
    reset()


def reset_to_today():
    today = str(date.today())
    with open(file_t, 'w+') as f:
        f.write(today)
        return f


def today():
    with open(file_t, 'r') as f:
        return datetime.strptime(f.readlines()[0], "%Y-%m-%d")


def yesterday():
    return today() - timedelta(1)


def custom_date():
    td = int(console.input("\n[b green]Enter the amount of days you want to go [u]back[/u] or [u]forward[/u] ('0' to ignore):[/b green] "))
    if td == 0:
        action()
    delta = today() + timedelta(td)
    with open(file_t, 'w+') as f:
        f.write(delta.strftime("%Y-%m-%d"))
    return


def check_inventory():
    df = pd.read_csv(file_i)
    df.drop(df[df['Expiration Date'] < today().strftime("%Y-%m-%d")].index, inplace = True)    # drop row containing this value
    df.to_csv(file_i, index=None)
    df.to_csv(file_b, index=None)
    return


def show_products():
    pr = ({
    'ID' : ['ap020035', 'ba025045', 'ki030060', 'pe020035', 'br045070', 'le040060', 'sp060090', 'bu070110', 
    'eg075120', 'mi075125', 'co080145', 'fa080140', 'si080140'],
    'Product Name' : ['Apple', 'Banana', 'Kiwi', 'Pear', 'Broccoli', 'Lettuce', 'Sprouts',
    'Butter', 'Eggs', 'Milk', 'Cola', 'Fanta', 'Sisi'],
    'Buy Price'  : [0.2, 0.25, 0.30, 0.2, 0.45, 0.4, 0.6, 0.7, 0.75, 0.75, 0.8, 0.8, 0.8],
    'Price' : [0.35, 0.45, 0.60, 0.35, 0.70, 0.6, 0.9, 1.1, 1.2, 1.25, 1.45, 1.4, 1.4]
})
    products = pd.DataFrame.from_dict(pr)
    return products


def buy_product():
    bought_id = datetime.now().strftime("%Y%m%d%H%M%S") # adds a unique ID to a transaction (using strftime)
    df = (show_products())
    my_list = [x for x in df['Product Name'].str[:].str.lower()]
    console.print("\n[b]What product would you like to add to your inventory? Please enter it's [u]name[/u].[/b]\n[b]To see available products, type [u]'check'[/u] or [u]'exit'[/u] to return:[/b]\n")
    name = input("").lower()
    if name == 'check':
        console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
    if name == 'exit':
        action()
    while name not in my_list:
        name = console.input("\n[b yellow]Enter a product's name:[/b yellow] ").lower()
        if name == 'check':
            console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
        if name == 'exit':
            action()
            
    if name in ['pear', 'kiwi', 'banana', 'apple']:
        exp_dt_f = today() + timedelta(14)                       
        exp_d = exp_dt_f.strftime("%Y-%m-%d")                   # Exp_d fruits
    if name in ['broccoli', 'lettuce', 'sprouts']:
        exp_dt_v = today() + timedelta(5)               
        exp_d = exp_dt_v.strftime("%Y-%m-%d")                   # Exp_d veggies
    if name in ['butter', 'eggs', 'milk']:
        exp_dt_d = today() + timedelta(7)           
        exp_d = exp_dt_d.strftime("%Y-%m-%d")                   # Exp_d dairy
    if name in ['cola', 'fanta', 'sisi']:
        exp_dt_s = today() + timedelta(200)           
        exp_d = exp_dt_s.strftime("%Y-%m-%d")                   # Exp_d soda
    
    index = df[df['Product Name'].str.lower() == name].index
    price = df.loc[index, 'Buy Price']
    id = df.loc[index, 'ID']
    buy_d = {'ID' : id, 'Product Name' : name, 'Buy Date' : today().strftime("%Y-%m-%d"),
    'Buy Price' : price, 'Expiration Date' : exp_d, 'Transaction ID' : bought_id}
    bp = pd.DataFrame(buy_d)

    bp.to_csv(file_b, mode = 'a', header = False, index = None)     # to sales file
    bp.to_csv(file_i, mode = 'a', header = False, index = None)   # to inventory

    return console.print(tabulate(bp, headers="keys", tablefmt="fancy_grid"))


def report_item():
    df = pd.read_csv(file_i)
   
    my_list = [x for x in df['Product Name'].str[:].str.lower()]
    count = 0
    product = console.input("\n[b green]Show the inventory of:[/b green] ").lower()
    if product not in my_list:
        console.print("[b u red]Sorry! Product not in stock[/b u red]\n")
        count += 1
        while product not in my_list:
            product = input("\nName your product: ").lower() 
            if product not in my_list:
                count += 1
                console.print("\n[b u red]Sorry! Product not in stock[/b u red]\n")  
            if count > 3:
                action()

    counts = df['Product Name'].value_counts()[product]

    index = df[df['Product Name'].str.lower() == product].index
    prices = [x for x in df.loc[index, 'Buy Price']]
    for price in prices:
        price = price           

    index = df[df['Product Name'].str.lower() == product].index
    dates = [x for x in df.loc[index, 'Expiration Date']]
    for date in dates:
        exp_d = date

    table_data = [['Product name', 'Count', 'Buy Price', 'Expiration Date'],
                    [product, counts, price, exp_d]]

    return tabulate(table_data, headers='firstrow', tablefmt="fancy_grid")


def products_in_stock():
    df = pd.read_csv(file_i)
    value_counts = df['Product Name'].value_counts()                        # counts the total of names for every product
    # creating dataframe with product name and count results
    df_value_counts = pd.DataFrame(value_counts) 
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['Product', 'Amount']                         # creates the desired column names (that 
    return tabulate(df_value_counts, headers="keys", tablefmt="fancy_grid") # shows the counted values of the products name)


def sell_product():
    df = pd.read_csv(file_i)
    my_list = [x for x in df['Product Name'].str[:].str.lower()]
    console.print("[b]What product would you like to purchase? Please enter it's [u]name[/u][/b].\n\n[b green]To see available products, type 'check':[/b green]")
    name = input("\n").lower()
    count = 0
    if name == 'check':
        console.print(products_in_stock())
    if name not in my_list:
        count += 1
        while name not in my_list:
            name = console.input("\n[b]What product would you like to purchase?\nPlease enter it's [u]name:[/u][/b] ").lower() 
            if name == 'check':
                console.print(products_in_stock())
            if name not in my_list:
                count += 1
                console.print("\n[b u red]Sorry! Product not in stock[/b u red]\n")  
            if count > 5:
                action()

    sdf = show_products()
    index = sdf[sdf['Product Name'].str.lower() == name].index
    price = sdf.loc[index, 'Price']

    index = df[df['Product Name'].str.lower() == name].index
    exp = df.loc[index[0], 'Expiration Date']
    sell_d = {'Sell Date' : today().strftime("%Y-%m-%d"), 'Sell Price' : price, 'Expiration Date' : exp}
    sp = pd.DataFrame(sell_d)

    sp.to_csv(file_s, mode = 'a', header = False, index = None)

    i = df[df['Product Name'].str.lower() == name].index
    tr_id = [x for x in df.loc[i, 'Transaction ID']][0]                 # get unique value (tr. ID)
    df.drop(df[df['Transaction ID'] == tr_id].index, inplace = True)    # drop row containing this value
    df.to_csv(file_i, index=None)                                       # rewrite it to the csv-file
    return console.print(tabulate(sp, headers="keys", tablefmt="fancy_grid")) 


def profit():
    bdf = pd.read_csv(file_b)
    sdf = pd.read_csv(file_s)
    bdf['Buy Date'] = pd.to_datetime(bdf['Buy Date'])
    sdf['Sell Date'] = pd.to_datetime(sdf['Sell Date'])
    filt_b = bdf['Buy Date'] == today()
    filt_s = sdf['Sell Date'] == today()
    b = bdf.loc[filt_b, 'Buy Price']
    s = sdf.loc[filt_s, 'Sell Price']
    total_b = b.sum()
    total_s = s.sum()
    sum = total_s - total_b
    if sum > 0 and sum < 1:
        return console.print(f"\n[b green]Nice! We're at a profit of {sum} already![/b green]")
    elif sum >= 1 and sum < 4:
        return console.print(f"\n[b green]Okay: {sum}! Not too shabby already![/b green]")
    elif sum >= 4 and sum < 10:
        return console.print(f"\n[b green]Wowsers! {sum}! Imma lookin' and Imma likin'![/b green]")
    elif sum >= 10:
        return console.print(f"\n[b green]OHHHH MYYYYY GOOODDDDDD!! {sum}!![/b green]")
    elif sum == 0:
        return console.print(f"\n[b green]Okay, we're at break even: {sum}. Not bad! Keep those customers coming![/b green]")
    else:
        return console.print(f"\n[b green]Let's hope for some more purchases, so we can get into some profits!\nWe're at a loss of {sum}[/b green]")


def profit_yesterday():
    bdf = pd.read_csv(file_b)
    sdf = pd.read_csv(file_s)
    bdf['Buy Date'] = pd.to_datetime(bdf['Buy Date'])
    sdf['Sell Date'] = pd.to_datetime(sdf['Sell Date'])
    filt_b = bdf['Buy Date'] == yesterday()
    filt_s = sdf['Sell Date'] == yesterday()
    b = bdf.loc[filt_b, 'Buy Price']
    s = sdf.loc[filt_s, 'Sell Price']
    total_b = b.sum()
    total_s = s.sum()
    sum = total_s - total_b
    if sum > 0 and sum < 1:
        return console.print(f"\n[b green]Nice! We're at a profit of {sum} already![/b green]")
    elif sum >= 1 and sum < 4:
        return console.print(f"\n[b green]Okay: {sum}! Not too shabby already![/b green]")
    elif sum >= 4 and sum < 10:
        return console.print(f"\n[b green]Wowsers! {sum}! Imma lookin' and Imma likin'![/b green]")
    elif sum >= 10:
        return console.print(f"\n[b green]OHHHH MYYYYY GOOODDDDDD!! {sum}!![/b green]")
    elif sum == 0:
        return console.print(f"\n[b green]Okay, we're at break even: {sum}. Not bad! Keep those customers coming![/b green]")
    else:
        return console.print(f"\n[b green]Let's hope for some more purchases, so we can get into some profits!\nWe're at a loss of {sum}[/b green]")


if __name__ == "__main__":
    app()