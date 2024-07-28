class Human:
    def __init__(self,weight,age,pay):
        self.weight=weight
        self.age=age
        self.pay=pay
        
    def __add__(self,n):
        return self.weight + n.weight 
    
p1=Human(20,45,70)
p2=Human(35,50,60)

print(p1+p2)