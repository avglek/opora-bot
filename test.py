from src.lexicon.lexicon_ru import BUTTONS_START,LEXICON_RU

print(BUTTONS_START)

for i in BUTTONS_START:
    print(BUTTONS_START[i])

print('===========================')

lam =lambda a: a

print(lam(BUTTONS_START))
print(LEXICON_RU['/start'])