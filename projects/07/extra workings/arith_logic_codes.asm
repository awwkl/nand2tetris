// add (x + y)
@SP
M=M-1   // move SP up 1
A=M
D=M     // D = y
@SP
A=M-1   // A references x
M=M+D   // M = x + y

// sub (x - y)
@SP
M=M-1   // move SP up 1
A=M
D=M     // D = y
@SP
A=M-1   // A references x
M=M-D   // M = x - y

// neg (-y) need add 1 at the end
@SP
A=M-1
M=-M
M=M+1

// eq (x == y)
@SP
M=M-1   // move SP up
A=M
D=M     // D = y
@SP
A=M-1   // point A at x
D=M-D   // D = x - y
@EQUAL_0
D;JEQ
@SP
A=M-1
M=0
@DONE_0
0;JMP
(EQUAL_0)
@SP
A=M-1
M=-1
(DONE_0)

// gt (x == y)
@SP
M=M-1
A=M
D=M     // D = y
@SP
A=M-1
D=M-D   // D = x - y
@GREATER_1
D;JGT   // goto GREATER if x - y > 0
@SP
A=M-1
M=0
@DONE_1
(GREATER_1)
@SP
A=M-1
M=-1
(DONE_1)

// lt (x == y)
@SP
M=M-1
A=M
D=M     // D = y
@SP
A=M-1
D=M-D   // D = x - y
@LESSER_2
D;JLT   // goto LESSER if x - y > 0
@SP
A=M-1
M=0
@DONE_2
(LESSER_2)
@SP
A=M-1
M=-1
(DONE_2)

// and (x & y)
@SP
M=M-1
A=M
D=M     // D = y
@SP
A=M-1
M=M&D   // M = x & y

// or (x | y)
@SP
M=M-1
A=M
D=M     // D = y
@SP
A=M-1
M=M|D   // M = x | y

// not (!y)
// bit-wise NOT need to add 1 at the end
@SP
A=M-1
M=!M
M=M+1