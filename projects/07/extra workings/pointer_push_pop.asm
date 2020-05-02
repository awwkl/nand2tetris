// pop pointer 0

@SP
M=M-1
A=M
D=M     // D = popped value

@THIS
M=D

// push pointer 0
@THIS
D=M

@SP
A=M
M=D     // push D onto stack

@SP
M=M+1