from CryptoExchange import app
from threading import Thread
from transaction_util import TransactionUtil



if __name__ == '__main__':
    # transaction_util = TransactionUtil()
    # transaction_thread = Thread(target=transaction_util, args=(1,))
    # transaction_thread.start()
    app.debug = True
    app.run(host="0.0.0.0")


