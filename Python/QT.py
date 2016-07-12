def hello():
    a = 0
    
    def james():
        print(a)
        a +=1
    
    james()
    print("Hello")
    print(a)
    
hello()