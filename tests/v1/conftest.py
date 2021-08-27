import pytest
from globalprogramlib.v1 import Language, Translator


@pytest.fixture()
def sync_pt_language():
    pt = Language()
    pt.name = "Portugu\u00eas"
    pt.code = "pt"
    pt.version = 1
    pt.revision = 1
    pt.authors = ["PWRScript"]
    pt.contributors = []
    pt.translations = {"bot.bye_message": "Adeus", "bot.thank_message": "Obrigado"}
    return pt


@pytest.fixture()
async def async_pt_language():
    pt = await Language()
    pt.name = "Portugu\u00eas"
    pt.code = "pt"
    pt.version = 1
    pt.revision = 1
    pt.authors = ["PWRScript"]
    pt.contributors = []
    pt.translations = {"bot.bye_message": "Adeus", "bot.thank_message": "Obrigado"}
    return pt


@pytest.fixture()
def sync_en_language():
    en = Language()
    en.name = "English"
    en.code = "en"
    en.version = 1
    en.revision = 1
    en.authors = ["PWRScript"]
    en.contributors = []
    en.translations = {"bot.thank_message": "Thanks"}
    return en


@pytest.fixture()
async def async_en_language():
    en = await Language()
    en.name = "English"
    en.code = "en"
    en.version = 1
    en.revision = 1
    en.authors = ["PWRScript"]
    en.contributors = []
    en.translations = {"bot.thank_message": "Thanks"}
    return en


@pytest.fixture()
def translator():
    tr = Translator()
    tr.load_file("tests/data/pt.json")
    tr.load_file("tests/data/en.json")
    tr.DefaultLanguageCode = "en"
    tr.SelectedLanguageCode = "pt"
    return tr


@pytest.fixture()
async def async_translator():
    tr = await Translator()
    await tr.async_load_file("tests/data/en.json")
    await tr.async_load_file("tests/data/pt.json")
    tr.DefaultLanguageCode = "en"
    tr.SelectedLanguageCode = "pt"
    return tr
