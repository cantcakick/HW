class Wax:
    def melt(self):
        print("wax can melt")
        
class Cheese:
    def melt(self):
        print('cheese melts') 
class Wood:
    def burn(self):
        print('wood burns')
        
for element in Wax(), Cheese(), Wood():
    try:
        element.melt()
    except AttributeError:
        print(f'{element} cannot melt')