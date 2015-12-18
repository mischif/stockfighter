################################################################################
#                           Stockfighter API Library                           #
#               Simple library to perform common in-game actions               #
#                               (C) 2015 Mischif                               #
#       Released under version 3.0 of the Non-Profit Open Source License       #
################################################################################

__version__ = "1.0.0"

import json
import logging
import requests
from ws4py.client.threadedclient import WebSocketClient

class CustomLogs(logging.Formatter):
	FORMATS = {
	logging.DEBUG    : "[*] %(message)s",
	logging.INFO     : "[+] %(message)s",
	logging.ERROR    : "[-] %(message)s",
	logging.CRITICAL : "[!] %(message)s"
	}

	def format(self, record):
		self._fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.DEBUG])
		return logging.Formatter.format(self, record)

################################################################################
#                                                                              #
#                 Useful common functions and shared variables                 #
#                                                                              #
################################################################################

class Util(object):

	headers = None
	log = logging.getLogger(__name__)
	ch = logging.StreamHandler()
	ch.setFormatter(CustomLogs())
	log.addHandler(ch)

	@classmethod
	def ticker_callback(cls, m):
		if m.is_text:
			try:
				msg = json.loads(m.data)
				cls.log.debug("Websocket message: %s" % msg)
			except ValueError as e:
					self.log.error("Websocket message isn't JSON: %s" % m.data)
					pass
		else:
			cls.log.error("Somehow got a binary message from the websocket")

	@classmethod
	def dokidoki(cls, venue):
		if not venue: cls.log.debug("Making sure Stockfighter APIs are up...")
		else: cls.log.debug("Making sure venue is up...")

		if not venue: endpoint = "https://api.stockfighter.io/ob/api/heartbeat"
		else: endpoint = "https://api.stockfighter.io/ob/api/venues/%s/heartbeat" % venue

		res = cls.get(endpoint)

		if res:
			if not venue:
				cls.log.info("APIs are up")
			else:
				cls.log.info("Venue is up")
			return True
		return False

	@classmethod
	def get(cls, url, headers = None):

		if not headers:
			res = requests.get(url, headers = cls.headers)
		else:
			hdrs = cls.headers.copy()
			hdrs.update(headers)
			res = requests.get(url, headers = hdrs)

		if not res.status_code == requests.codes.ok:
			cls.log.error("Got %d status code" % res.status_code)

		try:
			out = res.json()
			if "ok" not in out:
				cls.log.error("OK not in response; are they fucking with us?")
				cls.log.debug("Server's response:\n%s" % out)
			elif not out["ok"]:
				if "error" not in out:
					cls.log.error("Error message not in response; are they fucking with us?")
					cls.log.debug("Server's response:\n%s" % out)
				else:
					cls.log.error("Action failed with error %s" % out["error"])
			else:
				return out
		except ValueError:
			cls.log.error("Couldn't parse server's response")
			cls.log.debug("Server's response:\n%s" % res.text)

		return None

	@classmethod
	def post(cls, url, data = None, headers = None):

		if not headers:
			res = requests.post(url, headers = cls.headers, data = data)
		else:
			hdrs = cls.headers.copy()
			hdrs.update(headers)
			res = requests.post(url, headers = hdrs, json = data)

		if not res.status_code == requests.codes.ok:
			cls.log.error("Got %d status code" % res.status_code)

		try:
			out = res.json()
			if "ok" not in out:
				cls.log.error("OK not in response; are they fucking with us?")
				cls.log.debug("Server's response:\n%s" % out)
			elif not out["ok"]:
				if "error" not in out:
					cls.log.error("Error message not in response; are they fucking with us?")
					cls.log.debug("Server's response:\n%s" % out)
				else:
					cls.log.error("Action failed with error %s" % out["error"])
			else:
				return out
		except ValueError:
			cls.log.error("Couldn't parse server's response")
			cls.log.debug("Server's response:\n%s" % res.text)

		return None

	@classmethod
	def delete(cls, url, headers = None):

		if not headers:
			res = requests.delete(url, headers = cls.headers)
		else:
			hdrs = cls.headers.copy()
			hdrs.update(headers)
			res = requests.delete(url, headers = hdrs)

		if not res.status_code == requests.codes.ok:
			cls.log.error("Got %d status code" % res.status_code)

		try:
			out = res.json()
			if "ok" not in out:
				cls.log.error("OK not in response; are they fucking with us?")
				cls.log.debug("Server's response:\n%s" % out)
			elif not out["ok"]:
				if "error" not in out:
					cls.log.error("Error message not in response; are they fucking with us?")
					cls.log.debug("Server's response:\n%s" % out)
				else:
					cls.log.error("Action failed with error %s" % out["error"])
			else:
				return out
		except ValueError:
			cls.log.error("Couldn't parse server's response")
			cls.log.debug("Server's response:\n%s" % res.text)

		return None

################################################################################
#                                                                              #
#                 Methods for interacting with the Game Master                 #
#                                                                              #
################################################################################

class GM(object):

	@staticmethod
	def start_instance(level):
		Util.log.debug("Attempting to start new instance of level %s" % level)

		endpoint = "https://api.stockfighter.io/gm/levels/%s" % level
		res = Util.post(endpoint)

		if res:
			Util.log.info("Started new level!")
			return res
		return None

	@staticmethod
	def restart_instance(instance):
		Util.log.debug("Attempting to restart instance %d" % instance)

		endpoint = "https://api.stockfighter.io/gm/instances/%d/restart" % instance
		res = Util.post(endpoint)

		if res:
			Util.log.info("Restarted the instance!")
			return res
		return None

	@staticmethod
	def stop_instance(instance):
		Util.log.debug("Attempting to stop instance %d" % instance)

		endpoint = "https://api.stockfighter.io/gm/instances/%d/stop" % instance
		res = Util.post(endpoint)

		if res:
			Util.log.info("Stopped the instance!")
			return res
		return None

	@staticmethod
	def resume_instance(instance):
		Util.log.debug("Attempting to resume instance %d" % instance)

		endpoint = "https://api.stockfighter.io/gm/instances/%d/resume" % instance
		res = requests.post(endpoint)

		if res:
			Util.log.info("Resumed the instance!")
			return res
		return None

	@staticmethod
	def get_instance_status(instance):
		Util.log.debug("Attempting to get status of instance %d" % instance)

		endpoint = "https://api.stockfighter.io/gm/instances/%d" % instance
		res = requests.get(endpoint)

		if res:
			Util.log.info("Got instance status!")
			return res
		return None

################################################################################
#                                                                              #
#              Methods for interacting with the websocket tickers              #
#                                                                              #
################################################################################

class Ticker(WebSocketClient):

	def handshake_ok(self):
		Util.log.debug("Opened connection to %s" % self.peer_address[0])
		if self.manager:
			self.manager(self)
			Util.log.debug("Attaching websocket to manager")

	def closed(self, code, reason):
		Util.log.debug("Connection to %s closed" % self.peer_address)

	def add_manager(self, man):
		self.manager = man

	def change_callback(self, cb):
		self.received_message = cb

	@staticmethod
	def new_venue_quotes_ticker(acct, venue, cb = Util.ticker_callback):
		url = "wss://api.stockfighter.io/ob/api/ws/%s/venues/%s/tickertape" % (acct, venue)
		ticker = Ticker(url)
		ticker.received_message = cb
		return ticker

	@staticmethod
	def new_stock_quotes_ticker(acct, venue, stock, cb = Util.ticker_callback):
		url = "wss://api.stockfighter.io/ob/api/ws/%s/venues/%s/tickertape/stocks/%s" % (acct, venue, stock)
		ticker = Ticker(url)
		ticker.received_message = cb
		return ticker

	@staticmethod
	def new_venue_fills_ticker(acct, venue, cb = Util.ticker_callback):
		url = "wss://api.stockfighter.io/ob/api/ws/%s/venues/%s/executions" % (acct, venue)
		ticker = Ticker(url)
		ticker.received_message = cb
		return ticker

	@staticmethod
	def new_stock_fills_ticker(acct, venue, stock, cb = Util.ticker_callback):
		url = "wss://api.stockfighter.io/ob/api/ws/%s/venues/%s/executions/stocks/%s" % (acct, venue, stock)
		ticker = Ticker(url)
		ticker.received_message = cb
		return ticker

################################################################################
#                                                                              #
#                   Methods for interacting with the markets                   #
#                                                                              #
################################################################################

class Markets(object):

	@staticmethod
	def get_venue_listings(venue):
		Util.log.debug("Attempting to get stocks available at venue %s" % venue)

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/stocks" % venue
		res = Util.get(endpoint)

		if res:
			Util.log.info("Got listings!")
			return res["symbols"]
		return None

	@staticmethod
	def get_orderbook(venue, stock):
		Util.log.debug("Attempting to get orderbook for %s at venue %s" % (stock, venue))

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/stocks/%s" % (venue, stock)
		res = Util.get(endpoint)

		if res:
			Util.log.info("Got orderbook!")
			return res
		return None

	@staticmethod
	def get_quote(venue, stock):
		Util.log.debug("Attempting to get quote for %s at venue %s" % (venue, stock))

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/stocks/%s/quote" % (venue, stock)
		res = Util.get(endpoint)

		if res:
			Util.log.info("Got quote!")
			return res
		return None

	@staticmethod
	def get_order_status(venue, stock, order):
		Util.log.debug("Attempting to get status of order %d in venue %s" % (order, venue))

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/stocks/%s/orders/%d" % (venue, stock, order)
		res = Util.get(endpoint)

		if res:
			Util.log.info("Got order status!")
			return res
		return None

	@staticmethod
	def get_all_stock_orders_status(venue, acct):
		Util.log.debug("Attempting to get all orders for account %s in venue %s" % (acct, venue))

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/accounts/%s/orders" % (venue, acct)
		res = Util.get(endpoint, self.headers)

		if res:
			Util.log.info("Got orders statuses!")
			return res
		return None

	@staticmethod
	def get_single_stock_orders_status(venue, acct, stock):
		Util.log.debug("Attempting to get all orders of stock %s for account %s in venue %s" % (stock, acct, venue))

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/accounts/%s/stocks/%s/orders" % (venue, acct, stock)
		res = Util.get(endpoint)

		if res:
			Util.log.info("Got orders statuses!")
			return res
		return None

	@staticmethod
	def make_order(venue, acct, stock, order_type, order_dir, qty, price):
		Util.log.debug("Attempting to %s %d shares of %s at %d as a %s order in %s using account %s" % (order_dir, qty, stock, price, order_type, venue, acct))

		order = '{"account":"%s","venue":"%s","stock":"%s","direction":"%s","orderType":"%s","price":%d,"qty":%d}' % (acct, venue, stock, order_dir, order_type, price * 100, qty)

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/stocks/%s/orders" % (venue, stock)
		res = Util.post(endpoint, order)

		if res:
			Util.log.info("Bought shares!")
			return res
		return None

	@staticmethod
	def cancel_order(venue, stock, order):
		Util.log.debug("Attempting to cancel order %d of stock %s in venue %s" % (order, stock, venue))

		endpoint = "https://api.stockfighter.io/ob/api/venues/%s/stocks/%s/orders/%d" % (venue, stock, order)
		res = Util.delete(endpoint)

		if res:
			Util.log.info("Order canceled!")
			return res
		return None

	def basic_action(self):
		Util.log.debug("Attempting to perform action".format())

		endpoint = "https://api.stockfighter.io/ob/api/".format()
		res = Util.get(endpoint, self.headers)

		if res:
			Util.log.info("Action succeeded!")
			return res
		return None

################################################################################
#                                                                              #
#              Methods for interacting with venues using accounts              #
#                                                                              #
################################################################################

class Account(object):

	def __init__(self, venue, acct):
		self.venue = venue
		self.acct = acct
		self.quotes_ticker = Ticker.new_venue_quotes_ticker(acct, venue)
		self.fills_ticker = Ticker.new_venue_fills_ticker(acct, venue)

	def listings(self):
		return Markets.get_venue_listings(self.venue)

	def book(self, stock):
		return Markets.get_orderbook(self.venue, stock)

	def quote(self, stock):
		return Markets.get_quote(self.venue, stock)

#	def status(self, order):
#		return Markets.get_order_status(self.venue, stock, order)

	def status(self, stock, order):
		return Markets.get_order_status(self.venue, stock, order)

	def all_statuses(self):
		return Markets.get_all_stock_orders_status(self.venue, self.acct)

	def statuses_for_stock(self, stock):
		return get_single_stock_orders_status(self.venue, self.acct, stock)

	def order(self, order_type, order_dir, stock, qty, price):
		return Markets.make_order(self.venue, self.acct, stock, order_type, order_dir, qty, price)

#	def cancel(self, order):
#		return Markets.cancel_order(self.venue, stock, order)

	def cancel(self, stock, order):
		return Markets.cancel_order(self.venue, stock, order)

################################################################################
#                                                                              #
#                Methods for user interaction with Stockfighter                #
#                                                                              #
################################################################################

class API(object):

	def __init__(self, api_key):
		self.api_key = api_key
		Util.headers = {'X-Starfighter-Authorization': api_key}

	def new_account(self, venue, acct):
		return Account(venue, acct)

	def alive(self, venue = None):
		return Util.dokidoki(venue)

	def make_verbose(self, verbose):
		if verbose: Util.log.setLevel(logging.DEBUG)
		else: Util.log.setLevel(logging.INFO)
