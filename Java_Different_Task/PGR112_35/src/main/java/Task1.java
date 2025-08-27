import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.ArrayList;
import java.util.List;

public class Task1 {

    private static List<Shelter> shelterList=new ArrayList<>();
    private static List<Animal> animalList=new ArrayList<>();

    public static void main(String[] args) {
        try {


            readAllDataFromFile("animals.txt");
          Connection conn= DatabaseHelper.getConnection();

            conn.setAutoCommit(false);


            //store shelter to db

            for (Shelter shelter:shelterList) {
                PreparedStatement stmt = conn.prepareStatement(
                        "INSERT INTO Shelter (ShelterID, Name, Address, PhoneNumber) VALUES (?, ?, ?, ?)");

                stmt.setInt(1, shelter.getId());
                stmt.setString(2, shelter.getName());
                stmt.setString(3, shelter.getAddress());
                stmt.setString(4, shelter.getPhone());
                stmt.executeUpdate();
            }



            for (Animal animal:animalList)
            {
                if(animal instanceof Dog dog)
                {

                    PreparedStatement preparedStatement = conn.prepareStatement("INSERT INTO Dog VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
                    preparedStatement.setInt(1, dog.getId());
                    preparedStatement.setString(2, dog.getBreed());
                    preparedStatement.setString(3, dog.getAnimalName());
                    preparedStatement.setInt(4, dog.age);
                    preparedStatement.setBoolean(5, dog.vaccinated);
                    preparedStatement.setBoolean(6, dog.isReadyForAdoption());
                    preparedStatement.setInt(7, dog.shelterId);
                    preparedStatement.setString(8, dog.getFoodType());
                    preparedStatement.setInt(9, dog.getDailyFoodAmount());
                    preparedStatement.executeUpdate();

                }
                else
                if(animal instanceof Cat cat) {
                    PreparedStatement preparedStatement = conn.prepareStatement("INSERT INTO Cat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
                    preparedStatement.setInt(1, cat.getId());
                    preparedStatement.setString(2, cat.getBreed());
                    preparedStatement.setString(3, cat.getAnimalName());
                    preparedStatement.setInt(4, cat.age);
                    preparedStatement.setBoolean(5, cat.vaccinated);
                    preparedStatement.setBoolean(6, cat.isNeutered());
                    preparedStatement.setInt(7, cat.shelterId);
                    preparedStatement.setString(8, cat.getlType());
                    preparedStatement.setInt(9, cat.getDailyLitterAmount());
                    preparedStatement.executeUpdate();
                }

                else if(animal instanceof Bird bird)
                {
                    PreparedStatement preparedStatement = conn.prepareStatement("INSERT INTO Bird VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
                    preparedStatement.setInt(1, bird.getId());
                    preparedStatement.setString(2, bird.getSpecies());
                    preparedStatement.setString(3, bird.getAnimalName());
                    preparedStatement.setInt(4, bird.age);
                    preparedStatement.setBoolean(5, bird.vaccinated);
                    preparedStatement.setBoolean(6, bird.isCanFly());
                    preparedStatement.setInt(7, bird.shelterId);
                    preparedStatement.setString(8, bird.getCageSize());
                    preparedStatement.executeUpdate();
                }
            }


            conn.commit();
            conn.close();
            System.out.println("All data exported to database from text file..");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }



    public static void readAllDataFromFile(String fileName)
    {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(fileName));
            int totalShelters = Integer.parseInt(reader.readLine());


            for (int i = 0; i < totalShelters; i++) {
                int id = Integer.parseInt(reader.readLine());
                String name = reader.readLine();
                String address = reader.readLine();
                String phone = reader.readLine();
                reader.readLine();

                Shelter shelter=new Shelter(id,name,address,phone);
                shelterList.add(shelter);



            }

            reader.readLine();
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                int animalId = Integer.parseInt(line);
                String name = reader.readLine();
                int age = Integer.parseInt(reader.readLine());
                boolean vaccinated = Boolean.parseBoolean(reader.readLine());
                int shelterId = Integer.parseInt(reader.readLine());
                String type = reader.readLine().trim();


                    if(type.equalsIgnoreCase( "Hund")) {
                        String breedDog = reader.readLine();
                        boolean readyForAdoption = Boolean.parseBoolean(reader.readLine());
                        String food = reader.readLine();
                        int foodAmount = Integer.parseInt(reader.readLine());
                        Dog dog = new Dog(animalId, name, age, vaccinated, shelterId, breedDog, readyForAdoption, food, foodAmount);

                        animalList.add(dog);
                    }

                if(type.equalsIgnoreCase( "Katt")) {
                    String breedCat = reader.readLine();
                    boolean neutered = Boolean.parseBoolean(reader.readLine());
                    String litter = reader.readLine();
                    int litterAmt = Integer.parseInt(reader.readLine());
                    Cat cat = new Cat(animalId, name, age, vaccinated, shelterId, breedCat, neutered, litter, litterAmt);
                    animalList.add(cat);

                }

                if(type.equalsIgnoreCase( "Fugl"))
                {
                        String species = reader.readLine();
                        boolean canFly = Boolean.parseBoolean(reader.readLine());
                        String cageSize = reader.readLine();
                        Bird bird=new Bird(animalId,name,age,vaccinated,shelterId,species,canFly,cageSize);
                        animalList.add(bird);

                }

                reader.readLine();
            }




        }
        catch (Exception e)
        {

            new RuntimeException(e);
        }
    }





}
