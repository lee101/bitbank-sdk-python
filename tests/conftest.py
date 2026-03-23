import pytest
from bitbank.client import BitbankClient


@pytest.fixture
def base_url():
    return "https://bitbank.nz"


@pytest.fixture
async def client(base_url):
    async with BitbankClient(base_url=base_url) as c:
        yield c
