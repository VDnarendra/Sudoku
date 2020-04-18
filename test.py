
# for i in range(9):
# 	for j in range(9):

# 		print(i,j,(i//3)*3+(j//3))

for BOX in range(9):

	ibase = (BOX//3)*3
	jbase = (BOX%3)*3
	print('here',BOX,ibase,jbase)
	for i in range(3):
		for j in range(3):
			print(ibase+i,jbase+j)