import main


def test_llm_call(llm):
    messages = [
        (
            "system",
            "You are a helpful translator. Translate the user sentence to French.",
        ),
        ("human", "I viscerally detest programming."),
    ]
    resp = llm.invoke(messages)
    print(resp)
