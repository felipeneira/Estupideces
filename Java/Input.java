import java.util.Scanner;

class Input{
    public static void main(String[] args){
        Scanner myObj = new Scanner(System.in);
        System.out.println("Lucho o Kavi");

        String userName = myObj.nextLine();
        System.out.println("Este es " + userName);
    }
}