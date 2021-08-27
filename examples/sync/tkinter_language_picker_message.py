# globalprogramlib GUI example by PWRScript

# Import necessary libs
import tkinter
from globalprogramlib.v1 import Language, Translator


class App(tkinter.Tk):
    def __init__(self, translator: Translator, *args, **kwargs) -> None:
        """
        This class will take care of creating our application
        This isn't the best sample, but will demonstrate the
        principles of globalprogramlib using a sync GUI lib
        """
        super().__init__(*args, **kwargs)

        # Master canvas (for easely clear all screen)
        self.master_canvas = tkinter.Canvas(self)
        self.master_canvas.pack()

        # Make translator instance available for all class
        self.translator: Translator = translator

        # Render app
        self.render_choose_language_window()

    def clear_screen(self):
        """
        Deletes all widgets rendered in the Tkinter application
        by destroying the canvas and replacing it
        """
        self.master_canvas.destroy()
        self.master_canvas = tkinter.Canvas(self)
        self.master_canvas.pack()

    def render_choose_language_window(self):
        """
        This function is the render for our application
        """
        # Ensure that screen is cleared every reload to avoid duplicate widgets
        self.clear_screen()

        # Creates a new label
        # Displays the language pick message in current selected language in Translator
        # using translator.get_translation("pwrscript.guiapp.language_picker")
        tkinter.Label(
            self.master_canvas,
            text=self.translator.get_translation("pwrscript.guiapp.language_picker"),
        ).pack()

        # This will store the current selected language in translator
        # to be show in the "OptionMenu" widget
        language = tkinter.StringVar(self.master_canvas)
        language.set(self.translator.selected_language)

        tkinter.Label(
            self.master_canvas,
            text=self.translator.get_translation("pwrscript.guiapp.important_message"),
        ).pack()

        tkinter.OptionMenu(
            self.master_canvas,
            language,
            # Here we pass all Languages in the translator to the OptionMenu as separated arguments
            *self.translator.languages_loaded.values(),
            command=(
                # I know this isn't beginner friendly, but I will explain everything
                #
                # I need to execute an assignment (translator.SelectedLanguageCode = «selected language code»)
                # and to re-render this «window» using self.render_choose_language_window() when user changes the language (event)
                #
                # Unfortunately tkinter "command" only accepts a unique function with one argument (the value selected)
                #
                # This leaded to render issues and self not being available (no access to translator/application) when I tried
                # to implement a «beginner friendly» code for "command"
                #
                # To acoplish this tasks, I needed to create a lambda (a unique line function) which accepts the argument need
                # by the OptionMenu "command" [lang] and the [self] (for getting the translator and application) which is a automatically
                # passed when this «event» is «executed»
                #
                # To solve the assignment issue I defined the SelectedLanguageCode attribute in the translator using the built-in object method
                # __set_attr__ since you cannot assign values in a lambda (the best approach to use in other environments is
                # translator.SelectedLanguageCode = «selected_language_code»)
                #
                # The other issue, «re-rendering» was solved by the content in the 4th paragraph
                #
                lambda lang, self=self: [
                    self.translator.__setattr__("SelectedLanguageCode", lang.code),
                    self.render_choose_language_window(),
                ]
            )
        ).pack()


def BuildTranslator():
    """
    This function will take care of creating the translations dynamicaly at runtime, without
    needing dependent files, which is ideal for examples and the translator object ready for
    use
    """

    # Other way to do this, persisting the files in a folder and generating it at runtime if need (example: langs)
    """
    # load_translations.py
    from os.path import is_file, is_dir, join
    from os import mkdir
    
    TRANSLATIONS_FOLDER = "langs"
    
    if not is_dir(TRANSLATIONS_FOLDER):
        mkdir(TRANSLATIONS_FOLDER)
    
    if not is_file(join(TRANSLATIONS_FOLDER,"pt.json"))
        with Language() as pt:
            pt.name = "Português"
            pt.code = "pt"
            pt.version = 1  # The version needs to be always 1 in this case
            pt.revision = 1  # This is what you need to touch when you need to upgrade the version of the language
            pt.authors = [
                "PWRScript"
            ]  # You can add authors and contributors with their name like this or "name <email>"
            pt.contributors = []
            # Creating translations for our app
            pt.set_translation("pwrscript.guiapp.language_picker", "Escolha o seu idioma:") 
            # Saving the translation to a file
            pt.to_file(join(TRANSLATIONS_FOLDER,"pt.json"))

        # When the context ends, the language file is always cleaned to ensure that it doesn't overflow system resources, so it will look like a new
        # instanced Language() and can be clean at any moment by the garbage collector

        # This object can be clean since it won't be used again
        del pt

    if not is_file(join(TRANSLATIONS_FOLDER,"en.json"))
        with Language() as en:
            en.name = "English"
            en.code = "en"
            en.version = 1  # The version needs to be always 1 in this case
            en.revision = 1  # This is what you need to touch when you need to upgrade the version of the language
            en.authors = [
                "PWRScript"
            ]  # You can add authors and contributors with their name like this or "name <email>"
            en.contributors = []
            # Creating translations for our app
            en.set_translation("pwrscript.guiapp.language_picker", "Pick your language:") 
            # Saving the translation to a file
            en.to_file(join(TRANSLATIONS_FOLDER,"en.json"))
        del en 

    translator = Translator()
    translator.load_directory(TRANSLATIONS_FOLDER)
    translator.DefaultLanguageCode = "en"
    translator.SelectedLanguageCode = "en"
    """

    # PT Language instantiation
    pt = Language()
    # Add language information
    pt.name = "Português"
    pt.code = "pt"
    pt.version = 1  # The version needs to be always 1 in this case
    pt.revision = 1  # This is what you need to touch when you need to upgrade the version of the language
    pt.authors = [
        "PWRScript"
    ]  # You can add authors and contributors with their name like this or "name <email>"
    pt.contributors = []
    # Creating translations for our app
    pt.set_translation("pwrscript.guiapp.language_picker", "Escolha o seu idioma:")
    pt.set_translation("pwrscript.guiapp.important_message", "Funcionando em Português")

    # EN Language instantiation
    en = Language()
    # Add language information
    en.name = "English"
    en.code = "en"
    en.version = 1  # The version needs to be always 1 in this case
    en.revision = 1  # This is what you need to touch when you need to upgrade the version of the language
    en.authors = [
        "PWRScript"
    ]  # You can add authors and contributors with their name like this or "name <email>"
    en.contributors = []
    # Creating translations for our app
    en.set_translation("pwrscript.guiapp.language_picker", "Pick your language:")
    en.set_translation("pwrscript.guiapp.important_message", "Working in English")

    # Translator creation
    translator = Translator()
    # Loading languages from the created Language() objects
    translator.load_languages(pt, en)

    # Sets the default (fallback language used when translation can't be found in the selected_language)
    # and the selected (first language)
    # This is obligatory since the get_translation() method needs to now what languages to use and the codes
    # must be valid code languages in the translator (loaded languages) else it won't translate anyting and
    # willalways return None
    translator.DefaultLanguageCode = "en"
    translator.SelectedLanguageCode = "en"

    return translator


if __name__ == "__main__":
    # Creates the translator for use with the Tkinter class app
    translator = BuildTranslator()

    # Instances the application class and runs the application
    application = App(translator)
    application.mainloop()
