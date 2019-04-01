import re
class PrePro:
    def filter(code):
        new_code=re.sub("'.*\n", "\n", code)
        return new_code
