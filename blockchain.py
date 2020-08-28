import functools
REWARD = 10
genesis_block = {'previous hash': '', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
open_transection = []
owner = 'raju'
participents = {'raju'}


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_last_blockcahin_value():
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transection if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_recipient, 0)
    return amount_recieved - amount_sent


def varify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if varify_transaction(transaction):
        open_transection.append(transaction)
        participents.add(sender)
        participents.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'Mining',
        'recipient': owner,
        'amount': REWARD
    }
    copied_transection = open_transection[:]
    copied_transection.append(reward_transaction)
    block = {
        'previous hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transection,
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = str(input('name of reciever:'))
    tx_amount = float(input('enter amount :'))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = str(input('your choice:'))
    return user_input


def print_blockcahain_elements():
    for block in blockchain:
        print('outputting the blockchain')
        print(block)
    else:
        print('-' * 140)


def varify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


def varify_transactions():
    return all([varify_transaction(tx) for tx in open_transection])


waiting_for_input = True
while waiting_for_input:
    print('1: add a new tranasction value ')
    print('2: mine block')
    print('3: output the blockchain blocks')
    print('4: outputting the participents')
    print('5: check transactions are valid')
    print('h: manipulate the chain')
    print('q: quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('transaction added!')
        else:
            print('transaction failed')
        print(open_transection)
    elif user_choice == '2':
        if mine_block():
            open_transection = []
    elif user_choice == '3':
        print_blockcahain_elements()
    elif user_choice == '4':
        print(participents)
    elif user_choice == '5':
        if varify_transactions():
            print('all are valid')
        else:
            print('not valid')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous hash': '',
                'index': 0,
                'transactions': [
                    {'sender': 'raju', 'recipient': 'someone', 'amount': 100.0}
                ],
            }
    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('input invalid')
    if not varify_chain():
        print_blockcahain_elements()
        print('invalid blockchain')

    print('Balance of {} : {:6.2f} '.format('raju', get_balance(owner)))


print('done')
