# GoodWe Smart Charging Station

## Integrantes

* Diego de Oliveira Brandão - RM 569773
* Lucca Bertolini - RM 569552
* Raphaello Caffettani - RM 572334
* Cristhian Henrique Clementino - RM 574117
* Fabio Pena Vieira - RM 570441

## Sobre o projeto

O projeto consiste no desenvolvimento de uma estação inteligente de carregamento para veículos elétricos, simulada utilizando o Wokwi e programada em MicroPython com um Raspberry Pi Pico.

A solução foi desenvolvida com o conceito de gerenciamento inteligente de energia, buscando distribuir a energia disponível entre diferentes veículos de acordo com a demanda de carregamento e o nível de bateria de cada veículo.

O sistema gerencia três veículos elétricos simultaneamente, identificados como EV1, EV2 e EV3. Para cada veículo são armazenadas informações como:

* Identificação do veículo;
* Porcentagem da bateria;
* Potência solicitada;
* Potência efetivamente recebida;
* Estado do carregamento.

O projeto é uma solução educacional inspirada no conceito de gerenciamento inteligente de energia presente em soluções da GoodWe, não sendo uma reprodução de um produto comercial específico.

## Tecnologias utilizadas

* Raspberry Pi Pico
* MicroPython
* Wokwi
* LCD 16x2 com comunicação I2C
* LEDs indicadores
* Push buttons
* Comunicação serial

## Funcionamento

O sistema possui três cenários de disponibilidade de energia, selecionados por meio de três botões.

A demanda dos veículos é definida da seguinte forma:

| Veículo   | Bateria | Potência solicitada |
| --------- | ------: | ------------------: |
| EV1       |     40% |              2000 W |
| EV2       |     70% |              2500 W |
| EV3       |     25% |              3000 W |
| **Total** |         |          **7500 W** |

A estação compara a energia disponível com a demanda total dos veículos e define automaticamente quanto cada veículo receberá.

### Cenário 1 - Alta disponibilidade

Energia disponível: **8000 W**

Como a energia disponível é maior que a demanda total de 7500 W, todos os veículos recebem a potência solicitada.

* EV1: 2000 W
* EV2: 2500 W
* EV3: 3000 W

O LED verde de cada veículo é acionado, indicando carregamento ativo.

### Cenário 2 - Energia limitada

Energia disponível: **5000 W**

Como a energia disponível é menor que a demanda total, o sistema realiza uma distribuição proporcional da potência.

Os valores aproximados são:

* EV1: 1333 W
* EV2: 1666 W
* EV3: 2000 W

Nesse cenário, os veículos continuam carregando, porém com potência reduzida. Os LEDs amarelos são acionados para indicar carregamento reduzido.

### Cenário 3 - Baixa disponibilidade

Energia disponível: **2000 W**

Quando a energia disponível é muito baixa, o sistema utiliza o nível de bateria como critério de prioridade.

Como o EV3 possui a menor bateria, com 25%, ele recebe toda a energia disponível:

* EV1: 0 W
* EV2: 0 W
* EV3: 2000 W

O EV3 permanece em carregamento e os outros veículos ficam aguardando disponibilidade de energia.

Os LEDs vermelhos dos veículos que estão aguardando são acionados.

## Indicadores visuais

Cada veículo possui três LEDs:

* **Verde:** carregamento ativo com a potência solicitada;
* **Amarelo:** carregamento ativo com potência reduzida;
* **Vermelho:** veículo aguardando ou sem energia disponível.

Além dos LEDs, um LCD 16x2 apresenta informações sobre a energia disponível, demanda total, bateria e potência recebida por cada veículo.

As informações também são exibidas no monitor serial.

## Representação de dados

O projeto também demonstra a representação de um valor numérico em diferentes sistemas.

Por exemplo, para uma disponibilidade de energia de 5000 W:

* Decimal: 5000
* Hexadecimal: `0x1388`
* Binário: `1001110001000`

Essa representação demonstra como os dados podem ser armazenados e processados internamente pelo computador em diferentes bases numéricas.

## Algoritmo de gerenciamento

O sistema segue três regras principais:

1. Se a energia disponível for maior ou igual à demanda total, todos os veículos recebem a potência solicitada.
2. Se a energia for limitada, a potência é distribuída proporcionalmente entre os veículos.
3. Se a energia for muito baixa, o veículo com menor nível de bateria recebe prioridade e os demais aguardam.

Dessa forma, o sistema consegue adaptar automaticamente o carregamento de acordo com a disponibilidade de energia.

## Relação com Arquitetura de Computadores

O projeto permite visualizar diferentes conceitos relacionados à Arquitetura de Computadores.

### Entrada

Os botões funcionam como dispositivos de entrada, permitindo selecionar os diferentes cenários de disponibilidade de energia.

### Processamento

O Raspberry Pi Pico executa o programa em MicroPython e realiza os cálculos necessários para determinar a distribuição de energia.

### Memória

As informações dos veículos, como identificação, bateria e potência solicitada, são armazenadas durante a execução do programa.

### Saída

Os LEDs e o LCD representam as saídas do sistema, apresentando visualmente o estado do carregamento. O monitor serial também apresenta os dados processados.

### Comunicação

O LCD utiliza comunicação I2C para receber informações do Raspberry Pi Pico.

### Automação

A tomada de decisão sobre a distribuição da energia é realizada automaticamente pelo programa, sem necessidade de intervenção manual após a seleção do cenário.

## Estrutura do projeto

O projeto no Wokwi é composto principalmente pelos seguintes arquivos:

```text
main.py
diagram.json
```

O arquivo `main.py` contém a lógica de programação e gerenciamento da estação de carregamento.

O arquivo `diagram.json` contém a representação do circuito utilizado na simulação, incluindo o Raspberry Pi Pico, LCD, botões, LEDs e demais componentes.

## Links

### Vídeo de apresentação

https://youtu.be/O108EUoLCog

### Projeto no Wokwi

https://wokwi.com/projects/476054613345794049

## Conclusão

O projeto apresenta uma simulação de uma estação inteligente de carregamento capaz de gerenciar três veículos elétricos simultaneamente, adaptando a distribuição de energia de acordo com a disponibilidade e com as necessidades dos veículos.

A solução integra programação, eletrônica, comunicação, processamento de dados e automação, demonstrando na prática conceitos relacionados à Arquitetura de Computadores e ao gerenciamento inteligente de energia.
