#!/usr/bin/env python

################################################################################
#                         Stockfighter API Test Script                         #
#             Makes sure API endpoints do what they're supposed to             #
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

def prettify(obj):
	return "\n" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

def main():
	# Stockfighter's new, so it might not be up all the time
	if not api.alive(): sys.exit()
	if not api.alive("TESTEX"): sys.exit()

	acct = api.new_account("TESTEX", "EXB123456")
	acct.fills_ticker.connect()

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

	settle = acct.order("market", "buy", stock["symbol"], 1017, 9500)
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

	acct.quotes_ticker.connect()

	try:
		while True: time.sleep(5)
	except KeyboardInterrupt:
		sys.exit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = "scriptname",
		description = "Makes sure API endpoints do what they're supposed to.",
		epilog = "Released under NP-OSL v3.0, (C) 2015 Mischif")

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

