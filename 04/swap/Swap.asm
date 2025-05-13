//update all the memory registers to the first one
@R14
D = M
@R1
M = D
@R3
M = D
@R5
M = D
//update all the value registers to the first one
A = D
D = M
@0
M = D
@2
M = D
@4
M = D
@i
M = 1
(LOOP)
	//if reach the End of the arry
	@R15
	D = M
	@i
	D = D-M
	@SWAP
	D;JEQ
	// check the next value in the arry
	@R5
	M = M+1
	A = M
	D = M
	@R4
	M = D
	//check the min and update it
	@R0
	D = D-M
	@UPDATEMIN
	D;JLT
	@R4
	D = M
	@R2
	D = D-M
	@UPDATEMAX
	D;JGT
(CONT)
	@i
	M = M+1
	@LOOP
	0;JMP
(UPDATEMIN)
	@R4
	D = M
	@R0
	M = D
	@R5
	D = M
	@R1
	M = D
	@CONT
	0;JMP
(UPDATEMAX)
	@R4
	D = M
	@R2
	M = D
	@R5
	D = M
	@R3
	M = D
	@CONT
	0;JMP
(SWAP)
	@R0
	D = M
	@R3
	A = M
	M = D
	@R2
	D = M
	@R1
	A = M
	M = D
(END)
	@END
	0;JMP

