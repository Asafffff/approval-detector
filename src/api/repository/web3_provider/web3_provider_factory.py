from src.api.repository.web3_provider.web3_provider import Web3Provider
from src.api.repository.web3_provider.infura.infura_web3_provider import (
    InfuraWeb3Provider,
)
from src.api.core.config import settings


class Web3ProviderFactory:
    def create(self) -> Web3Provider:
        if settings.WEB3_PROVIDER == "infura":
            return InfuraWeb3Provider()
        else:
            raise ValueError("Unknown web3 provider: {}".format(settings.WEB3_PROVIDER))
