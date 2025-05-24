
def are_lists_same(list1, list2, check_vals_and_order): #Return values: False - not same, 
												#				True - same values (checking values only, or vals and order of element by the last argument)
												#check_vals_and_order arguments: True - Check that lists are same by values and order of elements, 
												# 								 False - Check that lists are same by values only (cane be in diferent order)
	lists_same_not_inc_order = True
	lists_same_inc_order = True

	if len(list1) != len(list2):
		return False
	if list1 == list2:
		return True
	if check_vals_and_order:  # after the above if's, it is clear that the lists are not the same by vals and order
		return False
	# checking if lists have same elements
	for x in list1:
		if x not in list2:
			return False
	return True


if __name__ == '__main__':
	list1 = [1,2,3,4,5]
	list2 = [1,2,3,4,5]
	list3 = [5,4,3,2,1]
	list4 = [1,2,3,4,5,6]

	print('--------------')
	print(are_lists_same(list1,list3,True))
	print(are_lists_same(list1,list3,False))
	


