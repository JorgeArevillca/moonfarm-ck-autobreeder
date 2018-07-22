# import libraries
import time
import json
from pprint import pprint
from web3 import Web3, HTTPProvider
from ethereum.transactions import Transaction
import codecs
import rlp
from numpy import binary_repr

print("Starting to breed your kittehs!")
# declare an object for breedingpairs
breedingpairs = []
private_key = 'wallet_private_key' # your wallet privatekey inside ''
# load breedingpairs from json
with open('breedingpairs.json') as f:
    breedingpairs = json.load(f)

# set infura api key
web3 = Web3(HTTPProvider('https://mainnet.infura.io/api_key_here')) # replace api_key_here with infura api key

# contract ABI of the functions we require
ABI = [{"constant":True,"inputs":[{"name":"_kittyId","type":"uint256"}],"name":"isReadyToBreed","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_matronId","type":"uint256"},{"name":"_sireId","type":"uint256"}],"name":"breedWithAuto","outputs":[],"payable":True,"stateMutability":"payable","type":"function"}]

# cryptokitty sales contract address
kittywallet = '0x06012c8cf97BEaD5deAe237070F9587f8E7A266d'
# your own wallet address
wallet = 'public_wallet_address' # add your public wallet address here
kitty = web3.eth.contract(kittywallet, abi=ABI)

# breedWithAuto MethodID
birthingmethod = 'f7d8c883'
# used to create the data to the transaction
zeros = '0000000000000000000000000000000000000000000000000000000000000000'
# transaction data later used in beedWithAuto
txn = {'from':wallet, 'value':web3.toWei(0.008, 'ether'), 'gas':119902, 'nonce':0}

i = 0
pair_breedable = False

# set gas price used throughout the script
gasPrice = web3.toWei(4,'gwei')
# define function for checking if pair is breedable
def is_breedable_pair(pair):
    try:
        # check sire and matron through contract method isReadyToBreed
        breedable_sire = bin(kitty.functions.isReadyToBreed(pair['sire']).call())
        breedable_matron = bin(kitty.functions.isReadyToBreed(pair['matron']).call())
        # check so both sire and matron are ready to breed and then return true
        if '0b1' == breedable_sire and '0b1' == breedable_matron:
            return True
        # otherwise a transaction has gone through recently and then set status to 1 and gasprice to default
        # return that the pair is not ready to breed
        return False
    except Exception as e:
        print(e)

# breeding function
def breed(pair):
    try:
        # sire and matron to hex values
        sire_hex = web3.toHex(pair['sire'])[2:]
        matron_hex = web3.toHex(pair['matron'])[2:]
        # find latest nonce
        web3_txn_count = web3.eth.getTransactionCount(wallet)
        # if there are pending transactions go with our own nonce count
        if txn['nonce'] < web3_txn_count:
            txn['nonce'] = web3.eth.getTransactionCount(wallet)
        else:
            txn['nonce'] += 1
        # set the transaction data
        txn['data'] = birthingmethod + zeros[:(len(zeros)-len(matron_hex))] + matron_hex + zeros[:(len(zeros)-len(sire_hex))] + sire_hex
        # create a transaction with pyethereums transaction class
        tx = Transaction(nonce = txn['nonce'], gasprice = txn['gasPrice'], startgas = txn['gas'], to = kittywallet, value = txn['value'], data = codecs.decode(txn['data'], 'hex'))
        # if status is 0 this is a retry of a transaction
        if pair['status'] == 0:
            pair['gasPrice'] += 2000000000
            tx = Transaction(nonce = pair['nonce'], gasprice = pair['gasPrice'], startgas = txn['gas'], to = kittywallet, value = txn['value'], data = codecs.decode(txn['data'], 'hex'))
        # sign the transaction with your private key
        tx.sign(private_key)
        # make the transaction transmittable to the blockchain
        raw_tx = rlp.encode(tx)
        raw_tx_hex = web3.toHex(raw_tx)
        # send the transaction
        pair['latest_tx'] = web3.toHex(web3.eth.sendRawTransaction(raw_tx_hex))
        print('********************')
        print('*** sending transaction: ', pair['latest_tx'])
        print('*** for breeding kitties: ', pair['sire'], ' and ', pair['matron'])
        print('*** with nonce: ', txn['nonce'])
        print('*** and gas price: ', txn['gasPrice'])
        print('********************')
        # set default values to the breedingpair and remember the nonce
        pair['cooldown'] = 5
        pair['status'] = 0
        pair['nonce'] = txn['nonce']
        # if something went wrong try again with higher nonce
    except Exception as e:
        print('error: ',e)
        if '-32000' in str(e):
            txn['nonce'] += 1
            tx = Transaction(nonce = txn['nonce'], gasprice = txn['gasPrice'], startgas = txn['gas'], to = kittywallet, value = txn['value'], data = codecs.decode(txn['data']))
            tx.sign(private_key)
            raw_tx = rlp.encode(tx)
            raw_tx_hex = web3.toHex(raw_tx)
            pair['latest_tx'] = web3.toHex(web3.eth.sendRawTransaction(raw_tx_hex))
            print('********************')
            print('*** sending transaction: ', pair['latest_tx'])
            print('*** for breeding kitties: ', pair['sire'], ' and ', pair['matron'])
            print('*** with nonce: ', txn['nonce'])
            print('*** and gas price: ', txn['gasPrice'])
            print('********************')

def isTransactionSent(txn, count):
    receipt = web3.eth.getTransactionReceipt(txn)
    if receipt != None:
        count += 1
        print('*** breeding count: ', count)
        print('********************')
        pair['status'] = 1
        pair['gasPrice'] = gasPrice
            
breeding_counter = 0
# main loop
while True:
    # set gasprice here
    txn['gasPrice'] = gasPrice
    # if the loop is complete reset i and sleep a minute
    if i >= len(breedingpairs):
        i = 0
        time.sleep(60)
        
    # check if the transaction is sent
    if breedingpairs[i]['status'] == 0:
        isTransactionSent(breedingpairs[i]['latest_tx'], breeding_counter)

    # tick down the cooldown, just so that the bot wont spam transactions
    if breedingpairs[i]['cooldown'] > 0:
        breedingpairs[i]['cooldown'] -= 1
    else:
        # if the cooldown is 0 go here and check every minute if the pair is breedable
        pair_breedable = is_breedable_pair(breedingpairs[i])

    # if the pair was breedable then breed
    if pair_breedable: 
        breed(breedingpairs[i])
        pair_breedable = False
        time.sleep(1)

    # go to next breedingpair
    i+=1
