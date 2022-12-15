import requests
import os
import transcription_compare

# Set ASR URL path
asr_url = 'https://api.openai.com/v1/engines/audio-transcribe-001/transcriptions'

def call_asr(api_key,filepath, response_format='vtt'):
    # Set headers and file references as expected by API
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    files = {
        'file': open(filepath,'rb')
    }

    body = {
        # Acceptable response_format inputs are vtt or text
        'response_format': response_format
    }


    try:
        print('Sending request')
        response = requests.post(url=asr_url,headers=headers,json=body,files=files)
        print('Request successful')
        return response
    except Exception as e:
        print('Oh no, dramas!')
        response = e
        print(e)
        return response

def run_transcription_compare(reference_path, output_file_list, output_html_path):
    print("Start to compare results")

    with open(reference_path, "r", encoding='utf-8') as reference_file:
        reference_text = reference_file.read()

    calculator = UKKLevenshteinDistanceCalculator(
        tokenizer=WordTokenizer(),
        get_alignment_result=True,
        local_optimizers=[DigitUtil(process_output_digit=True), LocalCerOptimizer()]
    )

    output_all = dict()  # (output identifier -> output string)
    for output_path in output_file_list:
        with open(output_path, "r", encoding='utf-8') as output_file:
            output_text = output_file.read()
        output_path_name = os.path.basename(output_path)
        output_all[output_path_name] = output_text
    print.info("Finish reading all results")

    output_results = dict()  # (output_identifier -> output_string)
    for (key, value) in output_all.items():
        print.info("Start to process {}".format(key))
        output_results[key] = calculator.get_distance(reference_text, value,
                                                      brackets_list=["[]", "()", "<>"],
                                                      to_lower=True,
                                                      remove_punctuation=True,
                                                      use_alternative_spelling=True)

    print.info("Merge all results into one HTML")
    calculator_local = UKKLevenshteinDistanceCalculator(
                tokenizer=CharacterTokenizer(),
                get_alignment_result=False)

    result = MultiResult(output_results, calculator_local)
    s = result.to_html()

    with open(output_html_path, 'w') as f:
        f.write(s)
