<a id="inicio"></a>
## MI Concorrência e Conectvidade - Consumo de Energia Inteligente


### Instalação

**A execução dos comandos deve seguir exatamente esta ordem**

## Execução do servidor
`python3 servidor.py`

## Execução do medidor  (Talvez separar os arquivos em pastas)
`python3 medidor.py`

## Execução da CLI do usuário
`python3 user_interface.py`

## Seções

&nbsp;&nbsp;&nbsp;[**1.** Introdução](#secao1)
&nbsp;&nbsp;&nbsp;[**2.** Fundamentação Teórica](#secao2)
&nbsp;&nbsp;&nbsp;[**3.** Metdologia](#secao3)
&nbsp;&nbsp;&nbsp;[**4.** Resultados](#secao4)
&nbsp;&nbsp;&nbsp;[**5.** Conclusão](#secao5)

<a id='secao1'><a/>
## Introdução

Será descrito aqui o funcionamento de um sistema que simula o comportamento de dispositivos em uma rede IOT que enviam informação para um servidor central. Constituindo-se de uma API REST, Medidore(s) Inteligente(s), capazes de envias informações para um servidor, e uma interface de usuário.
Tanto a API quando o Medidor foram construídos sobre *sockets TCP*.

Neste contexto, a **API REST** dispõe das seguinte informações:
	- Consumo de Energia
	- Fatura de Cada Cliente
	- Alerta de consumo	

**Medidor Inteligente**
 - Auto-registro
 - Detecção de consumo
 - Envio do consumo aAPI periodicamente.

<a id='secao2'><a/>
## Fundamentação Teórica

Para a criação deste sistema foi necessária a utilização de um servidor na forma de API e clientes na forma de medidor e CLI do usuário.
Levando em consideração tudo o que foi dito, um servidor pode ser entendido como um sistema computacional que provê serviços que podem ser consumidos por outros sistemas computacionais, uma API é um servidor, porém que se comunica por meio de requisições HTTP e os dados contidos nesta requisições estão em formato JSON.
Um cliente pode ser definido como a entidade que consome um recurso de um servidor.
Docker é um software de código aberto que permite a criação de máquina virtuais, bem como a virtualização de aplicações, os Containers, ambientes isolados que podem ser instalados e criados por meio do docker.

## Metodologia

Todos os dispositivos do sistema foram criados sobre sockets, de tal forma que para troca de mensagens foi escolhida como codificação UTF-8.
Toda a comunicação entre as entidades do sistema, é feita por meio de sockets. Por meio do protocolo HTTP a comunicação entre a API e a Interface de linha de comando é feita, por outro lado o envio de informações por parte do medidor para o servidor é realizada por meio de mensagens sockets codificadas em UTF-8.
Tanto a API quanto a CLI do usuário fazem a utilização do protocolo HTTP para realizarem as suas comunicações.


## Resultados

A solução do problema conta com 3 entidades. Servidor, CLI do usuário e o Medidor.

## Servidor
O servidor é capaz de responder requisições HTTP e mensagens socket codificadas em UTF-8, e capaz de lidar com várias conexões simultâneas de tal forma que possui as seguintes rotas:
	- clientes utiliza o método HTTP GET fornece os dados de data, hora e consumo de cada cliente registrado, sendo capaz de aceitar parâmetros query
	- faturas - guarda a fatura de todos os dispositivos cadastrados, sendo capaz de aceitar filtros por meio de parâmetros query


## Medidor
O medidor, ao ser executado, requisita ao servidor a sua identificação (UUID) e logo após faz o seu cadastro, ele mesmo.
O medidor executa em duas linha, a primeira é responsável por enviar os seus dados de consumo, enquanto a segunda é capaz de fornecer uma interface de linha de comando ao usuário, esta permite o aumento o redução do consumo de energia de forma manual.


## Interface do Usuário

A interface do usuário permite com que este acompanhe o seu consumo, bem como é capaz de alertá-lo sobre um aumento abrupto em seu consumo, dessa forma, também é possível, por meio da interface acompanhar o valor de sua fatura mensal. 


## Conclusão

O sistema desenvolvido é capaz de simular de forma fidedígna o funcionamento de medidores em uma rede IOT que enviam informações para uma entidade central, contudo há melhorias que poderiam ser realizadas, a substituição da comunicação TCP pela UDP por parte da comunicação entre o servidor e API certamente evita um overhead ao enviar os dados, pois estes são frequentemente enviados.