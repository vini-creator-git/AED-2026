# Lista de exercícios de Python

Esta lista foi elaborada exclusivamente a partir dos scripts já praticados em
`.python codes/`. A ordem é progressiva: cada bloco reutiliza conhecimentos dos
blocos anteriores.

## Como entregar

Para cada exercício:

- crie um arquivo `.py` com nome identificando o exercício;
- use entradas e mensagens em português;
- valide entradas quando o enunciado pedir;
- teste pelo menos um caso normal e dois casos de borda;
- quando houver repetição de lógica, extraia uma função;
- registre no início do arquivo um exemplo de entrada e saída em comentário.

## Bloco 1 — Fundamentos e decisões

1. **Conversor de temperatura**  
   Leia uma temperatura e uma unidade (`C`, `F` ou `K`) e converta para as
   outras duas unidades. Recuse unidades inválidas.

2. **Classificador de número**  
   Leia um número inteiro e informe se ele é positivo, negativo ou zero, e se
   é par ou ímpar.

3. **Calculadora de compra**  
   Leia o preço, a quantidade e a forma de pagamento. Aplique descontos de
   acordo com a forma escolhida e mostre o valor final.

4. **Ano bissexto**  
   Leia um ano e informe se ele é bissexto usando a regra completa dos anos
   divisíveis por 4, 100 e 400.

5. **Estatística de partidas**  
   Leia a quantidade de jogos de um campeonato e os gols de cada equipe.
   Calcule vitórias, empates, derrotas e pontuação final.

## Bloco 2 — Laços e validação

6. **Menu de operações**  
   Faça um menu com soma, subtração, multiplicação, divisão e saída. O menu
   deve continuar até o usuário escolher sair e não pode permitir divisão por
   zero.

7. **Fatorial e sequência**  
   Leia um número não negativo, calcule o fatorial com um laço e mostre também
   os fatoriais de `0` até esse número.

8. **Adivinhe a base**  
   Sorteie uma base entre `A`, `T`, `C` e `G`. O usuário terá até três tentativas
   para acertar, recebendo uma mensagem de acerto ou erro.

9. **Tabuada selecionável**  
   Leia um número e mostre sua tabuada em um intervalo informado pelo usuário.
   Rejeite intervalos em que o início seja maior que o fim.

10. **Senha com tentativas**  
    Defina uma senha e permita até três tentativas. Normalize a entrada com
    `strip().lower()` e informe quando o acesso for bloqueado.

## Bloco 3 — Strings e listas (vetores)

11. **Limpeza de nomes**  
    Leia vários nomes até o usuário digitar `fim`. Remova espaços extras,
    padronize com `title()`, elimine nomes vazios e mostre a lista ordenada.

12. **Analisador de texto**  
    Leia uma frase e informe quantidade de caracteres, palavras, vogais,
    ocorrências de cada vogal e a palavra mais longa.

13. **Busca em vetor**  
    Leia dez números, procure um valor informado e mostre todas as posições em
    que ele aparece. Não use `in` para realizar a busca principal.

14. **Notas da turma**  
    Leia nomes e notas até o usuário encerrar. Mostre média, maior nota, menor
    nota, alunos aprovados e alunos em recuperação.

15. **Ordenação manual**  
    Ordene uma lista de números sem usar `sort()` ou `sorted()`. Explique em
    comentário qual estratégia foi utilizada.

16. **Matriz de notas**  
    Armazene as notas de três alunos em três disciplinas usando listas
    aninhadas. Mostre a média por aluno e por disciplina.

## Bloco 4 — Dicionários e conjuntos

17. **Cadastro de alunos**  
    Use um dicionário aninhado para guardar nome, curso e notas de cada aluno.
    Implemente cadastro, consulta, atualização e remoção por menu.

18. **Contador de bases**  
    Leia uma sequência de DNA, valide se contém somente `A`, `T`, `C` e `G`,
    conte cada base e mostre as porcentagens.

19. **Complemento de DNA e RNA**  
    A partir de uma sequência válida, gere a fita complementar de DNA e a fita
    de RNA usando dicionários. Preserve a sequência original.

20. **Inventário**  
    Modele produtos com código, nome, quantidade e preço. Informe estoque
    baixo, valor total armazenado e produto de maior valor.

21. **Palavras repetidas**  
    Leia um texto, normalize maiúsculas e pontuação e construa um dicionário
    de frequência. Mostre as cinco palavras mais comuns.

22. **Operações entre conjuntos**  
    Leia as bases presentes em duas sequências e mostre união, interseção e
    bases exclusivas de cada sequência.

## Bloco 5 — Funções, módulos e arquivos

23. **Biblioteca de conversões**  
    Separe funções de temperatura, área, reajuste salarial e média em
    `funcoes.py`. Crie `main.py` para importar e testar as funções.

24. **Validação reutilizável**  
    Crie funções para ler inteiro, número decimal e resposta `s/n`. As
    funções devem repetir a pergunta quando a entrada for inválida.

25. **Relatório de notas em arquivo**  
    Leia alunos e notas, grave um relatório `.txt` e permita carregar o arquivo
    para exibir a média e a situação de cada aluno.

26. **Cadastro em JSON**  
    Salve e carregue o cadastro de alunos em JSON. O programa não deve apagar
    os dados existentes ao cadastrar um novo aluno.

27. **Simulação reproduzível**  
    Gere uma sequência aleatória de DNA usando `random`, ofereça uma opção de
    `seed` e mostre que a mesma seed produz o mesmo resultado.

## Bloco 6 — Integração e interface

28. **Quiz de biologia**  
    Crie um quiz com perguntas, alternativas, pontuação, limite de tentativas e
    opção de reiniciar. Armazene as perguntas em uma lista de dicionários.

29. **Gerador de DNA no terminal**  
    Refaça o gerador existente com funções separadas para gerar, validar,
    complementar, converter para RNA e exibir uma sequência em lotes.

30. **Menu de análise reutilizável**  
    Reorganize o exercício anterior em módulos. Separe o menu, as funções de
    análise e a gravação do relatório, sem duplicar código.

31. **Desafio final — análise de sequências**  
    Combine menu, funções, dicionários, listas, arquivos e aleatoriedade em um
    programa que aceite sequências digitadas ou geradas, produza estatísticas e
    salve um relatório.

## Critérios de autoavaliação

- **Fundamentos:** entradas, conversões, condicionais e laços corretos.
- **Estruturas:** uso adequado de listas, dicionários e conjuntos.
- **Organização:** funções pequenas, nomes claros e módulos separados.
- **Robustez:** entradas inválidas não encerram o programa inesperadamente.
- **Evidência:** exemplos de execução e testes de casos de borda.
- **Evolução:** o exercício final reaproveita funções dos exercícios anteriores.
