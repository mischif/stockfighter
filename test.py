#!/usr/bin/env python

################################################################################
#                           Put The Script Name Here                           #
#                Put short description of script's purpose here                #
#                               (C) 2015 Mischif                               #
#       Released under version 3.0 of the Non-Profit Open Source License       #
################################################################################

api_key = "You should probably put a persistent API key here"
__version__ = "1.0.0"

import sys
import json
import time
import argparse
from Stockfighter import API
from ws4py.manager import WebSocketManager

def prettify(obj):
	return "\n" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

def main():
	# Stockfighter's new, so it might not be up all the time
	if not api.alive(): sys.exit()
	if not api.alive("TESTEX"): sys.exit()

	acct = api.new_account("TESTEX", "EXB123456")

	listings = acct.listings()
	if not listings:
		sys.exit("[-] Can't get listings of always-up exchange; is it really up?")
	elif not len(listings):
		sys.exit("[-] Even the default stock wasn't listed; is it really up?")
	else:
		print "TESTEX Listings: {}".format(prettify(listings))

	stock = listings[0]

	book = acct.book(stock["symbol"])
	if not book:
		sys.exit("[-] Couldn't get orderbook")
	else:
		print "Orderbook for {} on TESTEX: {}".format(stock["symbol"], prettify(book))

	settle = acct.order("limit", "buy", stock["symbol"], 1017, 95)
	if not settle:
		sys.exit("[-] Order not placed")
	else:
		print "Result after ordering {}: {}".format(stock["symbol"], prettify(settle))

	quote = acct.quote(stock["symbol"])
	if not quote:
		sys.exit("[-] Couldn't get quote on {}".format(stock["symbol"]))
	else:
		print "Quote for {} on TESTEX: {}".format(stock["symbol"], prettify(quote))

	ccl = acct.cancel(stock["symbol"], settle["id"])
	if not ccl:
		sys.exit("[-] Couldn't cancel order")
	else:
		print "Result after canceling order: {}".format(prettify(ccl))

	wsm = WebSocketManager()

	try:
		wsm.start()
		acct.quotes_ticker.add_manager(wsm.add)
		acct.fills_ticker.add_manager(wsm.add)
		acct.quotes_ticker.connect()
		acct.fills_ticker.connect()

		while True:
			for ws in wsm.websockets.itervalues():
				if not ws.terminated:
					break
			else:
				break
			time.sleep(1)
	except KeyboardInterrupt:
		wsm.close_all()
		wsm.stop()
		wsm.join()

	sys.exit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = "scriptname",
		epilog = "Released under NP-OSL v3.0, (C) 201X Mischif",
		description = "Short description of script's purpose.")

	parser.add_argument("apiKey",
		default = api_key,
		nargs = "?",
		metavar = "key",
		help = "Stockfighter API key")

	parser.add_argument("-v", "--verbose",
		action = "store_true",
		help="Make the program tell you more about what it's doing")

	parser.add_argument("--version",
		action = "version",
		version = "%(prog)s {}".format(__version__))

	args = parser.parse_args()

	if len(args.apiKey) != 40:
		sys.exit("[!] Where's your API key?")
	else:
		api = API(args.apiKey)
		api.make_verbose(args.verbose)
	main()

