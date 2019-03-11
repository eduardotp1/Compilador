class PrePro:
    def filter(code):
        new_code=""
        for i in code:
            if i=="'":
                return new_code
            if i==" ":
                pass
            else:
                new_code+=i
        return new_code