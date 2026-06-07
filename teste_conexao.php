<?php
// ============================================================
//  STUDYFLOW - Teste de Conexão
//  DELETE este arquivo antes de colocar em produção!
// ============================================================

require_once "conexao.php";

echo "<h2>✅ Conexão com o banco OK!</h2>";

// Testa se as tabelas existem
$tabelas = ["usuarios", "materias", "anotacoes", "sessoes_estudo", "temporizador"];

echo "<ul>";
foreach ($tabelas as $tabela) {
    $result = $conn->query("SELECT COUNT(*) as total FROM $tabela");
    $row = $result->fetch_assoc();
    echo "<li>📋 Tabela <strong>$tabela</strong>: {$row['total']} registro(s)</li>";
}
echo "</ul>";

$conn->close();
?>