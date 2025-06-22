
def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

STRING_CHECK_LIST = [''
    , generate_string(255)
    , generate_string(1001)
    , russian_chars()
    , russian_chars().upper()
    , chinese_chars()
    , special_chars()
    ,"12345"]

IDS_STRING_CHECK_LIST = ('empty', '255 symbols', '1000+ symbols', 'russian', 'RUSSIAN', 'chinese', 'special', 'digit')

INT_CHECK_LIST = ('-1'
    ,'0'
    ,'1'
    ,'1.5'
    ,'2147483647'
    ,'2147483648'
    , special_chars()
    , russian_chars()
    , russian_chars().upper()
    , chinese_chars())

IDS_INT_CHECK_LIST = ('negative', 'zero', 'positive', 'float', 'int_max', 'int_max+1', 'special', 'russian', 'RUSSIAN', 'chinese')

NEGATIV_EMAIL_CHECK_LIST = (''
    ,'user@'
    ,'@test.com'
    ,'testov @test.com'
    ,'#/test,.\'ov!@test.com'
    ,f'{generate_string(255)}@test.com'
    ,'testov@@test.com'
    ,'testov@test.com" OR "1"="1'
    ,'TESTOV@TEST.COM')
#  'тестов@test.com'

IDS_NEGATIV_EMAIL_CHECK_LIST = ('empty email', 'email without domain part', 'email without user part', 'email with space',\
                                    'email with special symbols', '255+ symbols', 'email with double @', 'SQL injection', 'UPPER EMAIL')
                                # 'email with russian user'

NEGATIV_PASSWORD_CHECK_LIST =(''
    ,'a1!'
    ,f'{generate_string(125)}absd!'
    ,'password'
    ,'12345678')
    #special_chars()

IDS_NEGATIV_PASSWORD_CHECK_LIST = ('empty pass', 'min pass', 'max+ pass', 'only string', 'only int')
    #'special only'

INVALID_AUTH_KEYS = ({'key': ''}
    , {'key': 'a12642ed39615a40fa3f025babbcea6aac64f9670a556febc0647c3a'}
    , {'key': generate_string(255)}
    , {'key': 'another_old_key'}
    , {'key': 'a15647ed39615a40fa3f027babbcea6aac64f6670a556febc0j5g8'})

IDS_INVALID_AUTH_KEYS = ('empty key', 'invalid key', '255 symbols', 'old_key', 'valid key -1 symbol')