grammar noisy;
options { language = Python3; }

spec: name
      predistributed?
      body;

// e.g. Noise_FOO(bar, baz)
name: 'Noise_' subname '(' args? '):' WS? EOL;
subname: (UPPER | LOWER)+;
args: arg (SEP arg)?;
arg: 'r'? key;

// e.g. <- s
//      ...
predistributed:
    (line EOL)+
    (WS?) '...' (WS?) EOL;

// e.g. <- s, ss, e, se
body: (line EOL)+;
line: WS? direction WS? token (SEP token)*;
token: key | operation;

key: 'e' | 's';
operation: key key;

direction: LEFTWARDS | RIGHTWARDS;

SEP: ',' WS?;
LEFTWARDS: '<-';
RIGHTWARDS: '->';
UPPER: ('A'..'Z');
LOWER: ('a'..'z');
EOL: '\n';
WS: [ \t\r]+ -> skip; // skip all whitespace
