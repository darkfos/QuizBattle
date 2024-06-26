from random_word import RandomWords
from googletrans import Translator


class GenerateLanguage:

    def __init__(self) -> None:
        self.random_engine: RandomWords = RandomWords()
        self.translator_engine: Translator = Translator()
        self.__language: str = "en"

    def get_random_word(self, attr_lng: str = "en") -> str:
        
        random_word = ""
        while True:
            try:
                random_word: str = self.random_engine.get_random_word()

                if attr_lng == "en":
                    return {"word": random_word, "translate": self.translator_engine.translate(str(random_word), src=self.__language, dest='ru').text}
                
                elif attr_lng == "es":
                    spain_word: str = self.translator_engine.translate(random_word, src=self.__language, dest=attr_lng).text
                    return {"word": spain_word, 
                        "translate": self.translator_engine.translate(spain_word, src='es', dest='ru').text}
                elif attr_lng == "de":
                    german_word: str = self.translator_engine.translate(random_word, src=self.__language, dest=attr_lng).text
                    return {"word": german_word, 
                        "translate": self.translator_engine.translate(german_word, src='de', dest='ru').text}
                elif attr_lng == "fr":
                    france_word: str = self.translator_engine.translate(random_word, src=self.__language, dest=attr_lng).text
                    return {"word": france_word, 
                        "translate": self.translator_engine.translate(france_word, src='fr', dest='ru').text}
                elif attr_lng == "ja":
                    japan_word: str = self.translator_engine.translate(random_word, src=self.__language, dest=attr_lng).text
                    return {"word": japan_word, 
                        "translate": self.translator_engine.translate(japan_word, src='ja', dest='ru').text}
                elif attr_lng == "fi":
                    fin_word: str = self.translator_engine.translate(random_word, src=self.__language, dest=attr_lng).text
                    return {"word": fin_word, 
                        "translate": self.translator_engine.translate(fin_word, src='fi', dest='ru').text}
                elif attr_lng == "no":
                    norwat_word: str = self.translator_engine.translate(random_word, src=self.__language, dest=attr_lng).text
                    return {"word": norwat_word, 
                        "translate": self.translator_engine.translate(norwat_word, src='no', dest='ru').text}
                else:
                    break
            except TypeError as te:
                continue
    
    @property
    def language(self) -> str: return self.__language

    @language.setter
    def language(self, new_language) -> None:
        self.__language = new_language


generator_word = GenerateLanguage()