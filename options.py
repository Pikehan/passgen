import string
from enum import Enum


class Characters(Enum):
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{}~'


