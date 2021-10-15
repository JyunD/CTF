from web3 import Web3
import requests
from bs4 import BeautifulSoup

class Contract():

    def __init__(self, abi, bytecode, address = None, construction = False):
        self.w3 = Web3(Web3.WebsocketProvider('wss://ropsten.infura.io/ws/v3/faa6cd8da8984cc7b95b935d1bede5c7'))
        self.abi = abi
        self.bytecode = bytecode
        self.address = address
        self.object = self.w3.eth.contract(abi = self.abi, bytecode = self.bytecode, address = self.address)

        if construction:
            build = self.object.constructor().buildTransaction({
                'from': '0x348A4b3D65c0663190cda60e2981D5ae377db446',
                'nonce': self.w3.eth.getTransactionCount('0x348A4b3D65c0663190cda60e2981D5ae377db446'),
                'gas': 1000000,
                'gasPrice': self.w3.toWei("3", 'gwei')
            })
            transaction = self.w3.eth.sendRawTransaction(self.w3.eth.account.signTransaction(build, private_key).rawTransaction)
            print("Transaction -> https://ropsten.etherscan.io/tx/{}".format(transaction.hex()))
            self.w3.eth.waitForTransactionReceipt(transaction)

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            s = requests.session()
            while True:
                try:
                    html = s.get("https://ropsten.etherscan.io/tx/{}".format(transaction.hex()), headers = headers)
                    self.address = BeautifulSoup(html.text,  "html.parser").find(id='contractCopy').string
                    if self.address != None:
                        print(self.address)
                        break
                except:
                    pass


    def call(self, name, *args):
        return self.object.functions[name](*args).call()

    def send_transaction(self, name, addr, private_key, *args, value = 0, gas_limit = 1000000, gas_price = 3, unit = 'gwei'):
        build = self.object.functions[name](*args).buildTransaction({
            'from': addr,
            'value': value,
            'nonce': self.w3.eth.getTransactionCount(addr),
            'gas': gas_limit,
            'gasPrice': self.w3.toWei(str(gas_price), unit)
        })
        transaction = self.w3.eth.sendRawTransaction(self.w3.eth.account.signTransaction(build, private_key).rawTransaction)
        print("Transaction -> https://ropsten.etherscan.io/tx/{}".format(transaction.hex()))
        self.w3.eth.waitForTransactionReceipt(transaction)

    
address = '0x348A4b3D65c0663190cda60e2981D5ae377db446'
private_key = bytes.fromhex('')