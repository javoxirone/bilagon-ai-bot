from config.integrations import text_processor


def _get_text_response(context: list):
    stream = text_processor.generate_text_response(messages=[{"role": "developer", "content": "You are a helpful assistant named \"Bilag'on\"."}]+context, stream=True,
                                                   max_tokens=2000)
    return stream


def get_text_response_in_incognito_mode(user_message: str):
    stream = _get_text_response([{"role": "user", "content": user_message}])
    for chunk in stream:
        if chunk.choices[0].delta.content is not None and chunk.choices[0].delta.content != "":
            yield chunk.choices[0].delta.content


def get_text_response_with_context(conversation_list: list):
    stream = _get_text_response(conversation_list)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None and chunk.choices[0].delta.content != "":
            yield chunk.choices[0].delta.content
