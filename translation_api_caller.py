# TODO: Google Translate API
# service endpoint: https://translation.googleapis.com/language/translate/v2
# DOCS: https://googleapis.dev/python/translation/latest/client.html
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
import six

GERMAN = "de"


# from: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/translate/cloud-client/snippets.py
def translate_text_with_model(target, text, model='nmt'):
    # [START translate_text_with_model]
    """Translates text into the target language.
    Make sure your project is allowlisted.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target, model=model)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    # [END translate_text_with_model]
