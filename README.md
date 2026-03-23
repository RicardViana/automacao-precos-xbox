# 🎮 Monitor e Automação de Preços Xbox

![Python](https://img.shields.io/badge/Python-3.12-blue) 
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-success)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

Este projeto é um sistema automatizado **100% na nuvem** desenvolvido em Python para monitorizar diariamente os preços de jogos na loja digital da Xbox. O sistema extrai os valores atualizados de forma autónoma, guarda o histórico numa base de dados (CSV) versionada no próprio repositório, envia relatórios por e-mail e disponibiliza um Dashboard interativo na web.

## ✨ Funcionalidades

* **Automação na Nuvem (Serverless):** O script corre diariamente de forma automática através do **GitHub Actions**, sem necessidade de manter um computador local ligado.
* **Web Scraping Dinâmico:** Acede às páginas da Xbox e extrai os preços de forma fiável através da leitura de metadados invisíveis (JSON-LD).
* **Base de Dados Efémera:** O próprio GitHub atua como base de dados, atualizando o ficheiro `historico_precos.csv` através de commits automáticos do robô.
* **Notificações por E-mail:** Envio automatizado de um relatório diário consolidado usando o protocolo SMTP do Gmail.
* **Dashboard Interativo (Streamlit Cloud):** Uma interface web pública e responsiva para visualizar a evolução dos preços em gráficos de linha.
* **Setup Automatizado (Local):** Script `.bat` que baixa e configura todo o ambiente virtual de forma automática usando o gestor de pacotes ultra-rápido `uv`.

## 📂 Estrutura do Projeto

```text
automacao-precos-xbox/
│
├── .github/workflows/
│   └── automacao_diaria.yml    # O "cérebro" da automação (Agendamento no GitHub Actions)
├── dados/
    └── historico_precos.csv    # Base de dados em nuvem (historico_precos.csv)
├── app.py                      # Dashboard interativo (Frontend / Streamlit)
├── automacao.py                # Script principal de extração e e-mail (Backend)
├── instalar_ambiente.bat                
├── pyproject.toml              # Receita de dependências do projeto
└── uv.lock                     # Versões exatas das bibliotecas para replicação segura
```

## 🚀 Como Replicar este Projeto na Nuvem

Se quiseres criar o teu próprio monitor de preços 100% automatizado, segue estes passos:

### 1. Clonar o Repositório
Faz um "Fork" deste repositório para a tua conta do GitHub ou clona-o localmente:
```bash
git clone https://github.com/RicardViana/automacao-precos-xbox.git
```

### 2. Configurar os Segredos (GitHub Secrets)
Como o código vai rodar na nuvem pública, **nunca** deves colocar as tuas senhas no código. 
Vai à página do teu repositório no GitHub -> **Settings** -> **Secrets and variables** -> **Actions** e cria os seguintes *Repository Secrets*:
* `EMAIL_REMETENTE`: O teu e-mail do Gmail.
* `SENHA_APP_GMAIL`: A tua Senha de Aplicativo (gerada na segurança da Conta Google).
* `EMAIL_DESTINO`: Os e-mails que vão receber o relatório (separados por vírgula).

### 3. Ativar a Automação Diária
O ficheiro `.github/workflows/automacao_diaria.yml` já está configurado para correr todos os dias. 
Podes ir ao separador **Actions** no GitHub e clicar em **"Run workflow"** para forçar a primeira execução e criar o ficheiro CSV inicial.

### 4. Publicar o Dashboard
1. Cria uma conta gratuita no [Streamlit Community Cloud](https://share.streamlit.io/).
2. Clica em "New App" e liga o teu repositório do GitHub.
3. Define o *Main file path* como `app.py` e clica em **Deploy**. O teu site estará online em 2 minutos!

---

## 💻 Como Rodar Localmente (Para Desenvolvimento)

Se quiseres fazer alterações no código e testar na tua máquina, o processo é incrivelmente simples.

### 1. Configurar as Credenciais Seguras
Na raiz do projeto, cria um ficheiro chamado exatamente **`.env`** e adiciona as tuas credenciais:
```text
EMAIL_REMETENTE=teu_email@gmail.com
SENHA_APP_GMAIL=tua_senha_de_aplicativo_do_google
EMAIL_DESTINO=email_que_vai_receber_o_alerta@gmail.com
```

### 2. Instalar o Ambiente (A Magia do `.bat`)
Para Windows, basta dar um duplo clique no ficheiro **`instalar_ambiente.bat`**. 
Ele fará tudo sozinho: verifica o gestor `uv`, cria o ambiente virtual isolado (`.venv`) e instala as dependências corretas.

*(Se não usares Windows, basta rodar `uv sync` no terminal).*

### 3. Executar o Projeto
Abre o teu terminal na pasta do projeto e escolhe o que queres rodar:

**Para extrair os preços e enviar o e-mail:**
```bash
uv run automacao.py
```

**Para abrir o Dashboard interativo:**
```bash
uv run streamlit run app.py
```

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Cloud & CI/CD:** GitHub Actions / Streamlit Community Cloud
* **Gestor de Pacotes:** uv (Astral)
* **Bibliotecas Principais:** `requests`, `beautifulsoup4`, `pandas`, `streamlit`