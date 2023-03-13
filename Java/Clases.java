import java.util.Scanner;

class Intento{
    public static void main(String[] args){
        Input crear = new Input();
        String finalisimo = crear.getUserName();
        System.out.println("este amigo es: " + finalisimo);
    }
}

class Input{
    public String getUserName(){
        Scanner myObj = new Scanner(System.in);
        System.out.println("decímelo pibe");
        String finalisimo = myObj.nextLine().trim().toUpperCase();
        return finalisimo;
    } 
}