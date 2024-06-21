import networkx as nx
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def main():
    #===== Obter o node master e os nodes workers
    #===== Obter IP também dos nodes
    node_master = {}
    node_workers = []
    for item in k3s_nods["items"]:
        if item["metadata"]["annotations"]["k3s.io/node-args"] == "[\"server\"]":
            node_master["name"] = item["metadata"]["name"]
            for sub_item in item["status"]["addresses"]:
                if sub_item["type"] == "InternalIP":
                    node_master["ip-address"] = sub_item["address"]
        elif item["metadata"]["annotations"]["k3s.io/node-args"] == "[\"agent\"]":
            node_name = item["metadata"]["name"]
            for sub_item in item["status"]["addresses"]:
                if sub_item["type"] == "InternalIP":
                    node_ip = sub_item["address"]
            node_workers.append({
                "name" : node_name,
                "ip-address" : node_ip
            })

    #===== Obter os podes e os dados relevantes
    cluster_pods = []
    for item in k3s_pods['items']:
        name_pod = item["metadata"]["name"]
        name_node_pod = item["spec"]["nodeName"]
        cluster_pods.append({
            "name" : name_pod,
            "name_node_pod": name_node_pod
        })

    #===== Criar Gráfico
    G = nx.Graph()
    #===== Adicionar node master ao gráfico
    G.add_node(node_master["name"],color="red")
    for item in node_workers:
        #===== Adicionar nodes workers ao gráfico
        G.add_node(item["name"],color="orange")
        #===== Adicionar edges ao gráfico
        G.add_edges_from([(node_master["name"],item["name"])])
    
    #===== Adicionar pods ao gráfico
    for item in cluster_pods:
        G.add_node(item["name"],color="blue")
        G.add_edges_from([(item["name_node_pod"],item["name"])])
    

    #===== Criar Janela Tkinter
    root = tkinter.Tk()
    root.wm_title("Diagrama Dinâmico-Versão-Beta")
    
    #===== Vai buscar os atributos das cores dos nodes ou seja vai buscar uma lista com as cores
    node_colors = nx.get_node_attributes(G,'color').values()

    #===== Cria-se o objeto figra que vai ter dentro dele o grafico desenhado(como se fosse um container)
    fig = Figure(figsize=(15, 11), dpi=100)
    ax = fig.add_subplot()
    #nx.draw_planar(G, with_labels=True, node_color=node_colors ,font_weight='bold', ax=ax)
    nx.draw(G, with_labels=True, node_color=node_colors ,font_weight='bold', ax=ax)

    #===== O objeto figura em seguida é que é utilizado para ser apresentado na imagem
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill='both', expand=True)

    tkinter.mainloop()

if __name__ == "__main__":
    
    k3s_nods = {
    "kind": "NodeList",
    "apiVersion": "v1",
    "metadata": {
        "resourceVersion": "2623"
    },
    "items": [
        {
            "metadata": {
                "name": "kworker1",
                "uid": "fe878471-69d3-4797-b1c1-b51d8d62c965",
                "resourceVersion": "2418",
                "creationTimestamp": "2024-05-14T16:59:08Z",
                "labels": {
                    "beta.kubernetes.io/arch": "amd64",
                    "beta.kubernetes.io/instance-type": "k3s",
                    "beta.kubernetes.io/os": "linux",
                    "kubernetes.io/arch": "amd64",
                    "kubernetes.io/hostname": "kworker1",
                    "kubernetes.io/os": "linux",
                    "node.kubernetes.io/instance-type": "k3s"
                },
                "annotations": {
                    "alpha.kubernetes.io/provided-node-ip": "192.168.186.217",
                    "flannel.alpha.coreos.com/backend-data": "{\"VNI\":1,\"VtepMAC\":\"2e:f7:d3:70:96:48\"}",
                    "flannel.alpha.coreos.com/backend-type": "vxlan",
                    "flannel.alpha.coreos.com/kube-subnet-manager": "true",
                    "flannel.alpha.coreos.com/public-ip": "192.168.186.217",
                    "k3s.io/hostname": "kworker1",
                    "k3s.io/internal-ip": "192.168.186.217",
                    "k3s.io/node-args": "[\"agent\"]",
                    "k3s.io/node-config-hash": "JUNUKM5I4V4HTEWAT3JGPZBL537LFC7Q7Y3DUYSQMG6VQEE5FJRQ====",
                    "k3s.io/node-env": "{\"K3S_DATA_DIR\":\"/var/lib/rancher/k3s/data/b159f6e26663d8c92285e7bc4a6881d85bd8c81efc55eb2cf191c54100387fbb\",\"K3S_TOKEN\":\"********\",\"K3S_URL\":\"https://192.168.186.216:6443\"}",
                    "node.alpha.kubernetes.io/ttl": "0",
                    "volumes.kubernetes.io/controller-managed-attach-detach": "true"
                },
                "finalizers": [
                    "wrangler.cattle.io/node"
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:59:08Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    ".": {},
                                    "f:alpha.kubernetes.io/provided-node-ip": {},
                                    "f:k3s.io/hostname": {},
                                    "f:k3s.io/internal-ip": {},
                                    "f:k3s.io/node-args": {},
                                    "f:k3s.io/node-config-hash": {},
                                    "f:k3s.io/node-env": {},
                                    "f:node.alpha.kubernetes.io/ttl": {},
                                    "f:volumes.kubernetes.io/controller-managed-attach-detach": {}
                                },
                                "f:labels": {
                                    ".": {},
                                    "f:beta.kubernetes.io/arch": {},
                                    "f:beta.kubernetes.io/instance-type": {},
                                    "f:beta.kubernetes.io/os": {},
                                    "f:kubernetes.io/arch": {},
                                    "f:kubernetes.io/hostname": {},
                                    "f:kubernetes.io/os": {},
                                    "f:node.kubernetes.io/instance-type": {}
                                }
                            },
                            "f:spec": {
                                "f:podCIDR": {},
                                "f:podCIDRs": {
                                    ".": {},
                                    "v:\"10.42.2.0/24\"": {}
                                },
                                "f:providerID": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s-supervisor@kmaster",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:59:08Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:finalizers": {
                                    ".": {},
                                    "v:\"wrangler.cattle.io/node\"": {}
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-23T11:26:46Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    "f:flannel.alpha.coreos.com/backend-data": {},
                                    "f:flannel.alpha.coreos.com/backend-type": {},
                                    "f:flannel.alpha.coreos.com/kube-subnet-manager": {},
                                    "f:flannel.alpha.coreos.com/public-ip": {}
                                }
                            },
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"DiskPressure\"}": {
                                        "f:lastHeartbeatTime": {}
                                    },
                                    "k:{\"type\":\"MemoryPressure\"}": {
                                        "f:lastHeartbeatTime": {}
                                    },
                                    "k:{\"type\":\"PIDPressure\"}": {
                                        "f:lastHeartbeatTime": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        "f:lastHeartbeatTime": {},
                                        "f:message": {},
                                        "f:reason": {},
                                        "f:status": {}
                                    }
                                },
                                "f:images": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "podCIDR": "10.42.2.0/24",
                "podCIDRs": [
                    "10.42.2.0/24"
                ],
                "providerID": "k3s://kworker1"
            },
            "status": {
                "capacity": {
                    "cpu": "2",
                    "ephemeral-storage": "39937312Ki",
                    "hugepages-1Gi": "0",
                    "hugepages-2Mi": "0",
                    "memory": "1974468Ki",
                    "pods": "110"
                },
                "allocatable": {
                    "cpu": "2",
                    "ephemeral-storage": "38851017084",
                    "hugepages-1Gi": "0",
                    "hugepages-2Mi": "0",
                    "memory": "1974468Ki",
                    "pods": "110"
                },
                "conditions": [
                    {
                        "type": "MemoryPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:26:46Z",
                        "lastTransitionTime": "2024-05-14T16:59:08Z",
                        "reason": "KubeletHasSufficientMemory",
                        "message": "kubelet has sufficient memory available"
                    },
                    {
                        "type": "DiskPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:26:46Z",
                        "lastTransitionTime": "2024-05-14T16:59:08Z",
                        "reason": "KubeletHasNoDiskPressure",
                        "message": "kubelet has no disk pressure"
                    },
                    {
                        "type": "PIDPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:26:46Z",
                        "lastTransitionTime": "2024-05-14T16:59:08Z",
                        "reason": "KubeletHasSufficientPID",
                        "message": "kubelet has sufficient PID available"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastHeartbeatTime": "2024-05-23T11:26:46Z",
                        "lastTransitionTime": "2024-05-14T16:59:08Z",
                        "reason": "KubeletReady",
                        "message": "kubelet is posting ready status. AppArmor enabled"
                    }
                ],
                "addresses": [
                    {
                        "type": "InternalIP",
                        "address": "192.168.186.217"
                    },
                    {
                        "type": "Hostname",
                        "address": "kworker1"
                    }
                ],
                "daemonEndpoints": {
                    "kubeletEndpoint": {
                        "Port": 10250
                    }
                },
                "nodeInfo": {
                    "machineID": "a38f8eb989a4463c8c194d086528363d",
                    "systemUUID": "8e744d56-fba0-c071-a9c1-3cdf163ba8d7",
                    "bootID": "6bbde181-10e0-4c39-9b02-869f9d534218",
                    "kernelVersion": "5.15.0-107-generic",
                    "osImage": "Ubuntu 22.04.4 LTS",
                    "containerRuntimeVersion": "containerd://1.7.15-k3s1",
                    "kubeletVersion": "v1.29.4+k3s1",
                    "kubeProxyVersion": "v1.29.4+k3s1",
                    "operatingSystem": "linux",
                    "architecture": "amd64"
                },
                "images": [
                    {
                        "names": [
                            "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                            "docker.io/rancher/klipper-lb:v0.4.7"
                        ],
                        "sizeBytes": 4777465
                    },
                    {
                        "names": [
                            "docker.io/rancher/mirrored-pause@sha256:74c4244427b7312c5b901fe0f67cbc53683d06f4f24c6faee65d4182bf0fa893",
                            "docker.io/rancher/mirrored-pause:3.6"
                        ],
                        "sizeBytes": 301463
                    }
                ]
            }
        },
        {
            "metadata": {
                "name": "kworker2",
                "uid": "de52857a-510e-4c61-9b2f-11063cb63af3",
                "resourceVersion": "2579",
                "creationTimestamp": "2024-05-14T16:59:05Z",
                "labels": {
                    "beta.kubernetes.io/arch": "amd64",
                    "beta.kubernetes.io/instance-type": "k3s",
                    "beta.kubernetes.io/os": "linux",
                    "kubernetes.io/arch": "amd64",
                    "kubernetes.io/hostname": "kworker2",
                    "kubernetes.io/os": "linux",
                    "node.kubernetes.io/instance-type": "k3s"
                },
                "annotations": {
                    "alpha.kubernetes.io/provided-node-ip": "192.168.186.218",
                    "flannel.alpha.coreos.com/backend-data": "{\"VNI\":1,\"VtepMAC\":\"be:31:ea:7e:fc:e7\"}",
                    "flannel.alpha.coreos.com/backend-type": "vxlan",
                    "flannel.alpha.coreos.com/kube-subnet-manager": "true",
                    "flannel.alpha.coreos.com/public-ip": "192.168.186.218",
                    "k3s.io/hostname": "kworker2",
                    "k3s.io/internal-ip": "192.168.186.218",
                    "k3s.io/node-args": "[\"agent\"]",
                    "k3s.io/node-config-hash": "JUNUKM5I4V4HTEWAT3JGPZBL537LFC7Q7Y3DUYSQMG6VQEE5FJRQ====",
                    "k3s.io/node-env": "{\"K3S_DATA_DIR\":\"/var/lib/rancher/k3s/data/b159f6e26663d8c92285e7bc4a6881d85bd8c81efc55eb2cf191c54100387fbb\",\"K3S_TOKEN\":\"********\",\"K3S_URL\":\"https://192.168.186.216:6443\"}",
                    "node.alpha.kubernetes.io/ttl": "0",
                    "volumes.kubernetes.io/controller-managed-attach-detach": "true"
                },
                "finalizers": [
                    "wrangler.cattle.io/node"
                ],
                "managedFields": [
                    {
                        "manager": "k3s-supervisor@kmaster",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:59:05Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:finalizers": {
                                    ".": {},
                                    "v:\"wrangler.cattle.io/node\"": {}
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-23T10:49:10Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    ".": {},
                                    "f:alpha.kubernetes.io/provided-node-ip": {},
                                    "f:k3s.io/hostname": {},
                                    "f:k3s.io/internal-ip": {},
                                    "f:k3s.io/node-args": {},
                                    "f:k3s.io/node-config-hash": {},
                                    "f:k3s.io/node-env": {},
                                    "f:node.alpha.kubernetes.io/ttl": {},
                                    "f:volumes.kubernetes.io/controller-managed-attach-detach": {}
                                },
                                "f:labels": {
                                    ".": {},
                                    "f:beta.kubernetes.io/arch": {},
                                    "f:beta.kubernetes.io/instance-type": {},
                                    "f:beta.kubernetes.io/os": {},
                                    "f:kubernetes.io/arch": {},
                                    "f:kubernetes.io/hostname": {},
                                    "f:kubernetes.io/os": {},
                                    "f:node.kubernetes.io/instance-type": {}
                                }
                            },
                            "f:spec": {
                                "f:podCIDR": {},
                                "f:podCIDRs": {
                                    ".": {},
                                    "v:\"10.42.1.0/24\"": {}
                                },
                                "f:providerID": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-23T11:29:59Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    "f:flannel.alpha.coreos.com/backend-data": {},
                                    "f:flannel.alpha.coreos.com/backend-type": {},
                                    "f:flannel.alpha.coreos.com/kube-subnet-manager": {},
                                    "f:flannel.alpha.coreos.com/public-ip": {}
                                }
                            },
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"DiskPressure\"}": {
                                        "f:lastHeartbeatTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:message": {},
                                        "f:reason": {},
                                        "f:status": {}
                                    },
                                    "k:{\"type\":\"MemoryPressure\"}": {
                                        "f:lastHeartbeatTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:message": {},
                                        "f:reason": {},
                                        "f:status": {}
                                    },
                                    "k:{\"type\":\"PIDPressure\"}": {
                                        "f:lastHeartbeatTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:message": {},
                                        "f:reason": {},
                                        "f:status": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        "f:lastHeartbeatTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:message": {},
                                        "f:reason": {},
                                        "f:status": {}
                                    }
                                },
                                "f:images": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "podCIDR": "10.42.1.0/24",
                "podCIDRs": [
                    "10.42.1.0/24"
                ],
                "providerID": "k3s://kworker2"
            },
            "status": {
                "capacity": {
                    "cpu": "2",
                    "ephemeral-storage": "39937312Ki",
                    "hugepages-1Gi": "0",
                    "hugepages-2Mi": "0",
                    "memory": "1974496Ki",
                    "pods": "110"
                },
                "allocatable": {
                    "cpu": "2",
                    "ephemeral-storage": "38851017084",
                    "hugepages-1Gi": "0",
                    "hugepages-2Mi": "0",
                    "memory": "1974496Ki",
                    "pods": "110"
                },
                "conditions": [
                    {
                        "type": "MemoryPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:29:59Z",
                        "lastTransitionTime": "2024-05-23T10:49:10Z",
                        "reason": "KubeletHasSufficientMemory",
                        "message": "kubelet has sufficient memory available"
                    },
                    {
                        "type": "DiskPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:29:59Z",
                        "lastTransitionTime": "2024-05-23T10:49:10Z",
                        "reason": "KubeletHasNoDiskPressure",
                        "message": "kubelet has no disk pressure"
                    },
                    {
                        "type": "PIDPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:29:59Z",
                        "lastTransitionTime": "2024-05-23T10:49:10Z",
                        "reason": "KubeletHasSufficientPID",
                        "message": "kubelet has sufficient PID available"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastHeartbeatTime": "2024-05-23T11:29:59Z",
                        "lastTransitionTime": "2024-05-23T10:49:10Z",
                        "reason": "KubeletReady",
                        "message": "kubelet is posting ready status. AppArmor enabled"
                    }
                ],
                "addresses": [
                    {
                        "type": "InternalIP",
                        "address": "192.168.186.218"
                    },
                    {
                        "type": "Hostname",
                        "address": "kworker2"
                    }
                ],
                "daemonEndpoints": {
                    "kubeletEndpoint": {
                        "Port": 10250
                    }
                },
                "nodeInfo": {
                    "machineID": "a38f8eb989a4463c8c194d086528363d",
                    "systemUUID": "770c4d56-6ba7-05d5-234d-3ef7c6208713",
                    "bootID": "eabcdffe-292d-4dc6-89b9-5d4b2f437348",
                    "kernelVersion": "5.15.0-107-generic",
                    "osImage": "Ubuntu 22.04.4 LTS",
                    "containerRuntimeVersion": "containerd://1.7.15-k3s1",
                    "kubeletVersion": "v1.29.4+k3s1",
                    "kubeProxyVersion": "v1.29.4+k3s1",
                    "operatingSystem": "linux",
                    "architecture": "amd64"
                },
                "images": [
                    {
                        "names": [
                            "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                            "docker.io/rancher/klipper-lb:v0.4.7"
                        ],
                        "sizeBytes": 4777465
                    },
                    {
                        "names": [
                            "docker.io/rancher/mirrored-pause@sha256:74c4244427b7312c5b901fe0f67cbc53683d06f4f24c6faee65d4182bf0fa893",
                            "docker.io/rancher/mirrored-pause:3.6"
                        ],
                        "sizeBytes": 301463
                    }
                ]
            }
        },
        {
            "metadata": {
                "name": "kmaster",
                "uid": "98303f30-0cb4-401f-baf2-891d27169f7d",
                "resourceVersion": "2588",
                "creationTimestamp": "2024-05-14T16:42:06Z",
                "labels": {
                    "beta.kubernetes.io/arch": "amd64",
                    "beta.kubernetes.io/instance-type": "k3s",
                    "beta.kubernetes.io/os": "linux",
                    "kubernetes.io/arch": "amd64",
                    "kubernetes.io/hostname": "kmaster",
                    "kubernetes.io/os": "linux",
                    "node-role.kubernetes.io/control-plane": "true",
                    "node-role.kubernetes.io/master": "true",
                    "node.kubernetes.io/instance-type": "k3s"
                },
                "annotations": {
                    "alpha.kubernetes.io/provided-node-ip": "192.168.186.216",
                    "flannel.alpha.coreos.com/backend-data": "{\"VNI\":1,\"VtepMAC\":\"b6:c8:8d:ca:14:8a\"}",
                    "flannel.alpha.coreos.com/backend-type": "vxlan",
                    "flannel.alpha.coreos.com/kube-subnet-manager": "true",
                    "flannel.alpha.coreos.com/public-ip": "192.168.186.216",
                    "k3s.io/hostname": "kmaster",
                    "k3s.io/internal-ip": "192.168.186.216",
                    "k3s.io/node-args": "[\"server\"]",
                    "k3s.io/node-config-hash": "X4QWIEC5NTH4VTNX3IIGXUVFE5UB53UOJLKXHXWT5OQRMY3VP5DA====",
                    "k3s.io/node-env": "{\"K3S_DATA_DIR\":\"/var/lib/rancher/k3s/data/b159f6e26663d8c92285e7bc4a6881d85bd8c81efc55eb2cf191c54100387fbb\"}",
                    "node.alpha.kubernetes.io/ttl": "0",
                    "volumes.kubernetes.io/controller-managed-attach-detach": "true"
                },
                "finalizers": [
                    "wrangler.cattle.io/node"
                ],
                "managedFields": [
                    {
                        "manager": "k3s-supervisor@kmaster",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:08Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:finalizers": {
                                    ".": {},
                                    "v:\"wrangler.cattle.io/node\"": {}
                                },
                                "f:labels": {
                                    "f:node-role.kubernetes.io/control-plane": {},
                                    "f:node-role.kubernetes.io/master": {}
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:19Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    ".": {},
                                    "f:alpha.kubernetes.io/provided-node-ip": {},
                                    "f:k3s.io/hostname": {},
                                    "f:k3s.io/internal-ip": {},
                                    "f:k3s.io/node-args": {},
                                    "f:k3s.io/node-config-hash": {},
                                    "f:k3s.io/node-env": {},
                                    "f:node.alpha.kubernetes.io/ttl": {},
                                    "f:volumes.kubernetes.io/controller-managed-attach-detach": {}
                                },
                                "f:labels": {
                                    ".": {},
                                    "f:beta.kubernetes.io/arch": {},
                                    "f:beta.kubernetes.io/instance-type": {},
                                    "f:beta.kubernetes.io/os": {},
                                    "f:kubernetes.io/arch": {},
                                    "f:kubernetes.io/hostname": {},
                                    "f:kubernetes.io/os": {},
                                    "f:node.kubernetes.io/instance-type": {}
                                }
                            },
                            "f:spec": {
                                "f:podCIDR": {},
                                "f:podCIDRs": {
                                    ".": {},
                                    "v:\"10.42.0.0/24\"": {}
                                },
                                "f:providerID": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-23T11:30:05Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    "f:flannel.alpha.coreos.com/backend-data": {},
                                    "f:flannel.alpha.coreos.com/backend-type": {},
                                    "f:flannel.alpha.coreos.com/kube-subnet-manager": {},
                                    "f:flannel.alpha.coreos.com/public-ip": {}
                                }
                            },
                            "f:status": {
                                "f:allocatable": {
                                    "f:ephemeral-storage": {}
                                },
                                "f:conditions": {
                                    "k:{\"type\":\"DiskPressure\"}": {
                                        "f:lastHeartbeatTime": {}
                                    },
                                    "k:{\"type\":\"MemoryPressure\"}": {
                                        "f:lastHeartbeatTime": {}
                                    },
                                    "k:{\"type\":\"PIDPressure\"}": {
                                        "f:lastHeartbeatTime": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        "f:lastHeartbeatTime": {},
                                        "f:message": {},
                                        "f:reason": {},
                                        "f:status": {}
                                    }
                                },
                                "f:images": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "podCIDR": "10.42.0.0/24",
                "podCIDRs": [
                    "10.42.0.0/24"
                ],
                "providerID": "k3s://kmaster"
            },
            "status": {
                "capacity": {
                    "cpu": "2",
                    "ephemeral-storage": "39937312Ki",
                    "hugepages-1Gi": "0",
                    "hugepages-2Mi": "0",
                    "memory": "1974484Ki",
                    "pods": "110"
                },
                "allocatable": {
                    "cpu": "2",
                    "ephemeral-storage": "38851017084",
                    "hugepages-1Gi": "0",
                    "hugepages-2Mi": "0",
                    "memory": "1974484Ki",
                    "pods": "110"
                },
                "conditions": [
                    {
                        "type": "MemoryPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:30:05Z",
                        "lastTransitionTime": "2024-05-14T16:42:06Z",
                        "reason": "KubeletHasSufficientMemory",
                        "message": "kubelet has sufficient memory available"
                    },
                    {
                        "type": "DiskPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:30:05Z",
                        "lastTransitionTime": "2024-05-14T16:42:06Z",
                        "reason": "KubeletHasNoDiskPressure",
                        "message": "kubelet has no disk pressure"
                    },
                    {
                        "type": "PIDPressure",
                        "status": "False",
                        "lastHeartbeatTime": "2024-05-23T11:30:05Z",
                        "lastTransitionTime": "2024-05-14T16:42:06Z",
                        "reason": "KubeletHasSufficientPID",
                        "message": "kubelet has sufficient PID available"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastHeartbeatTime": "2024-05-23T11:30:05Z",
                        "lastTransitionTime": "2024-05-14T16:42:06Z",
                        "reason": "KubeletReady",
                        "message": "kubelet is posting ready status. AppArmor enabled"
                    }
                ],
                "addresses": [
                    {
                        "type": "InternalIP",
                        "address": "192.168.186.216"
                    },
                    {
                        "type": "Hostname",
                        "address": "kmaster"
                    }
                ],
                "daemonEndpoints": {
                    "kubeletEndpoint": {
                        "Port": 10250
                    }
                },
                "nodeInfo": {
                    "machineID": "a38f8eb989a4463c8c194d086528363d",
                    "systemUUID": "c4114d56-6039-3722-a3da-be309067ae25",
                    "bootID": "c955280f-9e81-43d8-8203-e9382b62c608",
                    "kernelVersion": "5.15.0-107-generic",
                    "osImage": "Ubuntu 22.04.4 LTS",
                    "containerRuntimeVersion": "containerd://1.7.15-k3s1",
                    "kubeletVersion": "v1.29.4+k3s1",
                    "kubeProxyVersion": "v1.29.4+k3s1",
                    "operatingSystem": "linux",
                    "architecture": "amd64"
                },
                "images": [
                    {
                        "names": [
                            "docker.io/rancher/klipper-helm@sha256:87db3ad354905e6d31e420476467aefcd8f37d071a8f1c8a904f4743162ae546",
                            "docker.io/rancher/klipper-helm:v0.8.3-build20240228"
                        ],
                        "sizeBytes": 91162124
                    },
                    {
                        "names": [
                            "docker.io/kubernetesui/dashboard@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93",
                            "docker.io/kubernetesui/dashboard:v2.7.0"
                        ],
                        "sizeBytes": 75788960
                    },
                    {
                        "names": [
                            "docker.io/library/nginx@sha256:4c02d4840499a52e8b3e54b24fe1ed08fef51348edba10d81e0588f5835b902b",
                            "docker.io/library/nginx:latest"
                        ],
                        "sizeBytes": 70991765
                    },
                    {
                        "names": [
                            "docker.io/rancher/mirrored-library-traefik@sha256:606c4c924d9edd6d028a010c8f173dceb34046ed64fabdbce9ff29b2cf2b3042",
                            "docker.io/rancher/mirrored-library-traefik:2.10.7"
                        ],
                        "sizeBytes": 43240420
                    },
                    {
                        "names": [
                            "docker.io/kubernetesui/metrics-scraper@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c",
                            "docker.io/kubernetesui/metrics-scraper:v1.0.8"
                        ],
                        "sizeBytes": 19746404
                    },
                    {
                        "names": [
                            "docker.io/rancher/mirrored-metrics-server@sha256:20b8b36f8cac9e25aa2a0ff35147b13643bfec603e7e7480886632330a3bbc59",
                            "docker.io/rancher/mirrored-metrics-server:v0.7.0"
                        ],
                        "sizeBytes": 19434712
                    },
                    {
                        "names": [
                            "docker.io/rancher/local-path-provisioner@sha256:aee53cadc62bd023911e7f077877d047c5b3c269f9bba25724d558654f43cea0",
                            "docker.io/rancher/local-path-provisioner:v0.0.26"
                        ],
                        "sizeBytes": 17182090
                    },
                    {
                        "names": [
                            "docker.io/rancher/mirrored-coredns-coredns@sha256:a11fafae1f8037cbbd66c5afa40ba2423936b72b4fd50a7034a7e8b955163594",
                            "docker.io/rancher/mirrored-coredns-coredns:1.10.1"
                        ],
                        "sizeBytes": 16190137
                    },
                    {
                        "names": [
                            "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                            "docker.io/rancher/klipper-lb:v0.4.7"
                        ],
                        "sizeBytes": 4777465
                    },
                    {
                        "names": [
                            "docker.io/rancher/mirrored-pause@sha256:74c4244427b7312c5b901fe0f67cbc53683d06f4f24c6faee65d4182bf0fa893",
                            "docker.io/rancher/mirrored-pause:3.6"
                        ],
                        "sizeBytes": 301463
                    }
                ]
            }
        }
    ]
}
    
    true = True
    null = None
    false = False

    k3s_pods = {
    "kind": "PodList",
    "apiVersion": "v1",
    "metadata": {
        "resourceVersion": "2558"
    },
    "items": [
        {
            "metadata": {
                "name": "local-path-provisioner-6c86858495-5qc96",
                "generateName": "local-path-provisioner-6c86858495-",
                "namespace": "kube-system",
                "uid": "d940ea27-083c-4f14-b4f8-6516799a3ae3",
                "resourceVersion": "479",
                "creationTimestamp": "2024-05-14T16:42:20Z",
                "labels": {
                    "app": "local-path-provisioner",
                    "pod-template-hash": "6c86858495"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "local-path-provisioner-6c86858495",
                        "uid": "d685c468-9cc1-4206-8eea-41bc6db6df96",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:20Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"d685c468-9cc1-4206-8eea-41bc6db6df96\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"local-path-provisioner\"}": {
                                        ".": {},
                                        "f:command": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"POD_NAMESPACE\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:valueFrom": {
                                                    ".": {},
                                                    "f:fieldRef": {}
                                                }
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:resources": {},
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/etc/config/\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:priorityClassName": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {},
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"config-volume\"}": {
                                        ".": {},
                                        "f:configMap": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:name": {}
                                        },
                                        "f:name": {}
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:39Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.5\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "config-volume",
                        "configMap": {
                            "name": "local-path-config",
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "kube-api-access-pbkdm",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "local-path-provisioner",
                        "image": "rancher/local-path-provisioner:v0.0.26",
                        "command": [
                            "local-path-provisioner",
                            "start",
                            "--config",
                            "/etc/config/config.json"
                        ],
                        "env": [
                            {
                                "name": "POD_NAMESPACE",
                                "valueFrom": {
                                    "fieldRef": {
                                        "apiVersion": "v1",
                                        "fieldPath": "metadata.namespace"
                                    }
                                }
                            }
                        ],
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "config-volume",
                                "mountPath": "/etc/config/"
                            },
                            {
                                "name": "kube-api-access-pbkdm",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent"
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "local-path-provisioner-service-account",
                "serviceAccount": "local-path-provisioner-service-account",
                "nodeName": "kmaster",
                "securityContext": {},
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priorityClassName": "system-node-critical",
                "priority": 2000001000,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:39Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:39Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:39Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.5",
                "podIPs": [
                    {
                        "ip": "10.42.0.5"
                    }
                ],
                "startTime": "2024-05-14T16:42:20Z",
                "containerStatuses": [
                    {
                        "name": "local-path-provisioner",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:42:39Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/local-path-provisioner:v0.0.26",
                        "imageID": "docker.io/rancher/local-path-provisioner@sha256:aee53cadc62bd023911e7f077877d047c5b3c269f9bba25724d558654f43cea0",
                        "containerID": "containerd://f1107225d55ee87727b3dba09e513c58dd46463379a81f723ef80eaeb2915a7c",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "coredns-6799fbcd5-sjdrq",
                "generateName": "coredns-6799fbcd5-",
                "namespace": "kube-system",
                "uid": "951480fc-9c82-4ecb-851d-99a1832592b2",
                "resourceVersion": "488",
                "creationTimestamp": "2024-05-14T16:42:20Z",
                "labels": {
                    "k8s-app": "kube-dns",
                    "pod-template-hash": "6799fbcd5"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "coredns-6799fbcd5",
                        "uid": "2567ad30-a974-4239-a9b3-c8ca53c4eef3",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:20Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:k8s-app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"2567ad30-a974-4239-a9b3-c8ca53c4eef3\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"coredns\"}": {
                                        ".": {},
                                        "f:args": {},
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:livenessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:initialDelaySeconds": {},
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":53,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            },
                                            "k:{\"containerPort\":53,\"protocol\":\"UDP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            },
                                            "k:{\"containerPort\":9153,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:readinessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:resources": {
                                            ".": {},
                                            "f:limits": {
                                                ".": {},
                                                "f:memory": {}
                                            },
                                            "f:requests": {
                                                ".": {},
                                                "f:cpu": {},
                                                "f:memory": {}
                                            }
                                        },
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {},
                                                "f:drop": {}
                                            },
                                            "f:readOnlyRootFilesystem": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/etc/coredns\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {},
                                                "f:readOnly": {}
                                            },
                                            "k:{\"mountPath\":\"/etc/coredns/custom\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {},
                                                "f:readOnly": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:nodeSelector": {},
                                "f:priorityClassName": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {},
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {},
                                "f:topologySpreadConstraints": {
                                    ".": {},
                                    "k:{\"topologyKey\":\"kubernetes.io/hostname\",\"whenUnsatisfiable\":\"DoNotSchedule\"}": {
                                        ".": {},
                                        "f:labelSelector": {},
                                        "f:maxSkew": {},
                                        "f:topologyKey": {},
                                        "f:whenUnsatisfiable": {}
                                    }
                                },
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"config-volume\"}": {
                                        ".": {},
                                        "f:configMap": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:items": {},
                                            "f:name": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"custom-config-volume\"}": {
                                        ".": {},
                                        "f:configMap": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:name": {},
                                            "f:optional": {}
                                        },
                                        "f:name": {}
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:40Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.6\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "config-volume",
                        "configMap": {
                            "name": "coredns",
                            "items": [
                                {
                                    "key": "Corefile",
                                    "path": "Corefile"
                                },
                                {
                                    "key": "NodeHosts",
                                    "path": "NodeHosts"
                                }
                            ],
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "custom-config-volume",
                        "configMap": {
                            "name": "coredns-custom",
                            "defaultMode": 420,
                            "optional": true
                        }
                    },
                    {
                        "name": "kube-api-access-tcrth",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "coredns",
                        "image": "rancher/mirrored-coredns-coredns:1.10.1",
                        "args": [
                            "-conf",
                            "/etc/coredns/Corefile"
                        ],
                        "ports": [
                            {
                                "name": "dns",
                                "containerPort": 53,
                                "protocol": "UDP"
                            },
                            {
                                "name": "dns-tcp",
                                "containerPort": 53,
                                "protocol": "TCP"
                            },
                            {
                                "name": "metrics",
                                "containerPort": 9153,
                                "protocol": "TCP"
                            }
                        ],
                        "resources": {
                            "limits": {
                                "memory": "170Mi"
                            },
                            "requests": {
                                "cpu": "100m",
                                "memory": "70Mi"
                            }
                        },
                        "volumeMounts": [
                            {
                                "name": "config-volume",
                                "readOnly": true,
                                "mountPath": "/etc/coredns"
                            },
                            {
                                "name": "custom-config-volume",
                                "readOnly": true,
                                "mountPath": "/etc/coredns/custom"
                            },
                            {
                                "name": "kube-api-access-tcrth",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/health",
                                "port": 8080,
                                "scheme": "HTTP"
                            },
                            "initialDelaySeconds": 60,
                            "timeoutSeconds": 1,
                            "periodSeconds": 10,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/ready",
                                "port": 8181,
                                "scheme": "HTTP"
                            },
                            "timeoutSeconds": 1,
                            "periodSeconds": 2,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_BIND_SERVICE"
                                ],
                                "drop": [
                                    "all"
                                ]
                            },
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "Default",
                "nodeSelector": {
                    "kubernetes.io/os": "linux"
                },
                "serviceAccountName": "coredns",
                "serviceAccount": "coredns",
                "nodeName": "kmaster",
                "securityContext": {},
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priorityClassName": "system-cluster-critical",
                "priority": 2000000000,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority",
                "topologySpreadConstraints": [
                    {
                        "maxSkew": 1,
                        "topologyKey": "kubernetes.io/hostname",
                        "whenUnsatisfiable": "DoNotSchedule",
                        "labelSelector": {
                            "matchLabels": {
                                "k8s-app": "kube-dns"
                            }
                        }
                    }
                ]
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:40Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:40Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:40Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.6",
                "podIPs": [
                    {
                        "ip": "10.42.0.6"
                    }
                ],
                "startTime": "2024-05-14T16:42:20Z",
                "containerStatuses": [
                    {
                        "name": "coredns",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:42:39Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/mirrored-coredns-coredns:1.10.1",
                        "imageID": "docker.io/rancher/mirrored-coredns-coredns@sha256:a11fafae1f8037cbbd66c5afa40ba2423936b72b4fd50a7034a7e8b955163594",
                        "containerID": "containerd://5b5521a580759c3a4cd9630018ee96e959fe6874cddc424d2c50a72b879a37db",
                        "started": true
                    }
                ],
                "qosClass": "Burstable"
            }
        },
        {
            "metadata": {
                "name": "helm-install-traefik-crd-g8s55",
                "generateName": "helm-install-traefik-crd-",
                "namespace": "kube-system",
                "uid": "3c584101-b179-488b-9c9e-c0c92f0cb273",
                "resourceVersion": "628",
                "creationTimestamp": "2024-05-14T16:42:20Z",
                "labels": {
                    "batch.kubernetes.io/controller-uid": "7fe32f8b-4980-481d-8c51-4810499b7d8b",
                    "batch.kubernetes.io/job-name": "helm-install-traefik-crd",
                    "controller-uid": "7fe32f8b-4980-481d-8c51-4810499b7d8b",
                    "helmcharts.helm.cattle.io/chart": "traefik-crd",
                    "job-name": "helm-install-traefik-crd"
                },
                "annotations": {
                    "helmcharts.helm.cattle.io/configHash": "SHA256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "batch/v1",
                        "kind": "Job",
                        "name": "helm-install-traefik-crd",
                        "uid": "7fe32f8b-4980-481d-8c51-4810499b7d8b",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:20Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    ".": {},
                                    "f:helmcharts.helm.cattle.io/configHash": {}
                                },
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:batch.kubernetes.io/controller-uid": {},
                                    "f:batch.kubernetes.io/job-name": {},
                                    "f:controller-uid": {},
                                    "f:helmcharts.helm.cattle.io/chart": {},
                                    "f:job-name": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"7fe32f8b-4980-481d-8c51-4810499b7d8b\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"helm\"}": {
                                        ".": {},
                                        "f:args": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"AUTH_PASS_CREDENTIALS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"CHART\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"CHART_NAMESPACE\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"FAILURE_POLICY\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"HELM_DRIVER\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"HELM_VERSION\"}": {
                                                ".": {},
                                                "f:name": {}
                                            },
                                            "k:{\"name\":\"NAME\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"NO_PROXY\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"REPO\"}": {
                                                ".": {},
                                                "f:name": {}
                                            },
                                            "k:{\"name\":\"TARGET_NAMESPACE\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"VERSION\"}": {
                                                ".": {},
                                                "f:name": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:drop": {}
                                            },
                                            "f:readOnlyRootFilesystem": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/chart\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/config\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/home/klipper-helm/.cache\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/home/klipper-helm/.config\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/home/klipper-helm/.helm\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/tmp\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:nodeSelector": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:runAsNonRoot": {},
                                    "f:seccompProfile": {
                                        ".": {},
                                        "f:type": {}
                                    }
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"content\"}": {
                                        ".": {},
                                        "f:configMap": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:name": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"klipper-cache\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"klipper-config\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"klipper-helm\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"tmp\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"values\"}": {
                                        ".": {},
                                        "f:name": {},
                                        "f:secret": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:secretName": {}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:49Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:reason": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:reason": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:reason": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.4\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "klipper-helm",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "klipper-cache",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "klipper-config",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "tmp",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "values",
                        "secret": {
                            "secretName": "chart-values-traefik-crd",
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "content",
                        "configMap": {
                            "name": "chart-content-traefik-crd",
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "kube-api-access-ssl4s",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "helm",
                        "image": "rancher/klipper-helm:v0.8.3-build20240228",
                        "args": [
                            "install"
                        ],
                        "env": [
                            {
                                "name": "NAME",
                                "value": "traefik-crd"
                            },
                            {
                                "name": "VERSION"
                            },
                            {
                                "name": "REPO"
                            },
                            {
                                "name": "HELM_DRIVER",
                                "value": "secret"
                            },
                            {
                                "name": "CHART_NAMESPACE",
                                "value": "kube-system"
                            },
                            {
                                "name": "CHART",
                                "value": "https://%{KUBERNETES_API}%/static/charts/traefik-crd-25.0.3+up25.0.0.tgz"
                            },
                            {
                                "name": "HELM_VERSION"
                            },
                            {
                                "name": "TARGET_NAMESPACE",
                                "value": "kube-system"
                            },
                            {
                                "name": "AUTH_PASS_CREDENTIALS",
                                "value": "false"
                            },
                            {
                                "name": "NO_PROXY",
                                "value": ".svc,.cluster.local,10.42.0.0/16,10.43.0.0/16"
                            },
                            {
                                "name": "FAILURE_POLICY",
                                "value": "reinstall"
                            }
                        ],
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "klipper-helm",
                                "mountPath": "/home/klipper-helm/.helm"
                            },
                            {
                                "name": "klipper-cache",
                                "mountPath": "/home/klipper-helm/.cache"
                            },
                            {
                                "name": "klipper-config",
                                "mountPath": "/home/klipper-helm/.config"
                            },
                            {
                                "name": "tmp",
                                "mountPath": "/tmp"
                            },
                            {
                                "name": "values",
                                "mountPath": "/config"
                            },
                            {
                                "name": "content",
                                "mountPath": "/chart"
                            },
                            {
                                "name": "kube-api-access-ssl4s",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "drop": [
                                    "ALL"
                                ]
                            },
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "OnFailure",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "nodeSelector": {
                    "kubernetes.io/os": "linux"
                },
                "serviceAccountName": "helm-traefik-crd",
                "serviceAccount": "helm-traefik-crd",
                "nodeName": "kmaster",
                "securityContext": {
                    "runAsNonRoot": true,
                    "seccompProfile": {
                        "type": "RuntimeDefault"
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Succeeded",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "False",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:48Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z",
                        "reason": "PodCompleted"
                    },
                    {
                        "type": "Ready",
                        "status": "False",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:47Z",
                        "reason": "PodCompleted"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "False",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:47Z",
                        "reason": "PodCompleted"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.4",
                "podIPs": [
                    {
                        "ip": "10.42.0.4"
                    }
                ],
                "startTime": "2024-05-14T16:42:20Z",
                "containerStatuses": [
                    {
                        "name": "helm",
                        "state": {
                            "terminated": {
                                "exitCode": 0,
                                "reason": "Completed",
                                "message": "Installing helm_v3 chart\n",
                                "startedAt": "2024-05-14T16:42:45Z",
                                "finishedAt": "2024-05-14T16:42:47Z",
                                "containerID": "containerd://ed34a77b136e08365ed6796dadb302ae0f9d0eb6d4ee72261ca97b3af09462bc"
                            }
                        },
                        "lastState": {},
                        "ready": false,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-helm:v0.8.3-build20240228",
                        "imageID": "docker.io/rancher/klipper-helm@sha256:87db3ad354905e6d31e420476467aefcd8f37d071a8f1c8a904f4743162ae546",
                        "containerID": "containerd://ed34a77b136e08365ed6796dadb302ae0f9d0eb6d4ee72261ca97b3af09462bc",
                        "started": false
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "helm-install-traefik-qndtg",
                "generateName": "helm-install-traefik-",
                "namespace": "kube-system",
                "uid": "33082e28-adfa-4e8d-9ca6-3c15a024c64f",
                "resourceVersion": "647",
                "creationTimestamp": "2024-05-14T16:42:20Z",
                "labels": {
                    "batch.kubernetes.io/controller-uid": "431224df-4d00-4c33-ab85-03735fd16db2",
                    "batch.kubernetes.io/job-name": "helm-install-traefik",
                    "controller-uid": "431224df-4d00-4c33-ab85-03735fd16db2",
                    "helmcharts.helm.cattle.io/chart": "traefik",
                    "job-name": "helm-install-traefik"
                },
                "annotations": {
                    "helmcharts.helm.cattle.io/configHash": "SHA256=84707319CDBA292F2F3CE30082ED04B61AF82B4E4E169A849D4ABC7356CAD361"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "batch/v1",
                        "kind": "Job",
                        "name": "helm-install-traefik",
                        "uid": "431224df-4d00-4c33-ab85-03735fd16db2",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:20Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    ".": {},
                                    "f:helmcharts.helm.cattle.io/configHash": {}
                                },
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:batch.kubernetes.io/controller-uid": {},
                                    "f:batch.kubernetes.io/job-name": {},
                                    "f:controller-uid": {},
                                    "f:helmcharts.helm.cattle.io/chart": {},
                                    "f:job-name": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"431224df-4d00-4c33-ab85-03735fd16db2\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"helm\"}": {
                                        ".": {},
                                        "f:args": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"AUTH_PASS_CREDENTIALS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"CHART\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"CHART_NAMESPACE\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"FAILURE_POLICY\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"HELM_DRIVER\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"HELM_VERSION\"}": {
                                                ".": {},
                                                "f:name": {}
                                            },
                                            "k:{\"name\":\"NAME\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"NO_PROXY\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"REPO\"}": {
                                                ".": {},
                                                "f:name": {}
                                            },
                                            "k:{\"name\":\"TARGET_NAMESPACE\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"VERSION\"}": {
                                                ".": {},
                                                "f:name": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:drop": {}
                                            },
                                            "f:readOnlyRootFilesystem": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/chart\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/config\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/home/klipper-helm/.cache\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/home/klipper-helm/.config\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/home/klipper-helm/.helm\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/tmp\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:nodeSelector": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:runAsNonRoot": {},
                                    "f:seccompProfile": {
                                        ".": {},
                                        "f:type": {}
                                    }
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"content\"}": {
                                        ".": {},
                                        "f:configMap": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:name": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"klipper-cache\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"klipper-config\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"klipper-helm\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"tmp\"}": {
                                        ".": {},
                                        "f:emptyDir": {
                                            ".": {},
                                            "f:medium": {}
                                        },
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"values\"}": {
                                        ".": {},
                                        "f:name": {},
                                        "f:secret": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:secretName": {}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:52Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:reason": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:reason": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:reason": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.2\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "klipper-helm",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "klipper-cache",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "klipper-config",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "tmp",
                        "emptyDir": {
                            "medium": "Memory"
                        }
                    },
                    {
                        "name": "values",
                        "secret": {
                            "secretName": "chart-values-traefik",
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "content",
                        "configMap": {
                            "name": "chart-content-traefik",
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "kube-api-access-jq8bf",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "helm",
                        "image": "rancher/klipper-helm:v0.8.3-build20240228",
                        "args": [
                            "install",
                            "--set-string",
                            "global.systemDefaultRegistry="
                        ],
                        "env": [
                            {
                                "name": "NAME",
                                "value": "traefik"
                            },
                            {
                                "name": "VERSION"
                            },
                            {
                                "name": "REPO"
                            },
                            {
                                "name": "HELM_DRIVER",
                                "value": "secret"
                            },
                            {
                                "name": "CHART_NAMESPACE",
                                "value": "kube-system"
                            },
                            {
                                "name": "CHART",
                                "value": "https://%{KUBERNETES_API}%/static/charts/traefik-25.0.3+up25.0.0.tgz"
                            },
                            {
                                "name": "HELM_VERSION"
                            },
                            {
                                "name": "TARGET_NAMESPACE",
                                "value": "kube-system"
                            },
                            {
                                "name": "AUTH_PASS_CREDENTIALS",
                                "value": "false"
                            },
                            {
                                "name": "NO_PROXY",
                                "value": ".svc,.cluster.local,10.42.0.0/16,10.43.0.0/16"
                            },
                            {
                                "name": "FAILURE_POLICY",
                                "value": "reinstall"
                            }
                        ],
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "klipper-helm",
                                "mountPath": "/home/klipper-helm/.helm"
                            },
                            {
                                "name": "klipper-cache",
                                "mountPath": "/home/klipper-helm/.cache"
                            },
                            {
                                "name": "klipper-config",
                                "mountPath": "/home/klipper-helm/.config"
                            },
                            {
                                "name": "tmp",
                                "mountPath": "/tmp"
                            },
                            {
                                "name": "values",
                                "mountPath": "/config"
                            },
                            {
                                "name": "content",
                                "mountPath": "/chart"
                            },
                            {
                                "name": "kube-api-access-jq8bf",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "drop": [
                                    "ALL"
                                ]
                            },
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "OnFailure",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "nodeSelector": {
                    "kubernetes.io/os": "linux"
                },
                "serviceAccountName": "helm-traefik",
                "serviceAccount": "helm-traefik",
                "nodeName": "kmaster",
                "securityContext": {
                    "runAsNonRoot": true,
                    "seccompProfile": {
                        "type": "RuntimeDefault"
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Succeeded",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "False",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:51Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z",
                        "reason": "PodCompleted"
                    },
                    {
                        "type": "Ready",
                        "status": "False",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:50Z",
                        "reason": "PodCompleted"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "False",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:50Z",
                        "reason": "PodCompleted"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.2",
                "podIPs": [
                    {
                        "ip": "10.42.0.2"
                    }
                ],
                "startTime": "2024-05-14T16:42:20Z",
                "containerStatuses": [
                    {
                        "name": "helm",
                        "state": {
                            "terminated": {
                                "exitCode": 0,
                                "reason": "Completed",
                                "message": "Installing helm_v3 chart\n",
                                "startedAt": "2024-05-14T16:42:47Z",
                                "finishedAt": "2024-05-14T16:42:50Z",
                                "containerID": "containerd://fac67c172c6556525e6af0b8a47645ce88d861c526e0833bf138382deeccf3db"
                            }
                        },
                        "lastState": {},
                        "ready": false,
                        "restartCount": 1,
                        "image": "docker.io/rancher/klipper-helm:v0.8.3-build20240228",
                        "imageID": "docker.io/rancher/klipper-helm@sha256:87db3ad354905e6d31e420476467aefcd8f37d071a8f1c8a904f4743162ae546",
                        "containerID": "containerd://fac67c172c6556525e6af0b8a47645ce88d861c526e0833bf138382deeccf3db",
                        "started": false
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "svclb-traefik-af76f4e9-djbvs",
                "generateName": "svclb-traefik-af76f4e9-",
                "namespace": "kube-system",
                "uid": "563b4e9d-f693-4083-a4bf-6f16c5a596f2",
                "resourceVersion": "650",
                "creationTimestamp": "2024-05-14T16:42:48Z",
                "labels": {
                    "app": "svclb-traefik-af76f4e9",
                    "controller-revision-hash": "6445db8dff",
                    "pod-template-generation": "1",
                    "svccontroller.k3s.cattle.io/svcname": "traefik",
                    "svccontroller.k3s.cattle.io/svcnamespace": "kube-system"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "DaemonSet",
                        "name": "svclb-traefik-af76f4e9",
                        "uid": "0035135d-cf99-4d63-a960-1d5352e0658b",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:48Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app": {},
                                    "f:controller-revision-hash": {},
                                    "f:pod-template-generation": {},
                                    "f:svccontroller.k3s.cattle.io/svcname": {},
                                    "f:svccontroller.k3s.cattle.io/svcnamespace": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"0035135d-cf99-4d63-a960-1d5352e0658b\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:affinity": {
                                    ".": {},
                                    "f:nodeAffinity": {
                                        ".": {},
                                        "f:requiredDuringSchedulingIgnoredDuringExecution": {}
                                    }
                                },
                                "f:automountServiceAccountToken": {},
                                "f:containers": {
                                    "k:{\"name\":\"lb-tcp-443\"}": {
                                        ".": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"DEST_IPS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PROTO\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_RANGES\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":443,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:hostPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {}
                                            }
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    },
                                    "k:{\"name\":\"lb-tcp-80\"}": {
                                        ".": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"DEST_IPS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PROTO\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_RANGES\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":80,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:hostPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {}
                                            }
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:sysctls": {}
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:53Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.7\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "containers": [
                    {
                        "name": "lb-tcp-80",
                        "image": "rancher/klipper-lb:v0.4.7",
                        "ports": [
                            {
                                "name": "lb-tcp-80",
                                "hostPort": 80,
                                "containerPort": 80,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "SRC_PORT",
                                "value": "80"
                            },
                            {
                                "name": "SRC_RANGES",
                                "value": "0.0.0.0/0"
                            },
                            {
                                "name": "DEST_PROTO",
                                "value": "TCP"
                            },
                            {
                                "name": "DEST_PORT",
                                "value": "80"
                            },
                            {
                                "name": "DEST_IPS",
                                "value": "10.43.246.47"
                            }
                        ],
                        "resources": {},
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_ADMIN"
                                ]
                            }
                        }
                    },
                    {
                        "name": "lb-tcp-443",
                        "image": "rancher/klipper-lb:v0.4.7",
                        "ports": [
                            {
                                "name": "lb-tcp-443",
                                "hostPort": 443,
                                "containerPort": 443,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "SRC_PORT",
                                "value": "443"
                            },
                            {
                                "name": "SRC_RANGES",
                                "value": "0.0.0.0/0"
                            },
                            {
                                "name": "DEST_PROTO",
                                "value": "TCP"
                            },
                            {
                                "name": "DEST_PORT",
                                "value": "443"
                            },
                            {
                                "name": "DEST_IPS",
                                "value": "10.43.246.47"
                            }
                        ],
                        "resources": {},
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_ADMIN"
                                ]
                            }
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "svclb",
                "serviceAccount": "svclb",
                "automountServiceAccountToken": false,
                "nodeName": "kmaster",
                "securityContext": {
                    "sysctls": [
                        {
                            "name": "net.ipv4.ip_forward",
                            "value": "1"
                        }
                    ]
                },
                "affinity": {
                    "nodeAffinity": {
                        "requiredDuringSchedulingIgnoredDuringExecution": {
                            "nodeSelectorTerms": [
                                {
                                    "matchFields": [
                                        {
                                            "key": "metadata.name",
                                            "operator": "In",
                                            "values": [
                                                "kmaster"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute"
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute"
                    },
                    {
                        "key": "node.kubernetes.io/disk-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/memory-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/pid-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/unschedulable",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:53Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:48Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:53Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:53Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:48Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.7",
                "podIPs": [
                    {
                        "ip": "10.42.0.7"
                    }
                ],
                "startTime": "2024-05-14T16:42:48Z",
                "containerStatuses": [
                    {
                        "name": "lb-tcp-443",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:42:52Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-lb:v0.4.7",
                        "imageID": "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                        "containerID": "containerd://3425e3df756bf7fef7a999e40341981e0824f3bc43576f705b39bc5812f270bf",
                        "started": true
                    },
                    {
                        "name": "lb-tcp-80",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:42:52Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-lb:v0.4.7",
                        "imageID": "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                        "containerID": "containerd://f78536b232d3f0e3c9ad9b17879455043ea2724b778500b4208e86b64978cad0",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "metrics-server-54fd9b65b-fj8jv",
                "generateName": "metrics-server-54fd9b65b-",
                "namespace": "kube-system",
                "uid": "05e8d97f-c1aa-4f92-be5c-dbd368dcc2e5",
                "resourceVersion": "657",
                "creationTimestamp": "2024-05-14T16:42:20Z",
                "labels": {
                    "k8s-app": "metrics-server",
                    "pod-template-hash": "54fd9b65b"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "metrics-server-54fd9b65b",
                        "uid": "f78e00ea-61fd-4e01-a8d8-33eeb8582a22",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:20Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:k8s-app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"f78e00ea-61fd-4e01-a8d8-33eeb8582a22\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"metrics-server\"}": {
                                        ".": {},
                                        "f:args": {},
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:livenessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:initialDelaySeconds": {},
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":10250,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:readinessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:resources": {
                                            ".": {},
                                            "f:requests": {
                                                ".": {},
                                                "f:cpu": {},
                                                "f:memory": {}
                                            }
                                        },
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:readOnlyRootFilesystem": {},
                                            "f:runAsNonRoot": {},
                                            "f:runAsUser": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/tmp\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:priorityClassName": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {},
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"tmp-dir\"}": {
                                        ".": {},
                                        "f:emptyDir": {},
                                        "f:name": {}
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:56Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.3\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "tmp-dir",
                        "emptyDir": {}
                    },
                    {
                        "name": "kube-api-access-rl2gr",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "metrics-server",
                        "image": "rancher/mirrored-metrics-server:v0.7.0",
                        "args": [
                            "--cert-dir=/tmp",
                            "--secure-port=10250",
                            "--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname",
                            "--kubelet-use-node-status-port",
                            "--metric-resolution=15s",
                            "--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305"
                        ],
                        "ports": [
                            {
                                "name": "https",
                                "containerPort": 10250,
                                "protocol": "TCP"
                            }
                        ],
                        "resources": {
                            "requests": {
                                "cpu": "100m",
                                "memory": "70Mi"
                            }
                        },
                        "volumeMounts": [
                            {
                                "name": "tmp-dir",
                                "mountPath": "/tmp"
                            },
                            {
                                "name": "kube-api-access-rl2gr",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/livez",
                                "port": "https",
                                "scheme": "HTTPS"
                            },
                            "initialDelaySeconds": 60,
                            "timeoutSeconds": 1,
                            "periodSeconds": 10,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/readyz",
                                "port": "https",
                                "scheme": "HTTPS"
                            },
                            "timeoutSeconds": 1,
                            "periodSeconds": 2,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "runAsUser": 1000,
                            "runAsNonRoot": true,
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "metrics-server",
                "serviceAccount": "metrics-server",
                "nodeName": "kmaster",
                "securityContext": {},
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priorityClassName": "system-node-critical",
                "priority": 2000001000,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:41Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:56Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:56Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:20Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.3",
                "podIPs": [
                    {
                        "ip": "10.42.0.3"
                    }
                ],
                "startTime": "2024-05-14T16:42:20Z",
                "containerStatuses": [
                    {
                        "name": "metrics-server",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:42:40Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/mirrored-metrics-server:v0.7.0",
                        "imageID": "docker.io/rancher/mirrored-metrics-server@sha256:20b8b36f8cac9e25aa2a0ff35147b13643bfec603e7e7480886632330a3bbc59",
                        "containerID": "containerd://d2881fc20b985ac4fbbae74d8b0bd21db80c11b4f6cf1d2acc8e72368d5e2e5b",
                        "started": true
                    }
                ],
                "qosClass": "Burstable"
            }
        },
        {
            "metadata": {
                "name": "traefik-7d5f6474df-rcthq",
                "generateName": "traefik-7d5f6474df-",
                "namespace": "kube-system",
                "uid": "11d5a399-7e5b-4259-83e1-44cac6fac1ff",
                "resourceVersion": "670",
                "creationTimestamp": "2024-05-14T16:42:48Z",
                "labels": {
                    "app.kubernetes.io/instance": "traefik-kube-system",
                    "app.kubernetes.io/managed-by": "Helm",
                    "app.kubernetes.io/name": "traefik",
                    "helm.sh/chart": "traefik-25.0.3_up25.0.0",
                    "pod-template-hash": "7d5f6474df"
                },
                "annotations": {
                    "prometheus.io/path": "/metrics",
                    "prometheus.io/port": "9100",
                    "prometheus.io/scrape": "true"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "traefik-7d5f6474df",
                        "uid": "cce1692d-7cae-4777-b47c-a5449301142f",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:48Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:annotations": {
                                    ".": {},
                                    "f:prometheus.io/path": {},
                                    "f:prometheus.io/port": {},
                                    "f:prometheus.io/scrape": {}
                                },
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app.kubernetes.io/instance": {},
                                    "f:app.kubernetes.io/managed-by": {},
                                    "f:app.kubernetes.io/name": {},
                                    "f:helm.sh/chart": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"cce1692d-7cae-4777-b47c-a5449301142f\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"traefik\"}": {
                                        ".": {},
                                        "f:args": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"POD_NAME\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:valueFrom": {
                                                    ".": {},
                                                    "f:fieldRef": {}
                                                }
                                            },
                                            "k:{\"name\":\"POD_NAMESPACE\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:valueFrom": {
                                                    ".": {},
                                                    "f:fieldRef": {}
                                                }
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:livenessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:initialDelaySeconds": {},
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":8000,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            },
                                            "k:{\"containerPort\":8443,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            },
                                            "k:{\"containerPort\":9000,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            },
                                            "k:{\"containerPort\":9100,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:readinessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:initialDelaySeconds": {},
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:drop": {}
                                            },
                                            "f:readOnlyRootFilesystem": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/data\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/tmp\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:priorityClassName": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:fsGroupChangePolicy": {},
                                    "f:runAsGroup": {},
                                    "f:runAsNonRoot": {},
                                    "f:runAsUser": {}
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"data\"}": {
                                        ".": {},
                                        "f:emptyDir": {},
                                        "f:name": {}
                                    },
                                    "k:{\"name\":\"tmp\"}": {
                                        ".": {},
                                        "f:emptyDir": {},
                                        "f:name": {}
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:42:59Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.8\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "data",
                        "emptyDir": {}
                    },
                    {
                        "name": "tmp",
                        "emptyDir": {}
                    },
                    {
                        "name": "kube-api-access-79qtl",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "traefik",
                        "image": "rancher/mirrored-library-traefik:2.10.7",
                        "args": [
                            "--global.checknewversion",
                            "--global.sendanonymoususage",
                            "--entrypoints.metrics.address=:9100/tcp",
                            "--entrypoints.traefik.address=:9000/tcp",
                            "--entrypoints.web.address=:8000/tcp",
                            "--entrypoints.websecure.address=:8443/tcp",
                            "--api.dashboard=true",
                            "--ping=true",
                            "--metrics.prometheus=true",
                            "--metrics.prometheus.entrypoint=metrics",
                            "--providers.kubernetescrd",
                            "--providers.kubernetesingress",
                            "--providers.kubernetesingress.ingressendpoint.publishedservice=kube-system/traefik",
                            "--entrypoints.websecure.http.tls=true"
                        ],
                        "ports": [
                            {
                                "name": "metrics",
                                "containerPort": 9100,
                                "protocol": "TCP"
                            },
                            {
                                "name": "traefik",
                                "containerPort": 9000,
                                "protocol": "TCP"
                            },
                            {
                                "name": "web",
                                "containerPort": 8000,
                                "protocol": "TCP"
                            },
                            {
                                "name": "websecure",
                                "containerPort": 8443,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "POD_NAME",
                                "valueFrom": {
                                    "fieldRef": {
                                        "apiVersion": "v1",
                                        "fieldPath": "metadata.name"
                                    }
                                }
                            },
                            {
                                "name": "POD_NAMESPACE",
                                "valueFrom": {
                                    "fieldRef": {
                                        "apiVersion": "v1",
                                        "fieldPath": "metadata.namespace"
                                    }
                                }
                            }
                        ],
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "data",
                                "mountPath": "/data"
                            },
                            {
                                "name": "tmp",
                                "mountPath": "/tmp"
                            },
                            {
                                "name": "kube-api-access-79qtl",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/ping",
                                "port": 9000,
                                "scheme": "HTTP"
                            },
                            "initialDelaySeconds": 2,
                            "timeoutSeconds": 2,
                            "periodSeconds": 10,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/ping",
                                "port": 9000,
                                "scheme": "HTTP"
                            },
                            "initialDelaySeconds": 2,
                            "timeoutSeconds": 2,
                            "periodSeconds": 10,
                            "successThreshold": 1,
                            "failureThreshold": 1
                        },
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "drop": [
                                    "ALL"
                                ]
                            },
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 60,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "traefik",
                "serviceAccount": "traefik",
                "nodeName": "kmaster",
                "securityContext": {
                    "runAsUser": 65532,
                    "runAsGroup": 65532,
                    "runAsNonRoot": true,
                    "fsGroupChangePolicy": "OnRootMismatch"
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priorityClassName": "system-cluster-critical",
                "priority": 2000000000,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:57Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:48Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:59Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:59Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:42:48Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.8",
                "podIPs": [
                    {
                        "ip": "10.42.0.8"
                    }
                ],
                "startTime": "2024-05-14T16:42:48Z",
                "containerStatuses": [
                    {
                        "name": "traefik",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:42:57Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/mirrored-library-traefik:2.10.7",
                        "imageID": "docker.io/rancher/mirrored-library-traefik@sha256:606c4c924d9edd6d028a010c8f173dceb34046ed64fabdbce9ff29b2cf2b3042",
                        "containerID": "containerd://f964f6be08fc0f3771695868964b6400a410d6dcc83c6932244d5d5d75c323a9",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "nginx-deployment-6d6565499c-4gwbq",
                "generateName": "nginx-deployment-6d6565499c-",
                "namespace": "default",
                "uid": "784b9f35-177f-4c9f-940c-da86991b13e8",
                "resourceVersion": "737",
                "creationTimestamp": "2024-05-14T16:44:47Z",
                "labels": {
                    "app": "nginx-deployment",
                    "pod-template-hash": "6d6565499c"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "nginx-deployment-6d6565499c",
                        "uid": "e87756b9-d5b5-416c-9614-ac4440a83d8e",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:44:47Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"e87756b9-d5b5-416c-9614-ac4440a83d8e\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"nginx\"}": {
                                        ".": {},
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:resources": {},
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {},
                                "f:terminationGracePeriodSeconds": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:44:59Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.9\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "kube-api-access-wwc2t",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx",
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "kube-api-access-wwc2t",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "Always"
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "default",
                "serviceAccount": "default",
                "nodeName": "kmaster",
                "securityContext": {},
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:59Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:47Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:59Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:59Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:47Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.9",
                "podIPs": [
                    {
                        "ip": "10.42.0.9"
                    }
                ],
                "startTime": "2024-05-14T16:44:47Z",
                "containerStatuses": [
                    {
                        "name": "nginx",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:44:59Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/library/nginx:latest",
                        "imageID": "docker.io/library/nginx@sha256:4c02d4840499a52e8b3e54b24fe1ed08fef51348edba10d81e0588f5835b902b",
                        "containerID": "containerd://cf774f229f60f1b098b7bf5dc846d14ad9a6e95b150d6fc74af201ea898cddac",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "nginx-deployment-6d6565499c-4h858",
                "generateName": "nginx-deployment-6d6565499c-",
                "namespace": "default",
                "uid": "66fa2274-1880-40ea-873f-d0ab02ca5ae2",
                "resourceVersion": "740",
                "creationTimestamp": "2024-05-14T16:44:47Z",
                "labels": {
                    "app": "nginx-deployment",
                    "pod-template-hash": "6d6565499c"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "nginx-deployment-6d6565499c",
                        "uid": "e87756b9-d5b5-416c-9614-ac4440a83d8e",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:44:47Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"e87756b9-d5b5-416c-9614-ac4440a83d8e\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"nginx\"}": {
                                        ".": {},
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:resources": {},
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {},
                                "f:terminationGracePeriodSeconds": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:44:59Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.10\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "kube-api-access-jd8ck",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx",
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "kube-api-access-jd8ck",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "Always"
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "default",
                "serviceAccount": "default",
                "nodeName": "kmaster",
                "securityContext": {},
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:59Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:47Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:59Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:59Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:44:47Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.10",
                "podIPs": [
                    {
                        "ip": "10.42.0.10"
                    }
                ],
                "startTime": "2024-05-14T16:44:47Z",
                "containerStatuses": [
                    {
                        "name": "nginx",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:44:59Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/library/nginx:latest",
                        "imageID": "docker.io/library/nginx@sha256:4c02d4840499a52e8b3e54b24fe1ed08fef51348edba10d81e0588f5835b902b",
                        "containerID": "containerd://122e2e1f15a1a587d6c9fc93faaef02b7fd4ed6f935a8b5d52d84663021ba927",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "dashboard-metrics-scraper-5657497c4c-k2wdt",
                "generateName": "dashboard-metrics-scraper-5657497c4c-",
                "namespace": "kubernetes-dashboard",
                "uid": "461cf436-dde2-46eb-9a76-d9477e2a7cb8",
                "resourceVersion": "840",
                "creationTimestamp": "2024-05-14T16:47:05Z",
                "labels": {
                    "k8s-app": "dashboard-metrics-scraper",
                    "pod-template-hash": "5657497c4c"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "dashboard-metrics-scraper-5657497c4c",
                        "uid": "15877e3d-2ea9-41d5-aa96-346eb293edc4",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:47:05Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:k8s-app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"15877e3d-2ea9-41d5-aa96-346eb293edc4\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"dashboard-metrics-scraper\"}": {
                                        ".": {},
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:livenessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:initialDelaySeconds": {},
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":8000,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:readOnlyRootFilesystem": {},
                                            "f:runAsGroup": {},
                                            "f:runAsUser": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/tmp\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:nodeSelector": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:seccompProfile": {
                                        ".": {},
                                        "f:type": {}
                                    }
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"tmp-volume\"}": {
                                        ".": {},
                                        "f:emptyDir": {},
                                        "f:name": {}
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:47:14Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.12\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "tmp-volume",
                        "emptyDir": {}
                    },
                    {
                        "name": "kube-api-access-h4kzc",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "dashboard-metrics-scraper",
                        "image": "kubernetesui/metrics-scraper:v1.0.8",
                        "ports": [
                            {
                                "containerPort": 8000,
                                "protocol": "TCP"
                            }
                        ],
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "tmp-volume",
                                "mountPath": "/tmp"
                            },
                            {
                                "name": "kube-api-access-h4kzc",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/",
                                "port": 8000,
                                "scheme": "HTTP"
                            },
                            "initialDelaySeconds": 30,
                            "timeoutSeconds": 30,
                            "periodSeconds": 10,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "runAsUser": 1001,
                            "runAsGroup": 2001,
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "nodeSelector": {
                    "kubernetes.io/os": "linux"
                },
                "serviceAccountName": "kubernetes-dashboard",
                "serviceAccount": "kubernetes-dashboard",
                "nodeName": "kmaster",
                "securityContext": {
                    "seccompProfile": {
                        "type": "RuntimeDefault"
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node-role.kubernetes.io/master",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:13Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:05Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:13Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:13Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:05Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.12",
                "podIPs": [
                    {
                        "ip": "10.42.0.12"
                    }
                ],
                "startTime": "2024-05-14T16:47:05Z",
                "containerStatuses": [
                    {
                        "name": "dashboard-metrics-scraper",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:47:13Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/kubernetesui/metrics-scraper:v1.0.8",
                        "imageID": "docker.io/kubernetesui/metrics-scraper@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c",
                        "containerID": "containerd://730abead18ee15133f6bf53cd2e562310422ee3314343f9d6c4dbc4a0c6d6362",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "kubernetes-dashboard-78f87ddfc-g8r2q",
                "generateName": "kubernetes-dashboard-78f87ddfc-",
                "namespace": "kubernetes-dashboard",
                "uid": "195f596a-a792-4697-8b6b-a64f4c089d89",
                "resourceVersion": "853",
                "creationTimestamp": "2024-05-14T16:47:05Z",
                "labels": {
                    "k8s-app": "kubernetes-dashboard",
                    "pod-template-hash": "78f87ddfc"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "ReplicaSet",
                        "name": "kubernetes-dashboard-78f87ddfc",
                        "uid": "562a25ae-c13e-433d-968f-986532bede5e",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:47:05Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:k8s-app": {},
                                    "f:pod-template-hash": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"562a25ae-c13e-433d-968f-986532bede5e\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:containers": {
                                    "k:{\"name\":\"kubernetes-dashboard\"}": {
                                        ".": {},
                                        "f:args": {},
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:livenessProbe": {
                                            ".": {},
                                            "f:failureThreshold": {},
                                            "f:httpGet": {
                                                ".": {},
                                                "f:path": {},
                                                "f:port": {},
                                                "f:scheme": {}
                                            },
                                            "f:initialDelaySeconds": {},
                                            "f:periodSeconds": {},
                                            "f:successThreshold": {},
                                            "f:timeoutSeconds": {}
                                        },
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":8443,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:allowPrivilegeEscalation": {},
                                            "f:readOnlyRootFilesystem": {},
                                            "f:runAsGroup": {},
                                            "f:runAsUser": {}
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {},
                                        "f:volumeMounts": {
                                            ".": {},
                                            "k:{\"mountPath\":\"/certs\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            },
                                            "k:{\"mountPath\":\"/tmp\"}": {
                                                ".": {},
                                                "f:mountPath": {},
                                                "f:name": {}
                                            }
                                        }
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:nodeSelector": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:seccompProfile": {
                                        ".": {},
                                        "f:type": {}
                                    }
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {},
                                "f:volumes": {
                                    ".": {},
                                    "k:{\"name\":\"kubernetes-dashboard-certs\"}": {
                                        ".": {},
                                        "f:name": {},
                                        "f:secret": {
                                            ".": {},
                                            "f:defaultMode": {},
                                            "f:secretName": {}
                                        }
                                    },
                                    "k:{\"name\":\"tmp-volume\"}": {
                                        ".": {},
                                        "f:emptyDir": {},
                                        "f:name": {}
                                    }
                                }
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:47:21Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.0.11\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "volumes": [
                    {
                        "name": "kubernetes-dashboard-certs",
                        "secret": {
                            "secretName": "kubernetes-dashboard-certs",
                            "defaultMode": 420
                        }
                    },
                    {
                        "name": "tmp-volume",
                        "emptyDir": {}
                    },
                    {
                        "name": "kube-api-access-xlhth",
                        "projected": {
                            "sources": [
                                {
                                    "serviceAccountToken": {
                                        "expirationSeconds": 3607,
                                        "path": "token"
                                    }
                                },
                                {
                                    "configMap": {
                                        "name": "kube-root-ca.crt",
                                        "items": [
                                            {
                                                "key": "ca.crt",
                                                "path": "ca.crt"
                                            }
                                        ]
                                    }
                                },
                                {
                                    "downwardAPI": {
                                        "items": [
                                            {
                                                "path": "namespace",
                                                "fieldRef": {
                                                    "apiVersion": "v1",
                                                    "fieldPath": "metadata.namespace"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "defaultMode": 420
                        }
                    }
                ],
                "containers": [
                    {
                        "name": "kubernetes-dashboard",
                        "image": "kubernetesui/dashboard:v2.7.0",
                        "args": [
                            "--auto-generate-certificates",
                            "--namespace=kubernetes-dashboard"
                        ],
                        "ports": [
                            {
                                "containerPort": 8443,
                                "protocol": "TCP"
                            }
                        ],
                        "resources": {},
                        "volumeMounts": [
                            {
                                "name": "kubernetes-dashboard-certs",
                                "mountPath": "/certs"
                            },
                            {
                                "name": "tmp-volume",
                                "mountPath": "/tmp"
                            },
                            {
                                "name": "kube-api-access-xlhth",
                                "readOnly": true,
                                "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                            }
                        ],
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/",
                                "port": 8443,
                                "scheme": "HTTPS"
                            },
                            "initialDelaySeconds": 30,
                            "timeoutSeconds": 30,
                            "periodSeconds": 10,
                            "successThreshold": 1,
                            "failureThreshold": 3
                        },
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "Always",
                        "securityContext": {
                            "runAsUser": 1001,
                            "runAsGroup": 2001,
                            "readOnlyRootFilesystem": true,
                            "allowPrivilegeEscalation": false
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "nodeSelector": {
                    "kubernetes.io/os": "linux"
                },
                "serviceAccountName": "kubernetes-dashboard",
                "serviceAccount": "kubernetes-dashboard",
                "nodeName": "kmaster",
                "securityContext": {
                    "seccompProfile": {
                        "type": "RuntimeDefault"
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node-role.kubernetes.io/master",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute",
                        "tolerationSeconds": 300
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:21Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:05Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:21Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:21Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:47:05Z"
                    }
                ],
                "hostIP": "192.168.186.216",
                "hostIPs": [
                    {
                        "ip": "192.168.186.216"
                    }
                ],
                "podIP": "10.42.0.11",
                "podIPs": [
                    {
                        "ip": "10.42.0.11"
                    }
                ],
                "startTime": "2024-05-14T16:47:05Z",
                "containerStatuses": [
                    {
                        "name": "kubernetes-dashboard",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:47:20Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/kubernetesui/dashboard:v2.7.0",
                        "imageID": "docker.io/kubernetesui/dashboard@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93",
                        "containerID": "containerd://afe253a91c1d3f44620003df5006f2dab406b7377d73f9e02bdb17c5027e10fc",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "svclb-traefik-af76f4e9-cfqpw",
                "generateName": "svclb-traefik-af76f4e9-",
                "namespace": "kube-system",
                "uid": "7cf3e8dd-e51d-4e06-be71-035a5b4f768d",
                "resourceVersion": "1149",
                "creationTimestamp": "2024-05-14T16:59:09Z",
                "labels": {
                    "app": "svclb-traefik-af76f4e9",
                    "controller-revision-hash": "6445db8dff",
                    "pod-template-generation": "1",
                    "svccontroller.k3s.cattle.io/svcname": "traefik",
                    "svccontroller.k3s.cattle.io/svcnamespace": "kube-system"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "DaemonSet",
                        "name": "svclb-traefik-af76f4e9",
                        "uid": "0035135d-cf99-4d63-a960-1d5352e0658b",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:59:09Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app": {},
                                    "f:controller-revision-hash": {},
                                    "f:pod-template-generation": {},
                                    "f:svccontroller.k3s.cattle.io/svcname": {},
                                    "f:svccontroller.k3s.cattle.io/svcnamespace": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"0035135d-cf99-4d63-a960-1d5352e0658b\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:affinity": {
                                    ".": {},
                                    "f:nodeAffinity": {
                                        ".": {},
                                        "f:requiredDuringSchedulingIgnoredDuringExecution": {}
                                    }
                                },
                                "f:automountServiceAccountToken": {},
                                "f:containers": {
                                    "k:{\"name\":\"lb-tcp-443\"}": {
                                        ".": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"DEST_IPS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PROTO\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_RANGES\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":443,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:hostPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {}
                                            }
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    },
                                    "k:{\"name\":\"lb-tcp-80\"}": {
                                        ".": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"DEST_IPS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PROTO\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_RANGES\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":80,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:hostPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {}
                                            }
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:sysctls": {}
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:59:23Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.2.2\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "containers": [
                    {
                        "name": "lb-tcp-80",
                        "image": "rancher/klipper-lb:v0.4.7",
                        "ports": [
                            {
                                "name": "lb-tcp-80",
                                "hostPort": 80,
                                "containerPort": 80,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "SRC_PORT",
                                "value": "80"
                            },
                            {
                                "name": "SRC_RANGES",
                                "value": "0.0.0.0/0"
                            },
                            {
                                "name": "DEST_PROTO",
                                "value": "TCP"
                            },
                            {
                                "name": "DEST_PORT",
                                "value": "80"
                            },
                            {
                                "name": "DEST_IPS",
                                "value": "10.43.246.47"
                            }
                        ],
                        "resources": {},
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_ADMIN"
                                ]
                            }
                        }
                    },
                    {
                        "name": "lb-tcp-443",
                        "image": "rancher/klipper-lb:v0.4.7",
                        "ports": [
                            {
                                "name": "lb-tcp-443",
                                "hostPort": 443,
                                "containerPort": 443,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "SRC_PORT",
                                "value": "443"
                            },
                            {
                                "name": "SRC_RANGES",
                                "value": "0.0.0.0/0"
                            },
                            {
                                "name": "DEST_PROTO",
                                "value": "TCP"
                            },
                            {
                                "name": "DEST_PORT",
                                "value": "443"
                            },
                            {
                                "name": "DEST_IPS",
                                "value": "10.43.246.47"
                            }
                        ],
                        "resources": {},
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_ADMIN"
                                ]
                            }
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "svclb",
                "serviceAccount": "svclb",
                "automountServiceAccountToken": false,
                "nodeName": "kworker1",
                "securityContext": {
                    "sysctls": [
                        {
                            "name": "net.ipv4.ip_forward",
                            "value": "1"
                        }
                    ]
                },
                "affinity": {
                    "nodeAffinity": {
                        "requiredDuringSchedulingIgnoredDuringExecution": {
                            "nodeSelectorTerms": [
                                {
                                    "matchFields": [
                                        {
                                            "key": "metadata.name",
                                            "operator": "In",
                                            "values": [
                                                "kworker1"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute"
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute"
                    },
                    {
                        "key": "node.kubernetes.io/disk-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/memory-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/pid-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/unschedulable",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:23Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:09Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:23Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:23Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:09Z"
                    }
                ],
                "hostIP": "192.168.186.217",
                "hostIPs": [
                    {
                        "ip": "192.168.186.217"
                    }
                ],
                "podIP": "10.42.2.2",
                "podIPs": [
                    {
                        "ip": "10.42.2.2"
                    }
                ],
                "startTime": "2024-05-14T16:59:09Z",
                "containerStatuses": [
                    {
                        "name": "lb-tcp-443",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:59:22Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-lb:v0.4.7",
                        "imageID": "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                        "containerID": "containerd://5366368d4f4e7ce58607ed2e1090ed0e0452f007b7de844537135544cda902d0",
                        "started": true
                    },
                    {
                        "name": "lb-tcp-80",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:59:22Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-lb:v0.4.7",
                        "imageID": "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                        "containerID": "containerd://f46727df4b7f00159867b1627aea84a7ffc970612097b65d2f8d8760c4073c2a",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        },
        {
            "metadata": {
                "name": "svclb-traefik-af76f4e9-9xn68",
                "generateName": "svclb-traefik-af76f4e9-",
                "namespace": "kube-system",
                "uid": "067e2cbf-18ca-4ac1-a4fa-b920d3c3bb89",
                "resourceVersion": "1283",
                "creationTimestamp": "2024-05-14T16:59:05Z",
                "labels": {
                    "app": "svclb-traefik-af76f4e9",
                    "controller-revision-hash": "6445db8dff",
                    "pod-template-generation": "1",
                    "svccontroller.k3s.cattle.io/svcname": "traefik",
                    "svccontroller.k3s.cattle.io/svcnamespace": "kube-system"
                },
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "DaemonSet",
                        "name": "svclb-traefik-af76f4e9",
                        "uid": "0035135d-cf99-4d63-a960-1d5352e0658b",
                        "controller": true,
                        "blockOwnerDeletion": true
                    }
                ],
                "managedFields": [
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-14T16:59:05Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:generateName": {},
                                "f:labels": {
                                    ".": {},
                                    "f:app": {},
                                    "f:controller-revision-hash": {},
                                    "f:pod-template-generation": {},
                                    "f:svccontroller.k3s.cattle.io/svcname": {},
                                    "f:svccontroller.k3s.cattle.io/svcnamespace": {}
                                },
                                "f:ownerReferences": {
                                    ".": {},
                                    "k:{\"uid\":\"0035135d-cf99-4d63-a960-1d5352e0658b\"}": {}
                                }
                            },
                            "f:spec": {
                                "f:affinity": {
                                    ".": {},
                                    "f:nodeAffinity": {
                                        ".": {},
                                        "f:requiredDuringSchedulingIgnoredDuringExecution": {}
                                    }
                                },
                                "f:automountServiceAccountToken": {},
                                "f:containers": {
                                    "k:{\"name\":\"lb-tcp-443\"}": {
                                        ".": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"DEST_IPS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PROTO\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_RANGES\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":443,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:hostPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {}
                                            }
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    },
                                    "k:{\"name\":\"lb-tcp-80\"}": {
                                        ".": {},
                                        "f:env": {
                                            ".": {},
                                            "k:{\"name\":\"DEST_IPS\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"DEST_PROTO\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_PORT\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            },
                                            "k:{\"name\":\"SRC_RANGES\"}": {
                                                ".": {},
                                                "f:name": {},
                                                "f:value": {}
                                            }
                                        },
                                        "f:image": {},
                                        "f:imagePullPolicy": {},
                                        "f:name": {},
                                        "f:ports": {
                                            ".": {},
                                            "k:{\"containerPort\":80,\"protocol\":\"TCP\"}": {
                                                ".": {},
                                                "f:containerPort": {},
                                                "f:hostPort": {},
                                                "f:name": {},
                                                "f:protocol": {}
                                            }
                                        },
                                        "f:resources": {},
                                        "f:securityContext": {
                                            ".": {},
                                            "f:capabilities": {
                                                ".": {},
                                                "f:add": {}
                                            }
                                        },
                                        "f:terminationMessagePath": {},
                                        "f:terminationMessagePolicy": {}
                                    }
                                },
                                "f:dnsPolicy": {},
                                "f:enableServiceLinks": {},
                                "f:restartPolicy": {},
                                "f:schedulerName": {},
                                "f:securityContext": {
                                    ".": {},
                                    "f:sysctls": {}
                                },
                                "f:serviceAccount": {},
                                "f:serviceAccountName": {},
                                "f:terminationGracePeriodSeconds": {},
                                "f:tolerations": {}
                            }
                        }
                    },
                    {
                        "manager": "k3s",
                        "operation": "Update",
                        "apiVersion": "v1",
                        "time": "2024-05-23T10:49:11Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:status": {
                                "f:conditions": {
                                    "k:{\"type\":\"ContainersReady\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Initialized\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"PodReadyToStartContainers\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    },
                                    "k:{\"type\":\"Ready\"}": {
                                        ".": {},
                                        "f:lastProbeTime": {},
                                        "f:lastTransitionTime": {},
                                        "f:status": {},
                                        "f:type": {}
                                    }
                                },
                                "f:containerStatuses": {},
                                "f:hostIP": {},
                                "f:hostIPs": {},
                                "f:phase": {},
                                "f:podIP": {},
                                "f:podIPs": {
                                    ".": {},
                                    "k:{\"ip\":\"10.42.1.2\"}": {
                                        ".": {},
                                        "f:ip": {}
                                    }
                                },
                                "f:startTime": {}
                            }
                        },
                        "subresource": "status"
                    }
                ]
            },
            "spec": {
                "containers": [
                    {
                        "name": "lb-tcp-80",
                        "image": "rancher/klipper-lb:v0.4.7",
                        "ports": [
                            {
                                "name": "lb-tcp-80",
                                "hostPort": 80,
                                "containerPort": 80,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "SRC_PORT",
                                "value": "80"
                            },
                            {
                                "name": "SRC_RANGES",
                                "value": "0.0.0.0/0"
                            },
                            {
                                "name": "DEST_PROTO",
                                "value": "TCP"
                            },
                            {
                                "name": "DEST_PORT",
                                "value": "80"
                            },
                            {
                                "name": "DEST_IPS",
                                "value": "10.43.246.47"
                            }
                        ],
                        "resources": {},
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_ADMIN"
                                ]
                            }
                        }
                    },
                    {
                        "name": "lb-tcp-443",
                        "image": "rancher/klipper-lb:v0.4.7",
                        "ports": [
                            {
                                "name": "lb-tcp-443",
                                "hostPort": 443,
                                "containerPort": 443,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "SRC_PORT",
                                "value": "443"
                            },
                            {
                                "name": "SRC_RANGES",
                                "value": "0.0.0.0/0"
                            },
                            {
                                "name": "DEST_PROTO",
                                "value": "TCP"
                            },
                            {
                                "name": "DEST_PORT",
                                "value": "443"
                            },
                            {
                                "name": "DEST_IPS",
                                "value": "10.43.246.47"
                            }
                        ],
                        "resources": {},
                        "terminationMessagePath": "/dev/termination-log",
                        "terminationMessagePolicy": "File",
                        "imagePullPolicy": "IfNotPresent",
                        "securityContext": {
                            "capabilities": {
                                "add": [
                                    "NET_ADMIN"
                                ]
                            }
                        }
                    }
                ],
                "restartPolicy": "Always",
                "terminationGracePeriodSeconds": 30,
                "dnsPolicy": "ClusterFirst",
                "serviceAccountName": "svclb",
                "serviceAccount": "svclb",
                "automountServiceAccountToken": false,
                "nodeName": "kworker2",
                "securityContext": {
                    "sysctls": [
                        {
                            "name": "net.ipv4.ip_forward",
                            "value": "1"
                        }
                    ]
                },
                "affinity": {
                    "nodeAffinity": {
                        "requiredDuringSchedulingIgnoredDuringExecution": {
                            "nodeSelectorTerms": [
                                {
                                    "matchFields": [
                                        {
                                            "key": "metadata.name",
                                            "operator": "In",
                                            "values": [
                                                "kworker2"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                },
                "schedulerName": "default-scheduler",
                "tolerations": [
                    {
                        "key": "node-role.kubernetes.io/master",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node-role.kubernetes.io/control-plane",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "CriticalAddonsOnly",
                        "operator": "Exists"
                    },
                    {
                        "key": "node.kubernetes.io/not-ready",
                        "operator": "Exists",
                        "effect": "NoExecute"
                    },
                    {
                        "key": "node.kubernetes.io/unreachable",
                        "operator": "Exists",
                        "effect": "NoExecute"
                    },
                    {
                        "key": "node.kubernetes.io/disk-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/memory-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/pid-pressure",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    },
                    {
                        "key": "node.kubernetes.io/unschedulable",
                        "operator": "Exists",
                        "effect": "NoSchedule"
                    }
                ],
                "priority": 0,
                "enableServiceLinks": true,
                "preemptionPolicy": "PreemptLowerPriority"
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "PodReadyToStartContainers",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:25Z"
                    },
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:06Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:25Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:25Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": null,
                        "lastTransitionTime": "2024-05-14T16:59:05Z"
                    }
                ],
                "hostIP": "192.168.186.218",
                "hostIPs": [
                    {
                        "ip": "192.168.186.218"
                    }
                ],
                "podIP": "10.42.1.2",
                "podIPs": [
                    {
                        "ip": "10.42.1.2"
                    }
                ],
                "startTime": "2024-05-14T16:59:06Z",
                "containerStatuses": [
                    {
                        "name": "lb-tcp-443",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:59:25Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-lb:v0.4.7",
                        "imageID": "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                        "containerID": "containerd://4ac0163a49e6bfa2289afe68f20105bcba17d8af4a7b8234f4a4c7856f8d2c3c",
                        "started": true
                    },
                    {
                        "name": "lb-tcp-80",
                        "state": {
                            "running": {
                                "startedAt": "2024-05-14T16:59:25Z"
                            }
                        },
                        "lastState": {},
                        "ready": true,
                        "restartCount": 0,
                        "image": "docker.io/rancher/klipper-lb:v0.4.7",
                        "imageID": "docker.io/rancher/klipper-lb@sha256:558dcf96bf0800d9977ef46dca18411752618cd9dd06daeb99460c0a301d0a60",
                        "containerID": "containerd://9b163366f23d0d08015e04260aa8ddfb66bdba0b0a34da90d959ff84d1f62b1f",
                        "started": true
                    }
                ],
                "qosClass": "BestEffort"
            }
        }
    ]
}

    main()


# def main():
#     # 1 - Criar nodes a partir do "nods"
#     # numero de nodes
#     #print(len(k3s_nods["items"]))
#     #nome nodes 
#     #Tipo nodes
#     node_master = ""
#     node_workers = []
#     for item in k3s_nods["items"]:
#         if item["metadata"]["annotations"]["k3s.io/node-args"] == "[\"server\"]":
#             node_master = item["metadata"]["name"]
#             node_master = f"{node_master}(Master)"
#         elif item["metadata"]["annotations"]["k3s.io/node-args"] == "[\"agent\"]":
#             node_workers.append(item["metadata"]["name"]+"(Worker)")
#     #print(item["metadata"]["name"])
#     #print(item["metadata"]["annotations"]["k3s.io/node-args"])
#     #print("\n")
#     #print(node_master)
#     #print(node_workers)
#     pass

    