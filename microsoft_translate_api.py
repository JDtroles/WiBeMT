import os, requests, uuid, json
from reader_saver import load_nested_list_to_list
# TODO: Microsoft Translate API
# https://api.cognitive.microsofttranslator.com/

# -*- coding: utf-8 -*-
# &to=de
# &from=en
some_json_str = "[{'Text':'Hello, what is your name?'}, {'Text':'I am fine, thank you.'}]"
json_data = json.loads(some_json_str.replace("\'", "\""))

# TODO: code this completely new!!!!! Accordingly to paper-notes

# TODO: check if json_sentences_str matches input format
# TODO: rename variables with better names
def create_splitted_json(sentences_to_translate: list, size_of_chunks: int = 50) -> str:
    for i in range(0, len(sentences_to_translate), size_of_chunks):
        yield sentences_to_translate[i:i + size_of_chunks]
    # create list with lists of dicts
    id_list_of_dicts = []
    sentence_list_of_dicts = []
    for sub_list in sentences_to_translate:
        id_dicts_list = []
        text_dicts_list = []
        for item in sub_list:
            id_dicts_list.append({"ID": item[0]})
            text_dicts_list.append({"Text": item[1]})
        id_list_of_dicts.append(id_dicts_list)
        sentence_list_of_dicts.append(text_dicts_list)
    json_sentences = json.loads(sentence_list_of_dicts)
    json_sentences_str: str = json.dumps(json_sentences)
    return json_sentences_str


def get_microsoft_translations_verb_sentences():
    verb_sentences_raw: list = load_nested_list_to_list()
    verb_sentences = []
    for sentence in verb_sentences_raw:
        verb_sentences.append([sentence[0], sentence[1]])


def api_caller(data: dict):
    key_var_name = 'MICROSOFT_TRANSLATE_TEXT_API_KEY'
    if key_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    endpoint_var_name = 'MICROSOFT_TRANSLATE_TEXT_ENDPOINT'
    if endpoint_var_name not in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    path = '/translate?api-version=3.0'
    params = '&from=en&to=de'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

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
