#!/usr/bin/env python3
from globalprogramlib.v1 import Language, check_language_file, evaluate_coverage
from globalprogramlib.utils import errors
from sys import argv

def main():
    print("*************************************")
    print("*    Language Coverage Evaluator    *")
    print("*       for globalprogramlib        *")
    print("*                                   *")
    print("*  Only analyzes v1 language files  *")
    print("*                                   *")
    print("*************************************")
    print(
        "\n[1] Checking language files to evaluate coverage (this might take a while...)"
    )

    try:
        files = check_language_file(*argv[1:])
    except (PermissionError):
        print(
            "\n    [CRITICAL] Looks like some software is using your files, so please close them first and then evaluate it"
        )
        exit(13)

    files_to_load = []  # Will be used to store valid files of the arguments

    for file in files:
        if files[file] == False:
            print(
                f"    [INVALID] Not using '{file}' because it isn't a valid language file"
            )
        elif files[file] == None:
            print(
                f"    [INCOMPATIBLE] Not using '{file}' because it has a higher language version"
            )
        elif files[file] == True:
            files_to_load.append(file)
            print(f"    [LOADED] Using '{file}'")
    if len(files_to_load) > 0:
        print(
            f"    [SUCCESS] {len(files_to_load)} files have been prepared for load, proceeding to next step\n"
        )
    else:
        print(
            f"    [FAILURE] You have specified no files/directories or the specified files are invalid, so won't proceed without files to analyze\n"
        )
        exit(1)
    del files

    languages = []

    l_n = {}

    print("[2] Loading files into memory")
    for file in files_to_load:
        language = Language().from_file(file)
        languages.append(language)
        l_n[language.code] = language.name
        print(f"    [LOADED] {file} as {language} ({language.code})")
    print(
        f"    [SUCCESS] {len(languages)} languages have been loaded, proceeding to next step\n"
    )
    del files_to_load

    print("[3] Executing coverage report test (this might take a while)")
    print("    [OK] Started coverage test")
    report = evaluate_coverage(*languages, export_analyzed_languages=True)

    print("    [SUCCESS] Finished coverage test\n")

    print("[4] Showing coverage report test results")
    print("\n    [Present languages]")
    for language in report["analyzed_languages"]:
        language: Language
        print(f"        «{language.code}» as {language.name}")
        print(f"            Authors: {language.authors}")
        print(f"            Contributors: {language.contributors}")
        print(f"            Revision: {language.revision}")
        print(f"            Translations: {len(language)} present")
        for tr in language.translations:
            print(f"                «{tr}» translates to '{language.translations[tr]}'")
        print()

    print("    [Missing Translation Keys]")
    for language in report["global_missing_keys"]:
        for key in report["global_missing_keys"][language]:
            print(f"        «{language}» doesn't have translation for «{key}»")

    print("\n    [Global Coverage Status]")
    print(
        f"        All languages have a medium global coverage of {report['global_avg_keys_percent']}% and {report['global_avg_keys']} translations present"
    )
    for language in report["global_coverage_percent"]:
        print(
            f"        «{language}» has {report['global_coverage_percent'][language]}% of global coverage ({len(report['global_all_keys']) - len(report['global_missing_keys'][language])} translations present)"
        )
    print()


if __name__ == "__main__":
    main()