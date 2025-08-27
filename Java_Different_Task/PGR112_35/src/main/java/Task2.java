import java.sql.Connection;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Task2 {
    private static  Connection conn;
    private static  List<Animal> animals=new ArrayList<>();
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        try {
            conn = DatabaseHelper.getConnection();
            animals= AnimalFetcher.loadAll(conn);
            run();
        } catch (SQLException e) {
            System.out.println(" Database Error: " + e.getMessage());
        }
    }



    public static void run() {
        while (true) {
            displayMenu();
            switch (scanner.nextLine()) {
                case "1" : showAllAnimals(); break;
                case "2" : showFlyingBirds(); break;
                case "3" : showVaccinatedAnimals(); break;
                case "4":searchAnimalsByName(); break;
                case "5" : {
                    System.out.println("Exiting.....");
                    return;
                }
                default : System.out.println("Invalid option. Try again.");break;
            }
        }
    }

    private static void displayMenu() {
        System.out.println("""
               **********************************
                  *****Select An Option****
               **********************************
                1. View all animals
                2. View animals that can fly
                3. View vaccinated animals
                4. Search animals by name
                5. Exit
                Choose an option:\s""");
    }

    private static void showAllAnimals() {
        System.out.println("\n***All Animals***");
        for (Animal a : animals) {
            if (a instanceof Dog d)
                System.out.println("Dog - ID: " + d.id + ", Name: " + d.animalName +
                        ", Breed: " + d.getBreed() + ", Age: " + d.age + ", Vaccinated: " + d.vaccinated);
            else if (a instanceof Cat c)
                System.out.println("Cat - ID: " + c.id + ", Name: " + c.animalName +
                        ", Breed: " + c.getBreed() + ", Age: " + c.age + ", Vaccinated: " + c.vaccinated);
            else if (a instanceof Bird b)
                System.out.println("Bird - ID: " + b.id + ", Name: " + b.animalName +
                        ", Species: " + b.getSpecies() + ", Age: " + b.age + ", Vaccinated: " + b.vaccinated);
        }
    }

    private static void showFlyingBirds() {
        System.out.println("\n***Animals That Can Fly***");
        animals.stream()
                .filter(a -> a instanceof Bird b && b.isCanFly())
                .map(b -> (Bird) b)
                .forEach(b -> System.out.println("Bird - ID: " + b.id + ", Name: " + b.animalName +
                        ", Species: " + b.getSpecies() + ", Cage Size: " + b.getCageSize()));
    }

    private static void showVaccinatedAnimals() {
        System.out.println("\n***Vaccinated Animals***");

        for (int i = 0; i < animals.size(); i++) {
            Animal a = animals.get(i);
            if (a.vaccinated) {
                String type;
                if (a instanceof Dog) {
                    type = "Dog";
                } else if (a instanceof Cat) {
                    type = "Cat";
                } else {
                    type = "Bird";
                }
                System.out.println(type + " - ID: " + a.id + ", Name: " + a.animalName);
            }
        }
    }


    private static void searchAnimalsByName() {
        System.out.print("Enter part or full animal name to search: ");
        String input = scanner.nextLine().toLowerCase();
        boolean found = false;

        for (Animal animal : animals) {
            if (animal.animalName.toLowerCase().contains(input)) {
                String type = animal instanceof Dog ? "Dog" :
                        animal instanceof Cat ? "Cat" : "Bird";
                System.out.println(type + " - ID: " + animal.id + ", Name: " + animal.animalName +
                        ", Age: " + animal.age + ", Vaccinated: " + animal.vaccinated);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No animals found with the given name.");
        }
    }

}
