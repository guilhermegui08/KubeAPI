import api_requests
import tkinter as tk
from tkinter import ttk
import base64
import os.path
import csv
from tkinter import messagebox
import ssh2.session
import socket
from tkinter import scrolledtext
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import networkx as nx

canvas2 = 0

def close_browser(driver):
    input("Press Enter to close the browser...")
    """
    Close the browser.
    """
    driver.quit()
    print("Browser closed.")

def string_para_base64(string):
    string = string.encode('utf-8')
    escrita = base64.b64encode(string)
    return escrita.decode('utf-8')

def base64_para_string(string):
    string = string.encode('utf-8')
    escrita = base64.b64decode(string)
    return escrita.decode('utf-8')

def save_credentials(ip_address_var, username_var, password_var, api_port_var, ssh_port_var, listbox):
    ip_address = ip_address_var.get()
    username = username_var.get()
    password = password_var.get()
    password = string_para_base64(password)
    api_port = api_port_var.get()
    ssh_port = ssh_port_var.get() 
    # Open the CSV file in append mode with newline=''
    if not os.path.exists("credentials.csv"):
        # If the file doesn't exist, create it and save the new credentials
        with open("credentials.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip_address, username, password, api_port, ssh_port])
        #print("Credentials saved successfully!")
        return
    
    # Check if the credentials already exist
    with open("credentials.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == ip_address and row[1] == username and row[2] == password and row[3] == api_port and row[4] == ssh_port:
                return
        
    # If credentials don't exist, append them to the file
    with open("credentials.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip_address, username, password, api_port, ssh_port])
    #print("Credentials saved successfully!")
    
    load_credentials(ip_address, username, password_var, api_port_var, ssh_port_var, listbox)

def load_credentials(ip_address_var, username_var, password_var, api_port_var, ssh_port_var, listbox):
    # Clear the existing items in the listbox
    listbox.delete(0, tk.END)
    
    # Check if credentials file exists
    if not os.path.exists("credentials.csv"):
        return  # Exit if the file doesn't exist
    
    # Open the CSV file for reading
    with open("credentials.csv", "r") as file:
        reader = csv.reader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            ip_address_var, username_var, password_var, api_port_var, ssh_port_var = row  # Password is not used for listbox
            listbox.insert(tk.END, f"IP= {ip_address_var}, Username= {username_var}, Password= {password_var}, API PORT= {api_port_var}, SSH PORT= {ssh_port_var}")

def login(ip_address_var, username_var, password_var, api_port_var, ssh_port_var, root, listbox):
    authorization = 0 
    ssh_host = ip_address_var.get()
    ssh_port = int(ssh_port_var.get())
    ssh_username = username_var.get()
    ssh_password = password_var.get()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ssh_host, ssh_port))
    session = ssh2.session.Session()

    command = f"echo {ssh_password} | sudo -S kubectl -n kube-system  create token admin-user"

    try:
        session.handshake(sock)
        session.userauth_password(username=ssh_username, password=ssh_password)
        channel = session.open_session()
        channel.execute(command)
        size, data = channel.read()
        authorization = data.decode().strip()

    finally:
        if 'channel' in locals():
            channel.close()
        session.disconnect()
        sock.close()

    if authorization == 0:
        return

    estado_pedido = api_requests.get_api(ip_address_var, api_port_var, authorization)

    if estado_pedido == 200:
        save_credentials(ip_address_var, username_var, password_var, api_port_var, ssh_port_var, listbox)
        cria_user_app(ip_address_var, username_var, authorization, password_var, api_port_var, ssh_port_var, root)

def cria_user_app(ip_address_var_temp, username_var_temp, authorization_temp, password_var_temp, api_port_var_temp, ssh_port_var_temp, root):
    #Função que vai buscar as estatisticas do router de 1 em 1 sgundo
    def update_labels():
        stats = api_requests.get_node_stats_perodically(ip_address_var, api_port_var, authorization)
       
        names = stats[0]
        timestamps = stats[1]
        cpus = stats[2]
        memorys = stats[3]

        for i in range(0, len(names)):
            if i == 0:
                time_label.config(text=f"Data e Hora: {timestamps[i]}")
                cluster_labels[i].config(text=f"{names[i]}: CPU-{cpus[i]} MEMORY-{memorys[i]}")
            else:
                cluster_labels[i].config(text=f"{names[i]}: CPU-{cpus[i]} MEMORY-{memorys[i]}")
    
        user_window.after(1000,update_labels)

    #Criação da janela para interagir com o dispositivo
    user_window = tk.Toplevel(root)
    user_window.title(f"K3S Cluster - User: {username_var_temp.get()} - IP Address: {ip_address_var_temp.get()} - API PORT: {api_port_var_temp.get()} - SSH PORT: {ssh_port_var_temp.get()}")
    user_window.geometry("1280x960")

    ip_address_var = tk.StringVar(user_window)
    username_var = tk.StringVar(user_window)
    authorization_var = tk.StringVar(user_window)
    password_var = tk.StringVar(user_window)
    api_port_var = tk.StringVar(user_window)
    ssh_port_var = tk.StringVar(user_window)
    ip_address_var.set(f"{ip_address_var_temp.get()}")
    username_var.set(f"{username_var_temp.get()}")
    authorization_var.set(f"{authorization_temp}")
    authorization = authorization_var.get()
    password_var.set(f"{password_var_temp.get()}")
    api_port_var.set(f"{api_port_var_temp.get()}")
    ssh_port_var.set(f"{ssh_port_var_temp.get()}")

    #Create a frame for for labels
    stats = api_requests.get_node_stats_perodically(ip_address_var, api_port_var, authorization)
    top_frame = tk.Frame(user_window, bg="light gray")
    top_frame.pack(side=tk.TOP, fill=tk.X)
    labels_frame = tk.Frame(top_frame, bg="light gray")
    labels_frame.pack(side=tk.RIGHT)
    
    names = stats[0]
    timestamps = stats[1]
    cpus = stats[2]
    memorys = stats[3]

    time_label = 0
    cluster_labels = []
    col = 0
    for i in range(0, len(names)):
        if i == 0:
            time_label = tk.Label(labels_frame, text=f"Data e Hora: {timestamps[i]}", bg="light gray", font=("consolas", 10, "bold"))
            time_label.grid(row=0, column=col, padx=5, pady=1, sticky=tk.E)
            col += 1
            cluster_labels.append(tk.Label(labels_frame, text=f"{names[i]}: CPU-{cpus[i]} MEMORY-{memorys[i]}", bg="light gray", fg='blue'))
            cluster_labels[i].grid(row=0, column=col, padx=5, pady=1, sticky=tk.E)
            col += 1
        else:
            cluster_labels.append(tk.Label(labels_frame, text=f"{names[i]}: CPU-{cpus[i]} MEMORY-{memorys[i]}", bg="light gray", fg='blue'))
            cluster_labels[i].grid(row=0, column=col, padx=5, pady=1, sticky=tk.E)
            col += 1
    
    # Create a frame for buttons
    left_frame = tk.Frame(user_window, width=200, bg="light gray")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    button0 = tk.Button(left_frame, text="Dashboard", command=lambda: cria_dashboard())
    button0.pack(fill=tk.X, padx=2, pady=1)
    button1 = tk.Button(left_frame, text="Listar Nodes", command=lambda: api_requests.get_all_nodes(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, user_window, old_buttons, new_buttons, labels_frame))
    button1.pack(fill=tk.X, padx=2, pady=1)
    button2 = tk.Button(left_frame, text="Listar Namespaces", command=lambda: api_requests.get_all_namespaces(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, user_window, old_buttons, new_buttons, labels_frame))
    button2.pack(fill=tk.X, padx=2, pady=1)
    button3 = tk.Button(left_frame, text="Listar Pods", command=lambda: api_requests.get_all_pods(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, user_window, old_buttons, new_buttons, labels_frame))
    button3.pack(fill=tk.X, padx=2, pady=1)
    button4 = tk.Button(left_frame, text="Listar Deployments", command=lambda: api_requests.get_all_deployments(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, user_window, old_buttons, new_buttons, labels_frame))
    button4.pack(fill=tk.X, padx=2, pady=1)
    button5 = tk.Button(left_frame, text="Listar Services", command=lambda: api_requests.get_all_services(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, user_window, old_buttons, new_buttons, labels_frame))
    button5.pack(fill=tk.X, padx=2, pady=1)
    
    button6 = tk.Button(left_frame, text="Listar Ingresses", command=lambda: api_requests.get_all_ingresses(ip_address_var, api_port_var, authorization, listbox, dashboard_frame, tk, user_window, old_buttons, new_buttons, labels_frame))
    button6.pack(fill=tk.X, padx=2, pady=1)
    button12 = tk.Button(left_frame, text="Interface Web", command=lambda: open_webpage())
    button12.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)
    button11 = tk.Button(left_frame, text="Terminal", command=lambda: cria_terminal_ssh())
    button11.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)
    button10 = tk.Button(left_frame, text="Wizard", command=lambda: api_requests.cria_wizard(ip_address_var, api_port_var, authorization, listbox, tk, user_window))
    button10.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)

    # Create a frame for the listbox and the texbox and button
    old_buttons = [] 
    right_frame = tk.Frame(user_window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    listbox = tk.Listbox(right_frame, font=("Arial", 12))
    #listbox.pack(expand=True, fill="both", side=tk.TOP)
    button_frame = tk.Frame(right_frame)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    labels_frame = tk.Frame(right_frame)
    labels_frame.pack(fill=tk.X, side=tk.BOTTOM)
    criar_button = tk.Button(button_frame, text="Criar")
    editar_button = tk.Button(button_frame, text="Abrir")
    apagar_button = tk.Button(button_frame, text="Apagar")
    ativar_button = tk.Button(button_frame, text="Ativar")
    desativar_button = tk.Button(button_frame, text="Desativar")
    configurar_button = tk.Button(button_frame, text="Configurar")
    new_buttons = [criar_button, editar_button, apagar_button, ativar_button, desativar_button, configurar_button, button_frame]
    
    dashboard_frame = tk.Frame(right_frame)
    canvas = tk.Canvas(dashboard_frame)
    scrollbar = tk.Scrollbar(dashboard_frame, orient=tk.VERTICAL, command=canvas.yview)
    new_window = tk.Frame(canvas)
    
    nodes_stats_frame = tk.Frame(new_window)
    workload_status_frame = tk.Frame(new_window)
    tables_frame = tk.Frame(new_window)

    def cria_dashboard():
        global canvas2
        if canvas2:
            canvas2.get_tk_widget().forget()
        
        data = api_requests.get_workload_status(ip_address_var, api_port_var, authorization)
        def create_bar_graph(data):
            labels = list(data.keys())
            values = list(data.values())
            
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            bars = ax.bar(labels, values, color=['#4CAF50', '#FF5722', '#FFEB3B', '#2196F3', '#FFC107'])
            
            ax.set_xlabel('Workload Types')
            ax.set_ylabel('Count')
            ax.set_title('Kubernetes Workload Status')
            
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')  # va: vertical alignment
            
            return fig

        for button in old_buttons:
            button.grid_forget()
            del button

        if listbox.winfo_ismapped():
            listbox.pack_forget()
            labels_frame.pack_forget()
            button_frame.pack_forget()

        if not dashboard_frame.winfo_ismapped():
            dashboard_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)
            canvas.create_window((0,0), window=new_window, anchor=tk.NW)
            nodes_stats_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
            workload_status_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
            tables_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
            new_window.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
            
        node_stats = api_requests.get_node_stats_dashboard(ip_address_var, api_port_var, authorization)

        nodes_label = tk.Label(nodes_stats_frame, text=f"Nodes", font=("consolas", 14, "bold"))
        nodes_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        row = 1
        for item in node_stats:
            tk.Label(nodes_stats_frame, text=f"{item['metadata']['name']}", font=("consolas", 12), fg='blue').grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            tk.Label(nodes_stats_frame, text=f"Data de criação: {item['metadata']['creationTimestamp']}").grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
            row +=1
            tk.Label(nodes_stats_frame, text=f"Data e Hora: {item['timestamp']}").grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
            row +=1
            tk.Label(nodes_stats_frame, text=f"Window: {item['window']}").grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
            row +=1
            tk.Label(nodes_stats_frame, text=f"CPU: {item['usage']['cpu']}").grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
            row +=1
            tk.Label(nodes_stats_frame, text=f"MEMORY: {item['usage']['memory']}").grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
            row +=1
            string_labels = ""
            for label in item['metadata']['labels']:
                string_labels += f" {item['metadata']['labels'][label]},"
            string_labels = string_labels[:-1]
            tk.Label(nodes_stats_frame, text=f"Labels: {string_labels}").grid(row=row, column=2, padx=5, pady=5, sticky=tk.W, columnspan=10)
            row +=1

        workload_label = tk.Label(workload_status_frame, text=f"Workload Status", font=("consolas", 14, "bold"))
        workload_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        chart_frame = tk.Frame(workload_status_frame)
        chart_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        fig = create_bar_graph(data)
        canvas2 = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        daemonsets_data = api_requests.get_daemonSets_dashboard(ip_address_var, api_port_var, authorization)
        deamonsets_label = tk.Label(tables_frame, text=f"Daemon Sets", font=("consolas", 14, "bold"))
        deamonsets_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tabble_frame = tk.Frame(tables_frame)
        tabble_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W, columnspan=10)
        columns = ('Name', 'Namespace', 'Creation Timestamp')
        tree = ttk.Treeview(tabble_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=300)
        for i in range(len(daemonsets_data['name'])):
            tree.insert('', tk.END, values=(daemonsets_data['name'][i], daemonsets_data['namespace'][i], daemonsets_data['creationTimestamp'][i]))
        tree.pack(fill=tk.X, expand=True)

        deploments_data = api_requests.get_deployments_dashboard(ip_address_var, api_port_var, authorization)
        deployments_label = tk.Label(tables_frame, text=f"Deployments", font=("consolas", 14, "bold"))
        deployments_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tabble2_frame = tk.Frame(tables_frame)
        tabble2_frame.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W, columnspan=10)
        columns2 = ('Name', 'Namespace', 'Creation Timestamp')
        tree2 = ttk.Treeview(tabble2_frame, columns=columns2, show='headings')
        for col in columns2:
            tree2.heading(col, text=col)
            tree2.column(col, width=300)
        for i in range(len(deploments_data['name'])):
            tree2.insert('', tk.END, values=(deploments_data['name'][i], deploments_data['namespace'][i], deploments_data['creationTimestamp'][i]))
        tree2.pack(fill=tk.X, expand=True)

        jobs_data = api_requests.get_jobs_dashboard(ip_address_var, api_port_var, authorization)
        jobs_label = tk.Label(tables_frame, text=f"Jobs", font=("consolas", 14, "bold"))
        jobs_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        tabble3_frame = tk.Frame(tables_frame)
        tabble3_frame.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W, columnspan=10)
        columns3 = ('Name', 'Namespace', 'Creation Timestamp')
        tree3 = ttk.Treeview(tabble3_frame, columns=columns3, show='headings')
        for col in columns3:
            tree3.heading(col, text=col)
            tree3.column(col, width=300)
        for i in range(len(jobs_data['name'])):
            tree3.insert('', tk.END, values=(jobs_data['name'][i], jobs_data['namespace'][i], jobs_data['creationTimestamp'][i]))
        tree3.pack(fill=tk.X, expand=True)

        pods_data = api_requests.get_pods_dashboard(ip_address_var, api_port_var, authorization)
        pods_label = tk.Label(tables_frame, text=f"Pods", font=("consolas", 14, "bold"))
        pods_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        tabble4_frame = tk.Frame(tables_frame)
        tabble4_frame.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W, columnspan=10)
        columns4 = ('Name', 'Namespace', 'Creation Timestamp')
        tree4 = ttk.Treeview(tabble4_frame, columns=columns4, show='headings')
        for col in columns4:
            tree4.heading(col, text=col)
            tree4.column(col, width=300)
        for i in range(len(pods_data['name'])):
            tree4.insert('', tk.END, values=(pods_data['name'][i], pods_data['namespace'][i], pods_data['creationTimestamp'][i]))
        tree4.pack(fill=tk.X, expand=True)

        replica_data = api_requests.get_replica_sets_dashboard(ip_address_var, api_port_var, authorization)
        replica_label = tk.Label(tables_frame, text=f"Replica Set", font=("consolas", 14, "bold"))
        replica_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        tabble5_frame = tk.Frame(tables_frame)
        tabble5_frame.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W, columnspan=10)
        columns5 = ('Name', 'Namespace', 'Creation Timestamp')
        tree5 = ttk.Treeview(tabble5_frame, columns=columns5, show='headings')
        for col in columns5:
            tree5.heading(col, text=col)
            tree5.column(col, width=300)
        for i in range(len(replica_data['name'])):
            tree5.insert('', tk.END, values=(replica_data['name'][i], replica_data['namespace'][i], replica_data['creationTimestamp'][i]))
        tree5.pack(fill=tk.X, expand=True)

        diagrama_label = tk.Label(tables_frame, text=f"Diagrama Dinâmico", font=("consolas", 14, "bold"))
        diagrama_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
        diagrama_frame = tk.Frame(tables_frame)
        diagrama_frame.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W, columnspan=10)

        nodes = api_requests.get_nodes_networkx_graph(ip_address_var, api_port_var, authorization)
        node_master = {}
        node_workers = []
        for item in nodes["items"]:
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
        pods = api_requests.get_pods_network_graph(ip_address_var, api_port_var, authorization)
        cluster_pods = []
        for item in pods['items']:
            name_pod = item["metadata"]["name"]
            if "nodeName" in item["spec"]: 
                name_node_pod = item["spec"]["nodeName"]
            else:
                name_node_pod = "kmaster"
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

        #===== Vai buscar os atributos das cores dos nodes ou seja vai buscar uma lista com as cores
        node_colors = nx.get_node_attributes(G,'color').values()

        #===== Cria-se o objeto figra que vai ter dentro dele o grafico desenhado(como se fosse um container)
        fig = Figure(figsize=(9, 10), dpi=100)
        ax = fig.add_subplot()
        #nx.draw_planar(G, with_labels=True, node_color=node_colors ,font_weight='bold', ax=ax)
        nx.draw(G, with_labels=True, node_color=node_colors ,font_weight='bold', ax=ax)

        #===== O objeto figura em seguida é que é utilizado para ser apresentado na imagem
        canvas6 = FigureCanvasTkAgg(fig, master=diagrama_frame)
        canvas6.get_tk_widget().pack(fill='both', expand=True)
        

    def open_webpage():
        ip_address = ip_address_var.get()
        port = 0

        ssh_host = ip_address_var.get()
        ssh_port = int(ssh_port_var.get())
        ssh_username = username_var.get()
        ssh_password = password_var.get()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ssh_host, ssh_port))
        session = ssh2.session.Session()

        command = f"echo {ssh_password} | sudo -S kubectl get svc -n kubernetes-dashboard | grep kubernetes-dashboard | cut -d ':' -f 2 | cut -d '/' -f 1"

        try:
            session.handshake(sock)
            session.userauth_password(username=ssh_username, password=ssh_password)
            channel = session.open_session()
            channel.execute(command)
            size, data = channel.read()
            port = data.decode().strip()

        finally:
            if 'channel' in locals():
                channel.close()
            session.disconnect()
            sock.close()
        
        if port == 0:
            return

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the RouterOS login page
        url = f"https://{ip_address}:{port}/"
        driver.get(url)

        # Wait for the page to load
        time.sleep(1)

        # Find the username and password fields and submit button
        token_field = driver.find_element(By.ID, "token")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Enter username and password
        token_field.clear()
        token_field.send_keys(authorization)

        # Submit the form
        submit_button.click()

        close_browser(driver)

    def cria_terminal_ssh():
        ssh_window = tk.Toplevel(user_window)
        ssh_window.title(f"Terminal: {username_var.get()}@{ip_address_var.get()}")
        ssh_window.geometry("800x600")
        parent = ssh_window
        
        last_command = tk.StringVar()
        last_command.set("")

        def carrega_comando(event=None):
            command_entry.insert(tk.END, last_command.get())

        def execute_ssh_command(event=None):
            last_command.set(command_entry.get())
            if command_entry.get() == 'clear':
                output_entry.delete("1.0", tk.END)
                command_entry.delete(0, tk.END)
                return

            ssh_host = ip_address_var.get()
            ssh_port = int(ssh_port_var.get())
            ssh_username = username_var.get()
            ssh_password = password_var.get()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ssh_host, ssh_port))
            session = ssh2.session.Session()

            try:
                session.handshake(sock)
                session.userauth_password(username=ssh_username, password=ssh_password)
                channel = session.open_session()
                channel.execute(command_entry.get())
                size, data = channel.read()
                prestring = f"[{ssh_username}@{ssh_host}] > {command_entry.get()}:\n"
                #output_entry.delete("1.0", tk.END)  # Clear previous output
                output_entry.insert(tk.END, prestring + data.decode() + "\n")
                command_entry.delete(0, tk.END)

            finally:
                if 'channel' in locals():
                    channel.close()
                session.disconnect()
                sock.close()

        ssh_window.configure(bg="#eeeeec")  # Set background color to Tango White-like color
        ssh_window.bind("<Return>", execute_ssh_command)
        ssh_window.bind("<KeyRelease-Up>", carrega_comando)

        upper_frame = tk.Frame(ssh_window, bg="#eeeeec")  # Use Tango White-like color
        upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        lower_frame = tk.Frame(ssh_window, bg="#eeeeec")  # Use Tango White-like color
        lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        lef_lower_frame = tk.Frame(lower_frame, bg="#eeeeec")  # Use Tango White-like color
        lef_lower_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        right_lower_frame = tk.Frame(lower_frame, bg="#eeeeec")  # Use Tango White-like color
        right_lower_frame.pack(side=tk.RIGHT, anchor='s')

        label_font = ("Consolas", 16)

        output_label = tk.Label(upper_frame, text="Terminal OUTPUT:", bg="#eeeeec", font=label_font)  # Use Tango White-like color
        output_label.pack(side=tk.TOP, padx=5, pady=5, anchor='w')

        output_entry = scrolledtext.ScrolledText(upper_frame, height=4, width=30, font=label_font, fg="#336699")
        output_entry.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='w', expand=True, fill=tk.BOTH)

        command_label = tk.Label(lef_lower_frame, bg="#eeeeec", text="Command Prompt:", font=label_font)  # Use Tango White-like color
        command_label.pack(side=tk.TOP, padx=5, pady=5, anchor='w')

        command_entry = tk.Entry(lef_lower_frame, font=label_font)  # Use Tango White-like color
        command_entry.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='w', expand=True)

        enviar_button = tk.Button(right_lower_frame, text="Enviar comando", command=execute_ssh_command, font=label_font)  # Use Tango White-like color
        enviar_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='s')

    cria_dashboard()
    update_labels()

def cria_app():
    def on_double_click(event):
        # Get the selected item in the listbox
        index = lista.curselection()
        if index :
            item = lista.get(index)
            # Extract IP address and username from the selected item
            ip_address = item.split(",")[0].split("= ")[1].strip()
            username = item.split(",")[1].split("= ")[1].strip()
            password = item.split(",")[2].split("= ")[1].strip()
            api_port = item.split(",")[3].split("= ")[1].strip()
            ssh_port = item.split(",")[4].split("= ")[1].strip()

            ip_address_var.set(ip_address)
            username_var.set(username)
            password_var.set(base64_para_string(password))
            api_port_var.set(api_port)
            ssh_port_var.set(ssh_port)

    root = tk.Tk()
    root.title("KubeAPI") # Define o Titulo do GUI

    # Set fixed window size # Define custom colors # Set background color
    root.geometry("1280x720")
    bg_color = "#F2F2F2"  # Light gray
    text_color = "#333333"  # Dark gray ### ELEMINAR ? 
    button_color = "#4CAF50"  # Green ### ELEMINAR ? 
    root.configure(bg=bg_color)

    #Criar um Frame na esquerda para as Credenciais 
    frame_esquerda = tk.Frame(root, bg="light gray")
    frame_esquerda.pack(side=tk.LEFT, fill=tk.Y)

    #Criar um Frame na direita para apresentar Credenciais já existentes
    frame_direita = tk.Frame(root, bg=bg_color)
    frame_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    #Cria ListBox para colocar os dados das credenciais
    lista = tk.Listbox(frame_direita, font=("Arial", 16))
    lista.pack(expand=True, fill="both")
    lista.bind("<Double-Button-1>", on_double_click)  # Bind double-click event

    # Create ip address label and entry 
    ip_address_label = tk.Label(frame_esquerda, text="IP Address:", bg="light gray")
    ip_address_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    ip_address_var = tk.StringVar()
    ip_address_entry = tk.Entry(frame_esquerda, textvariable=ip_address_var)
    ip_address_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create username label and entry
    username_label = tk.Label(frame_esquerda, text="Username:", bg="light gray")
    username_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    username_var = tk.StringVar()
    username_entry = tk.Entry(frame_esquerda, textvariable=username_var)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create password label and entry
    password_label = tk.Label(frame_esquerda, text="Password:", bg="light gray")
    password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    password_var = tk.StringVar()
    password_entry = tk.Entry(frame_esquerda, show="*", textvariable=password_var)
    password_entry.grid(row=2, column=1, padx=5, pady=5)
    
    # Create API_PORT label and entry
    api_port_label = tk.Label(frame_esquerda, text="K3S API PORT:", bg="light gray")
    api_port_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    api_port_var = tk.StringVar()
    api_port_entry = tk.Entry(frame_esquerda, textvariable=api_port_var)
    api_port_entry.grid(row=3, column=1, padx=5, pady=5)

    # Create SSH_PORT label and entry
    ssh_port_label = tk.Label(frame_esquerda, text="SSH Port:", bg="light gray")
    ssh_port_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    ssh_port_var = tk.StringVar()
    ssh_port_entry = tk.Entry(frame_esquerda, textvariable=ssh_port_var)
    ssh_port_entry.grid(row=4, column=1, padx=5, pady=5)

    # Create button to show values
    confirm_button = tk.Button(frame_esquerda, text="Confirmar", command=lambda: login(ip_address_var, username_var, password_var, api_port_var, ssh_port_var, root, lista))
    confirm_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W)

    load_credentials(ip_address_var.get(), username_var.get(), password_var.get(), api_port_var.get(), ssh_port_var.get(),lista)

    root.mainloop()
    return ip_address_var, username_var, password_var, root
