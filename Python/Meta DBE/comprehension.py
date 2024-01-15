#List Comprehension
#[<expression> for x in <sequence> if <condition>]
data = [1,2,3,4,9,5,6,7,8]
data = [x**2 for x in data]
print("Updates the data with the square of x: ", data)

#Dictionary comprehension
#dict = {key:value for key, value in <sequence> if <condition>}
usingrange = {x:x*2 for x in range(8)}
print("Using range():  ", usingrange)

#Set Comprehension
#{<expression> for x in <sequence> if <condition>}
set_a = {x for x in range(15, 32) if x not in [12,22,31] }
print(set_a)

#Generator Comprehension
#(<expression> for x in <sequence> if <condition>)
gen_obj = (x/2 for x in data)
print(gen_obj)
print(type(gen_obj))
for item in gen_obj:
    print(item, end=" ")