name = input("Enter Name ")
pwd = input("Enter Password ")
age = input("Enter Age")
#print(type(name))
if name == "john" and pwd == "abc":
    if int(age) < 18:
        print("not allowed")
    else:
        print("allowed")
        print("welcome john")
elif name == "ram" and pwd == "xyz":
    print("welcome ram")
else:
    print("wrong credentials")