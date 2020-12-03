from logging import setLoggerClass
import os
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException


class Constants(object):
    NAMESPACE = 'example'


class KubernetesApiClient(object):
    def __init__(self):
        # load
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        self.configuration = client.Configuration()
        # self.sanity_check()

    def sanity_check(self):
        client.CoreV1Api().create_namespace(client.V1Namespace(metadata={
            "name": Constants.NAMESPACE
        }))

    def create_batch_api_client(self):
        return client.BatchV1Api(client.ApiClient(self.configuration))

    def create_job_object(self, job_name, container_image, args):
        volume_name = ""  # volume inside of which you put your service account
        google_app_credentials_path = os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS')
        volume_mount = client.V1VolumeMount(
            mount_path='/'.join(google_app_credentials_path.split('/')[:-1]),
            name=volume_name
        )
        env = client.V1EnvVar(
            name='GOOGLE_APPLICATION_CREDENTIALS',
            value=google_app_credentials_path
        )
        container = client.V1Container(
            name=job_name,
            image=container_image,
            args=args,
            volume_mounts=[volume_mount],
            env=[env],
            image_pull_policy="Always")
        volume = client.V1Volume(
            name=volume_name,
            secret=client.V1SecretVolumeSource(
                secret_name='<secret-where-you-put-the-service-account>')
        )
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "sample"}),
            spec=client.V1PodSpec(restart_policy="Never",
                                  containers=[container],
                                  volumes=[volume]))
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=3,
            ttl_seconds_after_finished=60)
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=spec)
        return job


api_client = KubernetesApiClient()
job_api_client = api_client.create_batch_api_client()
job = api_client.create_job_object("hello", "rounak316/hello", None)
try:
    api_response = job_api_client.create_namespaced_job(
        namespace=Constants.NAMESPACE,
        body=job)
    print(str(api_response.status))
except ApiException as e:
    print(e)  # Handle the exception.
