import asyncio
from json import loads, dumps
from os.path import isfile, isdir, join
from os import listdir, getcwd
from globalprogramlib.utils.errors import (
    InvalidLanguageData,
    IncompatibleLanguageVersion,
    TranslationKeyNotFound,
)
from aiofiles import open as async_open
from typing import AnyStr, List, Dict, Set, Optional


class Language(object):
    def __init__(self):
        """
        Instances a new Language object which could be used to create a language from scratch or load a already existing
        language from a file, json or dictionary
        """
        self.name: str = None
        self.code: str = None
        self.version: int = 1
        self.revision: int = None
        self.authors: List[str] = None
        self.contributors: List[str] = None
        self.translations: Dict[str, str] = {}
        self.encoding: str = "utf-8"

    def __eq__(self, o: object) -> bool:
        """
        Compares two objects, to check if the are the same Language
        """
        if type(o) != type(self):
            return False
        name_eq = o.name == self.name
        code_eq = o.code == self.code
        version_eq = o.version == self.version
        revision_eq = o.revision == self.revision
        authors_eq = o.authors == self.authors
        if not authors_eq and (
            (o.authors == ([],) or o.authors == [])
            and (self.authors == ([],) or self.authors == [])
        ):

            authors_eq = True
        contributors_eq = o.contributors == self.contributors
        if not contributors_eq and (
            (o.contributors == ([],) or o.contributors == [])
            and (self.contributors == ([],) or self.contributors == [])
        ):

            contributors_eq = True
        translations_eq = o.translations == self.translations

        return (
            name_eq
            and code_eq
            and version_eq
            and revision_eq
            and authors_eq
            and contributors_eq
            and translations_eq
        )

    def __contains__(self, translation_key):
        """
        Checks if a translation key exists in this language
        """
        return self.is_translatable(translation_key)

    # Sync

    def __enter__(self):
        """
        Prepares this object for use with «with» statement
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
        Clears this object after use
        """
        self.clear()

    def clear(self):
        """
        Clears this object, recreating it
        :return: This instance cleared for new use
        """
        self.name = None
        self.code = None
        self.version = 1
        self.revision = None
        self.authors = None
        self.contributors = None
        self.translations = {}
        return self

    def __len__(self):
        """
        Counts the number of translations available in this language
        :return: Number of translations
        """
        return len(self.translations)

    def __repr__(self):
        """
        When printing the object, this will show the language name in the output
        :return: Language Name
        """
        return self.name if self.name != None else "Cleared/Initialized Language"

    def __str__(self):
        """
        When converting the object to string, this will show the language name in the output
        :return: Language Name
        """
        return self.name if self.name != None else "Cleared/Initialized Language"

    def is_ready(self) -> bool:
        """
        Checks if language is ready for use
        :return: True if ready, else false
        """
        return (
            self.name != None
            and self.code != None
            and self.revision != None
            and self.authors != None
            and self.contributors != None
        )

    def from_json(self, json_data: str):
        """
        Parses a language from a json string

        The language must be version 1 to be parsed correctly and have the following fields:
        name - String Language Name
        code - String Language Code (in ISO 639‑1 Code format)
        revision - Int representing the language version/revision
        authors - List containing the authors of the language
        contributors - List containing the contributors of the language
        translations - Dictionary containing the key and the translation in that language

        Example Json Data:
        '''
        {
            "name": "English",
            "code": "en",
            "version": 1,
            "revision": 1,
            "authors": ["VTNTV Team"],
            "contributors": [],
            "translations": {
                "com.vtntv.welcome" : "Welcome to VTNTV"
            }
        }
        '''

        :param json_data: a json string containing a valid version 1 language
        :return: This language object populated by the json data
        """
        try:
            data = loads(json_data)
            keys = data.keys()
            if "version" not in keys:
                raise InvalidLanguageData(
                    "Your file specified must have valid json language data"
                )
        except Exception:
            raise InvalidLanguageData(
                "Your file specified must have valid json language data"
            )

        if data["version"] != 1:
            raise IncompatibleLanguageVersion("language version not supported")

        if (
            "name" not in keys
            or "code" not in keys
            or "revision" not in keys
            or "authors" not in keys
            or "contributors" not in keys
            or "translations" not in keys
        ):
            raise InvalidLanguageData(
                "Your file specified must have valid json language data"
            )

        self.name = data["name"]
        self.code = data["code"]
        self.version = data["version"]
        self.revision = data["revision"]
        self.authors = data["authors"]
        self.contributors = data["contributors"]
        self.translations = data["translations"]
        return self

    def from_file(self, path: str):
        """
        Parses a language from a file

        The language must be version 1 to be parsed correctly and have the following fields:
        name - String Language Name
        code - String Language Code (in ISO 639‑1 Code format)
        revision - Int representing the language version/revision
        authors - List containing the authors of the language
        contributors - List containing the contributors of the language
        translations - Dictionary containing the key and the translation in that language

        Example language file:
        '''
        {
            "name": "English",
            "code": "en",
            "version": 1,
            "revision": 1,
            "authors": ["VTNTV Team"],
            "contributors": [],
            "translations": {
                "com.vtntv.welcome" : "Welcome to VTNTV"
            }
        }
        '''

        :param path: path to a file containing a valid version 1 language
        :return: This language object populated by the language in specified file
        """
        if isfile(path):
            with open(path, encoding=self.encoding) as language_file:
                return self.from_json(language_file.read())

    def from_dict(self, dict_data: dict):
        """
        Parses a language from a dictionary

        The language must be version 1 to be parsed correctly and have the following fields:
        name - String Language Name
        code - String Language Code (in ISO 639‑1 Code format)
        revision - Int representing the language version/revision
        authors - List containing the authors of the language
        contributors - List containing the contributors of the language
        translations - Dictionary containing the key and the translation in that language

        Example Dict Data:
        {
            "name": "English",
            "code": "en",
            "version": 1,
            "revision": 1,
            "authors": ["VTNTV Team"],
            "contributors": [],
            "translations": {
                "com.vtntv.welcome" : "Welcome to VTNTV"
            }
        }

        :param dict_data: a dictionary containing a valid version 1 language
        :return: This language object populated by the dict data
        """
        return self.from_json(dumps(dict_data))

    @property
    def to_dict(self) -> dict:
        """
        Generates a dictionary containing the language in this instance
        :return: Dictionary containing the Language in this instance
        """
        return {
            "name": self.name,
            "code": self.code,
            "version": self.version,
            "revision": self.revision,
            "authors": self.authors,
            "contributors": self.contributors,
            "translations": self.translations,
        }

    @property
    def to_json(self) -> str:
        """
        Generates a json containing the language in this instance
        :return: Json containing the Language in this instance
        """
        return dumps(self.to_dict)

    def to_file(self, path: str, override: bool = False):
        """
        Exports a file containing the language in this instance
        :param path: Path/file mame where to save the exported language
        :param override: If file exists, it should be overridden (True) or should not export the language (False)
        :return: None if not created, path if created
        """
        if not override and isfile(path):
            return
        with open(path, "w+", encoding=self.encoding) as file:
            file.write(self.to_json)
            file.close()
        return path

    def get_translation(
        self, key: str, default: str = None, throw_not_found: bool = False
    ) -> str:
        """
        Gets the translation associated with a specific key in this language
        :param key: The key to identify the translation
        :param default: If key could not be found and throw_not_found is False, the value to return
        :param throw_not_found: If the key could not be found, should a exception be raised instead of returning the
        default
        :return: The value of the key if found, default value if not found and throw_not_found is False
        """
        if default is None:
            default = key
        if throw_not_found and not self.is_translatable(key):
            raise TranslationKeyNotFound("Translation not found")
        return self.translations[key] if self.is_translatable(key) else default

    def is_translatable(self, key: str) -> bool:
        """
        Checks if the specified translation key exists in the Language
        :param key: translation key to check
        :return: True if found, False if not found
        """
        if key in self.translations.keys():
            return True
        else:
            return False

    def set_translation(self, key: str, value: str, override=False):
        """
        Creates a new translation in this language
        :param key: The name of the translation key to set
        :param value: The value to associate with the translation key
        :param override: If the key exists, it should be overridden (True) or should ignore this instruction (False)
        :return: value if key was set, else None
        """
        if self.is_translatable(key) and not override:
            return
        self.translations[key] = value
        return value

    def rename_translation(
        self, old_key: str, new_key: str, keep_old_key=False, override=False
    ):
        """
        Renames a translation key, keeping the value inside that key intact
        :param old_key: The name of the translation key to rename
        :param new_key: The name to give to the translation key
        :param keep_old_key: If this method should copy the key (True) or should move the key (False)
        :param override: If the new_key exists, it should be overridden (True) or should ignore this instruction (False)
        :return: None if old_key doesn't exists or the new key already exists and override is true, else new_key
        """
        if not self.is_translatable(old_key):
            return
        if self.is_translatable(new_key) and not override:
            return
        self.translations[new_key] = self.translations[old_key]
        if not keep_old_key:
            self.remove_translation(old_key)
        return new_key

    def remove_translation(self, key: str):
        """
        Deletes the translation associated with the key
        :param key: The translation key to remove
        :return: None if not found, key value if removed
        """
        if self.is_translatable(key):
            return self.translations.pop(key)

    # Async

    def __await__(self):
        """
        Instances a new Language object which could be used to create a language from scratch or load a already existing
        language from a file, json or dictionary (using async calls)
        """

        async def language():
            return self

        return language().__await__()

    async def __aenter__(self):
        """
        Prepares this object for use with «async with» statement
        """
        return await self

    async def __aexit__(self, *args):
        """
        Clears this object after use (using async calls)
        """
        await self.async_clear()

    async def async_is_ready(self) -> bool:
        """
        Checks if language is ready for use
        :return: True if ready, else false
        """
        return self.is_ready()

    async def async_clear(self):
        """
        Clears this object, recreating it (using async calls)
        :return: This instance cleared for new use
        """
        self.name = None
        self.code = None
        self.version = 1
        self.revision = None
        self.authors = None
        self.contributors = None
        self.translations = {}
        return await self

    async def async_from_json(self, json_data: str):
        """
        Parses a language from a json string (using async calls)

                The language must be version 1 to be parsed correctly and have the following fields:
                name - String Language Name
                code - String Language Code (in ISO 639‑1 Code format)
                revision - Int representing the language version/revision
                authors - List containing the authors of the language
                contributors - List containing the contributors of the language
                translations - Dictionary containing the key and the translation in that language

                Example Json Data:
        '''
        {
            "name": "English",
            "code": "en",
            "version": 1,
            "revision": 1,
            "authors": ["VTNTV Team"],
            "contributors": [],
            "translations": {
                "com.vtntv.welcome" : "Welcome to VTNTV"
            }
        }
        '''

        :param json_data: a json string containing a valid version 1 language
        :return: This language object populated by the json data
        """
        return await (self.from_json(json_data))

    async def async_from_file(self, path: str):
        """
        Parses a language from a file (using async calls)

        The language must be version 1 to be parsed correctly and have the following fields:
        name - String Language Name
        code - String Language Code (in ISO 639‑1 Code format)
        revision - Int representing the language version/revision
        authors - List containing the authors of the language
        contributors - List containing the contributors of the language
        translations - Dictionary containing the key and the translation in that language

        Example language file:
        '''
        {
            "name": "English",
            "code": "en",
            "version": 1,
            "revision": 1,
            "authors": ["VTNTV Team"],
            "contributors": [],
            "translations": {
                "com.vtntv.welcome" : "Welcome to VTNTV"
            }
        }
        '''

        :param path: path to a file containing a valid version 1 language
        :return: This language object populated by the language in specified file
        """
        if isfile(path):
            async with async_open(path, encoding=self.encoding) as language_file:
                return await (self.from_json(await language_file.read()))

    async def async_from_dict(self, dict_data: dict):
        """
        Parses a language from a dictionary (using async calls)

        The language must be version 1 to be parsed correctly and have the following fields:
        name - String Language Name
        code - String Language Code (in ISO 639‑1 Code format)
        revision - Int representing the language version/revision
        authors - List containing the authors of the language
        contributors - List containing the contributors of the language
        translations - Dictionary containing the key and the translation in that language

        Example Dict Data:
        {
            "name": "English",
            "code": "en",
            "version": 1,
            "revision": 1,
            "authors": ["VTNTV Team"],
            "contributors": [],
            "translations": {
                "com.vtntv.welcome" : "Welcome to VTNTV"
            }
        }

        :param dict_data: a dictionary containing a valid version 1 language
        :return: This language object populated by the dict data
        """
        return await (self.from_dict(dict_data))

    @property
    async def async_to_dict(self):
        """
        Generates a dictionary containing the language in this instance (using async calls)
        :return: Dictionary containing the Language in this instance
        """
        return self.to_dict

    @property
    async def async_to_json(self) -> str:
        """
        Generates a json containing the language in this instance (using async calls)
        :return: Json containing the Language in this instance
        """
        return self.to_json

    async def async_to_file(self, path: str, override: bool = False):
        """
        Exports a file containing the language in this instance (using async calls)
        :param path: Path/file mame where to save the exported language
        :param override: If file exists, it should be overridden (True) or should not export the language (False)
        :return: None if not created, path if created
        """
        if not override and isfile(path):
            return
        async with async_open(path, "w+", encoding=self.encoding) as file:
            await file.write(self.to_json)
            await file.close()
        return path

    async def async_get_translation(
        self, key: str, default: str = None, throw_not_found: bool = False
    ) -> str:
        """
        Gets the translation associated with a specific key in this language (using async calls)
        :param key: The key to identify the translation
        :param default: If key could not be found and throw_not_found is False, the value to return
        :param throw_not_found: If the key could not be found, should a exception be raised instead of returning the
        default
        :return: The value of the key if found, default value if not found and throw_not_found is False
        """
        if default is None:
            default = key
        if throw_not_found and not await self.async_is_translatable(key):
            raise TranslationKeyNotFound("Translation not found")
        return (
            self.translations[key] if await self.async_is_translatable(key) else default
        )

    async def async_is_translatable(self, key: str) -> bool:
        """
        Checks if the specified translation key exists in the Language (using async calls)
        :param key: translation key to check
        :return: True if found, False if not found
        """
        if key in self.translations.keys():
            return True
        else:
            return False

    async def async_set_translation(self, key: str, value: str, override=False):
        """
        Creates a new translation in this language (using async calls)
        :param key: The name of the translation key to set
        :param value: The value to associate with the translation key
        :param override: If the key exists, it should be overridden (True) or should ignore this instruction (False)
        :return: value if key was set, else None
        """
        if await self.async_is_translatable(key) and not override:
            return
        self.translations[key] = value
        return value

    async def async_rename_translation(
        self, old_key: str, new_key: str, keep_old_key=False, override=False
    ):
        """
        Renames a translation key, keeping the value inside that key intact (using async calls)
        :param old_key: The name of the translation key to rename
        :param new_key: The name to give to the translation key
        :param keep_old_key: If this method should copy the key (True) or should move the key (False)
        :param override: If the new_key exists, it should be overridden (True) or should ignore this instruction (False)
        :return: None if old_key doesn't exists or the new key already exists and override is true, else new_key
        """
        if not await self.async_is_translatable(old_key):
            return
        if await self.async_is_translatable(new_key) and not override:
            return
        self.translations[new_key] = self.translations[old_key]
        if not keep_old_key:
            await self.async_remove_translation(old_key)
        return new_key

    async def async_remove_translation(self, key: str):
        """
        Deletes the translation associated with the key (using async calls)
        :param key: The translation key to remove
        :return: None if not found, key value if removed
        """
        if await self.async_is_translatable(key):
            return self.translations.pop(key)


class Translator(object):
    def __init__(self):
        """
        Instances a new Translator object which could be used to write multi-language applications
        by loading already created languages, defining the primary (selected) language in SelectedLanguageCode
        and the fallback (default) in DefaultLanguageCode and using the get_translation method
        """
        self.languages_loaded: Dict[str, Language] = {}
        self.DefaultLanguageCode: str = None
        self.SelectedLanguageCode: str = None

    def __eq__(self, o: object):
        """
        Compares two objects to check if they are the same Translator
        """
        if type(o) != type(self):
            return False
        lang_eq = self.languages_loaded == o.languages_loaded
        return lang_eq

    def __contains__(self, language_code):
        """
        Checks if a language code is present in this translator
        """
        return self.is_language(language_code)

    def __repr__(self):
        """
        When printing the object, this will show the Translator languages in the output
        :return: Translator Name
        """
        return (
            repr([*self.languages_loaded.values()])
            if self.languages_loaded != None or len(self.languages) != 0
            else "Cleared/Initialized Translator"
        )

    def __str__(self):
        """
        When converting the object to string, this will show the Translator languages in the output
        :return: Translator Name
        """
        return (
            repr([*self.languages_loaded.values()])
            if self.languages_loaded != None or len(self.languages) != 0
            else "Cleared/Initialized Translator"
        )

    # Sync Methods

    def __enter__(self):
        """
        Prepares this object for use with «with» statement
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
        Clears this object after use
        """
        self.clear()

    def __len__(self):
        """
        Counts the number of languages loaded in this Translator
        :return: Number of translations
        """
        return len(self.languages_loaded)

    def load_directory(self, path: str = getcwd()):
        """
        Tries to import all language files in the specified directory to the Translator
        :param path: Directory to lookup for language files
        :return: This translator object populated with new loaded languages
        """
        if isdir(path):
            for file in listdir(path):
                try:
                    file_joined = join(path, file)
                    self.load_file(file_joined)
                except:
                    pass

        return self

    def load_file(self, path: str, encoding: str = "utf-8", override: bool = False):
        """
        Parses a language from the specified file and imports it in the Translator instance
        :param path: path to a file containing a valid version 1 language
        :param encoding: Encoding to use for reading the file
        :param override: if the language code already exists, should we override it or should we discard the file
        :return: This translator object populated with new loaded language
        """
        if isfile(path):
            with open(path, encoding=encoding) as language_file:
                self.load_languages(
                    Language().from_json(language_file.read()), override=override
                )

    def get_translation(self, key: str, default: str = None, throw_not_found=False):
        """
        Gets the translation associated with a specific key in this selected language, if not found tries to gets the
        translation from the default language, if not found in default, it will return the default value
        :param key: The key to identify the translation
        :param default: If key could not be found and throw_not_found is False, the value to return
        :param throw_not_found: If the key could not be found, should a exception be raised instead of returning the
        default
        :return: The value of the key if found, default value if key not found and throw_not_found is False
        or None if Translator is not ready to use
        """
        if not self.is_ready:
            return None
        if default is None:
            default = key
        try:
            return self.selected_language.get_translation(key, throw_not_found=True)
        except TranslationKeyNotFound:
            pass
        try:
            return self.default_language.get_translation(key, throw_not_found=True)
        except TranslationKeyNotFound:
            if throw_not_found:
                raise TranslationKeyNotFound("Translation not found")
            return default

    def remove_translation(self, key: str):
        """
        Removes the specified key from all languages in the translator
        :param key: translation key to remove
        """
        for language in self.languages_loaded.values():
            language.remove_translation(key)

    def rename_translation(
        self, old_key: str, new_key: str, keep_old_key=False, override=False
    ):
        """
        Renames a translation key on all languages loaded in this translator, keeping the value inside that key intact
        :param old_key: The name of the translation key to rename
        :param new_key: The name to give to the translation key
        :param keep_old_key: If this method should copy the key (True) or should move the key (False)
        :param override: If the new_key exists, it should be overridden (True) or should ignore this instruction (False)
        """
        for language in self.languages_loaded.values():
            language.rename_translation(old_key, new_key, keep_old_key, override)

    @property
    def default_language(self):
        """
        Gets the default language selected for this translator
        To set it, you should set the language code in the DefaultLanguageCode attribute
        The language code must be valid in this instance, else this will return None
        :return: Language if DefaultLanguageCode is chosen and valid, else None
        """
        if self.DefaultLanguageCode is None:
            return None
        elif not self.is_language(self.DefaultLanguageCode):
            return None
        return self.languages_loaded[self.DefaultLanguageCode]

    @property
    def selected_language(self):
        """
        Gets the selected language selected for this translator
        To set it, you should set the language code in the SelectedLanguageCode attribute
        The language code must be valid in this instance, else this will return None
        :return: Language if SelectedLanguageCode is chosen and valid, else None
        """
        if self.SelectedLanguageCode is None:
            return None
        elif not self.is_language(self.SelectedLanguageCode):
            return None
        return self.languages_loaded[self.SelectedLanguageCode]

    @property
    def is_ready(self):
        """
        Defines if this instance is ready to translate keys
        :return: True if SelectedLanguageCode and DefaultLanguageCode is set and valid, else False
        """
        return (
            True
            if self.default_language is not None and self.selected_language is not None
            else False
        )

    def is_language(self, code: str):
        """
        Checks if a language is present in this instance or not
        :param code: Language code to check
        :return: True if found, else False
        """
        if code in self.languages_loaded.keys():
            return True
        return False

    def load_languages(self, *languages: Language, override=False):
        """
        Loads the specified languages in the Translator instance
        :param *languages: Collection of Language Objects
        :param override: if the language code already exists, should we override it or should we discard the language
        :return: This translator object populated with new loaded languages
        """
        for language in languages:
            language = language
            if not override:

                if not (self.is_language(language.code)):

                    self.languages_loaded[language.code] = language
            else:
                self.languages_loaded[language.code] = language
        return self

    def unload_language(self, *codes: str) -> bool:
        """
        Removes the specified languages from this Translator instance
        :param *codes:
        """

        for code in codes:
            if self.is_language(code):
                self.languages_loaded.pop(code)

    def unload_all_languages(self):
        """
        Unloads all languages present in this instance
        :return: This instances without any language
        """
        self.languages_loaded = {}

    def clear(self):
        """
        Clears this object, recreating it
        :return: This instance cleared for new use
        """
        self.DefaultLanguageCode = None
        self.SelectedLanguageCode = None
        self.unload_all_languages()
        return self

    @property
    def coverage(self):
        """
        Gets the coverage report for the languages loaded in this translator
        Doesn't include the languages, since you can get it through languages_loaded
        :return: Dictionary containing the coverage report if there are languages loaded, else None
        """
        return evaluate_coverage(*self.languages_loaded.values())

    # Async

    def __await__(self):
        """
        Instances a new asyn Translator object which could be used to write multi-language applications
        by loading already created languages, defining the primary (selected) language in SelectedLanguageCode
        and the fallback (default) in DefaultLanguageCode and using the async_get_translation method
        """

        async def translator():
            return self

        return translator().__await__()

    async def __aenter__(self):
        """
        Prepares this object for use with «async with» statement
        """
        return self

    async def __aexit__(self, *args):
        """
        Clears this object after use
        """
        await self.async_clear()

    async def async_load_directory(self, path: str = getcwd()):
        """
        Tries to import all language files in the specified directory to the Translator (using async calls)
        :param path: Directory to lookup for language files
        :return: This translator object populated with new loaded languages
        """
        tasks = []
        if isdir(path):
            for file in listdir(path):
                file_joined = join(path, file)
                tasks.append(self.async_load_file(file_joined))
            c = await asyncio.gather(*tasks)
        return self

    async def async_load_file(
        self, path: str, encoding="utf-8", override: bool = False
    ):
        """
        Parses a language from the specified file and imports it in the Translator instance (using async calls)
        :param path: path to a file containing a valid version 1 language
        :param encoding: Encoding to use for reading the file
        :param override: if the language code already exists, should we override it or should we discard the file
        :return: This translator object populated with new loaded language
        """
        if isfile(path):
            async with async_open(path, encoding=encoding) as language_file:
                language_data = await language_file.read()

                lang = await Language()
                await lang.async_from_json(language_data)
                await self.async_load_languages(lang, override=override)

        return self

    async def async_get_translation(
        self, key: str, default: str = None, throw_not_found: bool = False
    ):
        """
        Gets the translation associated with a specific key in this selected language, if not found tries to gets the
        translation from the default language, if not found in default, it will return the default value
        (using async calls)
        :param key: The key to identify the translation
        :param default: If key could not be found and throw_not_found is False, the value to return
        :param throw_not_found: If the key could not be found, should a exception be raised instead of returning the
        default
        :return: The value of the key if found, default value if key not found and throw_not_found is False
        or None if Translator is not ready to use
        """

        status = await self.async_is_ready
        if not status:
            return None

        if default is None:
            default = key
        try:
            return await (await self.async_selected_language).async_get_translation(
                key, throw_not_found=True
            )
        except TranslationKeyNotFound:
            pass
        try:
            return await (await self.async_default_language).async_get_translation(
                key, throw_not_found=True
            )
        except TranslationKeyNotFound:
            if throw_not_found:
                raise TranslationKeyNotFound("Translation not found")
            return default

    async def async_remove_translation(self, key: str):
        """
        Removes the specified key from all languages in the translator (using async calls)
        :param key: translation key to remove
        """
        for language in self.languages_loaded.values():
            await language.async_remove_translation(key)

    async def async_rename_translation(
        self, old_key: str, new_key: str, keep_old_key=False, override=False
    ):
        """
        Renames a translation key on all languages loaded in this translator, keeping the value inside that key intact
        (using async calls)
        :param old_key: The name of the translation key to rename
        :param new_key: The name to give to the translation key
        :param keep_old_key: If this method should copy the key (True) or should move the key (False)
        :param override: If the new_key exists, it should be overridden (True) or should ignore this instruction (False)
        """
        for language in self.languages_loaded.values():
            await language.async_rename_translation(
                old_key, new_key, keep_old_key, override
            )

    @property
    async def async_default_language(self):
        """
        Gets the default language selected for this translator (using async calls)
        To set it, you should set the language code in the DefaultLanguageCode attribute
        The language code must be valid in this instance, else this will return None
        :return: Language if DefaultLanguageCode is chosen and valid, else None
        """
        if self.DefaultLanguageCode is None:
            return None
        elif not await self.async_is_language(self.DefaultLanguageCode):
            return None
        return self.languages_loaded[self.DefaultLanguageCode]

    @property
    async def async_selected_language(self):
        """
        Gets the selected language selected for this translator (using async calls)
        To set it, you should set the language code in the SelectedLanguageCode attribute
        The language code must be valid in this instance, else this will return None
        :return: Language if SelectedLanguageCode is chosen and valid, else None
        """
        if self.SelectedLanguageCode is None:
            return None
        elif not await self.async_is_language(self.SelectedLanguageCode):
            return None
        return self.languages_loaded[self.SelectedLanguageCode]

    @property
    async def async_is_ready(self):
        """
        Defines if this instance is ready to translate keys (using async calls)
        :return: True if SelectedLanguageCode and DefaultLanguageCode is set and valid, else False
        """
        return (
            True
            if (
                await self.async_default_language is not None
                and await self.async_selected_language is not None
            )
            and (
                await (await self.async_selected_language).async_is_ready()
                and await (await self.async_default_language).async_is_ready()
            )
            else False
        )

    async def async_is_language(self, code: str):
        """
        Checks if a language is present in this instance or not (using async calls)
        :param code: Language code to check
        :return: True if found, else False
        """
        if code in self.languages_loaded.keys():
            return True
        return False

    async def async_load_languages(self, *languages: Language, override=False):
        """
        Loads the specified languages in the Translator instance (using async calls)
        :param *languages: Collection of Language Objects
        :param override: if the language code already exists, should we override it or should we discard the language
        :return: This translator object populated with new loaded language
        """
        for language in languages:
            language = await language
            if not override:
                if not (await self.async_is_language(language.code)):

                    self.languages_loaded[language.code] = language
            else:
                self.languages_loaded[language.code] = language
        return await self

    async def async_unload_language(self, *codes: str):
        """
        Removes the specified languages from this Translator instance (using async calls)
        :param *codes:
        """
        for code in codes:
            if await self.async_is_language(code):
                self.languages_loaded.pop(code)

    async def async_unload_all_languages(self):
        """
        Unloads all languages present in this instance (using async calls)
        :return: This instances without any language
        """
        self.unload_all_languages()

    async def async_clear(self):
        """
        Clears this object, recreating it (using async calls)
        :return: This instance cleared for new use
        """
        self.DefaultLanguageCode = None
        self.SelectedLanguageCode = None
        await self.async_unload_all_languages()
        return await self

    @property
    async def async_coverage(self):
        """
        Gets the coverage report for the languages loaded in this translator
        Doesn't include the languages, since you can get it through languages_loaded
        :return: Dictionary containing the coverage report if there are languages loaded, else None
        """
        return await async_evaluate_coverage(*self.languages_loaded.values())


def evaluate_coverage(*languages: Language, export_analyzed_languages=False):
    """
    This function can be used to evaluate the translation status of your v1 languages

    You can also evaluate your Translator using *translator.languages_loaded.values()
    as a parameter

    :param *languages: Collection of Languages with version 1 to evaluate coverage
    :param export_analyzed_languages: Should the evaluated languages be exported with the report
    :return: Dictionary containing the language report
    """
    # If there aren't no languages to evaluate, why we should continue?
    if len(languages) == 0:
        return

    # Variables
    global_missing_keys: Dict[
        AnyStr, Set[AnyStr]
    ] = {}  # Will store missing keys of each language
    global_avg_keys: float = (
        0  # Will store the medium number of keys counting all valid languages
    )
    global_avg_keys_percent: float = 0  # Will store the medium number of keys in percentage counting all valid languages
    global_coverage_percent: Dict[
        AnyStr, float
    ] = (
        {}
    )  # Will store the coverage percent of the keys present in a language in relation to all valid keys
    valid_languages: List[Language] = []  # Stores languages used for the report
    valid_keys: Set[
        AnyStr
    ] = set()  # Will store all keys extracted from languages (global index)

    # First step - compute valid languages and all possible keys
    # We don´t want to include invalid languages in computation
    for language in languages:
        if type(language) != Language or not language.is_ready():
            continue
        valid_languages.append(language)
        valid_keys |= language.translations.keys()

    del languages

    # Again, if there aren't no valid languages to evaluate, why we should continue?
    if len(valid_languages) == 0:
        return

    # Second step - Compute global per language coverage report
    for language in valid_languages:
        global_missing_keys[language.code] = valid_keys - language.translations.keys()
        global_avg_keys += len(language)
        try:
            global_coverage_percent[language.code] = (len(language) * 100) / len(
                valid_keys
            )
        except ZeroDivisionError:
            global_coverage_percent[language.code] = 0

    # Third step - Compute global statistics
    global_avg_keys_percent = (global_avg_keys * 100) / (
        len(valid_languages) * len(valid_keys)
    )
    global_avg_keys /= len(valid_languages)

    # Last step - Build and return report
    report = {}
    report["global_missing_keys"] = global_missing_keys
    report["global_all_keys"] = valid_keys

    report["global_avg_keys"] = global_avg_keys
    report["global_avg_keys_percent"] = global_avg_keys_percent

    report["global_coverage_percent"] = global_coverage_percent

    if export_analyzed_languages:
        report["analyzed_languages"] = valid_languages

    return report


async def async_evaluate_coverage(
    *languages: Language, export_analyzed_languages=False
):
    """
    This function can be used to evaluate the translation status of your v1 languages

    You can also evaluate your Translator using *translator.languages_loaded.values()
    as a paramter (using async implementation)

    :param *languages: Collection of Languages with version 1 to evaluate coverage
    :param export_analyzed_languages: Should the evaluated languages be exported with the report
    :return: Dictionary containing the language report
    """
    # If there aren't no languages to evaluate, why we should continue?
    if len(languages) == 0:
        return

    # Variables
    global_missing_keys: Dict[
        AnyStr, Set[AnyStr]
    ] = {}  # Will store missing keys of each language
    global_avg_keys: float = (
        0  # Will store the medium number of keys counting all valid languages
    )
    global_avg_keys_percent: float = 0  # Will store the medium number of keys in percentage counting all valid languages
    global_coverage_percent: Dict[
        AnyStr, float
    ] = (
        {}
    )  # Will store the coverage percent of the keys present in a language in relation to all valid keys
    valid_languages: List[Language] = []  # Stores languages used for the report
    valid_keys: Set[
        AnyStr
    ] = set()  # Will store all keys extracted from languages (global index)

    # First step - compute valid languages and all possible keys
    # We don´t want to include invalid languages in computation
    for language in languages:
        if type(language) != Language or not await language.async_is_ready():
            continue
        valid_languages.append(language)
        valid_keys |= language.translations.keys()

    del languages

    # Again, if there aren't no valid languages to evaluate, why we should continue?
    if len(valid_languages) == 0:
        return

    # Second step - Compute global per language coverage report
    for language in valid_languages:
        global_missing_keys[language.code] = valid_keys - language.translations.keys()
        global_avg_keys += len(language)
        try:
            global_coverage_percent[language.code] = (len(language) * 100) / len(
                valid_keys
            )
        except ZeroDivisionError:
            global_coverage_percent[language.code] = 0

    # Third step - Compute global statistics
    global_avg_keys_percent = (global_avg_keys * 100) / (
        len(valid_languages) * len(valid_keys)
    )
    global_avg_keys /= len(valid_languages)

    # Last step - Build and return report
    report = {}
    report["global_missing_keys"] = global_missing_keys
    report["global_all_keys"] = valid_keys

    report["global_avg_keys"] = global_avg_keys
    report["global_avg_keys_percent"] = global_avg_keys_percent

    report["global_coverage_percent"] = global_coverage_percent

    if export_analyzed_languages:
        report["analyzed_languages"] = valid_languages

    return report


def check_language_file(*paths) -> Dict[str, Optional[bool]]:
    """
    Checks the if the specified files or the files in the
    specified directory are a valid language version 1 file

    if the file has None the language version was higher than 1
    if the file has False it isn't a valid language file
    if the file has True it is a valid language file

    :param *paths: files/directories to check
    :return: Dictionary containing the name of files as keys and bool or none as values
    """

    status: Dict[str, Optional[bool]] = {}

    for path in paths:

        if isfile(path):
            with Language() as lang:
                try:
                    lang.from_file(path)
                except (IncompatibleLanguageVersion):
                    status[path] = None
                except (InvalidLanguageData):
                    status[path] = False
                else:
                    # We had success in the verification
                    status[path] = True

        elif isdir(path):

            for file in listdir(path):
                if isfile(join(path, file)):
                    with Language() as lang:
                        try:
                            lang.from_file(join(path, file))
                        except (IncompatibleLanguageVersion):
                            status[join(path, file)] = None
                        except (InvalidLanguageData):
                            status[join(path, file)] = False
                        else:
                            status[join(path, file)] = True

        else:
            status[path] = False

    return status


async def async_check_language_file(*paths) -> Dict[str, Optional[bool]]:
    """
    Checks the if the specified files or the files in the
    specified directory are a valid language version 1 file

    if the file has None the language version was higher than 1
    if the file has False it isn't a valid language file
    if the file has True it is a valid language file

    :param *paths: files/directories to check
    :return: Dictionary containing the name of files as keys and bool or none as values
    """

    status: Dict[str, Optional[bool]] = {}

    for path in paths:

        if isfile(path):
            async with Language() as lang:
                try:
                    await lang.async_from_file(path)
                except (IncompatibleLanguageVersion):
                    status[path] = None
                except (InvalidLanguageData):
                    status[path] = False
                else:
                    status[path] = True

        elif isdir(path):
            # Same logic for each file in a directory (this doesn't check subdirectories)
            for file in listdir(path):
                if isfile(join(path, file)):
                    async with Language() as lang:
                        try:
                            await lang.async_from_file(join(path, file))
                        except (IncompatibleLanguageVersion):
                            status[join(path, file)] = None
                        except (InvalidLanguageData):
                            status[join(path, file)] = False
                        else:
                            status[join(path, file)] = True

        else:
            status[path] = False

    return status
