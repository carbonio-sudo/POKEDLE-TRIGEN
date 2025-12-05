# 🎮 PokéTrigen – Pokémon Wordle

Plataforma interativa de adivinhação inspirada no Wordle, utilizando dados reais da PokéAPI.  
Desenvolvido para fins educacionais e aperfeiçoamento em aplicações web.

---

## 📌 Sobre o Projeto

O **PokéTrigen** é um jogo onde o usuário tenta adivinhar um Pokémon da 1ª, 2ª ou 3ª geração com base em pistas fornecidas pelo sistema, como:

- Tipos (1 e 2)  
- Cor  
- Habitat  
- Altura  
- Peso  
- Estágio evolutivo  
- Sprite oficial do Pokémon  

O jogo possui **sistema de login**, **perfil personalizável**, **pontuação global**, **autocompletar inteligente**, **feedback visual completo** e uma interface estilizada, fluida e responsiva.

---

## 🚀 Funcionalidades

### 🎯 Modo de Jogo – Wordle de Pokémon

- Sorteio automático entre os 386 primeiros Pokémon  
- Feedback visual completo:
  - 🟩 **Verde** – valor correto  
  - 🟥 **Vermelho** – valor incorreto  
  - 🟨 **Amarelo** – existe, mas em outra posição (tipagem)  
  - 🔼 **Seta para cima** – o chute é menor que o alvo  
  - 🔽 **Seta para baixo** – o chute é maior que o alvo  
- Tentativas exibidas com sprite  
- Nenhum Pokémon pode ser chutado duas vezes  
- Autocomplete avançado  
- Tela de vitória personalizada  
- Reset a qualquer momento  

---

## 👤 Sistema de Usuário

- Criar conta  
- Login e logout  
- Alterar apelido (nickname)  
- Trocar foto de perfil  
- Avatar exibido na navbar  
- Exclusão completa da conta  

Todos os dados são armazenados em arquivos JSON.

---

## ⭐ Sistema de Pontuação

- **–5 pontos** para erros  
- **+50 pontos** ao acertar  
- Pontuação salva automaticamente  
- Carregada novamente ao logar  

---

## ✨ Autocomplete Avançado

- Sugestões aparecem enquanto digita  
- Navegação por setas ↑ ↓  
- Enter seleciona a sugestão ativa  
- Fechamento automático ao clicar fora  
- Estilizado e responsivo  

---

## 🧰 Tecnologias Utilizadas

### Backend
- Python  
- Flask  
- Requests  
- JSON  
- PokéAPI  

### Frontend
- HTML5  
- CSS3  
- JavaScript  
- Bootstrap  
- Jinja2  

---

## 🔧 Como Rodar o Projeto

### 1️⃣ Criar ambiente virtual

```bash
python -m venv .venv
```

### 2️⃣ Ativar ambiente

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install flask requests
```

### 4️⃣ Executar o servidor

```bash
flask run
```

OU:

```bash
python3 run.py
```

### 🌍 Acessar o jogo

```
http://127.0.0.1:5000
```

# 🧠 Como o Jogo Funciona

## 🎲 1. Sorteio do Pokémon
Um Pokémon entre os IDs 1 e 386 é selecionado via PokéAPI.

## 🔍 2. Jogador envia um chute
- Nome verificado  
- Dados carregados direto da API  
- Tentativas repetidas são bloqueadas  

## 🎨 3. Comparação com feedback visual
A função `montar_feedback()` analisa:

| Atributo | Avaliação |
|----------|-----------|
| Tipo     | Correto / Errado / Outro Lugar |
| Habitat  | Correto / Errado |
| Cor      | Correto / Errado |
| Fase     | Correto / Errado |
| Altura   | Maior / Menor / Igual |
| Peso     | Maior / Menor / Igual |

## 👨‍💻 Desenvolvedor
Desenvolvido por Otavio, 2025.  
Projeto criado para estudos e aprimoramento em desenvolvimento web.
