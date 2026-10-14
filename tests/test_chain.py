from cheburek_core import Chain

GUILD_ID = "1"


def test_chain_creation():
    chain = Chain()

    chain.get_chain(GUILD_ID)

    assert GUILD_ID in chain.chains
