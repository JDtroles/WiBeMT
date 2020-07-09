import json
def sample_return():
    json_output = '[{"detectedLanguage": {"language": "en", "score": 1.0}, "translations": [{"text": "Hallo Welt!", ' \
                  '"to": "de"}, {"text": "Salve, mondo!", "to": "it"}]}]'
    return json_output


def create_json_output_corresponding_to_input(middle_data: list) -> str:
    json_output_beginning = '[{"detectedLanguage": {"language": "en", "score": 1.0}, "translations":'
    json_output_ending = '}]'
    print(json.dumps(middle_data))
    return json_output_beginning + json.dumps(middle_data) + json_output_ending
