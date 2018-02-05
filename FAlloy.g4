grammar FAlloy;

specification : module? open* paragraph*;

module : 'module' name  ('['  ('exactly')? name  (',' ('exactly')? NUMBER)*    ']')?;

open : ('private')?  'open'  name  ('[' (ref (',' ref)*) ']')?  ('as' name)?;

paragraph :  factDecl | assertDecl | funDecl | cmdDecl | enumDecl | sigDecl;


factDecl : 'fact' name? block;

assertDecl : 'assert' name? block;
funDecl : ('private')? 'fun' (ref '.')? name '(' (decl (',' decl)*)? ')' ':' rootExpr block
        | ('private')? 'fun' (ref '.')? name '[' (decl (',' decl)*)? ']' ':' rootExpr block
        | ('private')? 'fun' (ref '.')? name                ':' rootExpr block
        | ('private')? 'pred' (ref '.')? name '(' (decl (',' decl)*)? ')' block
        | ('private')? 'pred' (ref '.')? name '[' (decl (',' decl)*)? ']' block
        | ('private')? 'pred' (ref '.')? name                block;

cmdDecl : (name ':')? ('run'|'check') (name|block) scope;

scope : 'for' NUMBER                   ('expect' ('0'|'1'))?
      | 'for' NUMBER 'but' (typescope (',' typescope)*) ('expect' ('0'|'1'))?
      | 'for'              (typescope (',' typescope)*) ('expect' ('0'|'1'))?
      |                                ('expect' ('0'|'1'))?;

typescope : ('exactly')? NUMBER (name|'int'|'seq');

sigDecl : sigQual* 'sig' (name (',' name)*) sigExt? '{' (declOrFuzzyDecl (',' declOrFuzzyDecl)*)? '}' block?;

enumDecl : 'enum' name '{' name  (',' name)*  '}';

sigQual : 'abstract' | 'lone' | 'one' | 'some' | 'private';

sigExt : 'extends' ref
       | 'in' ref ('+' ref)*;

rootExpr : letOrDeclExpr;
letOrDeclExpr : 'let' (letDecl (',' letDecl)*) blockOrBar | quant (decl (',' decl)*) blockOrBar | lExpr;
quant : 'all' | 'no' | 'some' | 'lone' | 'one' | 'sum';
// L = Logic
lExpr : '(' lExpr ')' | lExpr ('=>'|'implies') lExpr 'else' lExpr | lExpr lOpt lExpr | lCExpr;
lOpt : '||' | 'or' | '&&' | 'and' | '<=>' | 'iff' | '=>' | 'implies' ;
// C = Compare
lCExpr : lCExpr ('!'|'not')? cOp lCExpr | unHighOp lCExpr | binLogicExpr;
cOp : '=' | 'in' | '<' | '>' | '=<' | '>=';
unHighOp : '!' | 'not' | 'no' | 'some' | 'lone' | 'one' | 'set' | 'seq' | '#';

binLogicExpr : binLogicExpr otherBinOp binLogicExpr | binLogicExpr fuzzyCompareOp binLogicExpr | arrowExpr;
otherBinOp : '&' | '+' | '-' | '++' | '<:' | ':>'  | '<<' | '>>' | '>>>';
fuzzyCompareOp : 'is' fuzzyUnOp?;
fuzzyUnOp :  'none' | 'slightly' | 'half' | 'mostly' | 'fully';

arrowExpr : joinExpr | arrowExpr arrowOp arrowExpr;

joinExpr : joinExpr '.' joinExpr | joinExpr '[' (rootExpr (',' rootExpr)*)? ']' | expr;

expr : unLowOp expr
       |     NUMBER
       | '-' NUMBER
       | 'none'
       | 'iden'
       | 'univ'
       | 'Int'
       | 'seq/Int'
       | ('@')? name
       | block
       | '{' (decl (',' decl)*) blockOrBar '}';


unLowOp:  '~' | '*' | '^';

declOrFuzzyDecl : fuzzyDecl | decl;

decl : ('private')? ('disj')? (name (',' name)*) ':' ('disj')? rootExpr;

fuzzyDecl : ('private')? ('disj')? (name (',' name)*) ':' 'fuzzy' rootExpr;

letDecl : name '=' rootExpr;


binOp : '||' | 'or' | '&&' | 'and' | '&' | '<=>' | 'iff'
        | '=>' | 'implies' | '+' | '-' | '++' | '<:' | ':>' | '.' | '<<' | '>>' | '>>>';

arrowOp : ('some'|'one'|'lone'|'set')? '->' ('some'|'one'|'lone'|'set')?;





block : '{' rootExpr* '}';

blockOrBar : block
           | '|' rootExpr;

name : ('this' | ID) ('/' ID)*;
NUMBER: [0-9]+;
ID: [a-zA-Z_][a-zA-Z_0-9]*;
//number : '0' | '1' | '2' | '3' | '4' ;

ref : name | 'univ' | 'Int' | 'seq/Int';
