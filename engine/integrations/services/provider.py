from app.core.config import NOMAD_API_JOB, DOCKER_PRIVATE_REGISTRY
from enum import Enum
from engine.integrations.services.provider.providers import nomad


class SupportedProviders(str, Enum):
    NOMAD = "nomad"


class Provider():

    def __init__(self, provider_type: SupportedProviders = SupportedProviders.NOMAD, registry: str = DOCKER_PRIVATE_REGISTRY) -> None:
        self.__PROVDER_TYPE__ = provider_type
        self.__REGISTRY__ = registry
        pass

    def getDeployments(tool_name: str, tool_tag: str, namespace: str = "default"):
        return nomad.GetJobss(tool_name)


    # def getDeployment(id: str,  tool_name: str, tool_tag: str, namespace: str = "default"):
    #     pass

    def createDeployment(  tool_name: str, tool_tag: str, namespace: str = "default"):

        pass

