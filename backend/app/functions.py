from translate import Translator

def translate_text(text, from_lang='en', to_lang='ru'):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    try:
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Error: {e}")
        return "translate error"