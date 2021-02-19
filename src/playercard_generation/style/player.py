from enum import Enum

from .languages_dictionary import languages_dict
from .language import Language
from .exceptions import InvalidPositionError, InvalidLanguageError
from .en_position import EnPosition


class Player:
    def __init__(self, name, pos, club, country, overall=99, pac=99, dri=99, sho=99, deff=99, pas=99, phy=99, language='EN'):
        
        # Not sure why this is uppercased 
        self.name = name.upper()

        try:
            self.language = Language[language]
        except KeyError:
            raise InvalidLanguageError(f'Language ({language}) is not a valid language.')

        try:
            position = Enum('Position', languages_dict.get(language).get('positions'))
            self.position = position[pos.upper()]
        except KeyError:
            try:
                en_position = EnPosition[pos.upper()]
                position = Enum('Position', languages_dict.get(language).get('positions'))
                index = en_position.value - 1
                self.position = position[languages_dict.get(language).get('positions')[index]]
            except (KeyError, IndexError):
                raise InvalidPositionError(f'Position ({pos}) is not available in language {language}.'
                                           f'Conversion of {pos} from English position to {language} unsuccessful.')

        self.club = club
        self.country = country.lower()

        self.overall = str(overall).zfill(2)
        self.pac = str(pac).zfill(2)
        self.dri = str(dri).zfill(2)
        self.sho = str(sho).zfill(2)
        self.deff = str(deff).zfill(2)
        self.pas = str(pas).zfill(2)
        self.phy = str(phy).zfill(2)
