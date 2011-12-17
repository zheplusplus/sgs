def assert_eq(a, b):
    if not a == b:
        msg = '\ntwo objects do not equal\n'
        msg += '** expected: ' + str(a) + '\n'
        msg += '**  actual : ' + str(b) + '\n'
        raise AssertionError(msg)

def assert_ne(a, b):
    if a == b:
        raise AssertionError('\n** both are: ' + str(a) + '\ntwo objects equal')

def assert_list_eq(a, b):
    errmsg = ''
    if len(a) != len(b):
        errmsg = '\ntwo list has different length\n'
        errmsg += '** expected: ' + str(len(a)) + '\n'
        errmsg += '**  actual : ' + str(len(b)) + '\n'

    length = min(len(a), len(b))
    for i in range(0, length):
        if not a[i] == b[i]:
            errmsg += '\nat ' + str(i) + '\n'
            errmsg += '** expected: ' + str(a[i]) + '\n'
            errmsg += '**  actual : ' + str(b[i]) + '\n'

    if len(errmsg):
        raise AssertionError(errmsg)
