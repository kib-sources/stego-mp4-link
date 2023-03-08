from string import ascii_letters, digits, punctuation
print(ascii_letters + digits + punctuation)
def check(word):
    return all(map(lambda c: c in ascii_letters + digits + punctuation, word))

print(check('password123##'))