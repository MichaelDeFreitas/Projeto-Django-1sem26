-- ============================================================
--  STUDYFLOW - Banco de Dados
--  Projeto Integrador - 1º Semestre
-- ============================================================

CREATE DATABASE IF NOT EXISTS studyflow
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE studyflow;

-- ============================================================
-- TABELA: usuarios
-- Armazena os dados de cadastro e autenticação de cada usuário
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
  id           INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome         VARCHAR(100) NOT NULL,
  cpf          CHAR(11)     NOT NULL UNIQUE,          -- somente números
  idade        TINYINT      UNSIGNED NOT NULL,
  telefone     VARCHAR(15),
  email        VARCHAR(150) NOT NULL UNIQUE,
  senha_hash   VARCHAR(255) NOT NULL,                 -- bcrypt / password_hash()
  criado_em    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- TABELA: materias
-- Matérias cadastradas por cada usuário
-- ============================================================
CREATE TABLE IF NOT EXISTS materias (
  id           INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id   INT          UNSIGNED NOT NULL,
  nome         VARCHAR(100) NOT NULL,
  descricao    TEXT,
  criado_em    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- TABELA: anotacoes
-- Bloco de notas privado de cada usuário, vinculado a uma matéria
-- ============================================================
CREATE TABLE IF NOT EXISTS anotacoes (
  id           INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id   INT          UNSIGNED NOT NULL,
  materia_id   INT          UNSIGNED,                 -- NULL = nota geral
  titulo       VARCHAR(150) NOT NULL,
  conteudo     TEXT,
  criado_em    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP
                            ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (materia_id) REFERENCES materias(id)  ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================================
-- TABELA: sessoes_estudo
-- Registra cada sessão de estudo (tempo, matéria, data)
-- ============================================================
CREATE TABLE IF NOT EXISTS sessoes_estudo (
  id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id     INT          UNSIGNED NOT NULL,
  materia_id     INT          UNSIGNED,               -- NULL = sessão sem matéria específica
  duracao_seg    INT          UNSIGNED NOT NULL,       -- duração em segundos
  iniciado_em    DATETIME     NOT NULL,
  encerrado_em   DATETIME,
  criado_em      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (materia_id) REFERENCES materias(id)  ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================================
-- TABELA: temporizador
-- Guarda o estado atual do temporizador de cada usuário
-- (para manter o timer entre recarregamentos de página)
-- ============================================================
CREATE TABLE IF NOT EXISTS temporizador (
  id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id     INT          UNSIGNED NOT NULL UNIQUE, -- um por usuário
  segundos_acum  INT          UNSIGNED NOT NULL DEFAULT 0,
  rodando        TINYINT(1)   NOT NULL DEFAULT 0,      -- 0 = parado, 1 = rodando
  iniciado_em    DATETIME,
  atualizado_em  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                              ON UPDATE CURRENT_TIMESTAMP,

  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- DADOS DE EXEMPLO (pode apagar em produção)
-- ============================================================

-- Usuário de teste (senha: 123456 — troque por hash real em produção)
INSERT INTO usuarios (nome, cpf, idade, telefone, email, senha_hash)
VALUES ('Estudante Teste', '00000000000', 20, '11999999999',
        'teste@studyflow.com', '$2y$10$examplehashplaceholder12345');

-- Matérias de exemplo
INSERT INTO materias (usuario_id, nome, descricao) VALUES
  (1, 'Matemática',  'Funções, geometria e estatística'),
  (1, 'Português',   'Redação e interpretação de textos'),
  (1, 'História',    'Brasil colônia e história geral'),
  (1, 'Biologia',    'Citologia, genética e ecologia');

-- Anotação de exemplo
INSERT INTO anotacoes (usuario_id, materia_id, titulo, conteudo) VALUES
  (1, 1, 'Fórmula de Bhaskara', 'x = (-b ± √(b²-4ac)) / 2a');

-- Sessão de estudo de exemplo (30 minutos = 1800 seg)
INSERT INTO sessoes_estudo (usuario_id, materia_id, duracao_seg, iniciado_em, encerrado_em)
VALUES (1, 1, 1800, '2026-06-07 08:00:00', '2026-06-07 08:30:00');

-- Temporizador de exemplo (zerado)
INSERT INTO temporizador (usuario_id, segundos_acum, rodando)
VALUES (1, 0, 0);
