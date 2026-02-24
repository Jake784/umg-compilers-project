/*
  Programa de Prueba Avanzado
  Analizador Léxico - Fase 1
*/
public class CalculadoraAvanzada {

    public static void main(String[] args) {
        int limite = 100;
        int contador = 0;
        
        // Probando un ciclo while y operadores relacionales
        while (contador < limite) {
            contador = contador + 1;
            
            if (contador == 50) {
                String mensaje = "Llegamos a la mitad del calculo.";
                return; 
            } else {
                int calculoTemporal = contador * 2;
            }
        }
        
        // Probando el reconocimiento de numeros decimales
        int factorMultiplicador = 3.14159; 
        
        // ==========================================
        // SECCION DE ERRORES LEXICOS INTENCIONALES
        // ==========================================
        
        // 1. Un simbolo de arroba
        int @variableMala = 5;
        
        // 2. Un simbolo de numeral/hash
        String #textoRoto = "Falla";
        
        // 3. Un caracter de potencia (no incluido en nuestros operadores)
        contador = contador ^ 2;
    }
}