// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// pseudocode
// n = R0;          // n will be repeated added into product 
// counter = R1;    // counter is used as counter
// product = 0;

// while (counter > 0) {
//   product += n;
//   counter--;
// }

  @R0
  D=M
  @n
  M=D   // n = R0

  @R1
  D=M
  @counter
  M=D   // counter = R1

  @product
  M=0   // product = 0

(LOOP)
  @counter
  D=M       // D = counter
  @STOP
  D;JEQ     // goto STOP if (counter == 0)

  @n
  D=M       // D = n
  @product
  M=M+D     // product = product + n

  @counter
  M=M-1     // counter = counter - 1

  @LOOP
  0;JMP

(STOP)
  @product
  D=M
  @R2
  M=D       // R2 = product

(END)
  @END
  0;JMP

