grammar FAlloy;

specification : module? open* paragraph*;

module : 'module' name  ('['  ('exactly')? name  (',' ('exactly')? NUMBER)*    ']')?;

/*REMINDER: CHANGED ref,*/
open : ('private')?  'open'  name  ('[' (ref (',' ref)*) ']')?  ('as' name)?;

paragraph : factDecl | assertDecl | funDecl | cmdDecl | enumDecl | sigDecl;

factDecl : 'fact' name? block;

assertDecl : 'assert' name? block;
/*REMINDER: CHANGED decl,*/
funDecl : ('private')? 'fun' (ref '.')? name '(' (decl (',' decl)*)? ')' ':' expr block
        | ('private')? 'fun' (ref '.')? name '[' (decl (',' decl)*)? ']' ':' expr block
        | ('private')? 'fun' (ref '.')? name                ':' expr block
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

expr : 'let' (letDecl (',' letDecl)*) blockOrBar
       | quant (decl (',' decl)*)    blockOrBar
       | unOp expr
       | fuzzyUnOp expr
       | expr fuzzyCompareOp expr
       | expr binOp expr
       | expr arrowOp expr
       | expr ('!'|'not')? compareOp expr
       | expr ('=>'|'implies') expr 'else' expr
       | expr '[' (expr (',' expr)*)? ']'
       |     NUMBER
       | '-' NUMBER
       | 'none'
       | 'iden'
       | 'univ'
       | 'Int'
       | 'seq/Int'
       | '(' expr ')'
       | ('@')? name
       | block
       | '{' (decl (',' decl)*) blockOrBar '}';

declOrFuzzyDecl : fuzzyDecl | decl;

decl : ('private')? ('disj')? (name (',' name)*) ':' ('disj')? expr;

fuzzyDecl : ('private')? ('disj')? (name (',' name)*) ':' 'fuzzy' expr;

letDecl : name '=' expr;

quant : 'all' | 'no' | 'some' | 'lone' | 'one' | 'sum';

fuzzyUnOp :  'none' | 'slightly' | 'half' | 'mostly' | 'fully';

fuzzyCompareOp : 'is';

binOp : '||' | 'or' | '&&' | 'and' | '&' | '<=>' | 'iff'
        | '=>' | 'implies' | '+' | '-' | '++' | '<:' | ':>' | '.' | '<<' | '>>' | '>>>';

arrowOp : ('some'|'one'|'lone'|'set')? '->' ('some'|'one'|'lone'|'set')?;

compareOp : '=' | 'in' | '<' | '>' | '=<' | '>=';

unOp : '!' | 'not' | 'no' | 'some' | 'lone' | 'one' | 'set' | 'seq' | '#' | '~' | '*' | '^';

block : '{' expr* '}';

blockOrBar : block
           | '|' expr;

name : ('this' | ID) ('/' ID)*;
NUMBER: [0-9]+;
ID: [a-zA-Z_][a-zA-Z_0-9]*;
//number : '0' | '1' | '2' | '3' | '4' ;

ref : name | 'univ' | 'Int' | 'seq/Int';
