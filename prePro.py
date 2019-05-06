import re
class PrePro:
    def filter(code):
        new_code=re.sub("'.*\n", "\n", code)
        new_code+="\n\n"
        return new_code