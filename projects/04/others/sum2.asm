  @i
  M=1
  @sum
  M=0

(LOOP)
  @i
  D=M     // D=i
  @100
  D=D-A   // D=i-100
  @END
  D;JGT   // if (i-100 > 0) Jump
  @i
  D=M     // D=i
  @sum
  M=M+D   // sum=sum+i
  @i
  M=M+1   // i=i+1
  @LOOP
  0;JMP

(END)
  @END
  0;JMP
