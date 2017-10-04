from parsers import parser_Santocha

class ParserDC(parser_Santocha.ParserSantocha):
    def __init__(self):
        super().__init__()
        self._COMPANY = 'DC'
        self._MEN_URL = 'http://www.dcrussia.ru/skidki-men/'
        self._WOMAN_URL = 'http://www.dcrussia.ru/skidki-women/'
        self._KIDS_URL = 'http://www.dcrussia.ru/skidki-kids/'
        self._types_dict = {
            'men': self._MEN_URL,
            'woman': self._WOMAN_URL,
            'kids': self._KIDS_URL
        }
