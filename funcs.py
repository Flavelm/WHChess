def IsNone(*requests) -> bool:
	for i in requests:
		if i == None:
			return True
	return False