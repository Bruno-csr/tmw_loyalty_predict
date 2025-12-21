# Loyalty Predict — Minha Jornada Construindo um Sistema de Engajamento Inteligente

Este repositório reúne minha implementação e estudo do projeto **Loyalty Predict**, criado em parceria com o streamer e educador **Teo Me Why**.  
Além de acompanhar as lives, estou aplicando minha própria visão de negócio, engenharia e ciência de dados para transformar o ecossistema de pontos da comunidade em uma solução robusta, escalável e data-driven.

> 🚀 Meu objetivo aqui é documentar a evolução do projeto do ponto de vista **prático**, **técnico** e **profissional**, mostrando como aplico data science no mundo real.

<img src="img/Aprendiz_feiticeiro_canva.png">

---

## 🔍 Objetivo do Projeto

Criar uma solução capaz de **detectar ganho ou perda de engajamento** dos usuários da comunidade, utilizando:

- Análise de comportamento,
- Feature engineering baseado em ciclo de vida,
- Agrupamentos e perfis de usuários,
- Modelos de machine learning supervisionados,
- Métricas e interpretações acionáveis para retenção.

---

## 🧠 O que estou construindo aqui

- Métricas avançadas de uso e engajamento da comunidade TMW.
- Feature Store para padronizar variáveis utilizadas no modelo.
- Pipeline completo: ingestão → transformação → modelagem → inferência.
- Modelo de ML registrável e versionado via MLFlow.
- App de inferência para predição em tempo real.
- Integração com o ecossistema (pontos, cursos, comunidade).

Este repo contém o código **100% escrito por mim durante os estudos e as lives**.

---

## 🛠 Stack e Pré-Requisitos

Para acompanhar ou reproduzir o projeto, recomendo conhecimento em:

- SQL  
- Python  
- Pandas  
- Estatística  
- Machine Learning  
- Git e GitHub  

As playlists oficiais do TMW (gratuitas) estão aqui:

- [SQL](https://www.youtube.com/playlist?list=PLvlkVRRKOYFRo651oD0JptVqfQGDvMi3j)  
- [Python](https://www.youtube.com/playlist?list=PLvlkVRRKOYFSpRkqnR0p2A-eaVlpLnN3D)  
- [Pandas](https://www.youtube.com/playlist?list=PLvlkVRRKOYFQHnDhjTmXLEz3HU5WTgOcF)
- [Estatística](https://www.youtube.com/playlist?list=PLvlkVRRKOYFQGIZdz7BycJet9OncyXlbq)
- [Machine Learning](https://www.youtube.com/playlist?list=PLvlkVRRKOYFR6_LmNcJliicNan2TYeFO2)
- [Git e GitHub](https://www.youtube.com/playlist?list=PLvlkVRRKOYFQyKmdrassLNxkzSMM6tcSL)

---
## 🛠️ Configuração do Ambiente

Este projeto utiliza o **Conda** para gerenciar o ambiente virtual e as dependências. Para evitar erros de compatibilidade e DLLs no Windows, siga as instruções abaixo.

### 1. Pré-requisitos
* Ter o [Anaconda](https://www.anaconda.com/download) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html) instalado.

### 2. Criando o ambiente do zero
Se você acabou de clonar o repositório, execute o comando abaixo no seu terminal (Anaconda Prompt) para criar o ambiente com **Python 3.13.7**:

```bash
conda env create -f environment.yml
```

### 3. Atualizando um ambiente existente
Caso você já tenha o ambiente loyalty-predict criado, mas precise atualizar as versões para ficarem idênticas às do repositório:

```bash
conda env update -n loyalty-predict -f environment.yml --prune
```

### 4. Ativação e Uso
Após a instalação, ative o ambiente:

```bash
conda activate loyalty-predict
```

### 5. Atualizando o 'enviroment.yml'
Para garantir que todos os outros desenvolvedores fiquem com o mesmo ambiente (Python 3.13.7 e as mesmas bibliotecas), a melhor prática é criar um arquivo chamado environment.yml.

```bash
conda env export --no-builds > environment.yml
```


### No VS Code:

1. Abra o projeto.
2. Pressione Ctrl + Shift + P.
3. Busque por Python: Select Interpreter.
4. Selecione a opção que contém: ('loyalty-predict': conda).

> Nota para usuários Windows: Se encontrar erros de ImportError: DLL load failed, tente abrir o VS Code diretamente pelo terminal do Anaconda após ativar o ambiente, digitando o comando code ..

--- 
## 📚 Etapas do Desenvolvimento

1. Entendimento do problema  
2. Extração e limpeza dos dados  
3. Exploração e criação das variáveis  
4. Feature Stores  
5. Treinamento e validação dos modelos  
6. Registro no MLFlow  
7. Construção do app de inferência  
8. Deploy e integração ao ecossistema  

---

## 📂 Fontes de Dados

- [Sistema de Pontos](https://www.kaggle.com/datasets/teocalvo/teomewhy-loyalty-system)  
- [Plataforma de Cursos](https://www.kaggle.com/datasets/teocalvo/teomewhy-education-platform)

---

## ❤️ Apoie o criador do projeto

Se quiser fortalecer o trabalho do Teo:

- Pix: pix@teomewhy.org  
- LivePix: https://livepix.gg/teomewhy  
- GitHub Sponsors: https://github.com/sponsors/TeoMeWhy  
- ApoiaSe: https://apoia.se/teomewhy  
- Membro no YouTube / Sub na Twitch  

---

## ❓ FAQ

> As lives são gratuitas e abertas ao público pelo canal da Twitch.  
> Não há certificado.  
> O VOD fica disponível para subs por 16 dias.  
> Início: 9AM.  
> Lives de segunda a sexta.  

---

## ✨ Sobre este repositório

Este repo reflete:

- minhas soluções,  
- meus experimentos,  
- meus estudos,  
- minhas análises,  
- minha visão sobre Data Science aplicada a comunidades digitais.

Sinta-se à vontade para abrir issues, sugerir melhorias ou trocar ideias.  
Construir projetos em comunidade é sempre mais divertido.
