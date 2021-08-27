class GlobalProgramLibException(BaseException):
    """
    All exceptions in this lib must derive from this
    """

    pass


class IncompatibleLanguageVersion(GlobalProgramLibException):
    """
    Raises when you try to load a language data that is incompatible with the actual Language object
    """

    pass


class InvalidLanguageData(GlobalProgramLibException):
    """
    Raises when you try to load a file that is not a language, has syntax erros or is incomplete
    """

    pass


class TranslationKeyNotFound(GlobalProgramLibException):
    """
    Raises when the specified translation key is not found in a language
    """

    pass
