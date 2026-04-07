public class FibonacciSequence {
    public static void main(String[] args) {
        // Declaración de variables iniciales
        int n = 10;
        int terminoActual = 0;
        int terminoSiguiente = 1;
        int sumaTemporal = 0;
        int contador = 1;

        // Ciclo para calcular la secuencia
        while (contador <= n) {
            // El bloque de operaciones matemáticas y reasignaciones
            sumaTemporal = terminoActual + terminoSiguiente;
            terminoActual = terminoSiguiente;
            terminoSiguiente = sumaTemporal;
            
            // Incremento del contador
            contador = contador + 1;
        }
    }
}