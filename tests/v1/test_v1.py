from globalprogramlib.v1 import (
    Language,
    Translator,
    evaluate_coverage,
    async_evaluate_coverage,
)
import globalprogramlib.utils.errors
import pytest
from json import loads
from aiofiles import open as async_open

from os.path import isfile
from os import remove


def sync_readfile(path: str):
    if not isfile(path):
        raise FileNotFoundError()
    with open(path) as file:
        return file.read()


async def async_readfile(path: str):
    if not isfile(path):
        raise FileNotFoundError()
    async with async_open(path) as file:
        return await file.read()


pt_test_file_path = "tests/data/pt.json"
en_test_file_path = "tests/data/en.json"


class TestLanguageImportationExportation:
    # Sync
    def test_sync_import_invalid_language_dict(self):
        with pytest.raises(globalprogramlib.utils.errors.InvalidLanguageData):
            assert Language().from_dict({}) is None

    def test_sync_import_invalid_language_json(self):
        with pytest.raises(globalprogramlib.utils.errors.InvalidLanguageData):
            assert (
                Language().from_json(sync_readfile("tests/data/invalid/file.txt"))
                is None
            )

    def test_sync_import_invalid_language_file(self):
        with pytest.raises(globalprogramlib.utils.errors.InvalidLanguageData):
            assert Language().from_file("tests/data/invalid/file.txt") is None

    def test_sync_import_incompatible_language_dict(self):
        with pytest.raises(globalprogramlib.utils.errors.IncompatibleLanguageVersion):
            assert (
                Language().from_dict(loads(sync_readfile("tests/data/invalid/it.json")))
                is None
            )

    def test_sync_import_incompatible_language_json(self):
        with pytest.raises(globalprogramlib.utils.errors.IncompatibleLanguageVersion):
            assert (
                Language().from_json(sync_readfile("tests/data/invalid/it.json"))
                is None
            )

    def test_sync_import_incompatible_language_file(self):
        with pytest.raises(globalprogramlib.utils.errors.IncompatibleLanguageVersion):
            assert Language().from_file("tests/data/invalid/it.json") is None

    def test_sync_import_valid_language_dict(self, sync_pt_language: Language):
        assert (
            Language().from_dict(loads(sync_readfile(pt_test_file_path)))
            == sync_pt_language
        )

    def test_sync_import_valid_language_json(self, sync_pt_language: Language):
        assert (
            Language().from_json(sync_readfile(pt_test_file_path)) == sync_pt_language
        )

    def test_sync_import_valid_language_file(self, sync_pt_language: Language):
        file_language = Language().from_file(pt_test_file_path)
        assert file_language == sync_pt_language

    def test_sync_export_valid_language_dict(self, sync_pt_language: Language):
        assert loads(sync_readfile(pt_test_file_path)) == sync_pt_language.to_dict

    def test_sync_export_valid_language_json(self, sync_pt_language: Language):
        assert loads(sync_readfile(pt_test_file_path)) == loads(
            sync_pt_language.to_json
        )

    def test_sync_export_valid_language_file(self, sync_pt_language: Language):
        c = sync_pt_language.to_file("tests/pt_test.json")
        if c is None:
            raise FileNotFoundError(
                """Test failed because file can't be exported to tests directory
Please check permissions or verify the working state of method «to_file()» in the Language object"""
            )
        d = Language().from_file(c)
        remove(c)
        assert sync_pt_language == d

    # Async
    @pytest.mark.asyncio
    async def test_async_import_invalid_language_dict(self):
        with pytest.raises(globalprogramlib.utils.errors.InvalidLanguageData):
            assert await (await Language()).async_from_dict({}) is None

    @pytest.mark.asyncio
    async def test_async_import_invalid_language_json(self):
        with pytest.raises(globalprogramlib.utils.errors.InvalidLanguageData):
            assert (
                await (await Language()).async_from_json(
                    await async_readfile("tests/data/invalid/file.txt")
                )
                is None
            )

    @pytest.mark.asyncio
    async def test_async_import_invalid_language_file(self):
        with pytest.raises(globalprogramlib.utils.errors.InvalidLanguageData):
            assert (
                await (await Language()).async_from_file("tests/data/invalid/file.txt")
                is None
            )

    @pytest.mark.asyncio
    async def test_async_import_incompatible_language_dict(self):
        with pytest.raises(globalprogramlib.utils.errors.IncompatibleLanguageVersion):
            assert (
                await (await Language()).async_from_dict(
                    loads(await async_readfile("tests/data/invalid/it.json"))
                )
                is None
            )

    @pytest.mark.asyncio
    async def test_async_import_incompatible_language_json(self):
        with pytest.raises(globalprogramlib.utils.errors.IncompatibleLanguageVersion):
            assert (
                await (await Language()).async_from_json(
                    await async_readfile("tests/data/invalid/it.json")
                )
                is None
            )

    @pytest.mark.asyncio
    async def test_async_import_incompatible_language_file(self):
        with pytest.raises(globalprogramlib.utils.errors.IncompatibleLanguageVersion):
            assert (
                await (await Language()).async_from_file("tests/data/invalid/it.json")
                is None
            )

    @pytest.mark.asyncio
    async def test_async_import_valid_language_dict(self, async_pt_language: Language):
        assert (
            await (await Language()).async_from_dict(
                loads(await async_readfile(pt_test_file_path))
            )
            == async_pt_language
        )

    @pytest.mark.asyncio
    async def test_async_import_valid_language_json(self, async_pt_language: Language):
        assert (
            await (await Language()).async_from_json(
                await async_readfile(pt_test_file_path)
            )
            == async_pt_language
        )

    @pytest.mark.asyncio
    async def test_async_import_valid_language_file(self, async_pt_language: Language):
        file_language = await (await Language()).async_from_file(pt_test_file_path)
        assert file_language == async_pt_language

    @pytest.mark.asyncio
    async def test_async_export_valid_language_dict(self, async_pt_language: Language):
        assert (
            loads(await async_readfile(pt_test_file_path))
            == await async_pt_language.async_to_dict
        )

    @pytest.mark.asyncio
    async def test_async_export_valid_language_json(self, async_pt_language: Language):
        assert loads(await async_readfile(pt_test_file_path)) == loads(
            await async_pt_language.async_to_json
        )

    @pytest.mark.asyncio
    async def test_async_export_valid_language_file(self, async_pt_language: Language):
        c = await async_pt_language.async_to_file("tests/pt_test.json")
        if c is None:
            raise FileNotFoundError(
                """Test failed because file can't be exported to tests directory
Please check permissions or verify the working state of method «to_file()» in the Language object"""
            )
        d = await (await Language()).async_from_file(c)
        remove(c)
        assert async_pt_language == d


class TestLanguageAttributes:
    def test_len_language(self, sync_pt_language: Language):
        assert len(sync_pt_language) == len(sync_pt_language.translations)

    def test_eq_language(self, sync_pt_language, async_pt_language):
        assert sync_pt_language == async_pt_language

    def test_repr_language(self, sync_pt_language: Language):
        assert repr(sync_pt_language) == sync_pt_language.name

    def test_str_language(self, sync_pt_language: Language):
        assert str(sync_pt_language) == sync_pt_language.name

    def test_contains_language(self, sync_pt_language: Language):
        assert (
            "bot.thank_message" in sync_pt_language
            and not "bot.invalid_message" in sync_pt_language
        )

    def test_sync_instance_language(self):
        assert isinstance(Language(), Language)

    def test_sync_context_manager_language(self, sync_pt_language: Language):
        result1 = False
        result2 = False
        with Language() as e:
            e.from_dict(sync_pt_language.to_dict)
            if e == sync_pt_language:
                result1 = True
        if e != sync_pt_language:
            result2 = True
        assert result1 and result2

    def test_sync_is_ready_invalid_language(self):
        assert Language().is_ready() == False

    def test_sync_is_ready_valid_language(self, sync_pt_language):
        assert sync_pt_language.is_ready()

    @pytest.mark.asyncio
    async def test_async_instance_language(self):
        assert isinstance(await Language(), Language)

    @pytest.mark.asyncio
    async def test_async_context_manager_language(self, async_pt_language: Language):
        result1 = False
        result2 = False
        async with Language() as e:
            await e.async_from_dict(await async_pt_language.async_to_dict)
            if e == async_pt_language:
                result1 = True
        if e != async_pt_language:
            result2 = True
        assert result1 and result2

    @pytest.mark.asyncio
    async def test_async_is_ready_invalid_language(self):
        assert await (await Language()).async_is_ready() == False

    @pytest.mark.asyncio
    async def test_async_is_ready_valid_language(self, async_pt_language):
        assert await async_pt_language.async_is_ready()


class TestLanguageMethods:
    def test_sync_clear_language(self, sync_pt_language):
        lang = Language().from_dict(sync_pt_language.to_dict)
        assert lang.clear() == Language()

    def test_sync_valid_is_translatable(self, sync_pt_language: Language):
        assert sync_pt_language.is_translatable("bot.thank_message")

    def test_sync_invalid_is_translatable(self, sync_pt_language: Language):
        assert sync_pt_language.is_translatable("bot.message") == False

    def test_sync_valid_remove_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        g = l.remove_translation("bot.thank_message")
        f = l.is_translatable("bot.thank_message") == False
        assert g is not None and f

    def test_sync_invalid_remove_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        assert l.remove_translation("bot.message") == None

    def test_sync_valid_get_translation(self, sync_pt_language: Language):
        g = sync_pt_language.get_translation("bot.thank_message")
        assert (
            g
            == sync_pt_language.translations["bot.thank_message"]
            != None
            != "bot.thank_message"
        )

    def test_sync_invalid_default_get_translation(self, sync_pt_language: Language):
        g = sync_pt_language.get_translation("bot.message")
        e = sync_pt_language.get_translation("bot.message", "not_found")
        assert g == "bot.message" and e == "not_found"

    def test_sync_invalid_throw_get_translation(self, sync_pt_language: Language):
        with pytest.raises(globalprogramlib.utils.errors.TranslationKeyNotFound):
            sync_pt_language.get_translation("bot.message", throw_not_found=True)

    def test_sync_non_existent_set_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        h = l.set_translation("bot.message", "created")
        assert h is not None and h == l.get_translation("bot.message")

    def test_sync_existent_keep_set_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        g = l.get_translation("bot.thank_message")
        h = l.set_translation("bot.thank_message", "overrided")
        assert h is None and l.get_translation("bot.thank_message") == g

    def test_sync_existent_override_set_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        g = l.get_translation("bot.thank_message", True)
        h = l.set_translation("bot.thank_message", "overrided", True)
        assert h is not None and h == l.get_translation("bot.thank_message") != g

    def test_sync_old_key_invalid_rename_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        assert (
            l.rename_translation("bot.message", "bot.d") == None
            and not l.is_translatable("bot.message")
            and not l.is_translatable("bot.d")
        )

    def test_sync_new_key_keep_existent_rename_translation(
        self, sync_pt_language: Language
    ):
        i = Language().from_dict(sync_pt_language.to_dict)
        l = i.get_translation("bot.thank_message")
        assert (
            i.rename_translation(
                "bot.bye_message",
                "bot.thank_message",
                keep_old_key=False,
                override=False,
            )
            == None
            and i.get_translation("bot.thank_message") == l
            and i.is_translatable("bot.bye_message")
        )

    def test_sync_new_key_override_rename_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        b = l.get_translation("bot.bye_message")
        i = l.get_translation("bot.thank_message")
        assert (
            l.rename_translation(
                "bot.bye_message",
                "bot.thank_message",
                keep_old_key=False,
                override=True,
            )
            == "bot.thank_message"
            and l.is_translatable("bot.thank_message")
            and (b == l.get_translation("bot.thank_message") != i)
            and not l.is_translatable("bot.bye_message")
        )

    def test_sync_key_copy_rename_translation(self, sync_pt_language: Language):
        l = Language().from_dict(sync_pt_language.to_dict)
        b = l.get_translation("bot.bye_message")
        i = l.get_translation("bot.thank_message")
        assert (
            l.rename_translation(
                "bot.bye_message", "bot.thank_message", keep_old_key=True, override=True
            )
            == "bot.thank_message"
            and l.is_translatable("bot.thank_message")
            and (
                b
                == l.get_translation("bot.thank_message")
                == l.get_translation("bot.bye_message")
                != i
            )
            and l.is_translatable("bot.bye_message")
        )

    @pytest.mark.asyncio
    async def test_async_clear_language(self, async_pt_language):
        lang = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        assert await lang.async_clear() == Language()

    @pytest.mark.asyncio
    async def test_async_valid_is_translatable(self, async_pt_language: Language):
        assert await async_pt_language.async_is_translatable("bot.thank_message")

    @pytest.mark.asyncio
    async def test_async_invalid_is_translatable(self, async_pt_language: Language):
        assert await async_pt_language.async_is_translatable("bot.message") == False

    @pytest.mark.asyncio
    async def test_async_valid_remove_translation(self, async_pt_language: Language):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        g = await l.async_remove_translation("bot.thank_message")
        f = await l.async_is_translatable("bot.thank_message") == False
        assert g is not None and f

    @pytest.mark.asyncio
    async def test_async_invalid_remove_translation(self, async_pt_language: Language):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        assert await l.async_remove_translation("bot.message") == None

    @pytest.mark.asyncio
    async def test_async_valid_get_translation(self, async_pt_language: Language):
        g = await async_pt_language.async_get_translation("bot.thank_message")
        assert (
            g
            == async_pt_language.translations["bot.thank_message"]
            != None
            != "bot.thank_message"
        )

    @pytest.mark.asyncio
    async def test_async_invalid_default_get_translation(
        self, async_pt_language: Language
    ):
        g = await async_pt_language.async_get_translation("bot.message")
        e = await async_pt_language.async_get_translation("bot.message", "not_found")
        assert g == "bot.message" and e == "not_found"

    @pytest.mark.asyncio
    async def test_async_invalid_throw_get_translation(
        self, async_pt_language: Language
    ):
        with pytest.raises(globalprogramlib.utils.errors.TranslationKeyNotFound):
            await async_pt_language.async_get_translation(
                "bot.message", throw_not_found=True
            )

    @pytest.mark.asyncio
    async def test_async_non_existent_set_translation(
        self, async_pt_language: Language
    ):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        h = await l.async_set_translation("bot.message", "created")
        assert h is not None and h == await l.async_get_translation("bot.message")

    @pytest.mark.asyncio
    async def test_async_existent_keep_set_translation(
        self, async_pt_language: Language
    ):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        g = await l.async_get_translation("bot.thank_message")
        h = await l.async_set_translation("bot.thank_message", "overrided")
        assert h is None and await l.async_get_translation("bot.thank_message") == g

    @pytest.mark.asyncio
    async def test_async_existent_override_set_translation(
        self, async_pt_language: Language
    ):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        g = await l.async_get_translation("bot.thank_message", True)
        h = await l.async_set_translation("bot.thank_message", "overrided", True)
        assert (
            h is not None
            and h == await l.async_get_translation("bot.thank_message") != g
        )

    @pytest.mark.asyncio
    async def test_async_old_key_invalid_rename_translation(
        self, async_pt_language: Language
    ):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        assert (
            await l.async_rename_translation("bot.message", "bot.d") == None
            and not await l.async_is_translatable("bot.message")
            and not await l.async_is_translatable("bot.d")
        )

    @pytest.mark.asyncio
    async def test_async_new_key_keep_existent_rename_translation(
        self, async_pt_language: Language
    ):
        i = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        l = await i.async_get_translation("bot.thank_message")
        assert (
            await i.async_rename_translation(
                "bot.bye_message",
                "bot.thank_message",
                keep_old_key=False,
                override=False,
            )
            == None
            and await i.async_get_translation("bot.thank_message") == l
            and await i.async_is_translatable("bot.bye_message")
        )

    @pytest.mark.asyncio
    async def test_async_new_key_override_rename_translation(
        self, async_pt_language: Language
    ):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        b = await l.async_get_translation("bot.bye_message")
        i = await l.async_get_translation("bot.thank_message")
        assert (
            await l.async_rename_translation(
                "bot.bye_message",
                "bot.thank_message",
                keep_old_key=False,
                override=True,
            )
            == "bot.thank_message"
            and await l.async_is_translatable("bot.thank_message")
            and (b == await l.async_get_translation("bot.thank_message") != i)
            and not await l.async_is_translatable("bot.bye_message")
        )

    @pytest.mark.asyncio
    async def test_async_key_copy_rename_translation(self, async_pt_language: Language):
        l = await (await Language()).async_from_dict(
            await async_pt_language.async_to_dict
        )
        b = await l.async_get_translation("bot.bye_message")
        i = await l.async_get_translation("bot.thank_message")
        assert (
            await l.async_rename_translation(
                "bot.bye_message", "bot.thank_message", keep_old_key=True, override=True
            )
            == "bot.thank_message"
            and await l.async_is_translatable("bot.thank_message")
            and (
                b
                == await l.async_get_translation("bot.thank_message")
                == await l.async_get_translation("bot.bye_message")
                != i
            )
            and await l.async_is_translatable("bot.bye_message")
        )


class TestCoverageEvaluator:
    def test_sync_no_argument_evaluator_coverage(self):
        assert evaluate_coverage() == None

    def test_sync_invalid_language_evaluator_coverage(self):
        assert evaluate_coverage(Language(), None) == None

    def test_sync_export_analyzed_languages_evaluator_coverage(
        self, sync_pt_language: Language
    ):
        g = evaluate_coverage(sync_pt_language, export_analyzed_languages=True)
        f = evaluate_coverage(sync_pt_language, export_analyzed_languages=False)
        assert (
            "analyzed_languages" not in f
            and len(g["analyzed_languages"]) == 1
            and g["analyzed_languages"][0] == sync_pt_language
        )

    def test_sync_one_valid_invalid_evaluator_coverage(
        self, sync_pt_language: Language
    ):
        g = evaluate_coverage(
            None, sync_pt_language, Language(), export_analyzed_languages=True
        )
        assert (
            g["global_avg_keys_percent"] == 100
            and len(g["analyzed_languages"]) == 1
            and g["analyzed_languages"][0] == sync_pt_language
        )

    def test_sync_one_valid_evaluator_coverage(self, sync_pt_language: Language):
        g = evaluate_coverage(sync_pt_language, export_analyzed_languages=True)
        assert (
            g["global_avg_keys_percent"] == 100
            and len(g["analyzed_languages"]) == 1
            and g["analyzed_languages"][0] == sync_pt_language
        )

    def test_sync_multiple_valid_invalid_evaluator_coverage(
        self, sync_pt_language: Language, sync_en_language
    ):
        g = evaluate_coverage(
            sync_en_language,
            None,
            sync_pt_language,
            Language(),
            export_analyzed_languages=True,
        )
        test_avg = g["global_avg_keys_percent"] == 75.0
        test_num_lang = len(g["analyzed_languages"]) == 2
        test_missing_keys = len(g["global_missing_keys"]) == 2
        assert test_avg and test_num_lang and test_missing_keys

    def test_sync_multiple_valid_evaluator_coverage(
        self, sync_pt_language: Language, sync_en_language
    ):
        g = evaluate_coverage(
            sync_en_language, sync_pt_language, export_analyzed_languages=True
        )
        test_avg = g["global_avg_keys_percent"] == 75.0
        test_num_lang = len(g["analyzed_languages"]) == 2
        test_missing_keys = len(g["global_missing_keys"]) == 2
        assert test_avg and test_num_lang and test_missing_keys

    # Async

    @pytest.mark.asyncio
    async def test_async_no_argument_evaluator_coverage(self):
        assert await async_evaluate_coverage() == None

    @pytest.mark.asyncio
    async def test_async_invalid_language_evaluator_coverage(self):
        assert await async_evaluate_coverage(await Language(), None) == None

    @pytest.mark.asyncio
    async def test_async_export_analyzed_languages_evaluator_coverage(
        self, async_pt_language: Language
    ):
        g = await async_evaluate_coverage(
            async_pt_language, export_analyzed_languages=True
        )
        f = await async_evaluate_coverage(
            async_pt_language, export_analyzed_languages=False
        )
        assert (
            "analyzed_languages" not in f
            and len(g["analyzed_languages"]) == 1
            and g["analyzed_languages"][0] == async_pt_language
        )

    @pytest.mark.asyncio
    async def test_async_one_valid_invalid_evaluator_coverage(
        self, async_pt_language: Language
    ):
        g = await async_evaluate_coverage(
            None, async_pt_language, await Language(), export_analyzed_languages=True
        )
        assert (
            g["global_avg_keys_percent"] == 100
            and len(g["analyzed_languages"]) == 1
            and g["analyzed_languages"][0] == async_pt_language
        )

    @pytest.mark.asyncio
    async def test_async_one_valid_evaluator_coverage(
        self, async_pt_language: Language
    ):
        g = await async_evaluate_coverage(
            async_pt_language, export_analyzed_languages=True
        )
        assert (
            g["global_avg_keys_percent"] == 100
            and len(g["analyzed_languages"]) == 1
            and g["analyzed_languages"][0] == async_pt_language
        )

    @pytest.mark.asyncio
    async def test_async_multiple_valid_invalid_evaluator_coverage(
        self, async_pt_language: Language, async_en_language
    ):
        g = await async_evaluate_coverage(
            async_en_language,
            None,
            async_pt_language,
            await Language(),
            export_analyzed_languages=True,
        )
        test_avg = g["global_avg_keys_percent"] == 75.0
        test_num_lang = len(g["analyzed_languages"]) == 2
        test_missing_keys = len(g["global_missing_keys"]) == 2
        assert test_avg and test_num_lang and test_missing_keys

    @pytest.mark.asyncio
    async def test_async_multiple_valid_evaluator_coverage(
        self, async_pt_language: Language, async_en_language
    ):
        g = await async_evaluate_coverage(
            async_en_language, async_pt_language, export_analyzed_languages=True
        )
        test_avg = g["global_avg_keys_percent"] == 75.0
        test_num_lang = len(g["analyzed_languages"]) == 2
        test_missing_keys = len(g["global_missing_keys"]) == 2
        assert test_avg and test_num_lang and test_missing_keys


class TestTranslatorAttributes:
    def test_len_translator(self, translator: Translator):
        assert len(translator) == len(translator.languages_loaded)

    def test_eq_translator(self, translator, async_translator):
        assert (translator == async_translator) and (translator != Translator())

    def test_repr_translator(self, translator: Translator):
        assert repr(translator) == repr([*translator.languages_loaded.values()])

    def test_str_translator(self, translator: Translator):
        assert str(translator) == repr([*translator.languages_loaded.values()])

    def test_contains_translator(self, translator: Translator):
        assert "pt" in translator and not "it" in translator

    def test_sync_instance_translator(self, translator):
        assert isinstance(Translator(), Translator)

    def test_sync_context_manager_translator(self, translator):
        result1 = False
        result2 = False
        with Translator() as e:

            e.load_file(pt_test_file_path)
            e.load_file(en_test_file_path)
            if e == translator:
                result1 = True
        if e != translator and e.is_ready == False:
            result2 = True
        assert result1 and result2

    def test_sync_is_ready_invalid_translator(self):
        assert Translator().is_ready == False

    def test_sync_is_ready_valid_translator(self, translator):
        assert translator.is_ready

    def test_sync_default_language_valid_translator(self, translator):
        assert (
            translator.DefaultLanguageCode in translator.languages_loaded
            and isinstance(translator.default_language, Language)
        )

    def test_sync_default_language_invalid_translator(self):
        g = Translator()
        g.DefaultLanguageCode = "pt"
        assert (
            g.DefaultLanguageCode not in g.languages_loaded
            and g.default_language is None
        )

    def test_sync_selected_language_valid_translator(self, translator):
        assert (
            translator.SelectedLanguageCode in translator.languages_loaded
            and isinstance(translator.selected_language, Language)
        )

    def test_sync_selected_language_invalid_translator(self):
        g = Translator()
        g.SelectedLanguageCode = "pt"
        assert (
            g.SelectedLanguageCode not in g.languages_loaded
            and g.selected_language is None
        )

    def test_sync_coverage_no_language_translator(self, translator):
        assert Translator().coverage == None

    def test_sync_coverage_valid_translator(self, translator):
        coverage = translator.coverage
        assert (
            coverage is not None
            and "bot.bye_message" in coverage["global_missing_keys"]["en"]
        )

    # Async

    @pytest.mark.asyncio
    async def test_async_instance_translator(self):
        assert isinstance(await Translator(), Translator)

    @pytest.mark.asyncio
    async def test_async_context_manager_translator(self, async_translator):
        result1 = False
        result2 = False
        async with Translator() as e:

            await e.async_load_file(pt_test_file_path)
            await e.async_load_file(en_test_file_path)
            if e == async_translator:
                result1 = True
        if e != async_translator and await e.async_is_ready == False:
            result2 = True
        assert result1 and result2

    @pytest.mark.asyncio
    async def test_async_is_ready_invalid_translator(self):
        assert await (await Translator()).async_is_ready == False

    @pytest.mark.asyncio
    async def test_async_is_ready_valid_translator(self, async_translator):
        assert await async_translator.async_is_ready

    @pytest.mark.asyncio
    async def test_async_default_language_valid_translator(self, async_translator):
        assert (
            async_translator.DefaultLanguageCode in async_translator.languages_loaded
            and isinstance(await async_translator.async_default_language, Language)
        )

    @pytest.mark.asyncio
    async def test_async_default_language_invalid_translator(self):
        g = await Translator()
        g.DefaultLanguageCode = "pt"
        assert (
            g.DefaultLanguageCode not in g.languages_loaded
            and await g.async_default_language is None
        )

    @pytest.mark.asyncio
    async def test_async_selected_language_valid_translator(self, async_translator):
        assert (
            async_translator.SelectedLanguageCode in async_translator.languages_loaded
            and isinstance(await async_translator.selected_language, Language)
        )

    @pytest.mark.asyncio
    async def test_async_selected_language_invalid_translator(self):
        g = await Translator()
        g.SelectedLanguageCode = "pt"
        assert (
            g.SelectedLanguageCode not in g.languages_loaded
            and await g.async_selected_language is None
        )

    @pytest.mark.asyncio
    async def test_async_coverage_no_language_translator(self, translator):
        assert await (await Translator()).async_coverage == None

    @pytest.mark.asyncio
    async def test_async_coverage_valid_translator(self, translator):
        coverage = await translator.async_coverage
        assert (
            coverage is not None
            and "bot.bye_message" in coverage["global_missing_keys"]["en"]
        )


class TestTranslatorMethods:
    pass
