module FASample
open FuzzyAlloy

abstract sig Color {}
one sig  Black, Brown, Blonde extends Color {}
abstract sig Race {}
one sig Asian, Europian extends Race {}

sig Person {
	hairColor:  Color -> one FuzzyValue,
	humanRace: Race -> one FuzzyValue
}

fact {
    	all p: Person | fuzzyIF [ fuzzyIS [fuzzyDotJoin [p, hairColor], Blonde],
						fuzzyNOT[fuzzyIS [fuzzyDotJoin[p, humanRace], Asian] ]]
}

fact {
    	fuzzyMAXSUM [hairColor, Person]
    fuzzyMAXSUM [humanRace, Person]
}

pred BlondeGuy {
one p: Person | fuzzyIS [ fuzzyDotJoin[p, hairColor], Blonde] in fuzzyMostly
}

fact {
one Person
}

run BlondeGuy for 7 Int
