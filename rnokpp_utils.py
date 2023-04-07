"""РНОКПП analyze and generation tools"""
from datetime import date, timedelta
from random import randint, randrange

def analyze(ssn : str) -> tuple:
    """returns tuple (is_valid, sex, age) of given РНОКПП"""

    control_scheme = {
        0: -1,
        1: 5,
        2: 7,
        3: 9,
        4: 4,
        5: 6,
        6: 10,
        7: 5,
        8: 7
    }

    control_sum = sum(int(ssn[index]) * control_scheme[index] for index in range(9))
    control_number = 0 if control_sum % 11 == 0 else control_sum % 11

    is_valid = control_number == int(ssn[9])
    sex = 'M' if int(ssn[8]) % 2 else 'F'
    age = (date(1899, 12, 31) + timedelta(days=int(ssn[:5]))).isoformat()

    return (is_valid, sex, age)

def generate(dob : str =None, sex : str =None) -> str:
    """
    Generate random valid РНОКПП. Randomizes age/sex if no parameter is provided.
    dob supports any ISO date format.
    """

    #9th number is based on sex - odd for male, even for female.
    if sex in ('M', 'm', 'male', 'Male'):
        sex_digit = randrange(1, 10, 2)
    elif sex in ('F', 'f', 'female', 'Female'):
        sex_digit = randrange(0, 10, 2)
    else:
        sex_digit = randint(0, 9)

    #first 5 digits are based on date of birth.
    if dob is not None:
        dob_object = date.fromisoformat(dob)
        dob_digits = (dob_object - date(1899, 12, 31)).days
    else: #randomized value is based on random date of birth in 14-95 years old range
        dob_digits = ((date.today() - timedelta(days=randint(14, 95) * 365)) - date(1899, 12, 31)).days

    filler_digits = ''.join((str(randint(0,9)) for _ in range(1, 4)))

    base_rnokpp = f'{dob_digits}{filler_digits}{sex_digit}'
    control_scheme = {
        0: -1,
        1: 5,
        2: 7,
        3: 9,
        4: 4,
        5: 6,
        6: 10,
        7: 5,
        8: 7
    }

    control_digit = str(sum(int(base_rnokpp[index]) * control_scheme[index] for index in range(9)) % 11)
    if control_digit == '10':
        control_digit = '0'

    return base_rnokpp + control_digit

class RNOKPP:
    def __init__(self, ssn : str) -> None:
        self.ssn = ssn
        control_scheme = {
        0: -1,
        1: 5,
        2: 7,
        3: 9,
        4: 4,
        5: 6,
        6: 10,
        7: 5,
        8: 7
    }
        control_sum = sum(int(ssn[index]) * control_scheme[index] for index in range(9))
        control_number = 0 if control_sum % 11 == 0 else control_sum % 11

        self.is_valid = bool(control_number == int(ssn[9]))
        self.sex = 'M' if int(ssn[8]) % 2 else 'F'
        self.dob = (date(1899, 12, 31) + timedelta(days=int(ssn[:5]))).isoformat()
    def __str__(self) -> str:
        return f'{self.ssn} RNOKPP'
