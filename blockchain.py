from functools import reduce
import hashlib
import json
from collections import OrderedDict


from hash_util import hash_string_256, hash_block


REWARD = 10
genesis_block = {'previous hash': '',
                 'index': 0, 'proof': 100, 'transactions': []}
blockchain = [genesis_block]
open_transection = []
owner = 'raju'
participents = {'raju'}


def load_data():
    with open('blockchain.txt', mode='r') as f:
        file_content = f.readlines()
        blockchain = json.loads(file_content[0][:-1])
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                'previous hash': block['previous hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]}
            updated_blockchain.append(updated_block)
            blockchain = updated_block
        open_transection = json.loads(file_content[1])
        updated_transaction = []
        for tx in open_transection:
            updated_transactions = {'previous hash': block['previous hash'],
                                    'index': block['index'],
                                    'proof': block['proof'],
                                    'transactions': [OrderedDict(
                                        [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])for tx in block['transactions']]}
            updated_transaction.append(updated_transactions)
            open_transection = updated_transaction


load_data()


def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transection))


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions)+str(last_hash)+str(proof)).encode()
    print(guess)
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0: 2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transection, last_hash, proof):
        proof += 1
    return proof


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
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_recipient, 0)
    return amount_recieved - amount_sent


def varify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    # transaction = {
    #   'sender': sender,
    #  'recipient': recipient,
    # 'amount': amount
   # }
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if varify_transaction(transaction):
        open_transection.append(transaction)
        participents.add(sender)
        participents.add(recipient)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
   # reward_transaction = {
    #    'sender': 'Mining',
    #   'recipient': owner,
    #  'amount': REWARD
    # }
    reward_transaction = OrderedDict(
        [('sender', 'Mining'), ('recipient', owner), ('amount', REWARD)])
    copied_transection = open_transection[:]
    copied_transection.append(reward_transaction)
    block = {
        'previous hash': hashed_block,
        'index': len(blockchain),
        'proof': proof,
        'transactions': copied_transection
    }
    blockchain.append(block)
    save_data()
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
        if not valid_proof(block['transactions'][:-1], block['previous hash'], block['proof']):
            print('invalid blockchain!!')
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
