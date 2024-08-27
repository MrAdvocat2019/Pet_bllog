def check_if_string_correct(s, count):
    a = s.split()
    for i in a:
        try:
            i = int(i)
            if i > count or i < 1:
                return False
        except Exception:
            return False
    return True
print(check_if_string_correct("1 5 6", 6))
