Sistema versátil de reservas

O sistema fará o cadastro de novos membros, recuperação de senhas, e armazenamento de informações de diferentes formatos em um banco de dados.
Dentro do sistema será possível agendar, cancelar e consultar reservas por parte do usuário
Dentro do sistema será possível gerenciar reservas, horários e serviços por parte dos administradores

Os administradores acessarão o sistema através de um login e senha únicos (admin123, por exemplo) e cada ação tanto dos administradores quanto dos usuários irá gerar um log que
ficará salvo no próprio sistema ou salvará em um arquivo .txt

O sistema irá armazenar:
1. ID do cliente
2. Senha do cliente
3. Nome do cliente
4. Data de nascimento
5. Endereço
6. Telefone
7. Reservas
8. Horários disponíveis
9. Serviços disponíveis

Dentro do sistema ele irá apresentar:
1. Botão para adicionar reserva
2. Botão para editar reserva (com regras, por exemplo, até 1 dia antes da data marcada)
3. Botão remover reserva (com regras, por exemplo, até 1 dia antes da data marcada)
4. Botão de Opções
5. Botão para editar dados do perfil

________________________________________________________________________________________________________________________________________________
http://127.0.0.1:5000/ -> Para login dos usuários
http://127.0.0.1:5000/index_admin -> Para login dos administradores
________________________________________________________________________________________________________________________________________________

- Sistema feito em Flask utilizando Python para o back-end
- HTML e CSS para o front-end
- Sqlite para criação do banco de dados e DBeaver para exibição e manipulação dos dados


 * Fazer com que toda ação do usuário (adicionar reserva, editar reserva, cancelar reserva e recuperar senha) seja salva e retorne como log para o usuário
 * Caso um usuário tente fazer reserva em uma data que já foi reservada por outro usuário o sistema irá avisar o usuário atual que a data está indisponível
 * Fazer com que cada tipo de serviço tenha um tempo para a conclusão do serviço, por exemplo se um cliente pediu o serviço_1 que demora 30 minutos e reservou as
 13 horas então o próximo horário livre será a partir de 13:30 em diante. Isso evitará reservas muito próximas.
* fazer com que os administradores consigam gerenciar os serviços, os horários, as reservas e os clientes