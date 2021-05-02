# initialize error codes
error_codes = {
    '1': "Enter a valid email address.",
    '2': "user with this email already exists.",
    '3': "User name or password incorrect",
    '4': "Question doesnt exist",
    '5': "Answer doesnt exist",
    '6': "Question already answered",
    '7': "No more questions left"
}


def get_error_code(messages):
    try:
        message = list(messages)[0][0]
    except TypeError:
        return
    if not message:
        return
    for error_code, msg in error_codes.items():
        if msg == message:
            return error_code
