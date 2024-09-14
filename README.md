# Monitoramento de Valores Médios RGB com Webcam

Este projeto utiliza **Streamlit** e **WebRTC** para capturar vídeo em tempo real da webcam, calcular os valores médios dos canais RGB (vermelho, verde e azul) de cada frame e exibi-los em um gráfico. Também é possível salvar os dados coletados em um arquivo Excel.

## Funcionalidades

- Captura de vídeo em tempo real via **WebRTC**.
- Cálculo dos valores médios dos canais **RGB** a cada segundo.
- Exibição de um gráfico atualizado em tempo real dos valores médios dos canais RGB.
- Botão para salvar os dados em um arquivo Excel (.xlsx) para download.

## Pré-requisitos

Certifique-se de que você tenha as seguintes dependências instaladas:

- **Python 3.7+**
- **Streamlit**
- **OpenCV**
- **Pandas**
- **Numpy**
- **Matplotlib**
- **Streamlit-WebRTC**
- **Openpyxl**

Para instalar todas as dependências, você pode utilizar o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Como rodar o projeto

1. Clone o repositório para sua máquina local:

```bash
git clone https://github.com/seu-usuario/monitoramento-rgb-webcam.git
```

2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

3. Execute o aplicativo Streamlit:

```bash
streamlit run app.py
```

4. Acesse o aplicativo no navegador pelo endereço:

```
http://localhost:8501
```

## Funcionalidades do Aplicativo

### 1. Monitoramento RGB
- O aplicativo captura vídeo em tempo real da webcam e calcula os valores médios dos canais RGB (Vermelho, Verde e Azul) a cada segundo.
- Esses valores são plotados em um gráfico dinâmico que exibe os últimos 300 pontos (ou 300 segundos) de dados.

### 2. Salvar Dados em Excel
- Ao clicar no botão "Salvar Dados em Excel", um arquivo `.xlsx` será gerado contendo os valores de RGB ao longo do tempo.
- Um botão de download aparecerá, permitindo que o usuário baixe os dados coletados em formato Excel.

## Estrutura do Projeto

```bash
monitoramento-rgb-webcam/
│
├── app.py              # Arquivo principal da aplicação Streamlit
├── requirements.txt    # Arquivo de dependências do Python
└── README.md           # Documentação do projeto
```

## Tecnologias Utilizadas

- **Streamlit**: Framework para a criação de aplicações web em Python.
- **WebRTC**: Tecnologia para captura de vídeo em tempo real.
- **OpenCV**: Biblioteca para processamento de imagens.
- **Pandas**: Biblioteca para manipulação de dados.
- **Matplotlib**: Biblioteca para criação de gráficos.
- **Numpy**: Biblioteca para operações matemáticas e manipulação de arrays.

## Contribuições

Se você deseja contribuir com este projeto, siga os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma branch para a sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Envie para a branch principal (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Este arquivo `README.md` oferece um guia claro sobre como configurar, rodar e utilizar o projeto, além de mencionar as tecnologias envolvidas e a estrutura básica do projeto.