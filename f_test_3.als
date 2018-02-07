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
		(c.rateFood = Rancid || c.rateService = Poor => c.tip = Cheap) &&
		(c.rateService = Good => c.tip = Average) &&
		(c.rateFood = Delicious || c.rateService = Excellent => c.tip = Generous)
}

fact {
    all c : Customer | c.tip = Cheap && c.tip = Generous => c.tip = Average
}

assert asr_1 {
	some c: Customer | c.rateService = Good && not c.tip = Average
}

pred GenerousTip {
	some c : Customer | c.tip is mostly Generous
}

pred GenerousTipPoorService {
	some c : Customer | c.tip is mostly Generous && c.rateService is mostly Poor
}


run {} for 8 Int
