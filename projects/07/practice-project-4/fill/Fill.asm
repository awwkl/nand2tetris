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

// currentWord = SCREEN

// (LOOP)
// 	if noKeyPressed
// 		goto Lighten
// 	else
// 		goto Blacken

// (Lighten)
//   currentWord = 0
//   if currentWord == SCREEN 	// start of screen
//     goto LOOP
// 	currentWord--
//	goto LOOP										// to restart loop

// (Blacken)
// 	currentWord = -1
// 	if currentWord == 24575			// end of screen
// 		goto LOOP
// 	currentWord++
// 	goto LOOP										// to restart loop

@SCREEN
D=A						// D = 16384
@currentWord
M=D						// currentWord = 16384

(LOOP)
	@KBD
	D=M					// D = scan code of keyboard

	@LIGHTEN
	D;JEQ				// if scan code == 0, goto LIGHTEN

	@BLACKEN
	0;JMP				// else goto BLACKEN

(BLACKEN)
	@currentWord
	A=M
	M=-1

	@currentWord
	D=M
	@24575
	D=D-A				// D = currentWord - 24575
	@LOOP
	D;JEQ				// goto LOOP if (currentWord == 24575)

	@currentWord
	M=M+1

	@LOOP
	0;JMP

(LIGHTEN)
	@currentWord
	A=M					// A = 16384
	M=0					// make M[16384] white

	@currentWord
	D=M
	@SCREEN
	D=D-A				// D = currentWord - 16384
	@LOOP
	D;JEQ				// goto LOOP if (currentWord == 16384)

	@currentWord
	M=M-1

	@LOOP
	0;JMP



