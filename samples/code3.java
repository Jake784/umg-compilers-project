/*
  ======================================================
  Prueba de Estrés - Analizador Léxico (Fase 1)
  Probando límites de palabras, strings complejos
  y el nuevo contador de saltos de línea.
  ======================================================
*/
public class AnalisisAvanzado {

    public static void main(String[] args) {
        
        // 1. Probando los límites de palabras (Keywords vs Identificadores)
        // El escáner NO debe confundir estas variables con palabras reservadas
        int if_variable = 10;
        int whileContador = 20;
        
        // 2. Probando el reconocimiento de Strings con símbolos adentro
        String mensaje_texto = "Este String tiene (parentesis) y signos + - =";
        
        // 3. Operadores y variables con guion bajo
        int _resultadoFinal = if_variable + whileContador;
        
        if (_resultadoFinal >= 30) {
            _resultadoFinal = _resultadoFinal * 2;
        } else {
            return;
        }

        // ==========================================
        // NUEVOS ERRORES LÉXICOS INTENCIONALES
        // ==========================================
        
        // Error A: Comillas simples. 
        // Nuestra regla STRING_LIT solo acepta comillas dobles (""), 
        // así que las simples ('') darán error.
        String caracter = 'X'; 
        
        // Error B: Símbolo de interrogación.
        // No lo incluimos en nuestra lista de Puntuación ni de Operadores.
        int misterio = 10 ? 5;
        
        // Error C: Símbolo de dólar.
        // En Java real es válido, pero en nuestra expresión regular de IDENTIFIER 
        // solo permitimos [a-zA-Z_][a-zA-Z0-9_]*, así que el $ fallará.
        int precio$ = 500;
    }
}