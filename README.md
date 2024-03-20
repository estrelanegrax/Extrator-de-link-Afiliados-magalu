Extrator de Produtos Afiliados
Este é um programa Python que extrai informações de produtos do site da Magalu e exibe no campos designados, ao adicionar a quantidade de porcentagem ele destaca o produto na segunda aba.

Funcionalidades
Extrai informações de produtos da magalu fornecido pelo usuário.
Cria um posto de Afiliado ja pronto para postar no whatsap
Permite definir uma porcentagem mínima de desconto.
Exibe as promoções com desconto igual ou superior à porcentagem mínima.
Interface gráfica simples para interação do usuário.
Instruções de Uso (Windows)
Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo em python.org.
Instale as bibliotecas necessárias executando pip install requests beautifulsoup4.
Como Executar
Clone o repositório para o seu computador ou baixe o código-fonte como um arquivo ZIP e extraia-o.
Abra um terminal de comando (Prompt de Comando ou PowerShell) e navegue até o diretório onde o código-fonte está localizado.
Execute o comando python link.py para iniciar o programa.
Utilizando o Programa
Na interface gráfica, insira a URL do site, o nome da sua loja e a porcentagem mínima de desconto desejada.
Clique no botão "Buscar" para extrair e processar os produtos.
Você verá os produtos exibidos nas duas áreas de texto, separados em "Normal" e "Destacada", com base na porcentagem de desconto.
Você pode navegar entre as páginas normal e destacada usando os botões de paginação.
Convertendo para um Arquivo Executável (EXE)
Para transformar o código Python em um arquivo executável (.exe) no Windows, você pode usar o PyInstaller. Siga estes passos:

Instale o PyInstaller executando pip install pyinstaller.
No terminal de comando, navegue até o diretório onde o código-fonte está localizado.
Execute o comando pyinstaller --onefile magalu.py para gerar o arquivo executável.
Após a conclusão, você encontrará o arquivo executável na pasta dist.
Contribuindo
Se deseja contribuir com melhorias ou corrigir problemas, sinta-se à vontade para abrir uma "issue" ou enviar um "pull request".

Licença
Este projeto está licenciado sob a Licença MIT -
