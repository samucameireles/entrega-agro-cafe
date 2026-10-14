# Controle de Perdas na Colheita de Café

**Curso:** Tecnologia em Inteligência Artificial  
**Grupo:** Samuel da Silva Meireles

## 1. Problema tratado

Parte da produção de café se perde durante a colheita e o produtor, em geral, só percebe isso no final da safra. Uma perda acima do normal significa dinheiro que deixou de entrar e, muitas vezes, uma regulagem de máquina ou um manejo que poderia ter sido corrigido a tempo.

O setor tratado é o de **produção** do agronegócio, com foco na colheita de café. O sistema é a continuação da FarmTech Solutions, que na fase anterior cuidou da irrigação.

## 2. Solução

Um programa em Python, executado no prompt de comando, em que o produtor registra cada colheita por talhão (área, produção estimada, produção colhida, método e preço da saca). A partir desses dados o sistema calcula:

- a **perda percentual** de cada talhão;
- a **classificação** da perda (OK, ATENÇÃO ou CRÍTICO) comparada ao limite do método de colheita;
- o **prejuízo em reais** e a parte dele que seria **evitável**, ou seja, o que passou do limite aceitável;
- a **produtividade** em sacas por hectare;
- uma **recomendação** de ação para cada talhão e um resumo comparando colheita manual e mecânica.

O diferencial é transformar a perda em valor financeiro e separar quanto dele é evitável, o que ajuda a decidir onde agir primeiro.

## 3. Regras de negócio

| Método | Limite de perda aceitável |
|---|---|
| Manual | 5% |
| Mecânica | 15% |

Os limites vêm de estudos sobre perdas na colheita (colheita manual raramente passa de 5% e a mecânica chega a cerca de 15%), citados no material da atividade. Como esses números são do setor canavieiro, usamos como referência inicial para o café e deixamos os valores editáveis no arquivo `data/parametros.json`.

Classificação: até o limite é **OK**; até 1,5 vez o limite é **ATENÇÃO**; acima disso é **CRÍTICO**.

## 4. Conteúdo da disciplina aplicado

| Requisito | Onde está |
|---|---|
| Subalgoritmos (funções com parâmetros) | `calculos.py`, `validacao.py`, `arquivos.py`, `main.py` |
| Lista | lista de colheitas (`lotes`) |
| Tupla | `METODOS` em `calculos.py` |
| Dicionário | cada colheita, os limites de perda e os resultados da análise |
| Tabela de memória | lista de dicionários exibida em tabela na opção "Listar colheitas" |
| Arquivos texto e JSON | `data/colheitas.json`, `data/parametros.json` e `data/relatorio.txt` |
| Banco de dados Oracle | `banco.py` (biblioteca `oracledb`) |
| Validação de entradas | `validacao.py` |

## 5. Validação das entradas

Todas as perguntas ficam se repetindo até a resposta ser válida. O programa rejeita campos vazios, texto no lugar de número, valores zero ou negativos, método de colheita diferente de manual/mecânica e produção colhida maior que a estimada. Vírgula e ponto são aceitos como separador decimal.

## 6. Como executar

Requer Python 3.

```bash
pip install -r requirements.txt
python src/main.py
```

Menu:

```
1 - Registrar colheita
2 - Listar colheitas
3 - Analisar perdas
4 - Gerar relatório (TXT)
5 - Enviar dados para o Oracle
6 - Carregar dados do Oracle
0 - Sair
```

Os dados são salvos automaticamente em `data/colheitas.json` a cada novo registro. O arquivo já vem com três colheitas de exemplo.

## 7. Banco Oracle

As opções 5 e 6 usam a tabela `colheita_cafe`, criada automaticamente na primeira conexão. O usuário e a senha são pedidos no prompt (a senha não aparece na tela) ou lidos das variáveis de ambiente `ORACLE_USER` e `ORACLE_PASSWORD`. O endereço padrão é `oracle.fiap.com.br:1521/ORCL` e pode ser trocado pela variável `ORACLE_DSN`.

Se o Oracle não estiver acessível, o programa avisa e continua funcionando com os arquivos locais.

**Situação do teste:** a integração foi implementada com a biblioteca `oracledb`, mas no momento da entrega a conta do grupo no servidor da FIAP estava bloqueada (erro ORA-28000), por isso o envio e a carga de dados não puderam ser validados no banco real. O restante do sistema foi testado e funciona normalmente.

## 8. Estrutura

```
src/
  main.py        menu e fluxo do programa
  calculos.py    perda, prejuízo, classificação e recomendação
  validacao.py   leitura e validação das entradas
  arquivos.py    JSON, relatório em texto e formatação de valores
  banco.py       conexão e comandos Oracle
data/
  parametros.json
requirements.txt
```

## 9. Exemplo de uso

Talhão A1, colheita manual, 200 sacas estimadas e 150 colhidas, saca a R$ 1.500,00: perda de 25% (limite de 5%), classificação **CRÍTICO**, prejuízo de R$ 9.500,00 sendo R$ 7.600,00 evitável.
