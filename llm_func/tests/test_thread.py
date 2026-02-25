from ..thread import ChatThread


def test_thread_basic():

    thread = ChatThread()

    thread.add_system("sys")
    thread.add_user("user")
    thread.add_assistant("assistant")

    msgs = thread.get_messages()

    assert len(msgs) == 3
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    assert msgs[2]["role"] == "assistant"

    thread.reset()
    assert len(thread.get_messages()) == 0