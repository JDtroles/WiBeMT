import json
import os
import requests
import uuid
from time import sleep

import six
from dotenv import load_dotenv
from tqdm import tqdm
from google.cloud import translate_v2 as translate


from misc import split_list_equally
from reader_saver import load_nested_list_to_list, write_nested_list_to_file
from translation_api_tester import create_json_output_corresponding_to_input


def translate_sentences_via_api(api: str = "Microsoft", dataset_type: str = "Verb_sentences"):
    """

    :param api: "Microsoft" or "Google"
    :type api: str
    :param dataset_type: "Verb_sentences" or "WinoBias_sentences"
    :type dataset_type: str
    """

    print("Please select the corresponding data to:", dataset_type)
    sentences_info = load_nested_list_to_list()

    # TODO: add try catch phrase?
    # create new list with sublist which only contains the id and the sentence
    id_plus_sentences = []
    if dataset_type == "Verb_sentences":
        for sub_list in sentences_info:
            id_plus_sentences.append([sub_list[0], sub_list[1]])
    else:
        for sub_list in sentences_info:
            id_plus_sentences.append([sub_list[7], sub_list[2]])
    print("id_plus_sentences:")
    print(id_plus_sentences[0:5])

    # create a list with batches of 50 sentences
    id_plus_sentences_chunked = list(split_list_equally(id_plus_sentences, 30))
    print("len of sublist:")
    print(len(id_plus_sentences_chunked[0]))

    # create list of dict and list of id's for translation api
    all_translations = []
    descr_str = "Translating with " + api + " Translate:"
    for chunk in tqdm(id_plus_sentences_chunked, desc=descr_str):
        sleep(0.5)
        # send chunk to translation api
        if api == "Microsoft":
            # TODO: write method
            all_translations.append(microsoft_api_caller(chunk))
        elif api == "Google":
            # TODO: write method
            all_translations.append(google_api_caller(chunk))

    # append translation to list for verb_sentences
    sentences_info_with_translations = []
    if dataset_type == "Verb_sentences":
        for translations_batch in tqdm(all_translations, desc="Appending translation to list: "):
            for translation in translations_batch:
                for sentence in sentences_info:
                    if translation[0] == sentence[0]:
                        sentence.append(translation[1])
                        sentences_info_with_translations.append(sentence)
    elif dataset_type == "WinoBias_sentences":
        for translations_batch in all_translations:
            for translation in translations_batch:
                for sentence in sentences_info:
                    if translation[0] == sentence[7]:
                        sentence.append(translation[1])
                        sentences_info_with_translations.append(sentence)

    print("sentences_info_with_translations:")
    print(sentences_info_with_translations[0:5])
    write_nested_list_to_file(sentences_info)
    return


def google_api_caller(sentences_to_translate: list, test: bool = False) -> list:
    # create correct format and id list
    ids_sentences = []
    sentences = []
    for sentence in sentences_to_translate:
        ids_sentences.append(sentence[0])
        sentences.append(sentence[1])

    load_dotenv()

    # intialize client and parameters
    translate_client = translate.Client()
    model = "nmt"
    source = "en"
    target = "de"

    if isinstance(sentences, six.binary_type):
        text = sentences.decode("utf-8")

    result = translate_client.translate(sentences, target_language=target, source_language=source, model=model)

    # TODO: INSERT NEW KEY TO .env
    translations = []
    for text_id, text in zip(ids_sentences, result):
        try:
            translations.append([text_id, text['translatedText']])
        except TypeError:
            print("text_id:", text_id)
            print("text:", text)
            print(result)
            try:
                translations.append([text_id, text['error']['code']])
            except TypeError:
                translations.append([text_id, text])

    # print("Translation after saving translations with id in sub_lists:")
    # print(translations[0:5])
    return translations

    # translate(values, target_language=None, format_=None, source_language=None, customization_ids=(), model=None)
    # values = str or list
    # format_ = "text" or "html"
    # return type = str or list
    # Returns: a list of dict -> each dict contains keys "translatedText", "input", "model"


def microsoft_api_caller(sentences_to_translate: list, test: bool = False) -> list:
    load_dotenv()
    # create correct format and id list
    dict_sentences = []
    ids_sentences = []
    for sentence in sentences_to_translate:
        ids_sentences.append(sentence[0])
        dict_sentences.append({"text": sentence[1]})
        # TODO: test implementation
    if test:
        response = create_json_output_corresponding_to_input(dict_sentences)
    else:
        # check if key exists in .env
        key_var_name = 'MICROSOFT_TRANSLATE_TEXT_API_KEY'
        if key_var_name not in os.environ:
            raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
        subscription_key = os.environ[key_var_name]

        # check if translatio endpoint exists in .env
        endpoint_var_name = 'MICROSOFT_TRANSLATE_TEXT_ENDPOINT'
        if endpoint_var_name not in os.environ:
            raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
        endpoint = os.environ[endpoint_var_name]

        # create complete url
        path = '/translate?api-version=3.0'
        params = '&from=en&to=de'
        constructed_url = endpoint + path + params

        # header needed for translation api call
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': 'westeurope',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # assign dict_sentences to body for translation request
        body = dict_sentences
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        # print(response)
    if test:
        iterable_response = json.loads(str(response))
    else:
        iterable_response = response

    # TODO: ONLY WORKS WITH "text" as key NO "Text" possible modification needed
    # TODO: CATCH ERROR FROM TRANSLATOR API
    # TODO: INSERT NEW KEY TO .env
    translations = []
    for text_id, text in zip(ids_sentences, iterable_response):
        try:
            translations.append([text_id, text['translations'][0]['text']])
        except TypeError:
            print("text_id:", text_id)
            print("text:", text)
            print(iterable_response)
            try:
                translations.append([text_id, text['error']['code']])
            except TypeError:
                translations.append([text_id, text])

    # print("Translation after saving translations with id in sub_lists:")
    # print(translations[0:5])
    return translations




    # TODO: handle json responses


# multiple texts curl:
# curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en
# &to=zh-Hans" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d
# "[{'Text':'Hello, what is your name?'}, {'Text':'I am fine, thank you.'}]"
# RESPONSE WOULD BE:
# [
#     {
#         "translations":[
#             {"text":"你好, 你叫什么名字？","to":"zh-Hans"}
#         ]
#     },
#     {
#         "translations":[
#             {"text":"我很好，谢谢你。","to":"zh-Hans"}
#         ]
#     }
# ]