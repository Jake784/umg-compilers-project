public class PruebaDeFuego {
    public static void main(String[] args) {
        // 1. Arranque limpio y válido
        int limite = 100;
        int contador = 0;

        // 2. ERRORES LÉXICOS: Caracteres inválidos (@ y #)
        // El Scanner debe atraparlos en su tabla de errores léxicos.
        int @variableRota = 10;
        contador = contador + #5;

        // 3. ERROR SINTÁCTICO: Falta el punto y coma (;)
        // El Parser debe quejarse, pero el Scanner lo leerá bien.
        int saltoDeLinea = 20
        
        // 4. RECUPERACIÓN 1: El AST debe lograr dibujar esto a pesar del caos de arriba
        int puntoDeControl = 1;

        // 5. ERROR SINTÁCTICO: Falta cerrar el paréntesis de la condición
        while (contador < limite {
            contador = contador + 10;
        }

        // 6. COMBO (LÉXICO + SINTÁCTICO): Símbolo extraño (~) y operador colgante (+)
        int locuraTotal = 50 + ~ ;

        boolean compiladorSobrevive = true;
    }
}