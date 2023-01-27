The technical things I implemented ánd find notable are:

1. The ability to at once (on opening te file) add a standard list with products. Additionally you can modify this list of products by adding or deleting products to your own discretion. 
On top of this, you can edit anything of every single item that is already in te list (or has been added). If you accidentally made a small mistake (you entered the price incorrect or without capital letters) or if prices simply need to change because of the market, you can simply modify a product's name. You can change the buy price or the sell price, it's really easy if you simply follow the instrucions that the built-in help function shows. You can access it by typing 'help' or 'h' in the action-caller (right after starting the application by running main.py)

2. Working with the module Pandas to not only add my info to the csv-files, but to also have the ability to pick out the items that are:
    - expired by date when you simply check the inventory. In order to do so you do have to head back in time to buy a product (or clean everything that is expired) and then reset the date to be able to check if it works (and it should!).
    - sold and have to be removed from the inventory ánd added to the sold list. The fact that I had a unique transaction code generated (using the datetime module, without the dashes) allows the program to find that exact value and find and work with that specific item/row.

3. I used the Typer and Rich module, what resulted in a (what I think of as) easy to use CLI. It's pretty straightforward and does not require the long strings needed with argparse. I think the program is pretty self-explanatoy because of this.

4. Last but not least. The possibility to buy or sell multiple products. All products will be added to the underlaying data-files to properly manage your inventory. When a product is not properly stocked, the program will tell you exactly how many there are in stock.

Sidenote: I came up with the idea to create a list of sorts: fruits [], dairy [] in the global scope. In the case where the supermarket can input what sort of product they want to add. For instance 'fruit'. In this case, the item will get appended to the fruits_list. This way I could keep up with the expiration date system I inplemented. But since there are so many sorts of products I just added a basic/standard date for newly added products. If the supermarket really does want to add this feature to the application (and willing to pay...) SURE! :)
