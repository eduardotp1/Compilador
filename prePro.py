class PrePro:
    def filter(code):
        new_code=""
        for i in code:
            if i=="'":
                return new_code
            new_code+=i
        return new_code