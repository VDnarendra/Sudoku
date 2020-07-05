
# for i in range(9):
# 	for j in range(9):

# 		print(i,j,(i//3)*3+(j//3))

# for BOX in range(9):

# 	ibase = (BOX//3)*3
# 	jbase = (BOX%3)*3
# 	print('here',BOX,ibase,jbase)
# 00 01 02
# 10 11 12
# 20 21 22

i_off = 1
j_off = 1

for i in range(3):
	for j in range(3):
		print(i,j, (i*3)+(j))
