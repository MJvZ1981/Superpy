Three technical things I implemented and find notable are:

1. Automaticly generated expiration dates for the products that are bought by the supermarket. Soda does not have the same expiration date as a dairy product or fruit. To not get it out of hand I clustered similar products and their generated dates. For this I used listed items as I have learned by studying a earlier assignments solution. To make it a bit more compact:

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

2. Working with the module Pandas to not only add my info to the csv-files, but to also have the ability to pick out the items that are:
    - expired by date when you simply check the inventory. In order to do so you do have to head back in time to buy a product (or clean everything that is expired) and then reset the date to be able to check if it works (and it should!).
    - sold and have to be removed from the inventory ánd added to the sold list. The fact that I had a unique transaction code generated (using the datetime module, without the dashes) allows the program to find that exact value and find and work with that specific item/row. I didn't want the ID to increment by one, cause it doesn't seem realistic for a company to have such simplistic ID's for their products. Mostly an ID-number has attributes for further organizing purposes with the product (like size, color, price, sort).

3. I used the Typer and Rich module, what resulted in a (what I think of as) easy to use CLI. It's pretty straightforward and didn't require the far more code using argparse module. I think the program is pretty self explanatoy because of this.

Sidenote: I did want to add the function to buy more than one item, but it was quite a struggle. I tried to have the transaction code add the nanosecond (instead of the hours and seconds, to not make the strain too long), but it still adds all bought items in the same nanosecond. That would mean that if it tries to sell one item, it will sell all the items with the same products (unless I code it in such a way that it descends with the amount bought). So I stuck to buying one item, since I need to show I understand pretty much what it takes to create what I think I have. So hopefully it does show that! Anyhow, looking forward to some feedback after this tough cookie.