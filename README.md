# Projeto: NutriLab

A NutriLab é uma plataforma para nutricionistas, onde eles podem gerênciar seus pacientes, 
passar o plano alimentar com metas de macros nutrientes e opções de receitas para atingir 
estas metas, além de poder atualizar os dados como: peso, porcentagem de gordura corporal
e porcentagem de massa magra, que pode ser visualizado através de um gráfico.

O sistema consiste em uma página de cadastro/login, que conta com ativação via email, uma 
página para gerênciar os pacientes (adicionar, remover e alterar dados cadastrais), uma 
página de dados dos pacientes (onde é possível adicionar o peso, a % de gordura corporal e 
a % de massa magra e visualizar o gráfico), e a página do plano alimentar (onde se adiciona
as refeições e tambem tem a opção de exportar como pdf).

## Tecnologias 

As tecnologias principais foram Django e SQLite na parte do Backend. E Bootstrap, CSS e 
JavaScript para o Frontend. O projeto foi desenvolvido durante o curso PythonFull, com 
auxílio do professor Caio Sampaio.

## Como rodar

Crie um ambiente virtual:<br/>
  - python -m venv venv
  
Ative o ambiente virtual:<br/>
  - no windowns:<br/>
    - venv\Scripts\Activate
    
Instale o django e o pillow no ambiente virtual:<br/>
  - pip install django pillow

Inice o servidor:<br/>
  - python manage.py runserver
  
  
