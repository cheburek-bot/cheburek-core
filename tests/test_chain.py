import pytest

from cheburek_core import Chain

GUILD_ID = "1"


@pytest.fixture
def chain(tmp_path):
    return Chain(base_path=str(tmp_path))


def test_chain_creation(chain: Chain):
    chain.get_chain(GUILD_ID)
    assert GUILD_ID in chain.chains


def test_word_processing(chain: Chain):
    chain.process_words(["hello", "world"], GUILD_ID)
    assert chain.get_words_count(GUILD_ID) == 2
    assert chain.get_links_count(GUILD_ID) == 3


def test_freq_generation(chain: Chain):
    chain.process_words(["hello", "beautiful", "testing", "world"], GUILD_ID)
    chain.start_word_type = "freq"
    message = chain.generate_message(2, GUILD_ID).split(" ")
    assert len(message) == 2
    assert message[0] == "hello"
    assert message[1] == "world"
