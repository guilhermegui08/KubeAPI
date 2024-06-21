import requests
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel, Text, Scrollbar
import json
import time
from datetime import datetime
import platform
import webbrowser
import speech_recognition as sr
from speech_recognition.recognizers import google
import os
import time
from gtts import gTTS
from pygame import mixer

def show_in_list(list, listbox, tk):
    listbox.delete(0, tk.END)
    for item in list:
        listbox.insert(tk.END, f"{item}")

def get_node_stats_perodically(ip_address_var, api_port_var, authorization):
    names = []
    timestamps = []
    cpus = []
    memorys = []
    timestamps2 = []
    cpus2 = []
    memorys2 = []
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/metrics.k8s.io/v1beta1/nodes"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for space in items:
            names.append(space['metadata']['name'])
            timestamps.append(space['timestamp'])
            cpus.append(space['usage']['cpu'])
            memorys.append(space['usage']['memory'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    for item in timestamps:
        dt = datetime.strptime(item, "%Y-%m-%dT%H:%M:%SZ")
        timestamps2.append(dt.strftime("%B %d, %Y, %I:%M:%S %p UTC"))

    for item in cpus:
        cpu_usage_ns_value = int(item[:-1])
        cpu_usage_ms = cpu_usage_ns_value / 1_000_000
        cpus2.append(f"{cpu_usage_ms:.3f} ms")

    for item in memorys:
        memory_usage_ki_value = int(item[:-2])
        memory_usage_mib = memory_usage_ki_value / 1024
        memorys2.append(f"{memory_usage_mib:.2f} MiB")

    stats = []
    stats.append(names)
    stats.append(timestamps2)
    stats.append(cpus2)
    stats.append(memorys2)

    return stats

def get_node_stats_dashboard(ip_address_var, api_port_var, authorization):
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/metrics.k8s.io/v1beta1/nodes"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return items

def get_nodes_networkx_graph(ip_address_var, api_port_var, authorization):
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/nodes"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        nodes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return nodes



def get_workload_status(ip_address_var, api_port_var, authorization):
    data = {}
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/daemonsets"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        data['Daemon Sets'] = len(items)
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        data['Deployments'] = len(items)
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/batch/v1/jobs"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        data['Jobs'] = len(items)
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        data['Pods'] = len(items)
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/replicasets"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        data['Replica Sets'] = len(items)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data

def get_daemonSets_dashboard(ip_address_var, api_port_var, authorization):
    data = {
        "name" : [],
        "namespace" : [],
        "creationTimestamp" : [],
    }
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/daemonsets"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for item in items:
            data["name"].append(item['metadata']['name'])
            data["namespace"].append(item['metadata']['namespace'])
            data["creationTimestamp"].append(item['metadata']['creationTimestamp'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data

def get_deployments_dashboard(ip_address_var, api_port_var, authorization):
    data = {
        "name" : [],
        "namespace" : [],
        "creationTimestamp" : [],
    }
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for item in items:
            data["name"].append(item['metadata']['name'])
            data["namespace"].append(item['metadata']['namespace'])
            data["creationTimestamp"].append(item['metadata']['creationTimestamp'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data

def get_jobs_dashboard(ip_address_var, api_port_var, authorization):
    data = {
        "name" : [],
        "namespace" : [],
        "creationTimestamp" : [],
    }
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/batch/v1/jobs"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for item in items:
            data["name"].append(item['metadata']['name'])
            data["namespace"].append(item['metadata']['namespace'])
            data["creationTimestamp"].append(item['metadata']['creationTimestamp'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data

def get_pods_dashboard(ip_address_var, api_port_var, authorization):
    data = {
        "name" : [],
        "namespace" : [],
        "creationTimestamp" : [],
    }
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for item in items:
            data["name"].append(item['metadata']['name'])
            data["namespace"].append(item['metadata']['namespace'])
            data["creationTimestamp"].append(item['metadata']['creationTimestamp'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data

def get_pods_network_graph(ip_address_var, api_port_var, authorization):
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        pods = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return pods

def get_replica_sets_dashboard(ip_address_var, api_port_var, authorization):
    data = {
        "name" : [],
        "namespace" : [],
        "creationTimestamp" : [],
    }
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/replicasets"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for item in items:
            data["name"].append(item['metadata']['name'])
            data["namespace"].append(item['metadata']['namespace'])
            data["creationTimestamp"].append(item['metadata']['creationTimestamp'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data

def get_api(ip_address_var, api_port_var, authorization):
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        messagebox.showinfo("Message", "Cliente autenticado com Sucesso!")
        return response.status_code
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}")
        return response.status_code

def get_namspace_names(ip_address_var, api_port_var, authorization):
    names = []
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for space in items:
            names.append(space['metadata']['name'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return names

def get_pod_names(ip_address_var, api_port_var, authorization):
    names = []
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for space in items:
            names.append(space['metadata']['name'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return names

def get_deploy_names(ip_address_var, api_port_var, authorization):
    names = []
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for space in items:
            names.append(space['metadata']['name'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return names

def get_service_names(ip_address_var, api_port_var, authorization):
    names = []
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/services"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for space in items:
            names.append(space['metadata']['name'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return names

def get_ingress_names(ip_address_var, api_port_var, authorization):
    names = []
    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/ingresses"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        for space in items:
            names.append(space['metadata']['name'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return names

def get_all_nodes(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    if dashboard_frame.winfo_ismapped():
            dashboard_frame.pack_forget()

    if not listbox.winfo_ismapped():
            listbox.pack(expand=True, fill="both", side=tk.TOP)
            new_buttons[6].pack(side=tk.BOTTOM, fill=tk.X)
            labels_frame.pack(fill=tk.X, side=tk.BOTTOM)


    empty_label = tk.Label(labels_frame, text="", height=0)
    empty_label.grid(row=0, column=0)
    old_buttons.append(empty_label)

    #new_buttons[3].grid(row=1, column=0, padx=2, pady=2, sticky=tk.SW)
    #new_buttons[3].config()
    #old_buttons.append(new_buttons[3])

    def on_double_click(event):
        index = listbox.curselection()
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/nodes/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                node_data = response.json()

                nome_valor = node_data['metadata']['name']
                uid_valor = node_data['metadata']['uid']
                resource_ver_valor = node_data['metadata']['resourceVersion']
                creation_time_valor = node_data['metadata']['creationTimestamp']
                
                roles= []
                for item in node_data['metadata']['managedFields']:
                    if item['manager'] == 'k3s-supervisor@kmaster':
                        gestor_valor = item['manager']
                        operacao_valor = item['operation']
                        api_ver_valor = item['apiVersion']
                        time_valor = item['time']
                        if 'f:labels' in item['fieldsV1']['f:metadata']:
                            full_roles = [*item['fieldsV1']['f:metadata']['f:labels']]
                            for item in full_roles:
                                roles.append(item.split('/')[1])
                        else:
                            roles.append('<none>')
                            break
                string_roles = ""
                for item in roles:
                    string_roles += f"{item},"
                string_roles = string_roles[:-1]

                pod_cidr_valor = node_data['spec']['podCIDR']
                provider_id_valor = node_data['spec']['providerID']
                internal_ip_valor = node_data['status']['addresses'][0]['address']
                hostname_valor = node_data['status']['addresses'][1]['address']
                
                cpu_valor1 = node_data['status']['capacity']['cpu']
                ephemeral_sto_valor1 = node_data['status']['capacity']['ephemeral-storage']
                hugepages_valor1 = node_data['status']['capacity']['hugepages-2Mi']
                memory_valor1 = node_data['status']['capacity']['memory']
                pods_valor1 = node_data['status']['capacity']['pods']

                cpu_valor2 = node_data['status']['allocatable']['cpu']
                ephemeral_sto_valor2 = node_data['status']['allocatable']['ephemeral-storage']
                hugepages_valor2 = node_data['status']['allocatable']['hugepages-2Mi']
                memory_valor2 = node_data['status']['allocatable']['memory']
                pods_valor2 = node_data['status']['allocatable']['pods']

                condicoes_valor1 = node_data['status']['conditions'][0]['message']
                condicoes_valor2 = node_data['status']['conditions'][1]['message']
                condicoes_valor3 = node_data['status']['conditions'][2]['message']
                condicoes_valor4 = node_data['status']['conditions'][3]['message']

                machine_valor = node_data['status']['nodeInfo']['machineID']
                system_UUID_valor = node_data['status']['nodeInfo']['systemUUID']
                boot_id_valor = node_data['status']['nodeInfo']['bootID']
                kernel_version_valor = node_data['status']['nodeInfo']['kernelVersion']
                os_image_valor = node_data['status']['nodeInfo']['osImage']
                container_runtimeVersion_valor = node_data['status']['nodeInfo']['containerRuntimeVersion']
                kubelet_version_valor = node_data['status']['nodeInfo']['kubeletVersion']
                kube_proxy_version_valor = node_data['status']['nodeInfo']['kubeProxyVersion']
                operating_system_valor = node_data['status']['nodeInfo']['operatingSystem']
                architecture_valor = node_data['status']['nodeInfo']['architecture']

                images_names = []
                images_sizes = []
                for item in node_data['status']['images']:
                    images_sizes.append(item['sizeBytes'])
                    pre_name = item['names'][0]
                    parts = pre_name.split('/')
                    image_name_with_tag = parts[-1]
                    image_name = image_name_with_tag.split('@')[0]
                    image_name = image_name.split(':')[0]
                    images_names.append(image_name)

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

            pre_new_window = Toplevel(parent)
            pre_new_window.title(name_value)
            pre_new_window.geometry("800x600")
            
            #top_frame = tk.Frame(pre_new_window)
            #top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            bot_frame = tk.Frame(pre_new_window)
            bot_frame.pack(side=tk.BOTTOM , fill=tk.X)

            canvas = tk.Canvas(pre_new_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and attach it to the canvas
            scrollbar = tk.Scrollbar(pre_new_window, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the contents
            new_window = tk.Frame(canvas)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)

            metadata_label = tk.Label(new_window, text=f"Metadata", font=("consolas", 14, "bold"))
            metadata_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            name_label = tk.Label(new_window, text=f"Nome: {nome_valor}")
            name_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            uid_label = tk.Label(new_window, text=f"UID: {uid_valor}")
            uid_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            resource_ver_label = tk.Label(new_window, text=f"Resource Version: {resource_ver_valor}")
            resource_ver_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
            creation_time_label = tk.Label(new_window, text=f"Data de criação: {creation_time_valor}")
            creation_time_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
                
            maneged_label = tk.Label(new_window, text=f"Managed Fields", font=("consolas", 14, "bold"))
            maneged_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            gestor_label = tk.Label(new_window, text=f"Gestor: {gestor_valor}")
            gestor_label.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
            operacao_label = tk.Label(new_window, text=f"Operação: {operacao_valor}")
            operacao_label.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
            api_ver_label = tk.Label(new_window, text=f"Versão da API: {api_ver_valor}")
            api_ver_label.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
            time_label = tk.Label(new_window, text=f"Data e Hora: {time_valor}")
            time_label.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
            roles_label = tk.Label(new_window, text=f"Roles: {string_roles}")
            roles_label.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

            resource_info_label = tk.Label(new_window, text=f"Resouce Information", font=("consolas", 14, "bold"))
            resource_info_label.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
            pod_cidr_label = tk.Label(new_window, text=f"Pod CIDR: {pod_cidr_valor}")
            pod_cidr_label.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
            provider_label = tk.Label(new_window, text=f"Provider ID: {provider_id_valor}")
            provider_label.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)
            internal_ip_label = tk.Label(new_window, text=f"IP interno: {internal_ip_valor}")
            internal_ip_label.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
            hostname_label = tk.Label(new_window, text=f"Hostname: {hostname_valor}")
            hostname_label.grid(row=9, column=2, padx=5, pady=5, sticky=tk.W)

            status_label = tk.Label(new_window, text=f"Status", font=("consolas", 14, "bold"))
            status_label.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
            capacity_label = tk.Label(new_window, text=f"Capacity", font=("consolas", 12), fg='blue')
            capacity_label.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
            cpu_label = tk.Label(new_window, text=f"CPU: {cpu_valor1}")
            cpu_label.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
            ephemeral_sto_label = tk.Label(new_window, text=f"Ephemeral-storage: {ephemeral_sto_valor1}")
            ephemeral_sto_label.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
            hugepages_label = tk.Label(new_window, text=f"Hugepages-2Mi: {hugepages_valor1}")
            hugepages_label.grid(row=14, column=1, padx=5, pady=5, sticky=tk.W)
            memory_label = tk.Label(new_window, text=f"Memory: {memory_valor1}")
            memory_label.grid(row=15, column=1, padx=5, pady=5, sticky=tk.W)
            pods_label = tk.Label(new_window, text=f"Pods: {pods_valor1}")
            pods_label.grid(row=16, column=1, padx=5, pady=5, sticky=tk.W)
            allocatable_label = tk.Label(new_window, text=f"Allocatable", font=("consolas", 12), fg='blue')
            allocatable_label.grid(row=11, column=2, padx=5, pady=5, sticky=tk.W)
            cpu_label2 = tk.Label(new_window, text=f"CPU: {cpu_valor2}")
            cpu_label2.grid(row=12, column=2, padx=5, pady=5, sticky=tk.W)
            ephemeral_sto_label2 = tk.Label(new_window, text=f"Ephemeral-storage: {ephemeral_sto_valor2}")
            ephemeral_sto_label2.grid(row=13, column=2, padx=5, pady=5, sticky=tk.W)
            hugepages_label2 = tk.Label(new_window, text=f"Hugepages-2Mi: {hugepages_valor2}")
            hugepages_label2.grid(row=14, column=2, padx=5, pady=5, sticky=tk.W)
            memory_label2 = tk.Label(new_window, text=f"Memory: {memory_valor2}")
            memory_label2.grid(row=15, column=2, padx=5, pady=5, sticky=tk.W)
            pods_label2 = tk.Label(new_window, text=f"Pods: {pods_valor2}")
            pods_label2.grid(row=16, column=2, padx=5, pady=5, sticky=tk.W)
            conditions_label = tk.Label(new_window, text=f"Condições", font=("consolas", 12), fg='blue')
            conditions_label.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W)
            condicoes_label1 = tk.Label(new_window, text=f"{condicoes_valor1}")
            condicoes_label1.grid(row=18, column=1, padx=5, pady=5, sticky=tk.W)
            condicoes_label2 = tk.Label(new_window, text=f"{condicoes_valor2}")
            condicoes_label2.grid(row=19, column=1, padx=5, pady=5, sticky=tk.W)
            condicoes_label3 = tk.Label(new_window, text=f"{condicoes_valor3}")
            condicoes_label3.grid(row=20, column=1, padx=5, pady=5, sticky=tk.W)
            condicoes_label4 = tk.Label(new_window, text=f"{condicoes_valor4}")
            condicoes_label4.grid(row=21, column=1, padx=5, pady=5, sticky=tk.W)

            informacoes_label = tk.Label(new_window, text=f"Node Info", font=("consolas", 14, "bold"))
            informacoes_label.grid(row=22, column=1, padx=5, pady=5, sticky=tk.W)
            machine_label = tk.Label(new_window, text=f"Machine ID: {machine_valor}")
            machine_label.grid(row=23, column=1, padx=5, pady=5, sticky=tk.W)
            systemUUID_label = tk.Label(new_window, text=f"System UUID: {system_UUID_valor}")
            systemUUID_label.grid(row=24, column=1, padx=5, pady=5, sticky=tk.W)
            bootID_label = tk.Label(new_window, text=f"Boot ID: {boot_id_valor}")
            bootID_label.grid(row=25, column=1, padx=5, pady=5, sticky=tk.W)
            kernelVersion_label = tk.Label(new_window, text=f"Versão do Kernel: {kernel_version_valor}")
            kernelVersion_label.grid(row=26, column=1, padx=5, pady=5, sticky=tk.W)
            osImage_label = tk.Label(new_window, text=f"Imagem do OS: {os_image_valor}")
            osImage_label.grid(row=27, column=1, padx=5, pady=5, sticky=tk.W)
            containerRuntimeVersion_label = tk.Label(new_window, text=f"Versão do ContainerRuntime: {container_runtimeVersion_valor}")
            containerRuntimeVersion_label.grid(row=23, column=2, padx=5, pady=5, sticky=tk.W)
            kubeletVersion_label = tk.Label(new_window, text=f"Versão do Kubelet: {kubelet_version_valor}")
            kubeletVersion_label.grid(row=24, column=2, padx=5, pady=5, sticky=tk.W)
            kubeProxyVersion_label = tk.Label(new_window, text=f"Versão do KubeProxy: {kube_proxy_version_valor}")
            kubeProxyVersion_label.grid(row=25, column=2, padx=5, pady=5, sticky=tk.W)
            operatingSystem_label = tk.Label(new_window, text=f"Sistema Operativo: {operating_system_valor}")
            operatingSystem_label.grid(row=26, column=2, padx=5, pady=5, sticky=tk.W)
            architecture_label = tk.Label(new_window, text=f"Arquitetura: {architecture_valor}")
            architecture_label.grid(row=27, column=2, padx=5, pady=5, sticky=tk.W)

            imagens_label = tk.Label(new_window, text=f"Imagens", font=("consolas", 14, "bold"))
            imagens_label.grid(row=28, column=1, padx=5, pady=5, sticky=tk.W)
            nomes_label = tk.Label(new_window, text=f"Nome", font=("consolas", 12), fg='blue')
            nomes_label.grid(row=29, column=1, padx=5, pady=5, sticky=tk.W)
            i = 30
            for item in images_names:
                tk.Label(new_window, text=f"{item}").grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                i += 1
            tamanhos_label = tk.Label(new_window, text=f"Tamanho", font=("consolas", 12), fg='blue')
            tamanhos_label.grid(row=29, column=2, padx=5, pady=5, sticky=tk.W)
            i = 30
            for item in images_sizes:
                tk.Label(new_window, text=f"{item}").grid(row=i, column=2, padx=5, pady=5, sticky=tk.W)
                i += 1

            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            destroy_button = tk.Button(bot_frame, text="OK", command=pre_new_window.destroy)
            destroy_button.pack(padx=5, pady=5, expand=True)

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/nodes"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        nodes = response.json()
        items = nodes['items']
        nodes_names = []
        for node in items:
            roles = []
            for item in node['metadata']['managedFields']:
                if item['manager'] == 'k3s-supervisor@kmaster':
                    if 'f:labels' in item['fieldsV1']['f:metadata']:
                        full_roles = [*item['fieldsV1']['f:metadata']['f:labels']]
                        for item in full_roles:
                            roles.append(item.split('/')[1])
                    else:
                        roles.append('<none>')
                        break
            pre_string = f"Nome: {node['metadata']['name']}; {node['status']['addresses'][0]['type']}: {node['status']['addresses'][0]['address']}; Imagem do SO: {node['status']['nodeInfo']['osImage']}, Data de criação: {node['metadata']['creationTimestamp']}; Roles: "
            for item in roles:
                pre_string += f"{item},"
            pre_string = pre_string[:-1]
            nodes_names.append(pre_string)
        show_in_list(nodes_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_all_namespaces(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    if dashboard_frame.winfo_ismapped():
            dashboard_frame.pack_forget()

    if not listbox.winfo_ismapped():
            listbox.pack(expand=True, fill="both", side=tk.TOP)
            new_buttons[6].pack(side=tk.BOTTOM, fill=tk.X)
            labels_frame.pack(fill=tk.X, side=tk.BOTTOM)

    name_label = tk.Label(labels_frame, text="Nome*:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)

    metadata_label = tk.Label(labels_frame, text="metadata".upper(), font=("consolas", 12), fg='blue')
    metadata_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(metadata_label)
    labels_label = tk.Label(labels_frame, text="LABELS")
    labels_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(labels_label)
    environment_label = tk.Label(labels_frame, text="Environment:")
    environment_label.grid(row=3, column=0, padx=5, pady=5)
    old_buttons.append(environment_label)
    environment_entry = tk.Entry(labels_frame)
    environment_entry.grid(row=3, column=1, padx=5, pady=5)
    old_buttons.append(environment_entry)
    team_label = tk.Label(labels_frame, text="Team:")
    team_label.grid(row=4, column=0, padx=5, pady=5)
    old_buttons.append(team_label)
    team_entry = tk.Entry(labels_frame)
    team_entry.grid(row=4, column=1, padx=5, pady=5)
    old_buttons.append(team_entry)

    annotations_label = tk.Label(labels_frame, text="annotations".upper())
    annotations_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(annotations_label)
    owner_label = tk.Label(labels_frame, text="Owner:")
    owner_label.grid(row=3, column=2, padx=5, pady=5)
    old_buttons.append(owner_label)
    owner_entry = tk.Entry(labels_frame)
    owner_entry.grid(row=3, column=3, padx=5, pady=5)
    old_buttons.append(owner_entry)
    purpose_label = tk.Label(labels_frame, text="Purpose:")
    purpose_label.grid(row=4, column=2, padx=5, pady=5)
    old_buttons.append(purpose_label)
    purpose_entry = tk.Entry(labels_frame)
    purpose_entry.grid(row=4, column=3, padx=5, pady=5)
    old_buttons.append(purpose_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command= lambda: criar_namespaces(ip_address_var, api_port_var, authorization, listbox, tk, parent, name_entry, environment_entry, team_entry, owner_entry, purpose_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[2].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command= lambda: eliminar_namespaces(ip_address_var, api_port_var, authorization, listbox, tk, parent, get_namspace_names(ip_address_var, api_port_var, authorization)))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        index = listbox.curselection()
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                space_data = response.json()
                
                nome_valor = space_data['metadata']['name']
                uid_valor = space_data['metadata']['uid']
                resource_ver_valor = space_data['metadata']['resourceVersion']
                data_criacao_valor = space_data['metadata']['creationTimestamp']

                labels = space_data['metadata']['labels']

                managed_fields = space_data['metadata']['managedFields']

                annotations = 0
                if 'annotations' in space_data['metadata']:
                    annotations = space_data['metadata']['annotations']

                status_valor = space_data['status']['phase']
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
            pre_new_window = Toplevel(parent)
            pre_new_window.title(name_value)
            pre_new_window.geometry("800x600")
            
            #top_frame = tk.Frame(pre_new_window)
            #top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            bot_frame = tk.Frame(pre_new_window)
            bot_frame.pack(side=tk.BOTTOM , fill=tk.X)

            canvas = tk.Canvas(pre_new_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and attach it to the canvas
            scrollbar = tk.Scrollbar(pre_new_window, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the contents
            new_window = tk.Frame(canvas)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)
            
            metadata_label = tk.Label(new_window, text=f"Metadata", font=("consolas", 14, "bold"))
            metadata_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            name_label = tk.Label(new_window, text=f"Nome: {nome_valor}")
            name_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            uid_label = tk.Label(new_window, text=f"UID: {uid_valor}")
            uid_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            resource_ver_label = tk.Label(new_window, text=f"Resource Version: {resource_ver_valor}")
            resource_ver_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
            creation_time_label = tk.Label(new_window, text=f"Data de criação: {data_criacao_valor}")
            creation_time_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
            

            labels_label = tk.Label(new_window, text=f"Labels", font=("consolas", 14, "bold"))
            labels_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

            row = 4
            for item in labels:
                tk.Label(new_window, text=f"{item}: {labels[item]}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            
            managed_fields_label = tk.Label(new_window, text=f"Managed Fields", font=("consolas", 14, "bold"))
            managed_fields_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in managed_fields:
                tk.Label(new_window, text=f"{item['manager']}", font=("consolas", 12), fg='blue').grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Operação: {item['operation']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Versão da API: {item['apiVersion']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Data e Hora: {item['time']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
            
            if annotations:
                row+=1
                annotation_label = tk.Label(new_window, text=f"Anotações", font=("consolas", 14, "bold"))
                annotation_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row+=1
                for item in annotations:
                    last_config_label = tk.Label(new_window, text=f"{item}: {annotations[item]}")
                    last_config_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
                    #last_config_label2 = tk.Label(new_window, text=f"{annotations[item]}")
                    #last_config_label2.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
                    row+=1

            estado_label = tk.Label(new_window, text=f"Estado", font=("consolas", 14, "bold"))
            estado_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row+=1
            phase_label = tk.Label(new_window, text=f"Phase: {status_valor}")
            phase_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)

            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            destroy_button = tk.Button(bot_frame, text="OK", command=pre_new_window.destroy)
            destroy_button.pack(padx=5, pady=5, expand=True)

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        spaces_names = []
        for space in items:
            pre_string = f"Nome: {space['metadata']['name']}; Data de criação: {space['metadata']['creationTimestamp']}; Versão do recurso: {space['metadata']['resourceVersion']}; Estado: {space['status']['phase']}"
            spaces_names.append(pre_string)
        show_in_list(spaces_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_namespaces(ip_address_var, api_port_var ,authorization, listbox, tk, parent, name_entry, environment_entry, team_entry, owner_entry, purpose_entry):
    nome_valor = name_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    environment_valor = environment_entry.get().replace(" ", "")
    team_valor = team_entry.get().replace(" ", "")
    owner_valor = owner_entry.get().replace(" ", "")
    purpose_valor = purpose_entry.get().replace(" ", "")

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces"
        headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
        data = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": nome_valor,
                "labels": {
                },
                "annotations": {
                }
            }
        }
        if environment_valor:
            data['metadata']['labels']['environment'] = environment_valor
        if team_valor:
            data['metadata']['labels']['team'] = team_valor
        if owner_valor:
            data['metadata']['annotations']['owner'] = owner_valor
        if purpose_valor:
            data['metadata']['annotations']['purpose'] = purpose_valor
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        response.raise_for_status()
        if response.status_code == 201:
            messagebox.showinfo("Namespace Criado", "Namespace criado com sucesso", parent=parent )
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        namespaces = response.json()
        items = namespaces['items']
        spaces_names = []
        for space in items:
            pre_string = f"Nome: {space['metadata']['name']}; Data de criação: {space['metadata']['creationTimestamp']}; Versão do recurso: {space['metadata']['resourceVersion']}; Estado: {space['status']['phase']}"
            spaces_names.append(pre_string)
        show_in_list(spaces_names, listbox, tk)
        name_entry.delete(0, tk.END)
        environment_entry.delete(0, tk.END)
        team_entry.delete(0, tk.END)
        owner_entry.delete(0, tk.END)
        purpose_entry.delete(0, tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_namespaces(ip_address_var, api_port_var, authorization, listbox, tk, parent, namespace_names):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum namespace!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar namespace {name_value}",f"Tem a certeza que pretende eliminar o namespace {name_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{name_value}"
            headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
            response = requests.delete(url, headers=headers, verify=False)
            response.raise_for_status()
            #info_box = messagebox.showinfo("Info", "O namespace está a ser apagado...", parent=parent)
            while(1):
                if len(get_namspace_names(ip_address_var, api_port_var, authorization)) != len(namespace_names):
                       break
            #parent.after(0, lambda: parent.tk.call('tk', 'messagebox', 'destroy', info_box))
            messagebox.showinfo("Sucesso", "Namespace eliminado com sucesso", parent=parent)
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            namespaces = response.json()
            items = namespaces['items']
            spaces_names = []
            for space in items:
                pre_string = f"Nome: {space['metadata']['name']}; Data de criação: {space['metadata']['creationTimestamp']}; Versão do recurso: {space['metadata']['resourceVersion']}; Estado: {space['status']['phase']}"
                spaces_names.append(pre_string)
            show_in_list(spaces_names, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_all_pods(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    if dashboard_frame.winfo_ismapped():
            dashboard_frame.pack_forget()

    if not listbox.winfo_ismapped():
            listbox.pack(expand=True, fill="both", side=tk.TOP)
            new_buttons[6].pack(side=tk.BOTTOM, fill=tk.X)
            labels_frame.pack(fill=tk.X, side=tk.BOTTOM)


    namespace_names = get_namspace_names(ip_address_var, api_port_var, authorization)
    namespace_names.append("Todos")
    namespace_label = tk.Label(labels_frame, text="Namespace:")
    namespace_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(namespace_label)
    options = namespace_names
    pre_filled_value = "Todos"
    selected_option = tk.StringVar()
    combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
    try:
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)  # Set the pre-filled value
    except ValueError:
        pass
    combobox.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(combobox)
    
    editar_button = tk.Button(labels_frame, text="Filtrar", command= lambda: filtrar())
    editar_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.SW)
    old_buttons.append(editar_button)

    def filtrar():
        try:
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pods = response.json()
            items = pods['items']
            pods_names = []
            for pod in items:
                if selected_option.get().strip() == "Todos":
                    pre_string = f"Nome: {pod['metadata']['name']}; Namespace: {pod['metadata']['namespace']}; Data de criação: {pod['metadata']['creationTimestamp']}; Versão do recurso: {pod['metadata']['resourceVersion']}; Estado: {pod['status']['phase']}"
                    pods_names.append(pre_string)
                elif pod['metadata']['namespace'] == selected_option.get().strip():
                    pre_string = f"Nome: {pod['metadata']['name']}; Namespace: {pod['metadata']['namespace']}; Data de criação: {pod['metadata']['creationTimestamp']}; Versão do recurso: {pod['metadata']['resourceVersion']}; Estado: {pod['status']['phase']}"
                    pods_names.append(pre_string)
            show_in_list(pods_names, listbox, tk)
            listbox.bind("<Double-Button-1>", on_double_click)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    name_label = tk.Label(labels_frame, text="Nome*:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)

    containers_label = tk.Label(labels_frame, text="Container".upper())
    containers_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(containers_label)
    nome2_label = tk.Label(labels_frame, text="Nome*:")
    nome2_label.grid(row=3, column=0, padx=5, pady=5)
    old_buttons.append(nome2_label)
    nome2_entry = tk.Entry(labels_frame)
    nome2_entry.grid(row=3, column=1, padx=5, pady=5)
    old_buttons.append(nome2_entry)
    image_label = tk.Label(labels_frame, text="Imagem*:")
    image_label.grid(row=4, column=0, padx=5, pady=5)
    old_buttons.append(image_label)
    #image_entry = tk.Entry(labels_frame)
    #image_entry.grid(row=4, column=1, padx=5, pady=5)
    #old_buttons.append(image_entry)
    ports_label = tk.Label(labels_frame, text="Porto:")
    ports_label.grid(row=5, column=0, padx=5, pady=5)
    old_buttons.append(ports_label)
    ports_entry = tk.Entry(labels_frame)
    ports_entry.grid(row=5, column=1, padx=5, pady=5)
    old_buttons.append(ports_entry)
    quantidade_label = tk.Label(labels_frame, text="Quantidade:")
    quantidade_label.grid(row=6, column=0, padx=5, pady=5)
    old_buttons.append(quantidade_label)
    qauntidade_entry = tk.Entry(labels_frame)
    qauntidade_entry.grid(row=6, column=1, padx=5, pady=5)
    old_buttons.append(qauntidade_entry)

    image_names = ['nginx:latest', "httpd:latest", 'caddy:latest', 'mysql:latest', 'mysql:latest', 'postgres:latest', 'mongo:latest', 'redis:latest', 'mariadb:latest', 'python:latest', 'node:latest', 'ruby:latest', 'golang:latest', 'php:latest', 'busybox:latest', 'alpine:latest', 'ubuntu:latest', 'centos:latest', 'debian:latest', 'jenkins/jenkins:latest', 'gitlab/gitlab-ce:latest', 'sonarqube:latest', 'prom/prometheus:latest', 'grafana/grafana:latest', 'elasticsearch:latest', 'kibana:latest', 'varnish:latest', 'rabbitmq:latest', 'wurstmeister/kafka:latest', 'portainer/portainer-ce:latest']

    options2 = image_names
    pre_filled_value2 = "httpd:latest"
    selected_option2 = tk.StringVar()
    combobox2 = ttk.Combobox(labels_frame, textvariable=selected_option2, values=options2)
    try:
        pre_filled_index2 = options2.index(pre_filled_value2)
        combobox2.current(1)  # Set the pre-filled value
    except ValueError:
        pass
    combobox2.grid(row=4, column=1, padx=5, pady=5)
    old_buttons.append(combobox2)

    #inserir_button = tk.Button(labels_frame, text="Inserir", command= lambda: #inserir())
    #inserir_button.grid(row=4, column=3, padx=5, pady=5, sticky=tk.SW)
    #old_buttons.append(inserir_button)

    #def inserir():
    #    image_entry.delete(0, tk.END)
    #    image_entry.insert(0, selected_option2.get())

    metadata_label = tk.Label(labels_frame, text="metadata".upper(), font=("consolas", 12), fg='blue')
    metadata_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(metadata_label)
    labels_label = tk.Label(labels_frame, text="LABELS")
    labels_label.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(labels_label)
    environment_label = tk.Label(labels_frame, text="Environment:")
    environment_label.grid(row=4, column=2, padx=5, pady=5)
    old_buttons.append(environment_label)
    environment_entry = tk.Entry(labels_frame)
    environment_entry.grid(row=4, column=3, padx=5, pady=5)
    old_buttons.append(environment_entry)
    team_label = tk.Label(labels_frame, text="Team:")
    team_label.grid(row=5, column=2, padx=5, pady=5)
    old_buttons.append(team_label)
    team_entry = tk.Entry(labels_frame)
    team_entry.grid(row=5, column=3, padx=5, pady=5)
    old_buttons.append(team_entry)

    annotations_label = tk.Label(labels_frame, text="annotations".upper())
    annotations_label.grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(annotations_label)
    owner_label = tk.Label(labels_frame, text="Owner:")
    owner_label.grid(row=4, column=4, padx=5, pady=5)
    old_buttons.append(owner_label)
    owner_entry = tk.Entry(labels_frame)
    owner_entry.grid(row=4, column=5, padx=5, pady=5)
    old_buttons.append(owner_entry)
    purpose_label = tk.Label(labels_frame, text="Purpose:")
    purpose_label.grid(row=5, column=4, padx=5, pady=5)
    old_buttons.append(purpose_label)
    purpose_entry = tk.Entry(labels_frame)
    purpose_entry.grid(row=5, column=5, padx=5, pady=5)
    old_buttons.append(purpose_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command= lambda: criar_pods(ip_address_var, api_port_var, authorization, listbox, tk, parent, name_entry, nome2_entry, selected_option2, ports_entry, selected_option, environment_entry, team_entry, owner_entry, purpose_entry, qauntidade_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[2].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command= lambda: eliminar_pods(ip_address_var, api_port_var, authorization, listbox, tk, parent, get_pod_names(ip_address_var, api_port_var, authorization)))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        index = listbox.curselection()
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_value}/pods/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                pod_data = response.json()
                
                nome_valor = pod_data['metadata']['name']
                if 'generateName' in pod_data['metadata']:
                    generate_name_valor = pod_data['metadata']['generateName']
                namespace_valor = pod_data['metadata']['namespace']
                uid_valor = pod_data['metadata']['uid']
                reseourse_ver_valor = pod_data['metadata']['resourceVersion']
                data_creation_valor = pod_data['metadata']['creationTimestamp']

                if 'labels' in pod_data['metadata']:
                    labels = pod_data['metadata']['labels']
                
                annotations = 0
                if 'annotations' in pod_data['metadata']:
                    annotations = pod_data['metadata']['annotations']

                managed_fields = pod_data['metadata']['managedFields']

                if 'ownerReferences' in pod_data['metadata']: 
                    api_ver_valor = pod_data['metadata']['ownerReferences'][0]['apiVersion']
                    kind_valor = pod_data['metadata']['ownerReferences'][0]['kind']
                    owner_name_valor = pod_data['metadata']['ownerReferences'][0]['name']
                    owner_uid_valor = pod_data['metadata']['ownerReferences'][0]['uid']
                    controller_valor = pod_data['metadata']['ownerReferences'][0]['controller']
                    block_owner_valor = pod_data['metadata']['ownerReferences'][0]['blockOwnerDeletion']

                if 'volumes' in pod_data['spec']: 
                    vol_names = []
                    for item in pod_data['spec']['volumes']:
                        vol_names.append(item['name'])
                    string_names = ''
                    for item in vol_names:
                        string_names += item + ','
                    string_names = string_names[:-1]

                container_names = []
                container_images = []
                container_ports = []
                container_args = []
                container_envs= []
                for item in pod_data['spec']['containers']:
                    container_names.append(item['name'])
                    container_images.append(item['image'])
                    if 'ports' in item:
                        container_ports.append(item['ports'])
                    else:
                        container_ports.append(False)
                    if 'args' in item:
                        args_names = []
                        for item2 in item['args']:
                            args_names.append(item2)
                        string_args = ''
                        for item2 in args_names:
                            string_args += item2 + ','
                        container_args.append(string_args[:-1])
                    else:
                        container_args.append(False)
                    if 'env' in item:
                        string_env = ""
                        for item2 in item['env']:
                            for item3 in item2:
                                string_env += f"{item3}: {item2[item3]}, "
                        container_envs.append(string_env[:-1])
                    else:
                        container_envs.append(False)

                    restartPolicy_valor = pod_data['spec']['restartPolicy']
                    terminationGracePeriodSeconds_valor = pod_data['spec']['terminationGracePeriodSeconds']
                    dnsPolicy_valor = pod_data['spec']['dnsPolicy']
                    serviceAccount_valor = pod_data['spec']['serviceAccount']
                    if 'nodeName' in pod_data['spec']:
                        nodeName_valor = pod_data['spec']['nodeName']

                    phase_valor = pod_data['status']['phase']
                    conditions = []
                    for item in pod_data['status']['conditions']:
                        conditions.append(item['type'])
                    
                    if 'hostIP' in pod_data['status']:
                        host_ip_valor = pod_data['status']['hostIP']
                    if 'podIP' in pod_data['status']:
                        pod_ip_valor = pod_data['status']['podIP']
                    if 'startTime' in pod_data['status']:
                        startTime_valor = pod_data['status']['startTime']
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
            pre_new_window = Toplevel(parent)
            pre_new_window.title(name_value)
            pre_new_window.geometry("800x600")
            
            #top_frame = tk.Frame(pre_new_window)
            #top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            bot_frame = tk.Frame(pre_new_window)
            bot_frame.pack(side=tk.BOTTOM , fill=tk.X)

            canvas = tk.Canvas(pre_new_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and attach it to the canvas
            scrollbar = tk.Scrollbar(pre_new_window, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the contents
            new_window = tk.Frame(canvas)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)
            
            metadata_label = tk.Label(new_window, text=f"Metadata", font=("consolas", 14, "bold"))
            metadata_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            name_label = tk.Label(new_window, text=f"Nome: {nome_valor}")
            name_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            if 'generateName' in pod_data['metadata']:
                gen_name_label = tk.Label(new_window, text=f"Nome Gerado: {generate_name_valor}")
                gen_name_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            namespace_label = tk.Label(new_window, text=f"Namespace: {namespace_valor}")
            namespace_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            uid_label = tk.Label(new_window, text=f"UID: {uid_valor}")
            uid_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
            res_ver_label = tk.Label(new_window, text=f"Versão do recurso: {reseourse_ver_valor}")
            res_ver_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
            timestamp_label = tk.Label(new_window, text=f"Data de criação: {data_creation_valor}")
            timestamp_label.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
            
            row = 4
            if 'labels' in pod_data['metadata']:
                labels_label = tk.Label(new_window, text=f"Labels", font=("consolas", 14, "bold"))
                labels_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

                for item in labels:
                    tk.Label(new_window, text=f"{item}: {labels[item]}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1

            managed_fields_label = tk.Label(new_window, text=f"Managed Fields", font=("consolas", 14, "bold"))
            managed_fields_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in managed_fields:
                tk.Label(new_window, text=f"{item['manager']}", font=("consolas", 12), fg='blue').grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Operação: {item['operation']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Versão da API: {item['apiVersion']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Data e Hora: {item['time']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            if annotations:
                row+=1
                annotation_label = tk.Label(new_window, text=f"Anotações", font=("consolas", 14, "bold"))
                annotation_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row+=1
                for item in annotations:
                    last_config_label = tk.Label(new_window, text=f"{item}: {annotations[item]}")
                    last_config_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
                    #last_config_label2 = tk.Label(new_window, text=f"{annotations[item]}")
                    #last_config_label2.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
                    row+=1

            if 'ownerReferences' in pod_data['metadata']:
                proprietario_label = tk.Label(new_window, text=f"Referências do Proprietário", font=("consolas", 14, "bold"))
                proprietario_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                apiVersion_label = tk.Label(new_window, text=f"Vesão sa API: {api_ver_valor}")
                apiVersion_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                kind_label = tk.Label(new_window, text=f"Tipo: {kind_valor}")
                kind_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                name2_label = tk.Label(new_window, text=f"Nome: {owner_name_valor}")
                name2_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                uid2_label = tk.Label(new_window, text=f"UID: {owner_uid_valor}")
                uid2_label.grid(row=row-3, column=2, padx=5, pady=5, sticky=tk.W)
                controller_label = tk.Label(new_window, text=f"Controlador: {controller_valor}")
                controller_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)
                blockOwnerDeletion_label = tk.Label(new_window, text=f"Block Owner Deletion: {block_owner_valor}")
                blockOwnerDeletion_label.grid(row=row-1, column=2, padx=5, pady=5, sticky=tk.W)

            if 'volumes' in pod_data['spec']:
                volumes_label = tk.Label(new_window, text=f"Volumes", font=("consolas", 14, "bold"))
                volumes_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                volume_names_label = tk.Label(new_window, text=f"{string_names}", font=("consolas", 12), fg='blue')
                volume_names_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
                row += 1

            containers_label = tk.Label(new_window, text=f"Containers", font=("consolas", 14, "bold"))
            containers_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for i in range(0, len(container_names)):
                container_label = tk.Label(new_window, text=f"Container {i+1}", font=("consolas", 12), fg='blue')
                container_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                name3_label = tk.Label(new_window, text=f"Nome: {container_names[i]}")
                name3_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                image3_label = tk.Label(new_window, text=f"Imagem: {container_images[i]}")
                image3_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                if container_args[i]:
                    args_label = tk.Label(new_window, text=f"Args: {container_args[i]}")
                    args_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)
                if container_envs[i]:
                    envs_label = tk.Label(new_window, text=f"Env: {container_envs[i]}")
                    envs_label.grid(row=row-1, column=2, padx=5, pady=5, sticky=tk.W)
                if container_ports[i]:
                    ports_label = tk.Label(new_window, text=f"Portos {i+1}", font=("consolas", 12), fg='blue')
                    ports_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1
                    for item in container_ports[i]:
                        tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                        row += 1
            
            specs_label = tk.Label(new_window, text=f"Spec", font=("consolas", 14, "bold"))
            specs_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            restartPolicy_label = tk.Label(new_window, text=f"Restart Policy: {restartPolicy_valor}")
            restartPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            termination_label = tk.Label(new_window, text=f"Termination Grace Period: {terminationGracePeriodSeconds_valor}")
            termination_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            dnsPolicy_label = tk.Label(new_window, text=f"Dns Policy: {dnsPolicy_valor}")
            dnsPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            serviceAccount_label = tk.Label(new_window, text=f"Service Account: {serviceAccount_valor}")
            serviceAccount_label.grid(row=row-3, column=2, padx=5, pady=5, sticky=tk.W)
            if 'nodeName' in pod_data['spec']:
                nodeName_label = tk.Label(new_window, text=f"Node Name: {nodeName_valor}")
                nodeName_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)

            status_label = tk.Label(new_window, text=f"Estado", font=("consolas", 14, "bold"))
            status_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            phase_label = tk.Label(new_window, text=f"Estágio: {phase_valor}")
            phase_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if 'startTime' in pod_data['status']:
                startTime_label = tk.Label(new_window, text=f"Hora de Início: {startTime_valor}")
                startTime_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if 'hostIP' in pod_data['status']:
                host_ip_label = tk.Label(new_window, text=f"Host IP: {host_ip_valor}")
                host_ip_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)
            if 'podIP' in pod_data['status']:
                pod_ip_label = tk.Label(new_window, text=f"Pod IP: {pod_ip_valor}")
                pod_ip_label.grid(row=row-1, column=2, padx=5, pady=5, sticky=tk.W)
            condicoes_label = tk.Label(new_window, text=f"Condições", font=("consolas", 12), fg='blue')
            condicoes_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in conditions:
                tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            destroy_button = tk.Button(bot_frame, text="OK", command=pre_new_window.destroy)
            destroy_button.pack(padx=5, pady=5, expand=True)

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        pods = response.json()
        items = pods['items']
        pods_names = []
        for pod in items:
            pre_string = f"Nome: {pod['metadata']['name']}; Namespace: {pod['metadata']['namespace']}; Data de criação: {pod['metadata']['creationTimestamp']}; Versão do recurso: {pod['metadata']['resourceVersion']}; Estado: {pod['status']['phase']}"
            pods_names.append(pre_string)
        show_in_list(pods_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_pods(ip_address_var, api_port_var, authorization, listbox, tk, parent, name_entry, nome2_entry, selected_option2, ports_entry, selected_option, environment_entry, team_entry, owner_entry, purpose_entry, qauntidade_entry):
    namespace_valor = selected_option.get()
    if namespace_valor == "Todos":
        messagebox.showerror("Erro","Por vafor selecione um namespace!", parent=parent)
        return

    nome_valor = name_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    nome2_valor = nome2_entry.get().replace(" ", "")
    if not nome2_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome ao Container, a caixa de texto encontra-se vazia!", parent=parent)
        return

    imagem_valor = selected_option2.get().replace(" ", "")
    if not imagem_valor:
        messagebox.showerror("Erro","Não foi dado nenhuma Imagem ao Container, a caixa de texto encontra-se vazia!", parent=parent)
        return

    quantidade_valor = 1
    if qauntidade_entry.get().replace(" ", ""):
        quantidade_valor = int(qauntidade_entry.get().replace(" ", ""))

    portos_valor = ports_entry.get().replace(" ", "")
    environment_valor = environment_entry.get().replace(" ", "")
    team_valor = team_entry.get().replace(" ", "")
    owner_valor = owner_entry.get().replace(" ", "")
    purpose_valor = purpose_entry.get().replace(" ", "")

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_valor}/pods"
        headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
        data = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": nome_valor,
                "labels": {
                },
                "annotations": {
                }
            },
            "spec": {
                "containers": []
            }
        }
        for i in range(0,quantidade_valor):
            data['spec']['containers'].append({
                        "name": f"{nome2_valor}{i+1}",
                        "image": imagem_valor,
                        "ports": []
                    })
        if portos_valor:
            for i in range(0,quantidade_valor):
                data['spec']['containers'][i]['ports'].append({"containerPort": int(portos_valor)})
        if environment_valor:
            data['metadata']['labels']['environment'] = environment_valor
        if team_valor:
            data['metadata']['labels']['team'] = team_valor
        if owner_valor:
            data['metadata']['annotations']['owner'] = owner_valor
        if purpose_valor:
            data['metadata']['annotations']['purpose'] = purpose_valor
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        response.raise_for_status()
        if response.status_code == 201:
            messagebox.showinfo("Pod Criado", "Pod criado com sucesso", parent=parent )
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        pods = response.json()
        items = pods['items']
        pods_names = []
        for pod in items:
            pre_string = f"Nome: {pod['metadata']['name']}; Namespace: {pod['metadata']['namespace']}; Data de criação: {pod['metadata']['creationTimestamp']}; Versão do recurso: {pod['metadata']['resourceVersion']}; Estado: {pod['status']['phase']}"
            pods_names.append(pre_string)
        show_in_list(pods_names, listbox, tk)
        name_entry.delete(0, tk.END)
        nome2_entry.delete(0, tk.END)
        ports_entry.delete(0, tk.END)
        environment_entry.delete(0, tk.END)
        team_entry.delete(0, tk.END)
        owner_entry.delete(0, tk.END)
        purpose_entry.delete(0, tk.END)
        qauntidade_entry.delete(0, tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_pods(ip_address_var, api_port_var, authorization, listbox, tk, parent, pod_names):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum pod!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Pod {name_value}",f"Tem a certeza que pretende eliminar o Pod {name_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_value}/pods/{name_value}"
            headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
            response = requests.delete(url, headers=headers, verify=False)
            response.raise_for_status()
            while(1):
                if len(get_pod_names(ip_address_var, api_port_var, authorization)) != len(pod_names):
                       break
            messagebox.showinfo("Sucesso", "Pod eliminado com sucesso", parent=parent)
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/pods"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pods = response.json()
            items = pods['items']
            pods_names = []
            for pod in items:
                pre_string = f"Nome: {pod['metadata']['name']}; Namespace: {pod['metadata']['namespace']}; Data de criação: {pod['metadata']['creationTimestamp']}; Versão do recurso: {pod['metadata']['resourceVersion']}; Estado: {pod['status']['phase']}"
                pods_names.append(pre_string)
            show_in_list(pods_names, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_all_deployments(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    if dashboard_frame.winfo_ismapped():
            dashboard_frame.pack_forget()

    if not listbox.winfo_ismapped():
            listbox.pack(expand=True, fill="both", side=tk.TOP)
            new_buttons[6].pack(side=tk.BOTTOM, fill=tk.X)
            labels_frame.pack(fill=tk.X, side=tk.BOTTOM)


    namespace_names = get_namspace_names(ip_address_var, api_port_var, authorization)
    namespace_names.append("Todos")
    namespace_label = tk.Label(labels_frame, text="Namespace:")
    namespace_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(namespace_label)
    options = namespace_names
    pre_filled_value = "Todos"
    selected_option = tk.StringVar()
    combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
    try:
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)  # Set the pre-filled value
    except ValueError:
        pass
    combobox.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(combobox)
    
    editar_button = tk.Button(labels_frame, text="Filtrar", command= lambda: filtrar())
    editar_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.SW)
    old_buttons.append(editar_button)

    def filtrar():
        try:
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pods = response.json()
            items = pods['items']
            pods_names = []
            for deploy in items:
                if selected_option.get().strip() == "Todos":
                    pre_string = f"Nome: {deploy['metadata']['name']}; Namespace: {deploy['metadata']['namespace']}; Data de criação: {deploy['metadata']['creationTimestamp']}; Versão do recurso: {deploy['metadata']['resourceVersion']}; Réplicas: {deploy['status']['replicas']}"
                    pods_names.append(pre_string)
                elif deploy['metadata']['namespace'] == selected_option.get().strip():
                    pre_string = f"Nome: {deploy['metadata']['name']}; Namespace: {deploy['metadata']['namespace']}; Data de criação: {deploy['metadata']['creationTimestamp']}; Versão do recurso: {deploy['metadata']['resourceVersion']}; Réplicas: {deploy['status']['replicas']}"
                    pods_names.append(pre_string)
            show_in_list(pods_names, listbox, tk)
            listbox.bind("<Double-Button-1>", on_double_click)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    name_label = tk.Label(labels_frame, text="Nome*:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)
    replicas_label = tk.Label(labels_frame, text="Replicas*:")
    replicas_label.grid(row=2, column=0, padx=5, pady=5)
    old_buttons.append(replicas_label)
    replicas_entry = tk.Entry(labels_frame)
    replicas_entry.grid(row=2, column=1, padx=5, pady=5)
    old_buttons.append(replicas_entry)
    match_label = tk.Label(labels_frame, text="Match Labels:")
    match_label.grid(row=3, column=0, padx=5, pady=5)
    old_buttons.append(match_label)
    match_entry = tk.Entry(labels_frame)
    match_entry.grid(row=3, column=1, padx=5, pady=5)
    old_buttons.append(match_entry)
    template_label = tk.Label(labels_frame, text="Template Label:")
    template_label.grid(row=4, column=0, padx=5, pady=5)
    old_buttons.append(template_label)
    template_entry = tk.Entry(labels_frame)
    template_entry.grid(row=4, column=1, padx=5, pady=5)
    old_buttons.append(template_entry)

    containers_label = tk.Label(labels_frame, text="Container".upper())
    containers_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(containers_label)
    nome2_label = tk.Label(labels_frame, text="Nome*:")
    nome2_label.grid(row=2, column=2, padx=5, pady=5)
    old_buttons.append(nome2_label)
    nome2_entry = tk.Entry(labels_frame)
    nome2_entry.grid(row=2, column=3, padx=5, pady=5)
    old_buttons.append(nome2_entry)
    image_label = tk.Label(labels_frame, text="Imagem*:")
    image_label.grid(row=3, column=2, padx=5, pady=5)
    old_buttons.append(image_label)
    ports_label = tk.Label(labels_frame, text="Porto:")
    ports_label.grid(row=4, column=2, padx=5, pady=5)
    old_buttons.append(ports_label)
    ports_entry = tk.Entry(labels_frame)
    ports_entry.grid(row=4, column=3, padx=5, pady=5)
    old_buttons.append(ports_entry)
    quantidade_label = tk.Label(labels_frame, text="Quantidade:")
    quantidade_label.grid(row=5, column=2, padx=5, pady=5)
    old_buttons.append(quantidade_label)
    qauntidade_entry = tk.Entry(labels_frame)
    qauntidade_entry.grid(row=5, column=3, padx=5, pady=5)
    old_buttons.append(qauntidade_entry)

    image_names = ['nginx:latest', "httpd:latest", 'caddy:latest', 'mysql:latest', 'mysql:latest', 'postgres:latest', 'mongo:latest', 'redis:latest', 'mariadb:latest', 'python:latest', 'node:latest', 'ruby:latest', 'golang:latest', 'php:latest', 'busybox:latest', 'alpine:latest', 'ubuntu:latest', 'centos:latest', 'debian:latest', 'jenkins/jenkins:latest', 'gitlab/gitlab-ce:latest', 'sonarqube:latest', 'prom/prometheus:latest', 'grafana/grafana:latest', 'elasticsearch:latest', 'kibana:latest', 'varnish:latest', 'rabbitmq:latest', 'wurstmeister/kafka:latest', 'portainer/portainer-ce:latest']

    options2 = image_names
    pre_filled_value2 = "httpd:latest"
    selected_option2 = tk.StringVar()
    combobox3 = ttk.Combobox(labels_frame, textvariable=selected_option2, values=options2)
    try:
        pre_filled_index2 = options2.index(pre_filled_value2)
        combobox3.current(1)  # Set the pre-filled value
    except ValueError:
        pass
    combobox3.grid(row=3, column=3, padx=5, pady=5)
    old_buttons.append(combobox3)

    metadata_label = tk.Label(labels_frame, text="metadata".upper(), font=("consolas", 12), fg='blue')
    metadata_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(metadata_label)
    labels_label = tk.Label(labels_frame, text="LABELS")
    labels_label.grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(labels_label)
    environment_label = tk.Label(labels_frame, text="Environment:")
    environment_label.grid(row=3, column=4, padx=5, pady=5)
    old_buttons.append(environment_label)
    environment_entry = tk.Entry(labels_frame)
    environment_entry.grid(row=3, column=5, padx=5, pady=5)
    old_buttons.append(environment_entry)
    team_label = tk.Label(labels_frame, text="Team:")
    team_label.grid(row=4, column=4, padx=5, pady=5)
    old_buttons.append(team_label)
    team_entry = tk.Entry(labels_frame)
    team_entry.grid(row=4, column=5, padx=5, pady=5)
    old_buttons.append(team_entry)

    annotations_label = tk.Label(labels_frame, text="annotations".upper())
    annotations_label.grid(row=2, column=6, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(annotations_label)
    owner_label = tk.Label(labels_frame, text="Owner:")
    owner_label.grid(row=3, column=6, padx=5, pady=5)
    old_buttons.append(owner_label)
    owner_entry = tk.Entry(labels_frame)
    owner_entry.grid(row=3, column=7, padx=5, pady=5)
    old_buttons.append(owner_entry)
    purpose_label = tk.Label(labels_frame, text="Purpose:")
    purpose_label.grid(row=4, column=6, padx=5, pady=5)
    old_buttons.append(purpose_label)
    purpose_entry = tk.Entry(labels_frame)
    purpose_entry.grid(row=4, column=7, padx=5, pady=5)
    old_buttons.append(purpose_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command= lambda: criar_deployments(ip_address_var, api_port_var, authorization, listbox, tk, parent, name_entry, nome2_entry, selected_option2, ports_entry, selected_option, replicas_entry, match_entry, template_entry, environment_entry, team_entry, owner_entry, purpose_entry, qauntidade_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[2].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command= lambda: eliminar_deployments(ip_address_var, api_port_var, authorization, listbox, tk, parent, get_deploy_names(ip_address_var, api_port_var, authorization)))
    old_buttons.append(new_buttons[2])
    
    def on_double_click(event):
        index = listbox.curselection()
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/namespaces/{namespace_value}/deployments/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                space_data = response.json()
                
                nome_valor = space_data['metadata']['name']
                uid_valor = space_data['metadata']['uid']
                namespace_valor = space_data['metadata']['namespace']
                resource_ver_valor = space_data['metadata']['resourceVersion']
                data_criacao_valor = space_data['metadata']['creationTimestamp']
                generation_valor = space_data['metadata']['generation']
                
                if 'labels' in space_data['metadata']: 
                    labels = space_data['metadata']['labels']

                managed_fields = space_data['metadata']['managedFields']

                if 'volumes' in space_data['spec']: 
                    vol_names = []
                    for item in space_data['spec']['volumes']:
                        vol_names.append(item['name'])
                    string_names = ''
                    for item in vol_names:
                        string_names += item + ','
                    string_names = string_names[:-1]

                annotations = 0
                if 'annotations' in space_data['metadata']:
                    annotations = space_data['metadata']['annotations']
                try:
                    if space_data['spec']['template']['metadata']['labels']['app']:
                        template_valor = space_data['spec']['template']['metadata']['labels']['app']
                    if space_data['spec']['selector']['matchLabels']['app']:
                        matchlabels_valor = space_data['spec']['selector']['matchLabels']['app']
                except:
                    pass

                container_names = []
                container_images = []
                container_ports = []
                container_args = []
                container_volume_mounts = []
                for item in space_data['spec']['template']['spec']['containers']:
                    container_names.append(item['name'])
                    container_images.append(item['image'])
                    if 'ports' in item:
                        container_ports.append(item['ports'])
                    else:
                        container_ports.append(False)
                    if 'volumeMounts' in item:
                        container_volume_mounts.append(item['volumeMounts'])
                    else:
                        container_volume_mounts.append(False)
                    if 'args' in item:
                        args_names = []
                        for item2 in item['args']:
                            args_names.append(item2)
                        string_args = ''
                        for item2 in args_names:
                            string_args += item2 + ','
                        container_args.append(string_args[:-1])
                    else:
                        container_args.append(False)
                    
                    restartPolicy_valor = space_data['spec']['template']['spec']['restartPolicy']
                    terminationGracePeriodSeconds_valor = space_data['spec']['template']['spec']['terminationGracePeriodSeconds']
                    dnsPolicy_valor = space_data['spec']['template']['spec']['dnsPolicy']
                    if 'serviceAccount' in space_data['spec']['template']['spec']:
                        serviceAccount_valor = space_data['spec']['template']['spec']['serviceAccount']
                    if 'schedulerName' in space_data['spec']['template']['spec']:
                        schedulerName_valor = space_data['spec']['template']['spec']['schedulerName']
                    if 'priorityClassName' in space_data['spec']['template']['spec']:
                        priorityClassName_valor = space_data['spec']['template']['spec']['priorityClassName']
                    estrategia_valor = space_data['spec']['strategy']['type']

                    replicas_valor = space_data['status']['replicas']
                    if 'updatedReplicas' in space_data['status']:
                        updatedReplicas_valor = space_data['status']['updatedReplicas']
                    if 'readyReplicas' in space_data['status']:
                        readyReplicas_valor = space_data['status']['readyReplicas']
                    if 'availableReplicas' in space_data['status']:
                        availableReplicas_valor = space_data['status']['availableReplicas']

                    conditions = []
                    for item in space_data['status']['conditions']:
                        conditions.append(item['message'])
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
            pre_new_window = Toplevel(parent)
            pre_new_window.title(name_value)
            pre_new_window.geometry("800x600")
            
            #top_frame = tk.Frame(pre_new_window)
            #top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            bot_frame = tk.Frame(pre_new_window)
            bot_frame.pack(side=tk.BOTTOM , fill=tk.X)

            canvas = tk.Canvas(pre_new_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and attach it to the canvas
            scrollbar = tk.Scrollbar(pre_new_window, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the contents
            new_window = tk.Frame(canvas)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)
            
            metadata_label = tk.Label(new_window, text=f"Metadata", font=("consolas", 14, "bold"))
            metadata_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            name_label = tk.Label(new_window, text=f"Nome: {nome_valor}")
            name_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            uid_label = tk.Label(new_window, text=f"UID: {uid_valor}")
            uid_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            resource_ver_label = tk.Label(new_window, text=f"Resource Version: {resource_ver_valor}")
            resource_ver_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
            creation_time_label = tk.Label(new_window, text=f"Data de criação: {data_criacao_valor}")
            creation_time_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
            namespace_label = tk.Label(new_window, text=f"Namespace: {namespace_valor}")
            namespace_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            generation_label = tk.Label(new_window, text=f"Geração: {generation_valor}")
            generation_label.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

            row = 4
            
            if 'labels' in space_data['metadata']:
                labels_label = tk.Label(new_window, text=f"Labels", font=("consolas", 14, "bold"))
                labels_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                for item in labels:
                    tk.Label(new_window, text=f"{item}: {labels[item]}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1

            if annotations:
                row+=1
                annotation_label = tk.Label(new_window, text=f"Anotações", font=("consolas", 14, "bold"))
                annotation_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row+=1
                for item in annotations:
                    last_config_label = tk.Label(new_window, text=f"{item}: {annotations[item]}")
                    last_config_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=100)
                    #last_config_label2 = tk.Label(new_window, text=f"{annotations[item]}")
                    #last_config_label2.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
                    row+=1

            managed_fields_label = tk.Label(new_window, text=f"Managed Fields", font=("consolas", 14, "bold"))
            managed_fields_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in managed_fields:
                tk.Label(new_window, text=f"{item['manager']}", font=("consolas", 12), fg='blue').grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Operação: {item['operation']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Versão da API: {item['apiVersion']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Data e Hora: {item['time']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            if 'volumes' in space_data['spec']:
                volumes_label = tk.Label(new_window, text=f"Volumes", font=("consolas", 14, "bold"))
                volumes_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                volume_names_label = tk.Label(new_window, text=f"{string_names}", font=("consolas", 12), fg='blue')
                volume_names_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
                row += 1

            containers_label = tk.Label(new_window, text=f"Containers", font=("consolas", 14, "bold"))
            containers_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for i in range(0, len(container_names)):
                container_label = tk.Label(new_window, text=f"Container {i+1}", font=("consolas", 12), fg='blue')
                container_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                name3_label = tk.Label(new_window, text=f"Nome: {container_names[i]}")
                name3_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                image3_label = tk.Label(new_window, text=f"Imagem: {container_images[i]}")
                image3_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row +=1
                if container_args[i]:
                    args_label = tk.Label(new_window, text=f"Args: {container_args[i]}")
                    args_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)
                if container_ports[i]:
                    ports_label = tk.Label(new_window, text=f"Portos {i+1}", font=("consolas", 12), fg='blue')
                    ports_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1
                    for item in container_ports[i]:
                        tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                        row += 1
                if container_volume_mounts[i]:
                    volumeMounts = tk.Label(new_window, text=f"Volume Mounts {i+1}", font=("consolas", 12), fg='blue')
                    volumeMounts.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1
                    for item in container_volume_mounts[i]:
                        tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                        row += 1

            specs_label = tk.Label(new_window, text=f"Spec", font=("consolas", 14, "bold"))
            specs_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            restartPolicy_label = tk.Label(new_window, text=f"Restart Policy: {restartPolicy_valor}")
            restartPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            termination_label = tk.Label(new_window, text=f"Termination Grace Period: {terminationGracePeriodSeconds_valor}")
            termination_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            dnsPolicy_label = tk.Label(new_window, text=f"Dns Policy: {dnsPolicy_valor}")
            dnsPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            if 'serviceAccount' in space_data['spec']['template']['spec']:
                serviceAccount_label = tk.Label(new_window, text=f"Service Account: {serviceAccount_valor}")
                serviceAccount_label.grid(row=row-3, column=2, padx=5, pady=5, sticky=tk.W)
            if 'schedulerName' in space_data['spec']['template']['spec']:
                nodeName_label = tk.Label(new_window, text=f"Scheduler Name: {schedulerName_valor}")
                nodeName_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)
            if 'priorityClassName' in space_data['spec']['template']['spec']:
                nodeName_label = tk.Label(new_window, text=f"Priority Class Name: {priorityClassName_valor}")
                nodeName_label.grid(row=row-1, column=2, padx=5, pady=5, sticky=tk.W)
            estrategia_label = tk.Label(new_window, text=f"Estratégia: {estrategia_valor}")
            estrategia_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row +=1
            try:
                if space_data['spec']['selector']['matchLabels']['app']:
                    labels3_label = tk.Label(new_window, text=f"Labels", font=("consolas", 12), fg='blue')
                    labels3_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
                    row += 1
                    matchLabels_label = tk.Label(new_window, text=f"Match Labels: {matchlabels_valor}")
                    matchLabels_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row +=1
                    if space_data['spec']['template']['metadata']['labels']['app']:
                        template_label = tk.Label(new_window, text=f"Template Label: {template_valor}")
                        template_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                        row +=1
            except:
                pass

            status_label = tk.Label(new_window, text=f"Estado", font=("consolas", 14, "bold"))
            status_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            replicas_label = tk.Label(new_window, text=f"Réplicas: {replicas_valor}")
            replicas_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if 'updatedReplicas' in space_data['status']:
                updatedReplicas_label = tk.Label(new_window, text=f"Réplicas Atualizadas: {updatedReplicas_valor}")
                updatedReplicas_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if 'readyReplicas' in space_data['status']:
                readyReplicas_label = tk.Label(new_window, text=f"Réplicas Prontas: {readyReplicas_valor}")
                readyReplicas_label.grid(row=row-2, column=2, padx=5, pady=5, sticky=tk.W)
            if 'availableReplicas' in space_data['status']:
                availableReplicas_label = tk.Label(new_window, text=f"Réplicas Disponíveis: {availableReplicas_valor}")
                availableReplicas_label.grid(row=row-1, column=2, padx=5, pady=5, sticky=tk.W)
            condicoes_label = tk.Label(new_window, text=f"Condições", font=("consolas", 12), fg='blue')
            condicoes_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in conditions:
                tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            destroy_button = tk.Button(bot_frame, text="OK", command=pre_new_window.destroy)
            destroy_button.pack(padx=5, pady=5, expand=True)

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        deploys = response.json()
        items = deploys['items']
        deploys_names = []
        for deploy in items:
            pre_string = f"Nome: {deploy['metadata']['name']}; Namespace: {deploy['metadata']['namespace']}; Data de criação: {deploy['metadata']['creationTimestamp']}; Versão do recurso: {deploy['metadata']['resourceVersion']}; Réplicas: {deploy['status']['replicas']}"
            deploys_names.append(pre_string)
        show_in_list(deploys_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_deployments(ip_address_var, api_port_var, authorization, listbox, tk, parent, name_entry, nome2_entry, selected_option2, ports_entry, selected_option, replicas_entry, match_entry, template_entry, environment_entry, team_entry, owner_entry, purpose_entry, qauntidade_entry):
    namespace_valor = selected_option.get()
    if namespace_valor == "Todos":
        messagebox.showerror("Erro","Por vafor selecione um namespace!", parent=parent)
        return

    nome_valor = name_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    replicas_valor = replicas_entry.get().replace(" ", "")
    if not replicas_valor:
        messagebox.showerror("Erro","Não foi dado nenhuma Réplica, a caixa de texto encontra-se vazia!", parent=parent)
        return

    nome2_valor = nome2_entry.get().replace(" ", "")
    if not nome2_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome ao Container, a caixa de texto encontra-se vazia!", parent=parent)
        return

    imagem_valor = selected_option2.get().replace(" ", "")
    if not imagem_valor:
        messagebox.showerror("Erro","Não foi dado nenhuma Imagem ao Container, a caixa de texto encontra-se vazia!", parent=parent)
        return

    quantidade_valor = 1
    if qauntidade_entry.get().replace(" ", ""):
        quantidade_valor = int(qauntidade_entry.get().replace(" ", ""))

    portos_valor = ports_entry.get().replace(" ", "")
    match_valor = match_entry.get().replace(" ", "")
    template_valor = template_entry.get().replace(" ", "")
    environment_valor = environment_entry.get().replace(" ", "")
    team_valor = team_entry.get().replace(" ", "")
    owner_valor = owner_entry.get().replace(" ", "")
    purpose_valor = purpose_entry.get().replace(" ", "")

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/namespaces/{namespace_valor}/deployments"
        headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
        data = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": nome_valor,
                "labels": {
                },
                "annotations": {
                }
            },
            "spec": {
                "replicas": int(replicas_valor),
                "selector": {
                    "matchLabels": {
                        "app": nome2_valor
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": nome2_valor
                        }
                    },
                    "spec": {
                        "containers": []
                    }
                }
            }
        }
        for i in range(0,quantidade_valor):
            data['spec']['template']['spec']['containers'].append({
                        "name": f"{nome2_valor}{i+1}",
                        "image": imagem_valor,
                        "ports": []
                    })
        if portos_valor:
            for i in range(0,quantidade_valor):
                data['spec']['template']['spec']['containers'][i]['ports'].append({"containerPort": int(portos_valor)})
        if match_valor:
            data['spec']['selector']['matchLabels']['app'] = match_valor
        if template_valor:
            data['spec']['template']['metadata']['labels']['app'] = template_valor
        if environment_valor:
            data['metadata']['labels']['environment'] = environment_valor
        if team_valor:
            data['metadata']['labels']['team'] = team_valor
        if owner_valor:
            data['metadata']['annotations']['owner'] = owner_valor
        if purpose_valor:
            data['metadata']['annotations']['purpose'] = purpose_valor
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        response.raise_for_status()
        if response.status_code == 201:
            messagebox.showinfo("Deployment Criado", "Deployment criado com sucesso", parent=parent )
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        deploys = response.json()
        items = deploys['items']
        deploys_names = []
        for deploy in items:
            pre_string = f"Nome: {deploy['metadata']['name']}; Namespace: {deploy['metadata']['namespace']}; Data de criação: {deploy['metadata']['creationTimestamp']}; Versão do recurso: {deploy['metadata']['resourceVersion']}; Réplicas: {deploy['status']['replicas']}"
            deploys_names.append(pre_string)
        show_in_list(deploys_names, listbox, tk)
        name_entry.delete(0, tk.END)
        nome2_entry.delete(0, tk.END)
        ports_entry.delete(0, tk.END)
        match_entry.delete(0, tk.END)
        replicas_entry.delete(0, tk.END)
        template_entry.delete(0, tk.END)
        environment_entry.delete(0, tk.END)
        team_entry.delete(0, tk.END)
        owner_entry.delete(0, tk.END)
        purpose_entry.delete(0, tk.END)
        qauntidade_entry.delete(0, tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_deployments(ip_address_var, api_port_var, authorization, listbox, tk, parent, pod_names):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Deployment!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Deployment {name_value}",f"Tem a certeza que pretende eliminar o Deployment {name_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/namespaces/{namespace_value}/deployments/{name_value}"
            headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
            response = requests.delete(url, headers=headers, verify=False)
            response.raise_for_status()
            while(1):
                if len(get_deploy_names(ip_address_var, api_port_var, authorization)) != len(pod_names):
                       break
            messagebox.showinfo("Sucesso", "Deployment eliminado com sucesso", parent=parent)
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/deployments"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            deploys = response.json()
            items = deploys['items']
            deploys_names = []
            for deploy in items:
                pre_string = f"Nome: {deploy['metadata']['name']}; Namespace: {deploy['metadata']['namespace']}; Data de criação: {deploy['metadata']['creationTimestamp']}; Versão do recurso: {deploy['metadata']['resourceVersion']}; Réplicas: {deploy['status']['replicas']}"
                deploys_names.append(pre_string)
            show_in_list(deploys_names, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_all_services(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    if dashboard_frame.winfo_ismapped():
            dashboard_frame.pack_forget()

    if not listbox.winfo_ismapped():
            listbox.pack(expand=True, fill="both", side=tk.TOP)
            new_buttons[6].pack(side=tk.BOTTOM, fill=tk.X)
            labels_frame.pack(fill=tk.X, side=tk.BOTTOM)

    
    namespace_names = get_namspace_names(ip_address_var, api_port_var, authorization)
    namespace_names.append("Todos")
    namespace_label = tk.Label(labels_frame, text="Namespace:")
    namespace_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(namespace_label)
    options = namespace_names
    pre_filled_value = "Todos"
    selected_option = tk.StringVar()
    combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
    try:
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)  # Set the pre-filled value
    except ValueError:
        pass
    combobox.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(combobox)
    
    editar_button = tk.Button(labels_frame, text="Filtrar", command= lambda: filtrar())
    editar_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.SW)
    old_buttons.append(editar_button)

    def filtrar():
        try:
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/services"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pods = response.json()
            items = pods['items']
            services_names = []
            for service in items:
                if selected_option.get().strip() == "Todos":
                    pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
                    services_names.append(pre_string)
                elif service['metadata']['namespace'] == selected_option.get().strip():
                    pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
                    services_names.append(pre_string)
            show_in_list(services_names, listbox, tk)
            listbox.bind("<Double-Button-1>", on_double_click)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    name_label = tk.Label(labels_frame, text="Nome*:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)
    selector_label = tk.Label(labels_frame, text="Selector*:")
    selector_label.grid(row=2, column=0, padx=5, pady=5)
    old_buttons.append(selector_label)
    selector_entry = tk.Entry(labels_frame)
    selector_entry.grid(row=2, column=1, padx=5, pady=5)
    old_buttons.append(selector_entry)
    type_label = tk.Label(labels_frame, text="Type:")
    type_label.grid(row=3, column=0, padx=5, pady=5)
    old_buttons.append(type_label)
    options2 = ["LoadBalancer", "ClusterIP"]
    #pre_filled_value2 = "LoadBalancer"
    selected_option2 = tk.StringVar()
    combobox2 = ttk.Combobox(labels_frame, textvariable=selected_option2, values=options2)
    try:
        #pre_filled_index2 = options2.index(pre_filled_value2)
        combobox2.current(0)  # Set the pre-filled value
    except ValueError:
        pass
    combobox2.grid(row=3, column=1, padx=5, pady=5)
    old_buttons.append(combobox2)

    containers_label = tk.Label(labels_frame, text="Portos".upper())
    containers_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(containers_label)
    protocolo_label = tk.Label(labels_frame, text="Protocolo:")
    protocolo_label.grid(row=2, column=2, padx=5, pady=5)
    old_buttons.append(protocolo_label)
    options3 = ["TCP", "UDP", "SCTP"]
    #pre_filled_value3 = "TCP"
    selected_option3 = tk.StringVar()
    combobox3 = ttk.Combobox(labels_frame, textvariable=selected_option3, values=options3)
    try:
        #pre_filled_index3 = options3.index(pre_filled_value3)
        combobox3.current(0)  # Set the pre-filled value
    except ValueError:
        pass
    combobox3.grid(row=2, column=3, padx=5, pady=5)
    old_buttons.append(combobox3)
    ports_label = tk.Label(labels_frame, text="Porto:*")
    ports_label.grid(row=3, column=2, padx=5, pady=5)
    old_buttons.append(ports_label)
    ports_entry = tk.Entry(labels_frame)
    ports_entry.grid(row=3, column=3, padx=5, pady=5)
    old_buttons.append(ports_entry)
    targetport_label = tk.Label(labels_frame, text="Target Port*:")
    targetport_label.grid(row=4, column=2, padx=5, pady=5)
    old_buttons.append(targetport_label)
    targetport_entry = tk.Entry(labels_frame)
    targetport_entry.grid(row=4, column=3, padx=5, pady=5)
    old_buttons.append(targetport_entry)

    metadata_label = tk.Label(labels_frame, text="metadata".upper(), font=("consolas", 12), fg='blue')
    metadata_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(metadata_label)
    labels_label = tk.Label(labels_frame, text="LABELS")
    labels_label.grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(labels_label)
    environment_label = tk.Label(labels_frame, text="Environment:")
    environment_label.grid(row=3, column=4, padx=5, pady=5)
    old_buttons.append(environment_label)
    environment_entry = tk.Entry(labels_frame)
    environment_entry.grid(row=3, column=5, padx=5, pady=5)
    old_buttons.append(environment_entry)
    team_label = tk.Label(labels_frame, text="Team:")
    team_label.grid(row=4, column=4, padx=5, pady=5)
    old_buttons.append(team_label)
    team_entry = tk.Entry(labels_frame)
    team_entry.grid(row=4, column=5, padx=5, pady=5)
    old_buttons.append(team_entry)

    annotations_label = tk.Label(labels_frame, text="annotations".upper())
    annotations_label.grid(row=2, column=6, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(annotations_label)
    owner_label = tk.Label(labels_frame, text="Owner:")
    owner_label.grid(row=3, column=6, padx=5, pady=5)
    old_buttons.append(owner_label)
    owner_entry = tk.Entry(labels_frame)
    owner_entry.grid(row=3, column=7, padx=5, pady=5)
    old_buttons.append(owner_entry)
    purpose_label = tk.Label(labels_frame, text="Purpose:")
    purpose_label.grid(row=4, column=6, padx=5, pady=5)
    old_buttons.append(purpose_label)
    purpose_entry = tk.Entry(labels_frame)
    purpose_entry.grid(row=4, column=7, padx=5, pady=5)
    old_buttons.append(purpose_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command= lambda: criar_services(ip_address_var, api_port_var, authorization, listbox, tk, parent, selected_option, name_entry, selector_entry, selected_option2, selected_option3, ports_entry, targetport_entry, environment_entry, team_entry, owner_entry, purpose_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[2].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command= lambda: eliminar_services(ip_address_var, api_port_var, authorization, listbox, tk, parent, get_service_names(ip_address_var, api_port_var, authorization)))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        index = listbox.curselection()
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_value}/services/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                space_data = response.json()
                
                nome_valor = space_data['metadata']['name']
                uid_valor = space_data['metadata']['uid']
                resource_ver_valor = space_data['metadata']['resourceVersion']
                data_criacao_valor = space_data['metadata']['creationTimestamp']
                namespace_valor = space_data['metadata']['namespace']

                if 'labels' in space_data['metadata']: 
                    labels = space_data['metadata']['labels']
                
                annotations = 0
                if 'annotations' in space_data['metadata']:
                    annotations = space_data['metadata']['annotations']

                managed_fields = space_data['metadata']['managedFields']

                ports = False
                if 'ports' in space_data['spec']:
                    ports = space_data['spec']['ports']

                cluster_ip_valor = space_data['spec']['clusterIP']
                type_valor = space_data['spec']['type']
                sessionAffinity_valor = space_data['spec']['sessionAffinity']
                if 'externalTrafficPolicy' in space_data['spec']:
                    externalTrafficPolicy_valor = space_data['spec']['externalTrafficPolicy']
                ipFamilyPolicy_valor = space_data['spec']['ipFamilyPolicy']
                if 'internalTrafficPolicy' in space_data['spec']:
                    internalTrafficPolicy_valor = space_data['spec']['internalTrafficPolicy']
                type_valor = space_data['spec']['type']
                string_ipfamilies = ''
                for item in space_data['spec']['ipFamilies']:
                    string_ipfamilies += item + ','
                string_ipfamilies = string_ipfamilies[:-1]
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
            pre_new_window = Toplevel(parent)
            pre_new_window.title(name_value)
            pre_new_window.geometry("800x600")
            
            #top_frame = tk.Frame(pre_new_window)
            #top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            bot_frame = tk.Frame(pre_new_window)
            bot_frame.pack(side=tk.BOTTOM , fill=tk.X)

            canvas = tk.Canvas(pre_new_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and attach it to the canvas
            scrollbar = tk.Scrollbar(pre_new_window, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the contents
            new_window = tk.Frame(canvas)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)
            
            metadata_label = tk.Label(new_window, text=f"Metadata", font=("consolas", 14, "bold"))
            metadata_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            name_label = tk.Label(new_window, text=f"Nome: {nome_valor}")
            name_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            uid_label = tk.Label(new_window, text=f"UID: {uid_valor}")
            uid_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            resource_ver_label = tk.Label(new_window, text=f"Resource Version: {resource_ver_valor}")
            resource_ver_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
            creation_time_label = tk.Label(new_window, text=f"Data de criação: {data_criacao_valor}")
            creation_time_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
            namespcace_label = tk.Label(new_window, text=f"Namespace: {namespace_valor}")
            namespcace_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            
            row = 4
            
            if 'labels' in space_data['metadata']:
                labels_label = tk.Label(new_window, text=f"Labels", font=("consolas", 14, "bold"))
                labels_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                for item in labels:
                    tk.Label(new_window, text=f"{item}: {labels[item]}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1
            
            if annotations:
                row+=1
                annotation_label = tk.Label(new_window, text=f"Anotações", font=("consolas", 14, "bold"))
                annotation_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row+=1
                for item in annotations:
                    last_config_label = tk.Label(new_window, text=f"{item}: {annotations[item]}")
                    last_config_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=100)
                    #last_config_label2 = tk.Label(new_window, text=f"{annotations[item]}")
                    #last_config_label2.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
                    row+=1

            managed_fields_label = tk.Label(new_window, text=f"Managed Fields", font=("consolas", 14, "bold"))
            managed_fields_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in managed_fields:
                tk.Label(new_window, text=f"{item['manager']}", font=("consolas", 12), fg='blue').grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Operação: {item['operation']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Versão da API: {item['apiVersion']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Data e Hora: {item['time']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
            
            specs_label = tk.Label(new_window, text=f"Spec", font=("consolas", 14, "bold"))
            specs_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if ports:
                ports_label = tk.Label(new_window, text=f"Portos", font=("consolas", 12), fg='blue')
                ports_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                for item in ports:
                    tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1
            outros_label = tk.Label(new_window, text=f"Outros", font=("consolas", 12), fg='blue')
            outros_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            clusterIP_label = tk.Label(new_window, text=f"IP do Cluster: {cluster_ip_valor}")
            clusterIP_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            type_label = tk.Label(new_window, text=f"Tipo: {type_valor}")
            type_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            sessionAffinity_label = tk.Label(new_window, text=f"Session Affinity: {sessionAffinity_valor}")
            sessionAffinity_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if 'externalTrafficPolicy' in space_data['spec']:
                externalTrafficPolicy_label = tk.Label(new_window, text=f"External Traffic Policy: {externalTrafficPolicy_valor}")
                externalTrafficPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
            ipFamilies_label = tk.Label(new_window, text=f"Familias IP: {string_ipfamilies}")
            ipFamilies_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            ipFamilyPolicy_label = tk.Label(new_window, text=f"IP Family Policy: {ipFamilyPolicy_valor}")
            ipFamilyPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            if 'internalTrafficPolicy' in space_data['spec']:
                internalTrafficPolicy_label = tk.Label(new_window, text=f"Internal Traffic Policy: {internalTrafficPolicy_valor}")
                internalTrafficPolicy_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            destroy_button = tk.Button(bot_frame, text="OK", command=pre_new_window.destroy)
            destroy_button.pack(padx=5, pady=5, expand=True)

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/services"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        services = response.json()
        items = services['items']
        services_names = []
        for service in items:
            pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
            services_names.append(pre_string)
        show_in_list(services_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_services(ip_address_var, api_port_var, authorization, listbox, tk, parent, selected_option, name_entry, selector_entry, selected_option2, selected_option3, ports_entry, targetport_entry, environment_entry, team_entry, owner_entry, purpose_entry):
    namespace_valor = selected_option.get()
    if namespace_valor == "Todos":
        messagebox.showerror("Erro","Por vafor selecione um namespace!", parent=parent)
        return

    nome_valor = name_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    selector_valor = selector_entry.get().replace(" ", "")
    if not selector_valor:
        messagebox.showerror("Erro","Não foi dado nenhuma Selector, a caixa de texto encontra-se vazia!", parent=parent)
        return

    port_valor = ports_entry.get().replace(" ", "")
    if not port_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Porto, a caixa de texto encontra-se vazia!", parent=parent)
        return

    target_port_valor = targetport_entry.get().replace(" ", "")
    if not target_port_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Target Port, a caixa de texto encontra-se vazia!", parent=parent)
        return

    type_valor = selected_option2.get().replace(" ", "")
    protocol_valor = selected_option3.get().replace(" ", "")
    environment_valor = environment_entry.get().replace(" ", "")
    team_valor = team_entry.get().replace(" ", "")
    owner_valor = owner_entry.get().replace(" ", "")
    purpose_valor = purpose_entry.get().replace(" ", "")

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_valor}/services"
        headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
        data = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": nome_valor,
                "labels": {
                },
                "annotations": {
                }
            },
            "spec": {
                "selector": {
                    "app": selector_valor
                },
                "ports": [
                    {
                        "protocol": protocol_valor,
                        "port": int(port_valor),
                        "targetPort": int(target_port_valor)
                    }
                ],
                "type": type_valor
            }
        }
        if environment_valor:
            data['metadata']['labels']['environment'] = environment_valor
        if team_valor:
            data['metadata']['labels']['team'] = team_valor
        if owner_valor:
            data['metadata']['annotations']['owner'] = owner_valor
        if purpose_valor:
            data['metadata']['annotations']['purpose'] = purpose_valor
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        response.raise_for_status()
        if response.status_code == 201:
            messagebox.showinfo("Service Criado", "Service criado com sucesso", parent=parent )
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/services"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        services = response.json()
        items = services['items']
        services_names = []
        for service in items:
            pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
            services_names.append(pre_string)
        show_in_list(services_names, listbox, tk)
        name_entry.delete(0, tk.END)
        selector_entry.delete(0, tk.END)
        ports_entry.delete(0, tk.END)
        targetport_entry.delete(0, tk.END)
        environment_entry.delete(0, tk.END)
        team_entry.delete(0, tk.END)
        owner_entry.delete(0, tk.END)
        purpose_entry.delete(0, tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_services(ip_address_var, api_port_var, authorization, listbox, tk, parent, pod_names):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Service!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Service {name_value}",f"Tem a certeza que pretende eliminar o Service {name_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_value}/services/{name_value}"
            headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
            response = requests.delete(url, headers=headers, verify=False)
            response.raise_for_status()
            while(1):
                if len(get_service_names(ip_address_var, api_port_var, authorization)) != len(pod_names):
                       break
            messagebox.showinfo("Sucesso", "Service eliminado com sucesso", parent=parent)
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/services"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            services = response.json()
            items = services['items']
            services_names = []
            for service in items:
                pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
                services_names.append(pre_string)
            show_in_list(services_names, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_all_ingresses(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    if dashboard_frame.winfo_ismapped():
            dashboard_frame.pack_forget()

    if not listbox.winfo_ismapped():
            listbox.pack(expand=True, fill="both", side=tk.TOP)
            new_buttons[6].pack(side=tk.BOTTOM, fill=tk.X)
            labels_frame.pack(fill=tk.X, side=tk.BOTTOM)

    
    namespace_names = get_namspace_names(ip_address_var, api_port_var, authorization)
    namespace_names.append("Todos")
    namespace_label = tk.Label(labels_frame, text="Namespace:")
    namespace_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(namespace_label)
    options = namespace_names
    pre_filled_value = "Todos"
    selected_option = tk.StringVar()
    combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
    try:
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)  # Set the pre-filled value
    except ValueError:
        pass
    combobox.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(combobox)
    
    editar_button = tk.Button(labels_frame, text="Filtrar", command= lambda: filtrar())
    editar_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.SW)
    old_buttons.append(editar_button)

    def filtrar():
        try:
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/ingresses/"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pods = response.json()
            items = pods['items']
            services_names = []
            for service in items:
                if selected_option.get().strip() == "Todos":
                    pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
                    services_names.append(pre_string)
                elif service['metadata']['namespace'] == selected_option.get().strip():
                    pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
                    services_names.append(pre_string)
            show_in_list(services_names, listbox, tk)
            listbox.bind("<Double-Button-1>", on_double_click)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    name_label = tk.Label(labels_frame, text="Nome*:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)
    host_label = tk.Label(labels_frame, text="Host*:")
    host_label.grid(row=2, column=0, padx=5, pady=5)
    old_buttons.append(host_label)
    host_entry = tk.Entry(labels_frame)
    host_entry.grid(row=2, column=1, padx=5, pady=5)
    old_buttons.append(host_entry)
    
    service_name = tk.Label(labels_frame, text="Service Name:*")
    service_name.grid(row=3, column=0, padx=5, pady=5)
    old_buttons.append(service_name)
    service_names = get_service_names(ip_address_var, api_port_var, authorization)
    options2 = service_names
    selected_option2 = tk.StringVar()
    combobox3 = ttk.Combobox(labels_frame, textvariable=selected_option2, values=options2)
    try:
        combobox3.current(1)  # Set the pre-filled value
    except ValueError:
        pass
    combobox3.grid(row=3, column=1, padx=5, pady=5)
    old_buttons.append(combobox3)
    #service_name_entry = tk.Entry(labels_frame)
    #service_name_entry.grid(row=3, column=1, padx=5, pady=5)
    #old_buttons.append(service_name_entry)
    service_port_label = tk.Label(labels_frame, text="Service Port*:")
    service_port_label.grid(row=4, column=0, padx=5, pady=5)
    old_buttons.append(service_port_label)
    service_port_entry = tk.Entry(labels_frame)
    service_port_entry.grid(row=4, column=1, padx=5, pady=5)
    old_buttons.append(service_port_entry)

    metadata_label = tk.Label(labels_frame, text="metadata".upper(), font=("consolas", 12), fg='blue')
    metadata_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(metadata_label)
    labels_label = tk.Label(labels_frame, text="LABELS")
    labels_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(labels_label)
    environment_label = tk.Label(labels_frame, text="Environment:")
    environment_label.grid(row=3, column=2, padx=5, pady=5)
    old_buttons.append(environment_label)
    environment_entry = tk.Entry(labels_frame)
    environment_entry.grid(row=3, column=3, padx=5, pady=5)
    old_buttons.append(environment_entry)
    team_label = tk.Label(labels_frame, text="Team:")
    team_label.grid(row=4, column=2, padx=5, pady=5)
    old_buttons.append(team_label)
    team_entry = tk.Entry(labels_frame)
    team_entry.grid(row=4, column=3, padx=5, pady=5)
    old_buttons.append(team_entry)

    annotations_label = tk.Label(labels_frame, text="annotations".upper())
    annotations_label.grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(annotations_label)
    owner_label = tk.Label(labels_frame, text="Owner:")
    owner_label.grid(row=3, column=4, padx=5, pady=5)
    old_buttons.append(owner_label)
    owner_entry = tk.Entry(labels_frame)
    owner_entry.grid(row=3, column=5, padx=5, pady=5)
    old_buttons.append(owner_entry)
    purpose_label = tk.Label(labels_frame, text="Purpose:")
    purpose_label.grid(row=4, column=4, padx=5, pady=5)
    old_buttons.append(purpose_label)
    purpose_entry = tk.Entry(labels_frame)
    purpose_entry.grid(row=4, column=5, padx=5, pady=5)
    old_buttons.append(purpose_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command= lambda: criar_ingresses(ip_address_var, api_port_var, authorization, listbox, tk, parent, selected_option, name_entry, host_entry, selected_option2, service_port_entry, environment_entry, team_entry, owner_entry, purpose_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command= lambda: abrir_ingress(ip_address_var, api_port_var, authorization))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command= lambda: eliminar_ingresses(ip_address_var, api_port_var, authorization, listbox, tk, parent, get_ingress_names(ip_address_var, api_port_var, authorization)))
    old_buttons.append(new_buttons[2])

    def abrir_ingress(ip_address_var, api_port_var, authorization):
        index = listbox.curselection()
        if not index:
            messagebox.showerror("Erro","Não está selecionado nenhum Ingress!", parent=parent)
            return
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/namespaces/{namespace_value}/ingresses/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                space_data = response.json()
                host_valor = space_data['spec']['rules'][0]['host']
                webbrowser.open(f'https://{host_valor}')
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def on_double_click(event):
        index = listbox.curselection()
        if index:
            item = listbox.get(index)
            item = item.strip()
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/namespaces/{namespace_value}/ingresses/{name_value}"
                headers = {'Authorization': 'Bearer ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                space_data = response.json()
                
                nome_valor = space_data['metadata']['name']
                uid_valor = space_data['metadata']['uid']
                resource_ver_valor = space_data['metadata']['resourceVersion']
                data_criacao_valor = space_data['metadata']['creationTimestamp']
                namespace_valor = space_data['metadata']['namespace']

                if 'labels' in space_data['metadata']: 
                    labels = space_data['metadata']['labels']
                
                annotations = 0
                if 'annotations' in space_data['metadata']:
                    annotations = space_data['metadata']['annotations']

                managed_fields = space_data['metadata']['managedFields']

                ingress_call_name_valor =  space_data['spec']['ingressClassName']
                host_valor = space_data['spec']['rules'][0]['host']
                path_valor = space_data['spec']['rules'][0]['http']['paths'][0]['path']
                path_type_valor = space_data['spec']['rules'][0]['http']['paths'][0]['pathType']
                service_name_valor = path_type_valor = space_data['spec']['rules'][0]['http']['paths'][0]['backend']['service']['name']
                service_name_port = path_type_valor = space_data['spec']['rules'][0]['http']['paths'][0]['backend']['service']['port']['number']

                status = space_data['status']
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
            pre_new_window = Toplevel(parent)
            pre_new_window.title(name_value)
            pre_new_window.geometry("800x600")
            
            #top_frame = tk.Frame(pre_new_window)
            #top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            bot_frame = tk.Frame(pre_new_window)
            bot_frame.pack(side=tk.BOTTOM , fill=tk.X)

            canvas = tk.Canvas(pre_new_window)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and attach it to the canvas
            scrollbar = tk.Scrollbar(pre_new_window, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the contents
            new_window = tk.Frame(canvas)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)
            
            metadata_label = tk.Label(new_window, text=f"Metadata", font=("consolas", 14, "bold"))
            metadata_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
            name_label = tk.Label(new_window, text=f"Nome: {nome_valor}")
            name_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
            uid_label = tk.Label(new_window, text=f"UID: {uid_valor}")
            uid_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
            resource_ver_label = tk.Label(new_window, text=f"Resource Version: {resource_ver_valor}")
            resource_ver_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
            creation_time_label = tk.Label(new_window, text=f"Data de criação: {data_criacao_valor}")
            creation_time_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
            namespcace_label = tk.Label(new_window, text=f"Namespace: {namespace_valor}")
            namespcace_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            
            row = 4
            
            if 'labels' in space_data['metadata']:
                labels_label = tk.Label(new_window, text=f"Labels", font=("consolas", 14, "bold"))
                labels_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                for item in labels:
                    tk.Label(new_window, text=f"{item}: {labels[item]}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    row += 1
            
            if annotations:
                row+=1
                annotation_label = tk.Label(new_window, text=f"Anotações", font=("consolas", 14, "bold"))
                annotation_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row+=1
                for item in annotations:
                    last_config_label = tk.Label(new_window, text=f"{item}: {annotations[item]}")
                    last_config_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W, columnspan=100)
                    #last_config_label2 = tk.Label(new_window, text=f"{annotations[item]}")
                    #last_config_label2.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
                    row+=1

            managed_fields_label = tk.Label(new_window, text=f"Managed Fields", font=("consolas", 14, "bold"))
            managed_fields_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in managed_fields:
                tk.Label(new_window, text=f"{item['manager']}", font=("consolas", 12), fg='blue').grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Operação: {item['operation']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Versão da API: {item['apiVersion']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
                tk.Label(new_window, text=f"Data e Hora: {item['time']}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1
            
            spec_label = tk.Label(new_window, text=f"Spec", font=("consolas", 14, "bold"))
            spec_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            ingress_class_label = tk.Label(new_window, text=f"Ingress Class Name: {ingress_call_name_valor}")
            ingress_class_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            host_label = tk.Label(new_window, text=f"Host: {host_valor}")
            host_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            path_label = tk.Label(new_window, text=f"Path: {path_valor}")
            path_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            path_type_label = tk.Label(new_window, text=f"Path Type: {path_type_valor}")
            path_type_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            service_name_label = tk.Label(new_window, text=f"Service Name: {service_name_valor}")
            service_name_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            service_port_label = tk.Label(new_window, text=f"Service Port: {service_name_port}")
            service_port_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1

            status_label = tk.Label(new_window, text=f"Status", font=("consolas", 14, "bold"))
            status_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            load_label = tk.Label(new_window, text=f"Load Balancer Ingress", font=("consolas", 12), fg='blue')
            load_label.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            row += 1
            for item in status['loadBalancer']['ingress']:
                tk.Label(new_window, text=f"{item}").grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                row += 1

            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            destroy_button = tk.Button(bot_frame, text="OK", command=pre_new_window.destroy)
            destroy_button.pack(padx=5, pady=5, expand=True)

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/ingresses"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        services = response.json()
        items = services['items']
        services_names = []
        for service in items:
            pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
            services_names.append(pre_string)
        show_in_list(services_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_ingresses(ip_address_var, api_port_var, authorization, listbox, tk, parent, selected_option, name_entry, host_entry, service_name_entry, service_port_entry, environment_entry, team_entry, owner_entry, purpose_entry):
    namespace_valor = selected_option.get()
    if namespace_valor == "Todos":
        messagebox.showerror("Erro","Por vafor selecione um namespace!", parent=parent)
        return

    nome_valor = name_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    host_valor = host_entry.get().replace(" ", "")
    if not host_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Host, a caixa de texto encontra-se vazia!", parent=parent)
        return

    service_name_valor = service_name_entry.get()
    if not service_name_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome do Serviço, a caixa de texto encontra-se vazia!", parent=parent)
        return

    servce_port_valor = service_port_entry.get().replace(" ", "")
    if not servce_port_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Porto do Serviço, a caixa de texto encontra-se vazia!", parent=parent)
        return

    environment_valor = environment_entry.get().replace(" ", "")
    team_valor = team_entry.get().replace(" ", "")
    owner_valor = owner_entry.get().replace(" ", "")
    purpose_valor = purpose_entry.get().replace(" ", "")

    try:
        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/namespaces/{namespace_valor}/ingresses"
        headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
        data = {
                "apiVersion": "networking.k8s.io/v1",
                "kind": "Ingress",
                "metadata": {
                    "name": nome_valor,
                    "namespace": namespace_valor,
                    "labels": {
                    },
                    "annotations": {
                        "nginx.ingress.kubernetes.io/rewrite-target": "/"
                    }
                },
                "spec": {
                    "rules": [
                        {
                            "host": host_valor,
                            "http": {
                                "paths": [
                                    {
                                        "path": "/",
                                        "pathType": "Prefix",
                                        "backend": {
                                            "service": {
                                                "name": service_name_valor,
                                                "port": {
                                                    "number": int(servce_port_valor)
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        if environment_valor:
            data['metadata']['labels']['environment'] = environment_valor
        if team_valor:
            data['metadata']['labels']['team'] = team_valor
        if owner_valor:
            data['metadata']['annotations']['owner'] = owner_valor
        if purpose_valor:
            data['metadata']['annotations']['purpose'] = purpose_valor
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        response.raise_for_status()
        if response.status_code == 201:
            messagebox.showinfo("Ingress Criado", "Ingress criado com sucesso", parent=parent )
            os_name = platform.system()
    
            if os_name == "Windows":
                hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
            elif os_name == "Linux":
                hosts_path = "/etc/hosts"
            
            try:
                with open(hosts_path, 'a') as hosts_file:
                    hosts_file.write(f"{ip_address_var.get()} {host_valor}" + "\n")
                print(f"Successfully appended to {hosts_path}")
            except PermissionError:
                print(f"Permission denied: You need to run this script as an administrator/root to modify {hosts_path}")
            except Exception as e:
                print(f"An error occurred: {e}")

        url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/ingresses"
        headers = {'Authorization': 'Bearer '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        services = response.json()
        items = services['items']
        services_names = []
        for service in items:
            pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
            services_names.append(pre_string)
        show_in_list(services_names, listbox, tk)
        name_entry.delete(0, tk.END)
        host_entry.delete(0, tk.END)
        service_port_entry.delete(0, tk.END)
        environment_entry.delete(0, tk.END)
        team_entry.delete(0, tk.END)
        owner_entry.delete(0, tk.END)
        purpose_entry.delete(0, tk.END)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_ingresses(ip_address_var, api_port_var, authorization, listbox, tk, parent, ingress_names):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Ingress!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            name_value = item.split("Nome:")[1].split(";")[0].strip()
            namespace_value = item.split("Namespace:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Ingress {name_value}",f"Tem a certeza que pretende eliminar o Ingress {name_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/namespaces/{namespace_value}/ingresses/{name_value}"
            headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
            response = requests.delete(url, headers=headers, verify=False)
            response.raise_for_status()
            while(1):
                if len(get_ingress_names(ip_address_var, api_port_var, authorization)) != len(ingress_names):
                       break
            messagebox.showinfo("Sucesso", "Ingress eliminado com sucesso", parent=parent)
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/ingresses"
            url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/ingresses"
            headers = {'Authorization': 'Bearer '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            services = response.json()
            items = services['items']
            services_names = []
            for service in items:
                pre_string = f"Nome: {service['metadata']['name']}; Namespace: {service['metadata']['namespace']}; Data de criação: {service['metadata']['creationTimestamp']}; Versão do recurso: {service['metadata']['resourceVersion']}"
                services_names.append(pre_string)
            show_in_list(services_names, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def cria_wizard(ip_address_var, api_port_var, authorization, listbox, tk, parent):
    def traduzir_fala():
        assistente = sr.Recognizer()
        language = "pt-PT"

        with sr.Microphone() as source:
            print("A espera de comandos...")
            assistente.adjust_for_ambient_noise(source)
            audio = assistente.listen(source)
        
        try:
            comando = assistente.recognize_google(audio_data=audio,language=language)
            print("Tu disseste: ",comando)
            return comando.lower()
        except sr.UnknownValueError:
            print("Não percebi o que foi dito.Tenta outra vez.")
            return "-1"
        except sr.RequestError:
            print("Não foi possivel acessar a API Google Speech Recognition API")
            return "-2"

    def falar_audio(nome_audio):
        mixer.init()
        if platform.system == "Windows":
            mixer.music.load(os.getcwd() + "\\" + nome_audio)
        else:
            mixer.music.load(os.getcwd() + "/" + nome_audio)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)

    def criar_mensagem(nome_ficheiro,mensagem):
        language = "pt-PT"
        #texto = f"A api da google não se encontra disponível, por favor volte a tentar mais tarde."
        myobj = gTTS(text=mensagem, lang=language, slow=False)
        myobj.save(f"{nome_ficheiro}.mp3")

    def validacoes_assitente(mensagem,estado_erro,estado_nao_erro):
        if mensagem == "-1":
            criar_mensagem("nao-perceber-mensagem","Não foi possível entender a mensagem, por favor volte a repetir !")
            falar_audio(r"nao-perceber-mensagem.mp3")
            return estado_erro
        elif mensagem == "-2":
            criar_mensagem("api-nao-disponivel","A API da google não se encontra dísponivel, por favor volte a tentar mais tarde !")
            falar_audio(r"api-nao-disponivel.mp3")
            return estado_erro
        else:
            return estado_nao_erro
        
    def wizard_function():
        print(vars[0]['estagio'])
        if vars[0]['estagio'] == 0:
            namespace_valor.set(selected_option.get())
            if namespace_valor.get() not in get_namspace_names(ip_address_var, api_port_var, authorization):
                try:
                    url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces"
                    headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
                    data = {
                        "apiVersion": "v1",
                        "kind": "Namespace",
                        "metadata": {
                            "name": namespace_valor.get(),
                        }
                    }
                    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
                    pre_new_window.destroy()
            
            for button in old_buttons:
                button.grid_forget()
                del button

            deploy_label = tk.Label(top_frame, text=f"Deployment", font=("consolas", 14, "bold"))
            deploy_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            old_buttons.append(deploy_label)
            name_label = tk.Label(top_frame, text="Nome*:")
            name_label.grid(row=1, column=0, padx=5, pady=5)
            old_buttons.append(name_label)
            
            name_entry.grid(row=1, column=1, padx=5, pady=5)
            old_buttons.append(name_entry)
            replicas_label = tk.Label(top_frame, text="Replicas*:")
            replicas_label.grid(row=2, column=0, padx=5, pady=5)
            old_buttons.append(replicas_label)
            
            replicas_entry.grid(row=2, column=1, padx=5, pady=5)
            old_buttons.append(replicas_entry)
            match_label = tk.Label(top_frame, text="App Label*:")
            match_label.grid(row=3, column=0, padx=5, pady=5)
            old_buttons.append(match_label)
            
            match_entry.grid(row=3, column=1, padx=5, pady=5)
            old_buttons.append(match_entry)
            containers_label = tk.Label(top_frame, text="Container".upper())
            containers_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
            old_buttons.append(containers_label)
            nome2_label = tk.Label(top_frame, text="Nome*:")
            nome2_label.grid(row=5, column=0, padx=5, pady=5)
            old_buttons.append(nome2_label)
            
            nome2_entry.grid(row=5, column=1, padx=5, pady=5)
            old_buttons.append(nome2_entry)
            image_label = tk.Label(top_frame, text="Imagem*:")
            image_label.grid(row=6, column=0, padx=5, pady=5)
            old_buttons.append(image_label)
            
            image_names = ['nginx:latest', "httpd:latest", 'caddy:latest', 'mysql:latest', 'mysql:latest', 'postgres:latest', 'mongo:latest', 'redis:latest', 'mariadb:latest', 'python:latest', 'node:latest', 'ruby:latest', 'golang:latest', 'php:latest', 'busybox:latest', 'alpine:latest', 'ubuntu:latest', 'centos:latest', 'debian:latest', 'jenkins/jenkins:latest', 'gitlab/gitlab-ce:latest', 'sonarqube:latest', 'prom/prometheus:latest', 'grafana/grafana:latest', 'elasticsearch:latest', 'kibana:latest', 'varnish:latest', 'rabbitmq:latest', 'wurstmeister/kafka:latest', 'portainer/portainer-ce:latest']

            options2 = image_names
            
            combobox3 = ttk.Combobox(top_frame, textvariable=selected_option2, values=options2)
            try:
                combobox3.current(1)  # Set the pre-filled value
            except ValueError:
                pass
            combobox3.grid(row=6, column=1, padx=5, pady=5)
            
            old_buttons.append(combobox3)
            ports_label = tk.Label(top_frame, text="Porto*:")
            ports_label.grid(row=7, column=0, padx=5, pady=5)
            old_buttons.append(ports_label)
            
            ports_entry.grid(row=7, column=1, padx=5, pady=5)
            old_buttons.append(ports_entry)
            
            vars[0]['estagio'] += 1
            increment()
            if vars[0]['assistente']:
                assistente_voz()
        elif vars[0]['estagio'] == 1:
            print("cheguei aqui")
            nome_valor.set(name_entry.get().replace(" ", ""))
            replicas_valor.set(replicas_entry.get().replace(" ", ""))
            match_valor.set(match_entry.get().replace(" ", ""))
            nome2_valor.set(nome2_entry.get().replace(" ", ""))
            imagem_valor.set(selected_option2.get().replace(" ", ""))
            porto_valor.set(ports_entry.get().replace(" ", ""))

            if not nome_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
                return

            if not replicas_valor.get():
                messagebox.showerror("Erro","Não foi dada nenhuma Replica, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            if not match_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhuma Label par a App, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            if not nome2_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Nome ao Container, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            if not imagem_valor.get():
                messagebox.showerror("Erro","Não foi dada nenhuma Imagem, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            if not porto_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Porto, a caixa de texto encontra-se vazia!", parent=parent)
                return

            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/apps/v1/namespaces/{namespace_valor.get()}/deployments"
                headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
                data = {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "metadata": {
                        "name": nome_valor.get(),
                        "namespace": namespace_valor.get()
                    },
                    "spec": {
                        "replicas": int(replicas_valor.get()),
                        "selector": {
                            "matchLabels": {
                                "app": match_valor.get()
                            }
                        },
                        "template": {
                            "metadata": {
                                "labels": {
                                    "app": match_valor.get()
                                }
                            },
                            "spec": {
                                "containers": [
                                    {
                                        "name": nome2_valor.get(),
                                        "image": imagem_valor.get(),
                                        "ports": [
                                            {
                                                "containerPort": int(porto_valor.get())
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
                response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
                pre_new_window.destroy()

            for button in old_buttons:
                button.grid_forget()
                del button
            
            service_label = tk.Label(top_frame, text=f"Service", font=("consolas", 14, "bold"))
            service_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            old_buttons.append(service_label)
            name3_label = tk.Label(top_frame, text="Nome*:")
            name3_label.grid(row=1, column=0, padx=5, pady=5)
            old_buttons.append(name3_label)
            nome3_entry.grid(row=1, column=1, padx=5, pady=5)
            old_buttons.append(nome3_entry)
            
            protocolo_label = tk.Label(top_frame, text="Protocolo:")
            protocolo_label.grid(row=2, column=0, padx=5, pady=5)
            old_buttons.append(protocolo_label)
            options3 = ["TCP", "UDP", "SCTP"]
            combobox4 = ttk.Combobox(top_frame, textvariable=selected_option3, values=options3)
            try:
                combobox4.current(0)
            except ValueError:
                pass
            combobox4.grid(row=2, column=1, padx=5, pady=5)
            old_buttons.append(combobox4)

            port_label = tk.Label(top_frame, text="Port*:")
            port_label.grid(row=3, column=0, padx=5, pady=5)
            old_buttons.append(port_label)
            target_port_entry.grid(row=3, column=1, padx=5, pady=5)
            old_buttons.append(target_port_entry)
            
            vars[0]['estagio'] += 1
            increment()
            if vars[0]['assistente']:
                assistente_voz()
        elif vars[0]['estagio'] == 2:
            nome3_valor.set(nome3_entry.get().replace(" ", ""))
            target_port_valor.set(target_port_entry.get().replace(" ", ""))
            protocolo_valor.set(selected_option3.get().replace(" ", ""))

            if not nome3_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
                return

            if not target_port_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Target Port, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            if not protocolo_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Protocolo, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/api/v1/namespaces/{namespace_valor.get()}/services"
                headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
                data = {
                    "apiVersion": "v1",
                    "kind": "Service",
                    "metadata": {
                        "name": nome3_valor.get(),
                        "namespace": namespace_valor.get()
                    },
                    "spec": {
                        "selector": {
                            "app": match_valor.get()
                        },
                        "ports": [
                            {
                                "protocol": protocolo_valor.get(),
                                "port": int(target_port_valor.get()),
                                "targetPort": int(porto_valor.get())
                            }
                        ],
                        "type": "NodePort"
                    }
                }
                response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
                pre_new_window.destroy()

            for button in old_buttons:
                button.grid_forget()
                del button
            
            ingress_label = tk.Label(top_frame, text=f"Ingress", font=("consolas", 14, "bold"))
            ingress_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            old_buttons.append(ingress_label)
            name4_label = tk.Label(top_frame, text="Nome*:")
            name4_label.grid(row=1, column=0, padx=5, pady=5)
            old_buttons.append(name4_label)
            nome4_entry.grid(row=1, column=1, padx=5, pady=5)
            old_buttons.append(nome4_entry)
            
            host_label = tk.Label(top_frame, text="Host*:")
            host_label.grid(row=2, column=0, padx=5, pady=5)
            old_buttons.append(host_label)
            host_entry.grid(row=2, column=1, padx=5, pady=5)
            old_buttons.append(host_entry)

            vars[0]['estagio'] += 1
            increment()
            if vars[0]['assistente']:
                assistente_voz()
        elif vars[0]['estagio'] == 3:
            nome4_valor.set(nome4_entry.get().replace(" ", ""))
            host_valor.set(host_entry.get().replace(" ", ""))

            if not nome4_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            if not host_valor.get():
                messagebox.showerror("Erro","Não foi dado nenhum Host, a caixa de texto encontra-se vazia!", parent=parent)
                return
            
            try:
                url = f"https://{ip_address_var.get()}:{api_port_var.get()}/apis/networking.k8s.io/v1/namespaces/{namespace_valor.get()}/ingresses"
                headers = {'Authorization': 'Bearer '+ authorization, 'Content-Type': 'application/json'}
                data = {
                    "apiVersion": "networking.k8s.io/v1",
                    "kind": "Ingress",
                    "metadata": {
                        "name": nome4_valor.get(),
                        "namespace": namespace_valor.get(),
                        "annotations": {
                            "nginx.ingress.kubernetes.io/rewrite-target": "/"
                        }
                    },
                    "spec": {
                        "rules": [
                            {
                                "host": host_valor.get(),
                                "http": {
                                    "paths": [
                                        {
                                            "path": "/",
                                            "pathType": "Prefix",
                                            "backend": {
                                                "service": {
                                                    "name": nome3_valor.get(),
                                                    "port": {
                                                        "number": int(target_port_valor.get())
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
                response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
                pre_new_window.destroy()

            for button in old_buttons:
                button.grid_forget()
                del button
            
            os_name = platform.system()
    
            if os_name == "Windows":
                hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
            elif os_name == "Linux":
                hosts_path = "/etc/hosts"
            
            try:
                with open(hosts_path, 'a') as hosts_file:
                    hosts_file.write(f"{ip_address_var.get()} {host_valor.get()}" + "\n")
                print(f"Successfully appended to {hosts_path}")
            except PermissionError:
                print(f"Permission denied: You need to run this script as an administrator/root to modify {hosts_path}")
            except Exception as e:
                print(f"An error occurred: {e}")
            
            next_button.config(text="Close")

            sucesso_label = tk.Label(top_frame, text=f"Sucesso", font=("consolas", 14, "bold"))
            sucesso_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            old_buttons.append(sucesso_label)
            sucess_label = tk.Label(top_frame, text="Deployment, Service e Ingress Criado com sucesso!")
            sucess_label.grid(row=1, column=0, padx=5, pady=5)
            old_buttons.append(sucess_label)
            abrir_button = tk.Button(top_frame, text="Abrir", command= lambda: abrir_function())
            abrir_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

            def abrir_function():
                webbrowser.open(f'https://{host_valor.get()}')

            vars[0]['estagio'] += 1
            progressBar['value'] = 100
            if vars[0]['assistente']:
                assistente_voz()
        elif vars[0]['estagio'] == 4:
            pre_new_window.destroy()

    def increment():
        progressBar.step(25)

    old_buttons = []
    vars = [{'estagio' : 0, 'assistente' : 0}]

    pre_new_window = Toplevel(parent)
    pre_new_window.title("Wizard de configuração, Ingress")
    pre_new_window.geometry("640x480")
    parent=pre_new_window

    top_frame = tk.Frame(pre_new_window)
    top_frame.pack(side=tk.TOP , fill=tk.BOTH, expand=True)
    progress_frame = tk.Frame(pre_new_window)
    progress_frame.pack(side=tk.TOP , fill=tk.X)
    bot_frame = tk.Frame(pre_new_window)
    bot_frame.pack(side=tk.BOTTOM , fill=tk.X)
    
    assistente_label = tk.Label(top_frame, text=f"Assistente de Configuração", font=("consolas", 14, "bold"))
    assistente_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
    old_buttons.append(assistente_label)
    assistente_button = tk.Button(top_frame, text="Ativar", command= lambda: assistente_voz())
    assistente_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(assistente_button)

    namespaces_label = tk.Label(top_frame, text=f"Namespace", font=("consolas", 14, "bold"))
    namespaces_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    old_buttons.append(namespaces_label)
    namespace_names = get_namspace_names(ip_address_var, api_port_var, authorization)
    namespace_label = tk.Label(top_frame, text="Namespace:")
    namespace_label.grid(row=3, column=0, padx=5, pady=5)
    old_buttons.append(namespace_label)
    options = namespace_names
    selected_option = tk.StringVar()
    combobox = ttk.Combobox(top_frame, textvariable=selected_option, values=options)
    try:
        combobox.current(0)  # Set the pre-filled value
    except ValueError:
        pass
    combobox.grid(row=3, column=1, padx=5, pady=5)
    old_buttons.append(combobox)
    
    progressBar= ttk.Progressbar(progress_frame, mode='determinate')
    progressBar.pack(padx = 10, pady = 10, expand=True, fill=tk.X)

    next_button = tk.Button(bot_frame, text="Next", command= lambda: wizard_function())
    next_button.pack(padx=5, pady=5, side=tk.RIGHT)
    destroy_button = tk.Button(bot_frame, text="Cancel", command=pre_new_window.destroy)
    destroy_button.pack(padx=5, pady=5, side=tk.RIGHT)

    def assistente_voz():
        vars[0]['assistente'] = 1
        if vars[0]['estagio'] == 0:
            #===== variavel para guardar o estado em que se encontra o assistente
            estado = 0
            #===== variavel para as mensagens
            mensagem,resposta = "",""
            #===== variavel para guardar o nome do namespace, vai ser returnada no final
            nome_namespace = ""
            while(estado != 10):
                match estado:
                    case 0:
                        criar_mensagem("pergunta-nome-namespace",f"Por favor, indique o nome do namespace que quer usar ?")
                        falar_audio(r"pergunta-nome-namespace.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,0,1)

                    #=============================================== 2 -> DE ACORDO COM AS RESPOSTAS DECIDE O QUE VAI FAZER ===============================================#
                    case 1:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 10
                            nome_namespace = mensagem
            selected_option.set(nome_namespace.replace(" ", ""))
            wizard_function()
        elif vars[0]['estagio'] == 1:
            #===== variaevis para valores numéricos
            estado,replicas_deployment,porto_container = 0,0,0
            #===== variaveis para valores string
            mensagem,resposta = "",""
            nome_deployment,app_label_deployment = "",""
            nome_container,imagem_container,aux_imagem_container = "","",""
            #===== Ciclo while que faz com que o assistente contuinue até chegar ao final
            #===== 18 -> Estado em que já está tudo feito
            while(estado != 13): 
                match estado:
                    case 0:
                        criar_mensagem("pergunta-nome-deployment","Por favor, indique o nome para o deployment que pretende criar ?")
                        falar_audio(r"pergunta-nome-deployment.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,0,1)
                    
                    case 1:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 3
                            nome_deployment = mensagem
                    case 3:
                        criar_mensagem("pergunta-replicas-deployment",f"Por favor, indique o numero de réplicas que pretende criar ?")
                        falar_audio(r"pergunta-replicas-deployment.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,3,5)
                        if estado == 5:
                            if mensagem == "cancelar":
                                pre_new_window.destroy()
                                print(f"Cancelei")
                                return
                            try:
                                replicas_deployment = int(mensagem)
                                if replicas_deployment <= 0:
                                    criar_mensagem("aux-replicas-number-minor-zero",f"O numero de réplicas atribuido deve ser maior que zero !")
                                    falar_audio(r"aux-replicas-number-minor-zero.mp3")
                                    estado = 3
                            except ValueError:
                                criar_mensagem("aux-replicas-not-number",f"A mensagem que falou não foi possível converter em numero !")
                                falar_audio(r"aux-replicas-not-number.mp3")
                                estado = 3

                            replicas_deployment = mensagem                    
                    case 5:
                        criar_mensagem("pergunta-app-label-deployment",f"Por favor, indique um nome para o app label ?")
                        falar_audio(r"pergunta-app-label-deployment.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,5,6)
                    case 6:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 7
                            app_label_deployment = mensagem
                    case 7:
                        criar_mensagem("pergunta-container-nome",f"Indique o nome que pretende atribuir ao container !")
                        falar_audio(r"pergunta-container-nome.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,7,8)
                    case 8:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 9
                            nome_container = mensagem
                    case 9:
                        criar_mensagem("pergunta-container-imagem",f"Indique qual imagem do container que pretende usar ? Diga o numero 20 para imagem NGINX, ou o numero 30 para imagem Apache")
                        falar_audio(r"pergunta-container-imagem.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,9,11)
                        if estado == 11:
                            if mensagem == "cancelar":
                                pre_new_window.destroy()
                                print(f"Cancelei")
                                return
                            try:
                                aux_imagem_container = int(mensagem)
                                if aux_imagem_container == 20:
                                    imagem_container = "nginx:latest"
                                elif aux_imagem_container == 30:
                                    imagem_container = "httpd:latest"
                                else:
                                    criar_mensagem("aux-container-image-not-20-or-30",f"O numero dito não foi 20 nem 30 !")
                                    falar_audio(r"aux-container-image-not-20-or-30.mp3")
                                    estado = 9
                            except ValueError:
                                criar_mensagem("aux-container-image-not-value",f"A mensagem que falou não foi possível converter para numero !")
                                falar_audio(r"aux-container-image-not-value.mp3")
                                estado = 9

                            aux_imagem_container = mensagem
                    case 11:
                        criar_mensagem("pergunta-container-porto",f"Indique qual o porto que pretende usar para o container ?")
                        falar_audio(r"pergunta-container-porto.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,11,13)
                        if estado == 13:
                            if mensagem == "cancelar":
                                pre_new_window.destroy()
                                print(f"Cancelei")
                                return
                            try:
                                porto_container = int(mensagem)
                                if porto_container <= 0 or porto_container >= 65536:
                                    criar_mensagem("aux-container-image-not-range",f"O numero atribuido para o porto não se encontra dentro do intervalo de 1 a 65535 !")
                                    falar_audio(r"aux-container-image-not-range.mp3")
                                    estado = 11
                            except ValueError:
                                criar_mensagem("aux-container-porto-not-value",f"A mensagem que falou não foi possível converter para numero !")
                                falar_audio(r"aux-container-porto-not-value.mp3")
                                estado = 11
                            
                            porto_container = mensagem

            name_entry.insert(0, nome_deployment.replace(" ", "").lower())
            replicas_entry.insert(0, replicas_deployment.replace(" ", ""))
            match_entry.insert(0, app_label_deployment.replace(" ", "").lower())
            nome2_entry.insert(0, nome_container.replace(" ", "").lower())
            selected_option2.set(imagem_container.replace(" ", "").lower())
            ports_entry.insert(0, porto_container)
            wizard_function()
        elif vars[0]['estagio'] == 2:
            #===== variavel para guardar o estado em que se encontra o assistente
            estado = 0
            #===== variavel para as mensagens
            mensagem,resposta = "",""
            #===== variavel para guardar o nome do service e porto, vai ser returnada no final
            nome_service = ""
            porto_service = 0

            while(estado != 4):
                match estado:
                    #=============================================== O -> INCIO, FAZ A PERGUNTA INCIAL PARA O USER INDICAR O NOME PARA O NAMESPACE ===============================================#
                    case 0:
                        criar_mensagem("pergunta-nome-service",f"Por favor, indique o nome do service que quer criar ?")
                        falar_audio(r"pergunta-nome-service.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,0,1)
                    case 1:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 2
                            nome_service = mensagem
                    case 2:
                        criar_mensagem("pergunta-service-porto",f"Indique qual o porto que pretende usar para o service ?")
                        falar_audio(r"pergunta-service-porto.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,2,4)
                        if estado == 4:
                            if mensagem == "cancelar":
                                pre_new_window.destroy()
                                print(f"Cancelei")
                                return
                            try:
                                porto_service = int(mensagem)
                                if porto_service <= 0 or porto_service >= 65536:
                                    criar_mensagem("aux-service-port-not-range",f"O numero atribuido para o porto não se encontra dentro do intervalo de 1 a 65535 !")
                                    falar_audio(r"aux-service-port-not-range.mp3")
                                    estado = 2
                            except ValueError:
                                criar_mensagem("aux-service-port-not-value",f"A mensagem que falou não foi possível converter para numero !")
                                falar_audio(r"aux-service-port-not-value.mp3")
                                estado = 2

                        porto_service = mensagem

            print(f"{nome_service} ; {porto_service}")

            nome3_entry.insert(0, nome_service.replace(" ", "").lower())
            #selected_option3.set(tipo_porto.replace(" ", ""))
            target_port_entry.insert(0, porto_service)
            wizard_function()
        elif vars[0]['estagio'] == 3:
            #===== variavel para guardar o estado em que se encontra o assistente
            estado = 0
            #===== variavel para as mensagens
            mensagem,resposta = "",""
            #===== variavel para guardar o nome do ingress e o host, vai ser returnada no final
            nome_ingress,host_ingress = "",""
            
            while(estado != 4):
                match estado:
                    #=============================================== O -> INCIO, FAZ A PERGUNTA INCIAL PARA O USER INDICAR O NOME PARA O INGRESS ===============================================#
                    case 0:
                        criar_mensagem("pergunta-nome-ingress",f"Por favor, indique o nome do ingress que quer criar ?")
                        falar_audio(r"pergunta-nome-ingress.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,0,1)
                    case 1:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 2
                            nome_ingress = mensagem
                    case 2:
                        criar_mensagem("pergunta-host-ingress",f"Por favor, indique o host que pretende atribuir para este ingress ?")
                        falar_audio(r"pergunta-host-ingress.mp3")
                        mensagem = traduzir_fala()
                        estado = validacoes_assitente(mensagem,2,3)
                    case 3:
                        if mensagem == "cancelar":
                            pre_new_window.destroy()
                            print(f"Cancelei")
                            return
                        else:
                            estado = 4
                            host_ingress = mensagem + ".comm"
            print(f"{nome_ingress} ; {host_ingress}")
            nome4_entry.insert(0, nome_ingress.replace(" ", "").lower())
            host_entry.insert(0, host_ingress.replace(" ", "").lower())
            wizard_function()

    namespace_valor = tk.StringVar()
    name_entry = tk.Entry(top_frame)
    nome_valor = tk.StringVar()
    replicas_entry = tk.Entry(top_frame)
    replicas_valor = tk.StringVar()
    match_entry = tk.Entry(top_frame)
    match_valor = tk.StringVar()
    nome2_entry = tk.Entry(top_frame)
    nome2_valor = tk.StringVar()
    selected_option2 = tk.StringVar()
    imagem_valor = tk.StringVar()
    ports_entry = tk.Entry(top_frame)
    porto_valor = tk.StringVar()
    nome3_entry = tk.Entry(top_frame)
    nome3_valor = tk.StringVar()
    target_port_entry = tk.Entry(top_frame)
    target_port_valor = tk.StringVar()
    selected_option3 = tk.StringVar()
    protocolo_valor = tk.StringVar()
    nome4_entry = tk.Entry(top_frame)
    nome4_valor = tk.StringVar()
    host_entry = tk.Entry(top_frame)
    host_valor = tk.StringVar()
