  @R0
  D=M
  @n
  M=D   // n = R0

  @i
  M=1   // i = 1
  @sum
  M=0   // sum = 0

(LOOP)
  @i
  D=M     // D = i
  @n
  D=D-M   // D = i - n
  @STOP
  D;JGT   // goto STOP if i - n > 0 (i > n)

  @i
  D=M     // D = i
  @sum
  M=M+D   // sum = sum + i
  @i
  M=M+1   // i = i + 1
  
  @LOOP
  0;JMP

(STOP)
  @sum
  D=M   // D = sum
  @R1
  M=D   // R1 = D = sum

(END)
  @END
  0;JMP
