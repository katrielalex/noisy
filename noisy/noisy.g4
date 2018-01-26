grammar noisy;
options { language = Python3; }

spec: name
      predistributed?
      body;

// e.g. Noise_FOO(bar, baz)
name: 'Noise_' subname '(' args? '):' WS? EOL;
subname: (UPPER | LOWER)+;
args: arg (SEP arg)*;
arg: RESPONDER? key;

// e.g. <- s
//      ...
predistributed:
    preline EOL
    (preline EOL)?
    (WS?) '...' (WS?) EOL;
preline: WS? direction WS? key (SEP key)*;

// e.g. <- s, ss, e, se
body: (bodyline EOL)+;
bodyline: WS? direction WS? token (SEP token)*;
token: key | operation;

key: 'e' | 's';
operation: key key;

direction: LEFTWARDS | RIGHTWARDS;

RESPONDER: 'r';
SEP: ',' WS?;
LEFTWARDS: '<-';
RIGHTWARDS: '->';
UPPER: ('A'..'Z');
LOWER: ('a'..'z');
EOL: '\n';
WS: [ \t\r]+ -> skip; // skip all whitespace
