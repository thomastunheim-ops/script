import java.sql.Connection;
import java.util.List;
import java.util.Scanner;

public class Menu {
    private final Connection conn;
    private final List<Animal> animals;
    private final Scanner scanner = new Scanner(System.in);

    public Menu(Connection conn, List<Animal> animals) {
        this.conn = conn;
        this.animals = animals;
    }

    public void run() {
        while (true) {
            displayMenu();
            switch (scanner.nextLine()) {
                case "1" -> showAllAnimals();
                case "2" -> showFlyingBirds();
                case "3" -> showVaccinatedAnimals();
                case "4"->searchAnimalsByName();
                case "5" -> {
                    System.out.println("Goodbye!");
                    return;
                }
                default -> System.out.println("Invalid option. Try again.");
            }
        }
    }

    private void displayMenu() {
        System.out.println("""
                -------------------------------
                   Animal 
                          Shelter
                                   Menu
                -------------------------------
                1. View all animals
                2. View animals that can fly
                3. View vaccinated animals
                4. Search animals by name
                5. Exit
                Choose an option:\s""");
    }

    private void showAllAnimals() {
        System.out.println("\n--- All Animals ---");
        for (Animal a : animals) {
            if (a instanceof Dog d)
                System.out.printf("Dog - ID: %d, Name: %s, Breed: %s, Age: %d, Vaccinated: %b%n",
                        d.id, d.animalName, d.getBreed(), d.age, d.vaccinated);
            else if (a instanceof Cat c)
                System.out.printf("Cat - ID: %d, Name: %s, Breed: %s, Age: %d, Vaccinated: %b%n",
                        c.id, c.animalName, c.getBreed(), c.age, c.vaccinated);
            else if (a instanceof Bird b)
                System.out.printf("Bird - ID: %d, Name: %s, Species: %s, Age: %d, Vaccinated: %b%n",
                        b.id, b.animalName, b.getSpecies(), b.age, b.vaccinated);
        }
    }

    private void showFlyingBirds() {
        System.out.println("\n--- Animals That Can Fly ---");
        animals.stream()
                .filter(a -> a instanceof Bird b && b.isCanFly())
                .map(b -> (Bird) b)
                .forEach(b -> System.out.printf("Bird - ID: %d, Name: %s, Species: %s, Cage Size: %s%n",
                        b.id, b.animalName, b.getSpecies(), b.getCageSize()));
    }

    private void showVaccinatedAnimals() {
        System.out.println("\n--- Vaccinated Animals ---");
        animals.stream()
                .filter(a -> a.vaccinated)
                .forEach(a -> System.out.printf("%s - ID: %d, Name: %s%n",
                        a instanceof Dog ? "Dog" : a instanceof Cat ? "Cat" : "Bird", a.id, a.animalName));
    }


    private void searchAnimalsByName() {
        System.out.print("Enter part or full animal name to search: ");
        String input = scanner.nextLine().toLowerCase();
        boolean found = false;

        for (Animal animal : animals) {
            if (animal.animalName.toLowerCase().contains(input)) {
                String type = animal instanceof Dog ? "Dog" :
                        animal instanceof Cat ? "Cat" : "Bird";
                System.out.printf("%s - ID: %d, Name: %s, Age: %d, Vaccinated: %b%n",
                        type, animal.id, animal.animalName, animal.age, animal.vaccinated);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No animals found with the given name.");
        }
    }

}
