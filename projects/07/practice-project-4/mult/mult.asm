// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// pseudocode

// counter = R0
// num = R1
// product = 0

// while (counter > 0) {
//   product = product + num
//   counter = counter - 1
// }

// R2 = product

@R0
D=M
@counter
M=D         // counter = R0

@R1
D=M
@num
M=D         // num = R1

@product
M=0         // product = 0

(LOOP)
  @counter
  D=M       // D = counter
  @STOP
  D;JEQ

  @num
  D=M
  @product
  M=M+D     // product = product + num

  @counter
  M=M-1     // counter = counter - 1

  @LOOP
  0;JMP     // goto LOOP

(STOP)
  @product
  D=M
  @R2
  M=D

(END)
  @END
  0;JMP     // goto END (keep repeating)