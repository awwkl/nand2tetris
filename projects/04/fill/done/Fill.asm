// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

  @SCREEN
  D=A         // D = 16384
  @currentPixel
  M=D         // currentPixel = 16384

(LOOP)        // currentPixel always 16384 to 24575
  @KBD
  D=M         // D = scan code from keyboard
  
  @NOKEYPRESSED
  D;JEQ       // if (scanCode == 0), no key is pressed
  
  @KEYPRESSED
  0;JMP       // else goto KEYPRESSED

(KEYPRESSED)
  @currentPixel
  A=M         // A = currentPixel = 16384 e.g.
  M=-1        // M[16384] = -1

  @currentPixel
  D=M
  @24575
  D=D-A       // D = currentPixel - 24575
  @LOOP
  D;JEQ       // if (currentPixel == 24575) goto LOOP

  @currentPixel
  M=M+1       // currentPixel += 1

  @LOOP
  0;JMP

(NOKEYPRESSED)
  @currentPixel
  A=M         // A = currentPixel = 16384 e.g.
  M=0         // M[16384] = 0

  @currentPixel
  D=M
  @SCREEN
  D=D-A       // D = currentPixel - 16384
  @LOOP
  D;JEQ       // if (currentPixel == 16384) goto LOOP

  @currentPixel
  M=M-1       // currentPixel -= 1

  @LOOP
  0;JMP