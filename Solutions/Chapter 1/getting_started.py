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
import argparse
from Stockfighter import API

def fill_callback(m):
	if m.is_text:
		try:
			msg = json.loads(m.data)
			api.log_info("Filled %d shares of order at $%s" % (msg["filled"], str(msg["price"] / 100.0)))
			api.log_debug("Full message:\n%s" % msg)
		except ValueError as e:
				api.log_err("Websocket message isn't JSON: %s" % m.data)
				pass
	else:
		api.log_err("Somehow got a binary message from the websocket")

def main(venue, acct):
	acct = api.new_account(venue, acct)
	acct.fills_ticker.set_callback(fill_callback)
	acct.fills_ticker.connect()

	listings = acct.listings()
	if not listings: sys.exit(api.log_err("Can't get listings for given venue"))

	order = acct.order("market", "buy", listings[0]["symbol"], 100, 5900)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = "scriptname",
		epilog = "Released under NP-OSL v3.0, (C) 2015 Mischif",
		description = "Stockfighter Chapter 1 Level 1 Solution.")

	parser.add_argument("apiKey",
		default = api_key,
		nargs = "?",
		metavar = "key",
		help = "Stockfighter API key")

	parser.add_argument("acct",
		metavar = "account",
		help = "Level account number")

	parser.add_argument("venue",
		help = "Level venue")

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

	if api.alive(): main(args.venue, args.acct)
	else: sys.exit("[!] APIs are not up")
