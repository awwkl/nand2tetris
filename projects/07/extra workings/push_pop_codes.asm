// pop local i

// @LCL
// D=M
// @i
// D=D + A     // D = LCL + i
// @addr
// M=D         // addr = LCL + i

// @SP
// M=M-1       // SP = SP - 1
// A=M
// D=M        // D = *SP

// @addr
// A=M
// M=D         // *addr = *SP


// push local i

// @LCL
// D=M
// @i
// A=D+A     // A = LCL + i = addr
// D=M       // D = *addr

// @SP
// A=M
// M=D         // *SP = *addr

// @SP
// M=M+1       // SP = SP - 1

