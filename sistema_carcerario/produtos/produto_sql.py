# SQL para criar a tabela 'presidiarios' se ela não existir.
CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS presidiarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    crime TEXT NOT NULL,
    cela INTEGER NOT NULL
)
'''

# SQL para inserir um novo presidiario.
INSERT_PRESIDIARIO = '''
INSERT INTO presidiarios (nome, data_nascimento, crime, cela)
VALUES (?, ?, ?, ?)
'''

# SQL para selecionar um presidiario específico pelo seu ID.
SELECT_PRESIDIARIO = '''
SELECT id, nome, data_nascimento, crime, cela
FROM presidiarios
WHERE id = ?
'''

# SQL para selecionar todos os presidiarios da tabela.
SELECT_TODOS_PRESIDIARIOS = '''
SELECT id, nome, data_nascimento, crime, cela
FROM presidiarios
'''

# SQL para atualizar os dados de um presidiario existente, identificado pelo ID.
UPDATE_PRESIDIARIO = '''
UPDATE presidiarios
SET nome = ?, data_nascimento = ?, crime = ?, cela = ?
WHERE id = ?
'''

# SQL para excluir um presidiario da tabela, identificado pelo ID.
DELETE_PRESIDIARIO = '''
DELETE FROM presidiarios
WHERE id = ?
'''
