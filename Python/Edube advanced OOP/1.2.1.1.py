class Demo:
    class_var='shared var'
    def __init__(self,val):
        self.instance_var=val
        
d1=Demo(2000)
d2=Demo(50)

print("d1's instance var is: ", d1.instance_var)
print("d2's instance variable is: ",d2.instance_var)

print(Demo.class_var)
print(Demo.__dict__) 