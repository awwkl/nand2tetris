  @SCREEN   // 16384
  D=A       // D = 16384
  @addr
  M=D       // addr = 16384

  @R0       // contains some input provided by user for number of rows
  D=M       // D = 50 (or whatever value R0 contains)
  @n
  M=D       // n = R0 = 50

  @i
  M=0       // i = 0

(LOOP)
  @i
  D=M       // D = i
  @n
  D=D-M     // D = i - n
  @END
  D;JGE     // if (i - n > 0) goto END

  @addr     // addr is a pointer variable
  A=M       // A = addr
  M=-1      // RAM[addr] = -1

  @32
  D=A       // D = 32
  @addr
  M=M+D     // addr = addr + 32

  @i
  M=M+1     // i = i + 1

  @LOOP
  0;JMP

(END)
  @END
  0;JMP



