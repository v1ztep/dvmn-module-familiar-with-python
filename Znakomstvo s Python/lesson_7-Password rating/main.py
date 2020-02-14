import urwid

symbols = "!@#$%^&*()_-+={}[]"


def is_very_long(password):
    return len(password) > 12

def has_digit(password):
    return any(letter.isdigit() for letter in password)

def has_letters(password):
    return any(letter.isalpha() for letter in password)

def has_upper_letters(password):
    return any(letter.isupper() for letter in password)

def has_lower_letters(password):
    return any(letter.islower() for letter in password)

def has_symbols(password):
    return any(letter in symbols for letter in password)

def has_not_only_symbols(password):
    return any(letter not in symbols for letter in password)


def on_ask_change(edit, new_edit_text):
    score = 0
    for check in checks_password:
        if check(new_edit_text):
            score += 2
    reply.set_text(f'Рейтинг этого пароля: {score}')


checks_password = [is_very_long, has_digit, has_letters, has_upper_letters, has_lower_letters, has_symbols, has_not_only_symbols]


ask = urwid.Edit('Введите пароль: ', mask='*')
reply = urwid.Text('Рейтинг этого пароля: 0')
menu = urwid.Pile([ask, reply])
menu = urwid.Filler(menu, valign='top')
urwid.connect_signal(ask, 'change', on_ask_change)
urwid.MainLoop(menu).run()
