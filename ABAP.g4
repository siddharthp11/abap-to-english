grammar ABAP;

/*
Lexer Rules
 */

/*
Fragments for lettters
 */
fragment UPPERCASE : [A-Z];
fragment LOWERCASE : [a-z];
fragment DIGIT : [0-9];
fragment A:('a'|'A');
fragment B:('b'|'B');
fragment C:('c'|'C');
fragment D:('d'|'D');
fragment E:('e'|'E');
fragment F:('f'|'F');
fragment G:('g'|'G');
fragment H:('h'|'H');
fragment I:('i'|'I');
fragment J:('j'|'J');
fragment K:('k'|'K');
fragment L:('l'|'L');
fragment M:('m'|'M');
fragment N:('n'|'N');
fragment O:('o'|'O');
fragment P:('p'|'P');
fragment Q:('q'|'Q');
fragment R:('r'|'R');
fragment S:('s'|'S');
fragment T:('t'|'T');
fragment U:('u'|'U');
fragment V:('v'|'V');
fragment W:('w'|'W');
fragment X:('x'|'X');
fragment Y:('y'|'Y');
fragment Z:('z'|'Z');

/*
WHITESPACE
 */
WS:                 [ \t\r\n\u000C]+ -> channel(HIDDEN);

/*
Separators
 */
DOT:                '.';
OPEN_PAR:           '(';
CLOSE_PAR:          ')';
OPEN_CURLY:         '{';
OPEN_SQUARE:        '[';
CLOSE_SQUARE:       ']';
COMMA:              ',';
UNDERSCORE:         '_';

/*
Operators
 */
ASSIGN:             '=';
STAR:               '*';
PLUS:               '+';
MINUS:              '-';
DIV:                '/';
ADD_ASSIGN:         '+=';
SUB_ASSIGN:         '-=';
MUL_ASSIGN:         '*=';
DIV_ASSIGN:         '/=';
COLON:              ':';
MOD:                 M O D;
AND:                 A N D;
OR:                  O R;
NOT:                N O T;
LT:                 '<';
LT_EQ:              '<=';
GT:                 '>';
GT_EQ:              '>=';
NOT_EQ:             '<>';
/*
Other
 */
ARROW:        '->';
DOUBLEARROW:           '=>';
NEWLINE:'\n';

/*
Keywords
 */


ABSTRACT:A B S T R A C T ;
ACTIVATION: A C T I V A T I O N ;
ALIAS: A L I A S;
ALL: A L L ;
ASSIGNING: A S S I G N I N G ;
AT: A T ;
ATSEL:A T S E L E C T I O N '-' S C R E E N ;
BEGIN: B E G I N ;
BYTEFIELD: X;
CATCH: C A T C H ;
CHANGING: C H A N G I N G ;
CLASS: C L A S S;
CLASSDATA: CLASS'-'DATA;
CLASSMETHODS: CLASS'-'METHODS;
CLEAR: C L E A R;
COMPARING: C O M P A R I N G ;
COMPONENTS: C O M P O N E N T S;
CORRESPONDING: C O R R E S P O N D I N G ;
DATA: D A T A;
DECIMALS: D E C I M A L S;
DEFAULT: D E F A U L T ;
DEFINITION: D E F I N I T I O N;
DISPLAY: D I S P L A Y ;DO: D O ;
ELSE: E L S E ;
ELSEIF: E L S E I F ;
EMPTY: E M P T Y ;
END: E N D ;
ENDCLASS: E N D C L A S S;
ENDDO: E N D D O ;
ENDIF: E N D I F ;
ENDLOOP: E N D L O O P ;
ENDMETHOD: E N D M E T H O D;
ENDPAGE:E N D '-' O F '-' P A G E ;
ENDSEL:E N D '-' O F '-' S E L E C T I O N ;
ENDTRY: E N D T R Y ;
ENDWHILE: E N D W H I L E ;
EVENT: E V E N T ;
EXCEPTION: E X C E P T I O N ;
EXPORTING: E X P O R T I N G ;
FAIL:F A I L ;
FIELDS: F I E L D S ;
FIELDSYMBOL:F I E L D'-'S Y M B O L;
FINAL: F I N A L;
FLOAT: F;
FOR: F O R ;
FROM: F R O M ;
HANDLER: H A N D L E R ;
IF: I F ;
IGNORE:I G N O R E ;
IMPLEMENTATION: I M P L E M E N T A T I O N;
IMPORTING: I M P O R T I N G ;
INDEX: I N D E X ;
INIT:I N I T I A L I S A T I O N ;
INITIALSIZE:I N I T I A L' 'S I Z E;
INSTANCES: I N S T A N C E S ;
INTEGER: I;
INTO: I N T O ;
ISINITIAL: I S ' ' I N I T I A L;
KEY:K E Y;
LENGTH: L E N G T H;
LIKE: L I K E;
LOOP: L O O P ;
MESSAGE: M E S S A G E ;
METHOD: M E T H O D;
METHODS: M E T H O D S;
NO: N O ;
NONUNIQUE: N O N '-' U N I Q U E ;
OF:O F;
OPTIONAL:O P T I O N A L;
PACKED: P;
RAISING: R A I S I N G ;
READ: R E A D;
READONLY: R E A D'-'O N L Y;
REF: R E F' 'T O;
REFERENCE:R E F E R E N C E;
REPORT: R E P O R T;
SECTION: S E C T I O N;
SELECT: S E L E C T ;
SET: S E T ;
STARTSEL:S T A R T '-' O F '-' S E L E C T I O N ;
STRING: S T R I N G;
TABLE: T A B L E;
TEXTFIELD: C;
TIMES: T I M E S ;
TO: T O ;
TOPPAGE:T O P '-' O F '-' P A G E ;
TRANSPORTING: T R A N S P O R T I N G;
TRY: T R Y ;
TYPE: T Y P E;
TYPES: T Y P E S ;
UNIQUE: U N I Q U E ;
USING: U S I N G ;
VALUE: V A L U E;
WHERE: W H E R E ;
WHILE: W H I L E ;
WITH: W I T H;



/*
Literals
 */
BOOL_LITERAL:       'true'
            |       'false'
            ;
DECIMAL_LITERAL: DIGIT+ (DOT DIGIT+)?;
STRING_LITERAL:    ( '\''|'`') (~['\\\r\n])* ( '\''|'`');


/*
Identifiers
 */

IDENTIFIER: [A-Za-z]([0-9A-Za-z_-]*[0-9A-Za-z])?;




/*
                    PARSER
 */



/*
Program
 */
program: programName (block|statement)* EOF;

programName: REPORT id DOT ;
/*
Block
 */
block: 
        classBlock
        |eventBlock;
/*
Class
 */
classBlock: classHeader classBody;

classHeader: CLASS id (IMPLEMENTATION|DEFINITION) DOT;

classBody: (sectionBlock|methodBlock)* ENDCLASS DOT;
/*
Section
 */
sectionBlock: sectionHeader statementList;

sectionHeader: id SECTION DOT;
/*
Method
 */
methodBlock: methodHeader statementList ENDMETHOD DOT;

methodHeader: METHOD id DOT;

/*
Event
 */
eventBlock: eventHeader DOT statementList;

eventHeader: (STARTSEL| INIT| ATSEL|TOPPAGE|ENDPAGE|ENDSEL);


/*
statementList
*/
statementList: statement+;

statement: expression DOT
           |keywordStatement DOT
           |blockStatement ;

/*
Expressions
*/
expressions: expression (COMMA? expression)* ;

expression: primary
            |methodCall
            |OPEN_PAR expression CLOSE_PAR
            | expression bop=('=>'|'->') methodCall
            | prefix=NOT expression
            | expression bop=(STAR|DIV|MOD) expression
            | expression bop=(PLUS|MINUS) expression
            | expression ('<' '<' | '>' '>' '>' | '>' '>') expression
            | expression bop=(LT_EQ | GT_EQ | LT | GT|NOT_EQ) expression
            | expression bop=(ASSIGN | NOT) expression
            | expression bop=AND expression
            | expression bop=OR expression
            | <assoc=right> expression bop=(ASSIGN | ADD_ASSIGN | SUB_ASSIGN |MUL_ASSIGN | DIV_ASSIGN) expression
            
            ;

methodCall:  (id|DISPLAY ) '(' (expressions|settings)? ')';

inline: (DATA|CLASSDATA) '(' id ')'
        |TABLE? '@' id;

cast: fieldSymbol '-' id;

primary: id
          |literal
          |inline
          |cast
          ;

/*
block statements
*/
blockStatement: ifBlock
                |tryBlock
                |whileBlock
                |doBlock
                |loopBlock

                ;

/*
if
 */

ifBlock: if_ elif_* else_? ENDIF DOT;

if_: IF expression DOT statementList;

elif_: ELSEIF expression DOT statementList;

else_: ELSE DOT statementList;
/*
try
 */
tryBlock: try_ catch_ ENDTRY DOT;

try_: TRY DOT statementList;

catch_: CATCH expression DOT statementList;
/*
while
 */
whileBlock: while_ ENDWHILE DOT;

while_: WHILE expression DOT statementList;
/*
do
 */
doBlock: do_ ENDDO DOT;

do_ : DO times? DOT statementList;

times: expression TIMES;

/*
loop
*/
loopBlock: loop ENDLOOP DOT;

loop: LOOP AT declaration DOT statementList;




/*
keywordStatement: data name() settings...
*/
keywordStatement: keywords declaration
                  |keywords COLON declarations
                  ;

keywords : (DATA|CLASSDATA|METHODS|CLASSMETHODS|READ|TABLE|SET|HANDLER|SELECT|MESSAGE|CLEAR|TYPES)+;

declarations: declaration (COMMA declaration)*;

declaration: subject expression? settings?;

subject:(id|expressions|STAR|structure);
/*
structure
 */

structure: beginStructure  structureItems endStructure;

structureItems: (declaration|structure) (COMMA (declaration|structure))*;

beginStructure: BEGIN OF id COMMA;

endStructure: COMMA END OF id;
/*
settings keyword flags and keyword value pairs
*/

settings: setting setting*;

setting: flag
        |simpleSetting
        |type
        |value
        |for_
        |with
        |where
        |from
        |using
        |importExportChanging
        |index
        |transporting
        |comparing
        |reference
        |raising
        |assigning
        |into
        |display
        |using
        ;

flag: READONLY
      |ISINITIAL   
      |ABSTRACT
      |FINAL
      |IGNORE
      |FAIL
      |EMPTY
      |UNIQUE
      |NONUNIQUE
      |DEFAULT
      |TABLE
      ;

simpleSetting: (DECIMALS|LENGTH|INITIALSIZE|DEFAULT) (flag|expression);

value: VALUE expression
              ;
/*
Type
 */
type: pointer dataType
      |pointer literal ;

pointer: (TYPE|LIKE) REF?;

dataType: primitives
         |table
         |classOrInterface 
         ;

classOrInterface: id;

primitives: STRING
            |TEXTFIELD
            |BYTEFIELD
            |INTEGER
            |FLOAT
            |PACKED;

table: id? TABLE OF dataType ;

/*
import export changing
 */
importExportChanging:(IMPORTING|EXPORTING|CHANGING) (params|expressions);

params: param+;
param: id type? (OPTIONAL|(DEFAULT literal))?;

/*
with
 */
with: WITH keytype? key
      |WITH expressions  
      ;
keytype: (flag|id)+;

key: KEY id? alias? components?;

alias: ALIAS id;

components: COMPONENTS? expressions;

/*
index
 */

index: INDEX id;

/*
Raising
 */

raising: RAISING EXCEPTION;


/*
from and to
 */
from: FROM id;

to: TO id;
/*
where
 */
where: WHERE (expression);

/*
Using
 */
using: USING (key);

/*
result 
*/
into: INTO (CORRESPONDING FIELDS OF)? expression transporting?;

assigning: ASSIGNING fieldSymbol;

reference: REFERENCE into;

comparing: COMPARING transportObjects;

transporting: TRANSPORTING transportObjects;

transportObjects: (expressions|ALL FIELDS|NO FIELDS);

/*
field symbol
 */
fieldSymbol:  FIELDSYMBOL? OPEN_PAR? '<'id'>' CLOSE_PAR?;

/*
for
 */
for_:   FOR (
            EVENT id OF id
            |(expression| ALL INSTANCES) (ACTIVATION expression)?
            );
display: DISPLAY type;
/*
Literals
*/
literal: stringLiteral
         |booleanLiteral
         |numericLiteral;

stringLiteral: STRING_LITERAL;

numericLiteral: DECIMAL_LITERAL;

booleanLiteral: BOOL_LITERAL;

/*
Identifiers
*/
id:  (
    IDENTIFIER
    |passType OPEN_PAR id CLOSE_PAR
    );

passType: VALUE|REFERENCE;




/*
Arrows
*/
arrow:(ARROW|DOUBLEARROW);














