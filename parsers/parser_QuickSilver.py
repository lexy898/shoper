from parsers import parser_Santocha

class ParserQuickSilver(parser_Santocha.ParserSantocha):
    def __init__(self):
        super().__init__()
        self._COMPANY = 'QuickSilver'
        self._MEN_URL = 'http://www.quiksilver.ru/skidki-men/'
        self._KIDS_URL = 'http://www.quiksilver.ru/skidki-kids/'
        self._types_dict = {
            'men': self._MEN_URL,
            'kids': self._KIDS_URL
        }
