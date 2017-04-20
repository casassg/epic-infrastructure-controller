import os

import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "ENTER YOUR ACCESS TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "ENTER YOUR ACCESS TOKEN SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "ENTER YOUR API KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "ENTER YOUR API SECRET")


def load_config():
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()


def get_pod_ips():
    # Configs can be set in Configuration class directly or using helper utility

    load_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    return list(map(lambda x: x.status.pod_ip, ret.items))


def apply_eventparser(event_code, keywords):
    load_config()

    with open("k8sdeployments/event_parser.yaml") as f:
        name = '%s-event-parser' % event_code
        dep = yaml.load(
            f.read().replace('{{code}}', event_code).replace('{{keywords}}', keywords).replace('{{name}}', name))

        k8s_beta = client.ExtensionsV1beta1Api()
        try:
            resp = k8s_beta.create_namespaced_deployment(
                body=dep, namespace="default")
        except ApiException as e:
            resp = k8s_beta.patch_namespaced_deployment(name,
                                                        body=dep, namespace="default")

        return resp


def update_queries(queries):
    load_config()
    with open("k8sdeployments/twitter_streaming.yaml") as f:
        name = 'twitter_streaming'
        dep = yaml.load(
            f.read() \
                .replace('{{a_token}}', ACCESS_TOKEN) \
                .replace('{{a_token_secret}}', ACCESS_TOKEN_SECRET) \
                .replace('{{c_key}}', CONSUMER_KEY) \
                .replace('{{c_secret}}', CONSUMER_SECRET) \
                .replace('{{queries}}', queries)
        )

        k8s_beta = client.ExtensionsV1beta1Api()
        try:
            resp = k8s_beta.create_namespaced_deployment(
                body=dep, namespace="default")
        except ApiException as e:
            resp = k8s_beta.patch_namespaced_deployment(name,
                                                        body=dep, namespace="default")

        return resp
