# Proposta de projeto — Sistema de gerenciamento acadêmico

## 1. Título

**EduControl AED: cadastro e acompanhamento de alunos**

## 2. Contexto

Os scripts de `.python codes` já trabalham com entrada de dados, condicionais,
laços de repetição, listas, vetores, dicionários, funções, módulos, arquivos e
menus interativos. O projeto reúne esses conhecimentos em um sistema simples
para organizar alunos, notas e situações acadêmicas.

## 3. Problema

Informações de alunos e notas costumam ser digitadas e calculadas
separadamente. Falta uma aplicação única que permita cadastrar os dados,
consultar resultados, calcular médias e gerar um relatório organizado.

## 4. Objetivo geral

Desenvolver um programa em Python para cadastrar alunos, registrar notas,
calcular médias, classificar situações acadêmicas e salvar os dados em arquivo.

## 5. Objetivos específicos

- cadastrar, consultar, alterar e remover alunos;
- registrar até quatro notas para cada aluno;
- calcular média, maior nota e menor nota;
- classificar o aluno como aprovado, recuperação ou reprovado;
- listar alunos por situação;
- pesquisar alunos pelo nome;
- calcular estatísticas gerais da turma;
- salvar e carregar os dados em JSON ou TXT;
- organizar o sistema em funções e módulos reutilizáveis;
- criar um menu de terminal simples e claro.

## 6. Escopo do MVP

O primeiro entregável deve conter:

1. menu com as opções `cadastrar`, `listar`, `consultar`, `atualizar`,
   `remover`, `relatório` e `sair`;
2. cadastro com nome, matrícula, curso e notas;
3. validação de matrícula única e notas entre 0 e 10;
4. cálculo automático da média;
5. classificação conforme regras definidas;
6. busca por nome ou matrícula;
7. relatório geral da turma;
8. salvamento e carregamento dos dados;
9. tratamento explícito de entradas inválidas.

Regras sugeridas:

- média maior ou igual a 7: **aprovado**;
- média entre 5 e 6,9: **recuperação**;
- média menor que 5: **reprovado**.

## 7. Funcionalidades detalhadas

### Cadastro e validação

- `cadastrar_aluno()`: registra os dados de um novo aluno;
- `validar_nome()`: impede nomes vazios;
- `validar_matricula()`: garante matrícula preenchida e única;
- `ler_nota()`: aceita somente valores entre 0 e 10;
- `atualizar_aluno()`: altera dados sem duplicar matrículas.

### Notas e estatísticas

- `calcular_media(notas)`: retorna a média das notas;
- `classificar_aluno(media)`: retorna a situação acadêmica;
- `maior_nota(notas)` e `menor_nota(notas)`;
- média geral da turma;
- quantidade e porcentagem de alunos em cada situação;
- aluno com maior média;
- separação de alunos aprovados, em recuperação e reprovados.

### Consultas

- listar todos os alunos em ordem alfabética;
- consultar um aluno pela matrícula;
- pesquisar nomes por parte do texto;
- filtrar alunos por situação acadêmica;
- mostrar o boletim completo de um aluno.

### Persistência

Os dados devem ser salvos para não desaparecerem quando o programa for
encerrado. JSON é recomendado para guardar os dicionários estruturados; TXT
pode ser usado para gerar um relatório legível.

## 8. Organização sugerida

```text
educontrol/
    main.py              # menu e fluxo principal
    alunos.py            # cadastro, alteração, remoção e busca
    notas.py             # médias, situações e estatísticas
    persistencia.py      # leitura e gravação de JSON/TXT
    relatorios.py        # exibição e geração de relatórios
    testes/
        test_alunos.py
        test_notas.py
```

As funções devem receber dados e retornar resultados. A leitura com `input()`
e a impressão de mensagens devem ficar principalmente em `main.py`, para que
as funções possam ser testadas sem depender do terminal.

## 9. Plano de execução

### Etapa 1 — Estrutura de dados

- definir o formato do dicionário de cada aluno;
- criar listas para armazenar a turma;
- implementar cadastro e validação;
- testar nomes, matrículas repetidas e notas inválidas.

### Etapa 2 — Notas e consultas

- implementar média e classificação;
- criar listagem, busca e atualização;
- criar filtros por situação;
- testar alunos sem notas e casos de limite.

### Etapa 3 — Menu e relatórios

- construir o menu principal;
- calcular estatísticas da turma;
- gerar um relatório de texto;
- tratar escolhas inexistentes sem encerrar o programa.

### Etapa 4 — Arquivos e apresentação

- salvar e carregar JSON;
- testar arquivo inexistente ou com dados inválidos;
- preparar exemplos de execução;
- apresentar o fluxo completo do sistema.

## 10. Critérios de avaliação

- **Correção (30%):** médias, classificações e estatísticas corretas.
- **Estruturas de dados (20%):** listas e dicionários usados adequadamente.
- **Funções e modularização (20%):** responsabilidades separadas e código
  reutilizável.
- **Robustez (15%):** entradas inválidas tratadas sem falhas inesperadas.
- **Persistência e testes (10%):** dados salvos e funções principais testadas.
- **Apresentação (5%):** instruções claras e demonstração do sistema.

## 11. Entregáveis

- código-fonte organizado em módulos;
- menu funcional no terminal;
- arquivo de instruções de execução;
- exemplos de entrada e saída;
- testes das funções principais;
- arquivo JSON com dados de exemplo;
- relatório final da turma;
- apresentação curta mostrando o MVP.

## 12. Extensões futuras

- cadastro de disciplinas e professores;
- cálculo de frequência;
- lançamento de várias avaliações por disciplina;
- exportação para CSV;
- ranking de desempenho;
- geração de gráficos;
- sistema de login para diferentes tipos de usuário.
