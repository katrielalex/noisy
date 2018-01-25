grammar noisy;
options { language = Python3; }

spec: name ':\n'
      line+;

name: 'Noise_' subname '()';
subname: UPPER+;

line: WS? direction (token sep)? token EOL;
sep: ',' WS?;
token: key | operation;

key: 'e';
operation: key key;

direction: LEFTWARDS | RIGHTWARDS;

LEFTWARDS: '<-';
RIGHTWARDS: '->';
UPPER: ('A'..'Z');
EOL: '\n';
WS: [ \t\r]+ -> skip; // skip all whitespace
