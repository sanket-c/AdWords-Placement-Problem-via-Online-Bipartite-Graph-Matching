import sys
import math
import csv
import random
random.seed(0)

bidders_budget = {}
ad_bid_for_query = {}

def loadBidders():
	filename = "bidder_dataset.csv"
	with open(filename, 'rb') as bidders_files:
		bidders = csv.DictReader(bidders_files, delimiter = ",")
		for row in bidders:
			if bidders_budget.get(row['Advertiser']) == None:
				bidders_budget[row['Advertiser']] = float(row['Budget'])
			if ad_bid_for_query.get(row['Keyword']) == None:
				advertiser_bid = {row['Advertiser'] : float(row['Bid Value'])}
				ad_bid_for_query[row['Keyword']] = advertiser_bid
			else:
				advertiser_bid = ad_bid_for_query.get(row['Keyword'])
				advertiser_bid[row['Advertiser']] = float(row['Bid Value'])
				ad_bid_for_query[row['Keyword']] = advertiser_bid

def loadQueries():
	filename = "queries.txt"
	with open(filename, 'rb') as queries_files:
		queries = queries_files.read().split("\n")
	return queries

def getOptimalRevenue():
	opt_revenue = 0.0
	for bidder in bidders_budget.keys():
		opt_revenue = opt_revenue + bidders_budget.get(bidder)
	return opt_revenue
	
def greedyAlgorithm(queries):
	revenue = 0.0
	bidder_spent_budget = bidders_budget.copy()
	for query in queries:
		if ad_bid_for_query.get(query) != None:
			is_bidder_available = False
			advertiser_bid = ad_bid_for_query.get(query)
			for advertiser in  advertiser_bid.keys():
				if bidder_spent_budget.get(advertiser) > 0:
					is_bidder_available = True
					break
			if not is_bidder_available:
				continue
			max_bidder = -1
			max_bid = -1
			for advertiser in  advertiser_bid.keys():
				if bidder_spent_budget.get(advertiser) >= advertiser_bid.get(advertiser):
					if max_bid < advertiser_bid.get(advertiser):
						max_bidder = advertiser
						max_bid = advertiser_bid.get(advertiser)
					elif max_bid == advertiser_bid.get(advertiser):
						if int(max_bidder) > int(advertiser):
							max_bidder = advertiser
							max_bid = advertiser_bid.get(advertiser)
			if max_bidder == -1 or max_bid == -1:
				continue
			revenue = revenue + max_bid
			budget = bidder_spent_budget.get(max_bidder)
			bidder_spent_budget[max_bidder] = budget - max_bid
	return revenue

def greedy(queries):
	revenue = greedyAlgorithm(queries)
	totalRevenue = 0.0
	for i in range(100):
		random.shuffle(queries)
		r = greedyAlgorithm(queries)
		totalRevenue = totalRevenue + r
	print str(round(revenue, 2))
	mean = totalRevenue / 100
	opt = getOptimalRevenue()
	cmp_ratio = mean / opt
	print str(round(cmp_ratio, 2))
	
def balanceAlgorithm(queries):
	revenue = 0.0
	bidder_spent_budget = bidders_budget.copy()
	for query in queries:
		if ad_bid_for_query.get(query) != None:
			is_bidder_available = False
			advertiser_bid = ad_bid_for_query.get(query)
			for advertiser in  advertiser_bid.keys():
				if bidder_spent_budget.get(advertiser) > 0:
					is_bidder_available = True
					break
			if not is_bidder_available:
				continue
			max_bidder = -1
			max_budget = -1
			for advertiser in  advertiser_bid.keys():
				if bidder_spent_budget.get(advertiser) >= advertiser_bid.get(advertiser):
					if max_budget < bidder_spent_budget.get(advertiser):
						max_bidder = advertiser
						max_budget = bidder_spent_budget.get(advertiser)
					elif max_budget == bidder_spent_budget.get(advertiser):
						if int(max_bidder) > int(advertiser):
							max_bidder = advertiser
							max_budget = bidder_spent_budget.get(advertiser)
			if max_bidder == -1 or max_budget == -1:
				continue
			revenue = revenue + advertiser_bid.get(max_bidder)
			budget = bidder_spent_budget.get(max_bidder)
			bidder_spent_budget[max_bidder] = budget - advertiser_bid.get(max_bidder)
	return revenue

def balance(queries):
	revenue = balanceAlgorithm(queries)
	totalRevenue = 0.0
	for i in range(100):
		random.shuffle(queries)
		r = balanceAlgorithm(queries)
		totalRevenue = totalRevenue + r
	print str(round(revenue, 2))
	mean = totalRevenue / 100
	opt = getOptimalRevenue()
	cmp_ratio = mean / opt
	print str(round(cmp_ratio, 2))
	
def mssvAlgorithm(queries):
	revenue = 0.0
	bidder_spent_budget = bidders_budget.copy()
	for query in queries:
		if ad_bid_for_query.get(query) != None:
			is_bidder_available = False
			advertiser_bid = ad_bid_for_query.get(query)
			for advertiser in  advertiser_bid.keys():
				if bidder_spent_budget.get(advertiser) > 0:
					is_bidder_available = True
					break
			if not is_bidder_available:
				continue
			max_bidder = -1
			max_bid = -1
			for advertiser in  advertiser_bid.keys():
				if bidder_spent_budget.get(advertiser) >= advertiser_bid.get(advertiser):
					spent_budget = (bidders_budget.get(advertiser) - bidder_spent_budget.get(advertiser))/bidders_budget.get(advertiser)
					function = 1 - math.exp(spent_budget - 1)
					bid = advertiser_bid.get(advertiser) * function
					if max_bid < bid:
						max_bidder = advertiser
						max_bid = bid
					elif max_bid == bid:
						if int(max_bidder) > int(advertiser):
							max_bidder = advertiser
							max_bid = bid
			if max_bidder == -1 or max_bid == -1:
				continue
			revenue = revenue + advertiser_bid.get(max_bidder)
			budget = bidder_spent_budget.get(max_bidder)
			bidder_spent_budget[max_bidder] = budget - advertiser_bid.get(max_bidder)
	return revenue

def mssv(queries):
	revenue = mssvAlgorithm(queries)
	totalRevenue = 0.0
	for i in range(100):
		random.shuffle(queries)
		r = mssvAlgorithm(queries)
		totalRevenue = totalRevenue + r
	print str(round(revenue, 2))
	mean = totalRevenue / 100
	opt = getOptimalRevenue()
	cmp_ratio = mean / opt
	print str(round(cmp_ratio, 2))
	
def main(args):
	if len(args) == 1:
		loadBidders()
		queries = loadQueries()
		if args[0] == "greedy":
			greedy(queries)
		elif args[0] == "balance":
			balance(queries)
		elif args[0] == "mssv":
			mssv(queries)
		else:
			print "Error in argument name : " + args[0]
	else:
		print "Error in number of arguments."

if __name__ == "__main__":
	main(sys.argv[1:])