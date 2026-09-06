import re
from enum import Enum


class PatternRule(Enum):
    STRING_PREFIX = 'string prefix'
    FILE_PREFIX = 'file prefix'
    IMAGE_FILE_PREFIX = 'image file prefix'

    @classmethod
    def get(cls, pattern_rule: str) -> 'PatternRule':

        match pattern_rule:
            case cls.STRING_PREFIX.value:
                return cls.STRING_PREFIX
            case cls.FILE_PREFIX.value:
                return cls.FILE_PREFIX
            case cls.IMAGE_FILE_PREFIX.value:
                return cls.IMAGE_FILE_PREFIX
            case _:
                raise ValueError('This Pattern Rule does not exist')

    @classmethod
    def get_string_4_pattern(cls, pattern_rule: 'PatternRule', string_4_pattern: str):

        match pattern_rule:
            case cls.STRING_PREFIX:
                return fr'{string_4_pattern.split('.')[0]} '
            case cls.FILE_PREFIX:
                return fr'{string_4_pattern}_'
            case cls.IMAGE_FILE_PREFIX:
                return fr'image_\[{string_4_pattern}]_'
            case _:
                raise ValueError('This Pattern Rule does not exist')


def get_pattern(pattern_rule: PatternRule, str_used_in_pattern: str) -> re.Pattern[str]:

    if 'prefix' in pattern_rule.value:
        return re.compile(fr'^{str_used_in_pattern}.*')
    else:
        raise ValueError('This Pattern Rule does not exist')


def is_str_match_pattern(string_to_check: str, pattern_rule: PatternRule, str_used_in_pattern: str) -> bool:
    pattern = get_pattern(pattern_rule, str_used_in_pattern)

    return True if pattern.search(string_to_check) else False

