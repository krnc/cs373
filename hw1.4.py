colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[0,-1],[1,0],[0,1]]

sensor_right = 1

p_move = .99



def show(p):
	for i in range(len(p)):
		print p[i]

pDistribution = 1./len(colors[0]) * len(colors)
p = [len(colors[0]) * [pDistribution] for i in range(len(colors))]

pHit = (sensor_right * pDistribution)
pMiss = ((1-sensor_right) * pDistribution)
p_notMove = 1 - p_move


def sense(p, Z):
	q = [len(colors[0]) * [0] for i in range(len(colors))]
	sumRows = []
	for row in range(len(p)):
		for element in range(len(p[row])):
			hit = (Z == colors[row][element-1])
			q[row][element-1] = (p[row][element-1] * (hit * pHit + (1-hit) * pMiss))
		sumRows.append(sum(q[row]))

	matrixSum = sum(sumRows)
	if matrixSum == 0:
		print "All zero for move"
		return q
	#Normalize matrix
	for row in range(len(q)):
		for element in range(len(q[row])):
			q[row][element] = q[row][element] / matrixSum
	return q

def move(p, U):
	q=[len(colors[0]) * [0] for i in range(len(colors))]
	for row in range(len(p)):
		for element in range(len(p[row])):
			rowMove = abs(int(U[1]))
			columnMove = abs(int(U[0]))
			noMove = (rowMove|columnMove)^1
		## Move in row
			s = rowMove * (p_move * p[row][(element - U[1]) % len(p[row])]) 
			s = s + rowMove * (p_notMove * p[row][element])
		## Move in column
			s = s + columnMove * (p_move * p[(row - U[0] % len(p))][element])
			s = s + columnMove * (p_notMove * p[row][element])
		## Don't move
			s = s + noMove * (p_move * p[row][element])
			
			q[row][element] = s
	return q

for k in range(len(measurements)):
	p = move(p, motions[k])
	p = sense(p, measurements[k])


show(p)




