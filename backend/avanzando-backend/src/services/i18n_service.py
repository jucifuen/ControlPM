import json
import os
from flask import request

class I18nService:
    def __init__(self):
        self.translations = {}
        self.default_language = 'es'
        self.supported_languages = ['es', 'en', 'pt', 'fr']
        self.load_translations()
    
    def load_translations(self):
        """Carga las traducciones desde archivos JSON"""
        translations_dir = 'src/translations'
        
        for lang in self.supported_languages:
            file_path = os.path.join(translations_dir, f'{lang}.json')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            else:
                self.translations[lang] = {}
    
    def get_user_language(self):
        """Obtiene el idioma del usuario desde headers o parámetros"""
        # Prioridad: parámetro URL > header Accept-Language > default
        lang = request.args.get('lang')
        if lang and lang in self.supported_languages:
            return lang
        
        accept_language = request.headers.get('Accept-Language', '')
        for lang in self.supported_languages:
            if lang in accept_language:
                return lang
        
        return self.default_language
    
    def translate(self, key, language=None, **kwargs):
        """Traduce una clave a un idioma específico"""
        if language is None:
            language = self.get_user_language()
        
        if language not in self.translations:
            language = self.default_language
        
        # Buscar la traducción usando notación de punto
        translation = self.translations[language]
        for part in key.split('.'):
            if isinstance(translation, dict) and part in translation:
                translation = translation[part]
            else:
                # Fallback al idioma por defecto
                translation = self.translations[self.default_language]
                for part in key.split('.'):
                    if isinstance(translation, dict) and part in translation:
                        translation = translation[part]
                    else:
                        return key  # Retorna la clave si no encuentra traducción
                break
        
        # Reemplazar variables en la traducción
        if isinstance(translation, str) and kwargs:
            for var, value in kwargs.items():
                translation = translation.replace(f'{{{var}}}', str(value))
        
        return translation if isinstance(translation, str) else key
    
    def get_translations_for_frontend(self, language=None):
        """Obtiene todas las traducciones para el frontend"""
        if language is None:
            language = self.get_user_language()
        
        return self.translations.get(language, self.translations[self.default_language])

# Instancia global del servicio
i18n = I18nService()

