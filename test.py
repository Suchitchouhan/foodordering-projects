print('a')
with open('data/food.csv') as f:
	first=0
	for x in f:
		if first == 0:
			first=1
			pass
		else:
			l1 = x.split(',')
			print(l1)
			pName=l1[0]
			brand_name=l1[1]
			category=l1[2]
			price=l1[3]
			des=l1[4]
			highlight=l1[5]
			overview=l1[6]
			gst=l1[7]
			# food_type=l1[8]
			specification=l1[1]

			for x in specification.split('+'):
				x=x.strip()
				y = x.split('-')
				for q in y:
					q=q.strip()
					# print(q[-1])
					if q[0].strip() == '[':
						#spec
						print(q[1:])
					elif q[-1].strip() == ']':
						#desc
						print(q[:-1])
