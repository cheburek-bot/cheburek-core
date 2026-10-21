import pytest

from cheburek_core import Chain

GUILD_ID = "1"


@pytest.fixture
def chain():
    return Chain()


def test_chain_creation(chain: Chain):
    chain.get_chain(GUILD_ID)
    assert GUILD_ID in chain.chains


def test_word_processing(chain: Chain):
    chain.process_words(["hello", "world"], GUILD_ID)
    assert chain.get_words_count(GUILD_ID) == 2
    assert chain.get_links_count(GUILD_ID) == 3


def test_generation(chain: Chain):
    words = ["hello", "beautiful", "testing", "world"]
    chain.process_words(words, GUILD_ID)
    message = chain.generate_message(2, GUILD_ID).split(" ")
    assert len(message) > 0
    assert all(item in words for item in message)
