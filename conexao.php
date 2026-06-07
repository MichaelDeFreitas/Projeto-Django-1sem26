<?php
// ============================================================
//  STUDYFLOW - Conexão com o Banco de Dados
// ============================================================

$host     = "localhost";   // endereço do banco (XAMPP = localhost)
$usuario  = "root";        // usuário padrão do XAMPP
$senha    = "";            // senha padrão do XAMPP é vazia
$banco    = "studyflow";   // nome do banco que você criou

$conn = new mysqli($host, $usuario, $senha, $banco);

// Verifica se conectou com sucesso
if ($conn->connect_error) {
    die("Erro na conexão: " . $conn->connect_error);
}

// Define o charset pra evitar problemas com acentos
$conn->set_charset("utf8mb4");
?>