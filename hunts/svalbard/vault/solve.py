data = 'TACGATGCATGGCTACYZZWXVAVYZTTAGACTAGCACTCGA'
# da = 'TACGATGCATGGCTAC______A__ZTTAGACTAGCACTCGA'

answ = list(data)

foo_to_bar = {
    'V': chr(0x55),
    'W': chr(0X4E),
    'X': chr(0x46),
    'Y': chr(0x52),
    'Z': chr(0x45)
}

for index, char in enumerate(data):
    if char in 'VWXYZ':
        answ[index] = foo_to_bar[char]

# CREENFUAURE
# G      T
