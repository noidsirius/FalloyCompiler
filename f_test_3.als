module FASample_Food
open FuzzyAlloy

abstract sig FoodQuality {}
one sig Rancid, Delicious extends FoodQuality {}
abstract sig ServiceQuality {}
one sig Poor, Good, Excellent extends ServiceQuality {}
abstract sig Tip {}
one sig Cheap, Average, Generous extends Tip {}


sig Customer {
	rateFood: fuzzy FoodQuality,
	rateService: fuzzy ServiceQuality,
	tip: fuzzy Tip
}

fact {
	all c: Customer |
		((c.rateFood is Rancid || c.rateService is Poor => c.tip is Cheap) &&
		(c.rateService is Good => c.tip is Average) &&
		(c.rateFood is Delicious || c.rateService is Excellent => c.tip is Generous)) || c.rateFood is Rancid
}

assert asr_1 {
	some c: Customer | c.rateService is Good && not c.tip is Average
}

pred GenerousTip {
	some c : Customer | c.tip is mostly Generous
}


run {} for 3
