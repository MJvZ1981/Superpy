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
current = os.getcwd()
file_b = os.path.join(current, 'bght.csv')
file_s = os.path.join(current, 'sld.csv')
file_i = os.path.join(current, 'invntry.csv')
file_p = os.path.join(current, 'poducts.csv')
file_t = os.path.join(current, 'set_dt.txt')
info_f = os.path.join(current, 'info.txt')


# creating the csv-files
def create_csv():
    if not os.path.exists(file_b):
        with open(file_b, 'w+') as bought:
            headers = ['Product', 'Buy Date', 'Buy Price', 'Expiration Date', 'Bought ID']
            writer = csv.DictWriter(bought, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
    if not os.path.exists(file_s):
        with open(file_s, 'w+') as sold:
            headers = ['Sell Date', 'Sell Price', 'Expiration Date']
            writer = csv.DictWriter(sold, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
    if not os.path.exists(file_i):
        with open(file_i, 'w+') as inv:
            headers = ['Product', 'Buy Date', 'Buy Price', 'Expiration Date', 'Bought ID']
            writer = csv.DictWriter(inv, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
    if not os.path.exists(file_t):
        with open(file_t, 'w+') as f:
            f.write(str(date.today().strftime("%Y-%m-%d")))
    if not os.path.exists(file_p):
        with open(file_p, 'w+') as inv:
            headers = ['Product', 'Buy Price', 'Sell Price']
            writer = csv.DictWriter(inv, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()


@app.command()
def main():
    action()
    reset()
    return


def reset():
    app()


act_list = ['help', 'h', 'products', 'p', 'info', "i", 'add', 'a', 'del', 'd', 'edit', 'e', 'buy', 'b', 'sell', 's', 'stock', 'st', 'full stock', 'fs', 'check', 'c', 'custom date', 
            'cd', 'reset', 'r', 'today', 't', 'profit', 'w', 'profit yesterday', 'py', 'exit', 'x']


def action():
    create_csv()
    create_product_list()
    action = console.input("""\n[b blue]Choose your action. Type [b u]'help'[/b u] (or 'h') for all options or [b u]'exit'[/b u] (or 'x') to quit:\n\n[/b blue]""").lower()
    if action == 'help' or action == 'h':
        console.print("""\n[u b]Choose one of the following actions:[/u b]\n
        [b green]info[/b green] = shows a manual [b green](i)[/b green]
        [b green]products[/b green] = shows all the avaiable products [b green](p)[/b green]
        [b green]add[/b green] = add a new product [b green](a)[/b green]
        [b green]del[/b green] =  delete a product [b green](d)[/b green]
        [b green]edit[/b green] =  edit a product [b green](e)[/b green]
        [b green]buy[/b green] = adds a product to your inventory [b green](b)[/b green]
        [b green]sell[/b green] = lets you sell an item (if it's in stock) [b green](s)[/b green]
        [b green]stock[/b green] = shows the amount in stock of the desired product [b green](st)[/b green]
        [b green]full stock[/b green] = shows all products in stock [b green](fs)[/b green]
        [b green]check[/b green] = checks for potential expired dates (and auto-removes expired ones) [b green](c)[/b green]
        [b green]custom date[/b green] = create a specific date in time (+ or - a specific number of days) [b green](cd)[/b green]
        [b green]reset[/b green] = resets the date to the present time [b green](r)[/b green]
        [b green]today[/b green] = shows the given date (reset or not) [b green](t)[/b green]
        [b green]profit[/b green] = shows today's profit (or loss) [b green](w)[/b green]
        [b green]profit yesterday[/b green] = shows yesterdays profit (or loss) [b green](py)[/b green]
        [b red]exit[/b red] = quit [b red](x)[/b red]""")
    if action == 'info' or action == 'i':
        read_info()
    if action == 'products' or action == 'p':
        console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
    if action == 'add' or action == 'a':
        add_product()
    if action == 'del' or action == 'd':
        del_product()
    if action == 'edit' or action == 'e':
        edit_product()
    if action == 'buy' or action == 'b':
        buy_product()
    if action == 'sell' or action == 's':
        sell_product()
    if action == 'stock' or action == 'st':
        console.print(report_item())
    if action == 'full stock' or action == 'fs':
        console.print(products_in_stock())
    if action == 'check' or action == 'c':
        check_inventory()
    if action == 'custom date' or action == 'cd':
        custom_date()
    if action == 'reset' or action == 'r':
        reset_to_today()
    if action == 'today' or action == 't':
        console.print("\n[b green]Today it is: [/b green]", today().strftime("%Y-%m-%d"))
    if action == 'profit' or action == 'w':
        profit()
    if action == 'profit yesterday' or action == 'py':
        profit_yesterday()
    if action == 'exit' or action == 'x':
        quit()
    if action not in act_list:
        console.print("\n[b red]INVALID ACTION[/b red], [b]type [u]'help'[/u] of [u]'h'[/u] for more info[/b]")
    reset()


def reset_to_today():
    today = str(date.today())
    with open(file_t, 'w+') as f:
        f.write(today)
        return f


def today():
    with open(file_t, 'r') as f:
        return datetime.strptime(f.readlines()[0], "%Y-%m-%d")


def read_info():
    with open(info_f) as file:
        text = [line.strip().replace("', ''", "") for line in file]
        for line in text:
            line = print(line)
    return line


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
    df.drop(df[df['Expiration Date'] < today().strftime("%Y-%m-%d")].index, inplace = True)     # drop row containing this value
    df.to_csv(file_i, index=None)
    df.to_csv(file_b, index=None)
    return


products = ({
    'Product' : ['Apple', 'Banana', 'Kiwi', 'Pear', 'Broccoli', 'Lettuce', 'Sprouts',
    'Butter', 'Eggs', 'Milk', 'Cola', 'Fanta', 'Sisi'],
    'Buy Price'  : [0.2, 0.25, 0.30, 0.2, 0.45, 0.4, 0.6, 0.7, 0.75, 0.75, 0.8, 0.8, 0.8],
    'Sell Price' : [0.35, 0.45, 0.60, 0.35, 0.70, 0.6, 0.9, 1.1, 1.2, 1.25, 1.45, 1.4, 1.4]
})


def create_product_list():
    df = pd.read_csv(file_p)
    if df.empty:
        df = pd.DataFrame(products)
        df.to_csv(file_p, mode = 'a+', header = False, index = None)
    return df


def add_product():
    count = 0
    name = console.input("\n[b yellow]Enter the product's name:[/b yellow] ").capitalize()
    if name == 'exit':
        action()
    count += 1
    while name.capitalize() in products['Product']:
        console.print("[b red]ERROR![/b red] [b]product already available.[/b]")
        name = input("Enter product's name: ").capitalize()
        count += 1
        if name not in products['Product']:
            continue
        if count > 3:
            action()

    buy_price = float(input("Enter product's buy price (float): "))
    sell_price = float(input("Enter product's selling price (float): "))
    
    products['Product'].append(str(name))
    products['Buy Price'].append(float(buy_price))
    products['Sell Price'].append(float(sell_price))

    df = pd.DataFrame(products)
    df.to_csv(file_p, mode = 'w+', header = True, index = None)
    return


def del_product():
    df = (show_products())
    my_list = [x for x in df['Product'].str[:].str.lower()]
    console.print("[b yellow]What product would you like removed? Please enter it's [u]name[/u][/b yellow].\n")
    count = 0
    name = input("").lower()
    if name == 'Check':
        console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
    if name == 'Exit':
        action()
        
    count += 1
    while name.lower() not in my_list:
        console.print("[b red]ERROR![/b red] [b]Unknown product![/b]\n")
        name = console.input("[b yellow]Enter a product's name:[/b yellow] ").lower()
        count += 1
        if name == 'check':
            console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
        if name.capitalize() in my_list:
            continue
        if count > 3:
            action()
    
    df = pd.read_csv(file_p)   
    df.drop(df[df['Product'].str.lower() == name].index, inplace = True)
    df.to_csv(file_p, index=None)
    return df


def edit_product():
    console.print(tabulate(show_products(), headers="keys", tablefmt="fancy_grid"))
    df = (show_products())
    count = 0
    my_list = [x for x in df['Product'].str[:].str.lower()]
    # getting the index via name of the product
    name = console.input("\n[b yellow]What's the [b u]name[/b u] of the product?[/b yellow]\n")
    count += 1
    while name.lower() not in my_list:
        console.print("[b red]ERROR![/b red] [b]Unknown product![/b]\n")
        name = console.input("[b yellow]Enter a product's name:[/b yellow] ").lower()
        count += 1
        if name.capitalize() in my_list:
            continue
        if count > 3:
            action()
    index_nr = df[df['Product'].str.lower() == name].index
    # getting the key
    key = console.input("[b yellow]What lable do you want to edit? The [b red]'product'[/b red] the [b red]'buy price'[/b red] or the [b red]'sell price'[/b red]?[/b yellow]\n")
    while key.lower() not in ['product', 'buy price', 'sell price']:
        console.print("[b red]ERROR![/b red] [b]Unknown lable![/b]\n")
        key = console.input("[b yellow]What lable do you want to edit? The [b red]'product'[/b red] the [b red]'buy price'[/b red] or the [b red]'sell price'[/b red]?[/b yellow]\n")
        count += 1
        if key.lower() in ['product', 'buy price', 'sell price']:
            continue
        if count > 3:
            action()
    # variable to enter the right value (after replacing)
    edit = console.input("[b yellow]New input:[/b yellow] ")
    while edit.lower() in my_list:
        console.print("[b red]ERROR![/b red] [b]Product already exists![/b]\n")
        edit = console.input("[b yellow]New input:[/b yellow] ")
        count += 1
        if edit.lower() not in my_list:
            continue
        if count > 3:
            action()

    df.loc[index_nr, str(key).title()] = edit.capitalize()
    df.to_csv(file_p, index=None)
    return df


def show_products():
    df = pd.read_csv(file_p)
    return df


def buy_product():
    df = (show_products())
    my_list = [x for x in df['Product'].str[:].str.lower()]
    name = console.input("\n[b yellow]What product would you like to add to your inventory? Please enter it's [u]name[/u].[/b yellow]\n[b yellow]To see available products, type [u]'check'[/u] or [u]'exit'[/u] to return:[/b yellow] ").lower()
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

    while True:
        amount = console.input("[b yellow]How many would you like to purchase?[/b yellow] ")
        try:
            amount = int(amount)
            break
        except ValueError:
            console.print("\n[b red]ERROR! Input is not a number, type the amount:[/b red] ")
        
    if name.lower() in ['pear', 'kiwi', 'banana', 'apple']:
        exp_dt_f = today() + timedelta(14)                       
        exp_d = exp_dt_f.strftime("%Y-%m-%d")                   # Exp_d fruits
    if name.lower() in ['broccoli', 'lettuce', 'sprouts']:
        exp_dt_v = today() + timedelta(5)               
        exp_d = exp_dt_v.strftime("%Y-%m-%d")                   # Exp_d veggies
    if name.lower() in ['butter', 'eggs', 'milk']:
        exp_dt_d = today() + timedelta(7)           
        exp_d = exp_dt_d.strftime("%Y-%m-%d")                   # Exp_d dairy
    if name.lower() in ['cola', 'fanta', 'sisi']:
        exp_dt_s = today() + timedelta(200)           
        exp_d = exp_dt_s.strftime("%Y-%m-%d")                   # Exp_d soda
    if name.capitalize() not in products['Product']:
        exp_dt_s = today() + timedelta(6)
        exp_d = exp_dt_s.strftime("%Y-%m-%d")                   # random exp_d (for new products)

    bought_id = int(datetime.now().strftime("%Y%m%d%H%f"))
    index = df[df['Product'].str.lower() == name].index
    price = df.loc[index, 'Buy Price']
    buy_d = {'Product' : name.capitalize(), 'Buy Date' : today().strftime("%Y-%m-%d"),
    'Buy Price' : price, 'Expiration Date' : exp_d}
    bp = pd.DataFrame(buy_d)

    index = bp[bp['Product'].str.lower() == name].index
    my_list = bp.loc[index, :].values.flatten().tolist()

    nested_list = [my_list] * amount
    for list in nested_list:
        bought_id = bought_id + 1
        row = pd.Series(list)
        count = pd.Series(bought_id)
        row_to_add = pd.concat([row, count])
        bdf = pd.DataFrame([[x for x in row_to_add]], columns=['Product', 'Buy Date', 'Buy Price', 'Expiration Date', 'Bought ID'])
        bdf.to_csv(file_b, mode = 'a', header = False, index = None)
        bdf.to_csv(file_i, mode = 'a', header = False, index = None)
    
    return console.print(tabulate(bdf, headers="keys", tablefmt="fancy_grid"), f"\n\n[b yellow]{name.capitalize()} x {amount} have been added to your inventory![/b yellow]")


def report_item():
    df = pd.read_csv(file_i)
    print(df)
    
    my_list = [x for x in df['Product'].str[:].str.lower()]
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

    counts = (df['Product'].values == product.capitalize()).sum()
    index = df[df['Product'].str.lower() == product].index
    prices = [x for x in df.loc[index, 'Buy Price']]
    for price in prices:
        price = price           

    index = df[df['Product'].str.lower() == product].index
    dates = [x for x in df.loc[index, 'Expiration Date']]
    for date in dates:
        exp_d = date

    table_data = [['Product', 'Count', 'Buy Price', 'Expiration Date'],
                    [product, counts, price, exp_d]]

    return tabulate(table_data, headers='firstrow', tablefmt="fancy_grid")


def products_in_stock():
    df = pd.read_csv(file_i)
    value_counts = df['Product'].value_counts()                             # counts the total of names for every product
    # creating dataframe with product name and count results
    df_value_counts = pd.DataFrame(value_counts) 
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['Product', 'Amount']                         # creates the desired column names (that 
    return tabulate(df_value_counts, headers="keys", tablefmt="fancy_grid") # shows the counted values of the products name)


def sell_product():
    df = pd.read_csv(file_i)
    my_list = [x for x in df['Product'].str[:].str.lower()]
    count = 0
    name = console.input("[b yellow]What product would you like to purchase? Please enter it's [u]name[/u][/b yellow].\n[b yellow]To see available products, type 'check':[/b yellow] ").lower()
    counts = (df['Product'].values == name.capitalize()).sum()
    console.print(f"[b]\nA total of [b green]{counts}[/b green] in stock![/b]")
    if name == 'check':
        console.print(products_in_stock()) 
    count += 1
    while name not in my_list:
        console.print("\n[b red]ERROR! Product not available![/b red]")
        name = console.input("\n[b yellow]What product would you like to purchase?\nPlease enter it's [u]name:[/u][/b yellow] ").lower()
        console.print(f"[b]\nA total of [b green]{counts}[/b green] in stock![/b]")
        count += 1
        if name == 'check':
            console.print(products_in_stock()) 
        if count > 5:
            action()

    while True:
        amount = console.input("\n[b yellow]How many would you like to purchase?[/b yellow] ")
        try:
            amount = int(amount)
            break
        except ValueError:
            console.print("\n[b red]ERROR! Input is not a number, type the amount:[/b red] ")

    sdf = show_products()
    index = sdf[sdf['Product'].str.lower() == name].index
    price = sdf.loc[index, 'Sell Price']

    index = df[df['Product'].str.lower() == name].index
    exp = df.loc[index[0], 'Expiration Date']
    sell_d = {'Sell Date' : today().strftime("%Y-%m-%d"), 'Sell Price' : price, 'Expiration Date' : exp}
    sp = pd.DataFrame(sell_d)

    i = df[df['Product'].str.lower() == name].index
    id_list = [x for x in df.loc[i, 'Bought ID']][:(amount)]                # get unique value (tr. ID)
    stocked = [x for x in df.loc[i, 'Bought ID']][:]                        # check for amount stocked of the desired product
    stock = len(stocked)
    if len(stocked) >= amount:
        for ids in id_list:
            id = ids
            df.drop(df[df['Bought ID'] == id].index, inplace = True)
            df.to_csv(file_i, index=None)
            sp.to_csv(file_s, mode = 'a', header = False, index = None)
    else:
        return console.print(f"[b red]ERROR! Only {stock} in store. Amount not available[/b red].")

    return console.print(tabulate(sp, headers="keys", tablefmt="fancy_grid"), f"\n\n[b yellow]Sold {amount}![/b yellow]") 


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
        return console.print(f"\n[b green]Nice! We made a profit of {sum}![/b green]")
    elif sum >= 1 and sum < 4:
        return console.print(f"\n[b green]Okay: {sum}! Not too shabby![/b green]")
    elif sum >= 4 and sum < 10:
        return console.print(f"\n[b green]Wowsers! {sum}! Imma lookin' and Imma likin'![/b green]")
    elif sum >= 10:
        return console.print(f"\n[b green]OHHHH MYYYYY GOOODDDDDD!! {sum}!![/b green]")
    elif sum == 0:
        return console.print(f"\n[b green]Okay, break even: {sum}. Not bad!![/b green]")
    else:
        return console.print(f"\n[b green]Let's hope for a better day tomorrow!\nWe're down {sum}![/b green]")


if __name__ == "__main__":
    app()
