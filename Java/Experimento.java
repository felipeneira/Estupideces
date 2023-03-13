import java.util.Scanner;

class CFG{
    public static void main(String args[])
    {
        Input input = new Input();
        String userName = input.getUserName();
        if (userName.equals("KAVI")){
            System.out.println("Kavi");
        }
        else {
            System.out.println("Lucho");
        }
        System.out.println("Este es " + userName);
    }
}

class Input{
    public String getUserName(){
        Scanner myObj = new Scanner(System.in);
        System.out.println("Lucho o Kavi:");

        String userName = myObj.nextLine().trim().toUpperCase();
        while (!(userName.equals("1") || userName.equals("2"))){
            System.out.println("Solo ingrese '1' o '2':");
            userName = myObj.nextLine().trim().toUpperCase();
        }
        return userName;
    }
}


