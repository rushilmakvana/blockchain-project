genesis_block = {"previous hash": "", "index": 0, "transactions": []}
blockchain = [genesis_block]
open_transection = []
owner = "Rj"


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


def hash_block(last_block):
    return "-".join([str(last_block[key]) for key in last_block])


def get_last_blockcahin_value():
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    open_transection.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)
    block = {
        "previous hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transection,
    }
    blockchain.append(block)


def get_transaction_value():
    tx_recipient = str(input("name of reciever:"))
    tx_amount = float(input("enter transaction amount please:"))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = str(input("your choice:"))
    return user_input


def print_blockcahain_elements():
    for block in blockchain:
        print("outputting the blockchain")
        print(block)
    else:
        print("-" * 110)


def varify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous hash"] != hash_block(blockchain[index - 1]):
            return False
    return True


waiting_for_input = True
while waiting_for_input:
    print("1: add a new tranasction value ")
    print("2: output the blockchain blockchain blocks")
    print("3: output the blockchain blocks")
    print("h: manipulate the chain")
    print("q: quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_recipent, tx_amount = get_transaction_value()
        add_transaction(recipient=tx_recipent, amount=tx_amount)
        print(open_transection)
    if user_choice == "2":
        mine_block()
    elif user_choice == "3":
        print_blockcahain_elements()
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous hash": "",
                "index": 0,
                "transactions": [
                    {"sender": "rushil", "recipeint": "someone", "amount": 100.0}
                ],
            }
    elif user_choice == "q":
        break
    else:
        print("input was unvalid,please select value from the list ")
    if not varify_chain():
        print_blockcahain_elements()
        print("invalid blockchain")
        break


print("done")
