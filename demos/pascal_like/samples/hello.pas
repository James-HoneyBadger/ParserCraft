(* Hello World — Pascal-Like via ParserCraft
   Demonstrates basic variable assignment and arithmetic.
   Run with: parsercraft repl configs/examples/pascal_like.yaml *)

PROGRAM HelloWorld;

VAR
  greeting : STRING;
  count     : INTEGER;
  message   : STRING;

BEGIN
  greeting := 'Hello';
  count    := 42;
  message  := 'ParserCraft Pascal demo';

  WriteLn(greeting, ', World!');
  WriteLn('Count = ', count);
  WriteLn('Message: ', message);
END.
