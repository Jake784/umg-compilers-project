public class StressTestParser {
    public static void main(String[] args) {
        // Todo bien aquí
        int base = 10;
        int altura = 5;
        
        // ❌ ERROR 1: Falta el punto y coma al final
        int areaRectangulo = base * altura
        
        // ✅ RECUPERACIÓN 1: El parser debe saltarse el error anterior y lograr leer esto
        int perimetro = base + base + altura + altura;
        
        // ❌ ERROR 2: Falta el paréntesis derecho de la condición
        while (perimetro > 0 {
            perimetro = perimetro - 1;
        }
        
        // ❌ ERROR 3: Expresión matemática incompleta (operador colgante)
        int calculoRoto = 100 / ;
        
        // ✅ RECUPERACIÓN FINAL: El AST DEBE mostrar este nodo al final del árbol
        boolean pruebaSuperada = true;
    }
}