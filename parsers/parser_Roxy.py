from parsers import parser_Santocha

class ParserRoxy(parser_Santocha.ParserSantocha):
    def __init__(self):
        super().__init__()
        self._COMPANY = 'Roxy'
        self._WOMAN_URL = 'http://www.roxy-russia.ru/skidki-women/'
        self._KIDS_URL = 'http://www.roxy-russia.ru/skidki-kids/'
        self._types_dict = {
            'woman': self._WOMAN_URL,
            'kids': self._KIDS_URL
        }
