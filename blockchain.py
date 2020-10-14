genesis_block = {"previous hash": "", "index": 0, "transactions": []}
blockchain = [genesis_block]
open_transection = []
owner = "p_key"


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


def hash_block():
    return "-".join([str(last_block[key]) for key in last_block])


def get_last_blockcahin_value():
    """return the last value from blockchain"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


""" this function accepts two arguments
one required one(transaction amonut) and optional  one is (last transaction)
optional one is optimal because it has default vaue is [1] """


def add_transaction(recipient, sender=owner, amount=1.0):
    """append a new value as well as last bockchain valuse to the blockchain
    arguments:
        sender:the sender of the coins
        recipient:the recipient of the coins
        amount:the amount of coins sent with the transaction(default=1.0)
    """

    transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    open_transection.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    #  print(hashed_block)
    block = {
        "previous hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transection,
    }
    blockchain.append(block)


def get_transaction_value():
    """returns the input of the user (new amount as float)
    """
    tx_recipient = input("name of reciever:")
    tx_amount = float(input("enter transaction amount please:"))
    return tx_recipient, tx_amount


def get_user_choice():
    """user choice and return it"""
    user_input = input("your choice:")
    return user_input


def print_blockcahain_elements():
    """prints all block in blockchain
    output the blockchain list"""
    for block in blockchain:
        print("outputting the blockchain")
        print(block)
    else:
        print("-" * 20)


def varify_chain():
    """varify the current blockchain and return true if it is valid,false otherwise"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous hash"] != hash_block(blockchain[index - 1] ):
            return False
    return True

# a while loop for the user input interface.
while True:
    print("1: add a new tranasction value ")
    print("2: output the blockchain blockchain blocks")
    print("3: output the blockchain blocks")
    print("h: manipulate the chain")
    print("q: quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        # recipient, amount == tx_data
        # add the transaction amount to the blockchain
        # add_transaction(recipient, amount=amount)
        print(open_transection)
    elif user_choice == "2":
        pr = mine_block()
        print(pr)
    elif user_choice == "3":
        print_blockcahain_elements()
    elif user_choice == "h":
        # make sure that you dont try  to "hack" the blockchain if it is empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous hash": "",
                "index": 0,
                "transactions": [
                    {"sender": "rushil", "recipeint": "someone", "amount": 100.0}
                ],
            }
        elif user_choice == "q":
            # this will lead to the loop to exist because it running condition
            break
        else:
            print("input was unvalid,please select value from the list ")

    else:
        print("user left")

