import java.util.Scanner;
class Calculadora{
    public static void main(String[] args){
        System.out.println("Ingresa el primer número");
        Numero primero = new Numero();
        int numero1 = primero.Number();
        System.out.println("Ingresa el segundo número");
        Numero segundo = new Numero();
        int numero2 = segundo.Number();
        System.out.println("¿Que operación quieres hacer?");
        Simbolo operacion =  new Simbolo();
        String simbolos = operacion.simbolo();
        if (simbolos.equals("SUMAR") || simbolos.equals("SUMA") || simbolos.equals("ADICION")){
            System.out.println("El resultado es: " + (numero1 + numero2));
        }
        if (simbolos.equals("RESTAR") || simbolos.equals("RESTA") || simbolos.equals("SUSTRACCION")){
            System.out.println("El resultado es: " + (numero1 - numero2));
        }
        if (simbolos.equals("MULTIPLICACION") || simbolos.equals("MULTIPLICAR")){
            System.out.println("El resultado es: " + (numero1 * numero2));
        }
        if (simbolos.equals("DIVISION") || simbolos.equals("DIVIDIR")){
            System.out.println("El resultado es: " + (numero1 / numero2));
        }
    }
}
class Numero{
    public int Number(){
        int numero = new Scanner(System.in).nextInt();
        int numeros = numero;
        return numeros;
    }
}
class Simbolo{
    public String simbolo(){
        Scanner symbol = new Scanner(System.in);    
        String simbolos = symbol.nextLine().trim().toUpperCase();
        return simbolos;
    } 
}