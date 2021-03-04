from engine import tool
from app.core.config import NOMAD_API_GC, NOMAD_API_JOB, DOCKER_PRIVATE_REGISTRY, NOMAD_API_JOBS, NOMAD_API_SEARCH
from enum import Enum
import requests


def CreateJob(jobId: str, tool_name: str, image_name: str, image_tag: str, namespace: str, scale: int = 1):

    # jobId = tool_name + ":" + image_name + ":" + image_tag
    data = {
        "Job": {
            "EnforceIndex": False,
            "JobModifyIndex": 0,
            "Region": None,
            "Namespace": namespace,
            "Name": tool_name,
            "Id":  jobId,
            "Type": None,
            "Priority": None,
            "AllAtOnce": None,
            "Datacenters": [
                "dc1"
            ],
            "Constraints": None,
            "Affinities": None,
            "TaskGroups": [
                {
                    "Name": tool_name,
                    "Count": scale,
                    "Constraints": None,
                    "Affinities": None,
                    "Tasks": [
                        {
                            "Name": tool_name,
                            "Driver": "docker",
                            "User": "",
                            "Lifecycle": None,
                            "Config": {
                                "image": DOCKER_PRIVATE_REGISTRY.format(image_name, image_tag),
                            },
                            "Constraints": None,
                            "Affinities": None,
                            "Env": {
                                "RMQ_HOST": "192.168.29.5",
                                "RMQ_PASSWORD": "bitnami",
                                "RMQ_USERNAME": "user",
                                "message_queue_topic": jobId,
                                "fluent_host": "192.168.29.5",
                                "MINIOURL": "192.168.29.5:9000",
                            },
                            "Services": None,
                            "Resources": None,
                            "RestartPolicy": None,
                            "Meta": None,
                            "KillTimeout": None,
                            "LogConfig": None,
                            "Artifacts": None,
                            "Vault": None,
                            "Templates": None,
                            "DispatchPayload": None,
                            "VolumeMounts": None,
                            "Leader": False,
                            "ShutdownDelay": 0,
                            "KillSignal": "",
                            "Kind": "",
                            "ScalingPolicies": None
                        }
                    ],
                    "Spreads": None,
                    "Volumes": None,
                    "RestartPolicy": {
                        "Interval": 60000000000,
                        "Attempts": 2,
                        "Delay": 30000000000,
                        "Mode": "delay"
                    },
                    "ReschedulePolicy": None,
                    "EphemeralDisk": None,
                    "Update": None,
                    "Migrate": None,
                    "Networks": None,
                    "Meta": None,
                    "Services": None,
                    "ShutdownDelay": None,
                    "StopAfterClientDisconnect": None,
                    "Scaling": None
                }
            ],
            "Update": None,
            "Multiregion": None,
            "Spreads": None,
            "Periodic": None,
            "ParameterizedJob": None,
            "Reschedule": None,
            "Migrate": None,
            "Meta": None,
            "ConsulToken": None,
            "VaultToken": None,
            "Stop": None,
            "ParentID": None,
            "Dispatched": False,
            "Payload": None,
            "VaultNamespace": None,
            "NomadTokenID": None,
            "Status": None,
            "StatusDescription": None,
            "Stable": None,
            "Version": None,
            "SubmitTime": None,
        }
    }

    print(data)
    response = requests.post(NOMAD_API_JOB + f"/{jobId}", json=data)
    try:
        response = response.json()
    except:
        response = response.text
        print("Can't convert to JSON",  response)
    return response


def GetJobs(tool_name: str):
    response = requests.get(NOMAD_API_JOBS)
    try:
        response = response.json()
    except:
        response = response.text
        print("Can't convert to JSON",  response)
    return response


def GetJob(tool_name: str):

    response = requests.get(NOMAD_API_JOB + f"/{tool_name}")
    try:
        response = response.json()
    except:
        response = response.text
        print("Can't convert to JSON",  response)
    return response


def SearchJobs(prefix: str):

    response = requests.post(NOMAD_API_SEARCH, json={
        "Context": "jobs",
        "Prefix": prefix
    })
    try:
        response = response.json()["Matches"]["jobs"]
    except:
        response = response.text
        print("Can't convert to JSON",  response)
    return response


def DeleteJob(job_id: str):

    response = requests.delete(NOMAD_API_JOB + f"/{job_id}")
    try:
        response = response.json()
    except:
        response = response.text
        print("Can't convert to JSON",  response)
    return response


def RunGC():

    response = requests.put(NOMAD_API_GC)
    try:
        response = response.json()
    except:
        response = response.text
        print("Can't convert to JSON",  response)
    return response
