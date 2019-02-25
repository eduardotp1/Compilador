def calculate(text):
    text=text.replace(" ","")
    temp_number=""
    number=[]
    signal=[]
    index=0
    
    while index<len(text):
        n=text[index]
        if n.isdigit():
            temp_number+=n
        if n == "-" or n == "+":
            signal.append(n)
            number.append(temp_number)
            temp_number=""

        index+=1
    number.append(temp_number)
    print(number)
    print(signal)
    count=int(number.pop(0))
    while len(number)>0:
        num = int(number.pop(0))
        s = signal.pop(0)
        if s == "+":
            count += num
        else:
            count -= num
        
    return count


print(calculate("1+2+10"))