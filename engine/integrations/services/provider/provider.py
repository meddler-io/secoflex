from app.core.config import NOMAD_API_JOB, DOCKER_PRIVATE_REGISTRY
from enum import Enum
from engine.integrations.services.provider.providers import nomad
import requests


class SupportedProviders(str, Enum):
    NOMAD = "nomad"


class Provider():

    def __init__(self, provider_type: SupportedProviders = SupportedProviders.NOMAD, registry: str = DOCKER_PRIVATE_REGISTRY) -> None:
        self.__PROVDER_TYPE__ = provider_type
        self.__REGISTRY__ = registry
        pass

    def getDeployments(self, tool_name: str,  namespace: str = "default"):
        return nomad.GetJobs(tool_name)

    def getDeployment(self, tool_name: str, namespace: str = "default"):
        return nomad.GetJob(tool_name)

    def searchDeployments(self, prefix: str = "",  namespace: str = "default"):
        return nomad.SearchJobs(prefix)

    # def getDeployment(id: str,  tool_name: str, tool_tag: str, namespace: str = "default"):
    #     pass

    def createDeployment(self, id: str,  tool_name: str, image_name: str, image_tag: str, namespace: str = "default"):
        return nomad.CreateJob(id, tool_name, image_name, image_tag, namespace)
        pass

    def deleteDeployment(self, job_id: str, namespace: str = "default"):
        return nomad.DeleteJob(job_id)

    def purge(self, namespace: str = "default"):
        return nomad.RunGC()

    def scaleDeployment(self, tool_name: str, tool_tag: str, scale: int, namespace: str = "default"):
        pass
