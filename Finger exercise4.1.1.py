def isIn(str1, str2):
    return (str1 in str2) or (str2 in str1)

if __name__ == "__main__":
    print(isIn('hello', 'hello world'))
    print(isIn('hello', 'world'))
    print(isIn('hello world', 'hello'))