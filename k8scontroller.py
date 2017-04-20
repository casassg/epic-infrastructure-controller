import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException


def get_pod_ips():
    # Configs can be set in Configuration class directly or using helper utility

    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    return map(lambda x: x.status.pod_ip, ret.items)


def apply_deployment(event_code, keywords):
    config.load_kube_config()

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
