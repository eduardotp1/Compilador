class PrePro:
    def filter(code):
        new_code=""
        i=0
        while i <len(code):
            if code[i]=="'":
                while code[i]!="\\" and i<len(code)-1:
                    i+=1
                i+=1
            else:
                new_code+=code[i]
            i+=1
        return new_code
