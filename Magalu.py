import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import re
import unidecode
import threading

# Variáveis globais
current_page_normal = 1
current_page_highlighted = 1
products_per_page = 2
product_items = []
discount_threshold = 0

# Função para limpar o nome de arquivo
def clean_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)  
    filename = unidecode.unidecode(filename)
    return filename.strip()

# Função ajustada para calcular a porcentagem de desconto e incluir parcelamento
def get_discount_percentage(item):
    try:
        price_original_tag = item.find('p', {'data-testid': 'price-original'})
        price_pix_tag = item.find('p', {'data-testid': 'price-value'})
        installment_info_tag = item.find('p', {'data-testid': 'installment'})  # Busca a informação de parcelamento
        
        # Inicializando variáveis
        original_price = 0.0
        pix_price = 0.0
        installment_info = "Informação de parcelamento não disponível"  # Texto padrão caso não encontre a tag

        if price_original_tag and price_pix_tag:
            original_price_str = re.sub(r'[^\d,]', '', price_original_tag.text).replace(',', '.')
            pix_price_str = re.sub(r'[^\d,]', '', price_pix_tag.text).replace(',', '.')
            
            # Convertendo para float
            original_price = float(original_price_str)
            pix_price = float(pix_price_str)
        
        if installment_info_tag:
            installment_info = installment_info_tag.text.strip()  # Extrai o texto da tag

        # Calculando desconto
        if original_price > 0 and pix_price > 0:
            discount_percentage = (original_price - pix_price) / original_price * 100
            return discount_percentage, installment_info
    except Exception as e:
        print(f"Erro ao calcular a porcentagem de desconto: {e}")
    return 0, installment_info  # Retorna 0 e a informação de parcelamento


# Função ajustada para exibir produtos, agora incluindo parcelamento
def display_product(widget, item, nome_loja):
    link_tag = item.find('a', attrs={'data-testid': 'product-card-container'})
    product_url = link_tag.get('href')
    full_url = f"https://www.magazinevoce.com.br/{nome_loja}{product_url}" if product_url.startswith('/') else product_url

    product_title_tag = item.find('h2', {'data-testid': 'product-title'})
    if product_title_tag:
        product_title = clean_filename(product_title_tag.text)
    else:
        product_title = "Título não disponível"

    price_original_tag = item.find('p', {'data-testid': 'price-original'})
    if price_original_tag:
        price_original = price_original_tag.text.strip()
    else:
        price_original = "Preço original não disponível"

    price_pix_tag = item.find('p', {'data-testid': 'price-value'})
    if price_pix_tag:
        price_pix = price_pix_tag.text.strip()
    else:
        price_pix = "Preço com desconto não disponível"

    discount_percentage, installment_info = get_discount_percentage(item)  # Agora também recebe a informação de parcelamento

    message = f"*{product_title}*\n\n"
    message += f"❌De: ~{price_original}~\n"
    message += f"✅Por: *{price_pix}*\n"
    message += f"Desconto: {discount_percentage:.2f}%\n"
    message += f"{installment_info}\n\n"  # Adiciona a informação de parcelamento à mensagem
    message += f"Link da compra 👇:\n {full_url}\n\n"

    widget.insert(tk.END, message)


# Função chamada pelo botão para iniciar o processamento
def fetch_and_process_products_thread():
    global product_items, current_page_normal, current_page_highlighted
    url = entry_url.get().strip()
    nome_loja = entry_nome_loja.get().strip()
    porcentagem = entry_porcentagem.get().strip()
    
    # Verificar se todos os campos estão preenchidos
    if not url or not nome_loja or not porcentagem:
        messagebox.showerror("Erro", "Todos os campos (URL, nome da loja e porcentagem de desconto) devem ser preenchidos.")
        return

    try:
        # Tentar converter a porcentagem de desconto para float
        global discount_threshold
        discount_threshold = float(porcentagem)
    except ValueError:
        messagebox.showerror("Erro", "Porcentagem de desconto inválida.")
        return
    
    # Reiniciar a paginação e limpar os dados anteriores dos produtos
    current_page_normal = 1
    current_page_highlighted = 1
    product_items = []  # Limpa a lista de itens
    fetch_button.config(text="Carregando...", state="disabled")

    # Iniciar o processamento em uma nova thread, passando o nome da loja
    threading.Thread(target=lambda: fetch_and_process_products(nome_loja)).start()



# Ajustar a função fetch_and_process_products para aceitar o nome da loja como parâmetro
def fetch_and_process_products(nome_loja):
    global product_items, discount_threshold
    url = entry_url.get().strip()
    # A verificação de URL e nome da loja já foi feita, não é necessário repetir
    try:
        discount_threshold = float(entry_porcentagem.get())
    except ValueError:
        messagebox.showerror("Erro", "Porcentagem de desconto inválida.")
        fetch_button.config(text="Processar Produtos", state="normal")
        return

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        product_items = soup.find_all("li", class_="sc-kTbCBX ciMFyT")
        update_product_display(nome_loja)
    else:
        messagebox.showerror("Erro", "Não foi possível acessar o site.")
    
    fetch_button.config(text="Processar Produtos", state="normal")

# Função ajustada para incluir o nome da loja
def update_product_display(nome_loja):
    all_promotions_text.delete("1.0", tk.END)
    highlighted_promotions_text.delete("1.0", tk.END)
    
    normal_products_indices = range((current_page_normal - 1) * products_per_page, min(current_page_normal * products_per_page, len(product_items)))
    for index in normal_products_indices:
        display_product(all_promotions_text, product_items[index], nome_loja)

    # Ajuste para desempacotar corretamente a porcentagem de desconto e o parcelamento
    highlighted_products = []
    for item in product_items:
        discount_percentage, _ = get_discount_percentage(item)  # Ignorando o parcelamento aqui
        if discount_percentage >= discount_threshold:
            highlighted_products.append(item)
    
    highlighted_products_indices = range((current_page_highlighted - 1) * products_per_page, min(current_page_highlighted * products_per_page, len(highlighted_products)))
    for index in highlighted_products_indices:
        display_product(highlighted_promotions_text, highlighted_products[index], nome_loja)

    label_current_page_normal.config(text=f"Página Normal: {current_page_normal}/{max(1, (len(product_items) + products_per_page - 1) // products_per_page)}")
    label_current_page_highlighted.config(text=f"Página Destacada: {current_page_highlighted}/{max(1, (len(highlighted_products) + products_per_page - 1) // products_per_page)}")


# Funções de navegação ajustadas para incluir o nome da loja
def next_page_normal():
    global current_page_normal
    nome_loja = entry_nome_loja.get().strip()  # Obter o nome da loja do campo de entrada
    if current_page_normal < (len(product_items) + products_per_page - 1) // products_per_page:
        current_page_normal += 1
        update_product_display(nome_loja)  # Atualiza a exibição com o nome da loja

def prev_page_normal():
    global current_page_normal
    nome_loja = entry_nome_loja.get().strip()  # Obter o nome da loja do campo de entrada
    if current_page_normal > 1:
        current_page_normal -= 1
        update_product_display(nome_loja)  # Atualiza a exibição com o nome da loja

def next_page_highlighted():
    global current_page_highlighted
    nome_loja = entry_nome_loja.get().strip()  # Obter o nome da loja do campo de entrada
    highlighted_products = [item for item in product_items if get_discount_percentage(item)[0] >= discount_threshold]  # Obtenha apenas a porcentagem de desconto
    if current_page_highlighted < (len(highlighted_products) + products_per_page - 1) // products_per_page:
        current_page_highlighted += 1
        update_product_display(nome_loja)  # Atualiza a exibição com o nome da loja


def prev_page_highlighted():
    global current_page_highlighted
    nome_loja = entry_nome_loja.get().strip()  # Obter o nome da loja do campo de entrada
    if current_page_highlighted > 1:
        current_page_highlighted -= 1
        update_product_display(nome_loja)  # Atualiza a exibição com o nome da loja


# Interface Gráfica
root = tk.Tk()
root.title("Extrator de Produtos")

frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=10, pady=5)

tk.Label(frame_inputs, text="URL do site:").pack(side="left")
entry_url = tk.Entry(frame_inputs, width=30)
entry_url.pack(side="left", padx=5)

# Adicionar campo de entrada para o nome da loja na interface gráfica
tk.Label(frame_inputs, text="Sua Loja:").pack(side="left")
entry_nome_loja = tk.Entry(frame_inputs, width=20)
entry_nome_loja.pack(side="left", padx=5)

tk.Label(frame_inputs, text="Porcentagem de desconto mínima:").pack(side="left")
entry_porcentagem = tk.Entry(frame_inputs, width=3)
entry_porcentagem.pack(side="left", padx=5)


fetch_button = tk.Button(frame_inputs, text="Bucar", command=fetch_and_process_products_thread)
fetch_button.pack(side="left", padx=5)

all_promotions_text = tk.Text(root, height=15, width=70)
all_promotions_text.pack(padx=10, pady=5)

highlighted_promotions_text = tk.Text(root, height=15, width=70)
highlighted_promotions_text.pack(padx=10, pady=5)

pagination_frame = tk.Frame(root)
pagination_frame.pack(padx=10, pady=5)

prev_normal_button = tk.Button(pagination_frame, text="< Anterior Normal", command=prev_page_normal)
prev_normal_button.pack(side="left")

label_current_page_normal = tk.Label(pagination_frame, text=f"Página Normal: {current_page_normal}")
label_current_page_normal.pack(side="left", padx=20)

next_normal_button = tk.Button(pagination_frame, text="Próximo Normal >", command=next_page_normal)
next_normal_button.pack(side="left")

prev_highlighted_button = tk.Button(pagination_frame, text="< Anterior Destacada", command=prev_page_highlighted)
prev_highlighted_button.pack(side="left", padx=20)

label_current_page_highlighted = tk.Label(pagination_frame, text=f"Página Destacada: {current_page_highlighted}")
label_current_page_highlighted.pack(side="left", padx=20)

next_highlighted_button = tk.Button(pagination_frame, text="Próximo Destacada >", command=next_page_highlighted)
next_highlighted_button.pack(side="left")

root.mainloop()
