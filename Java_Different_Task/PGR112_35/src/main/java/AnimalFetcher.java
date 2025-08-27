import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class AnimalFetcher {

    public static List<Animal> loadAll(Connection conn) throws SQLException {
        List<Animal> animals = new ArrayList<>();
        animals.addAll(fetchDogs(conn));
        animals.addAll(fetchCats(conn));
        animals.addAll(fetchBirds(conn));
        return animals;
    }

    private static List<Dog> fetchDogs(Connection conn) throws SQLException {
        String query = "SELECT * FROM Dog";
        List<Dog> list = new ArrayList<>();
       PreparedStatement stmt = conn.prepareStatement(query); ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                list.add(new Dog(rs.getInt("AnimalID"), rs.getString("Name"), rs.getInt("Age"),
                        rs.getBoolean("Vaccinated"), rs.getInt("ShelterID"), rs.getString("Breed"),
                        rs.getBoolean("ReadyForAdoption"), rs.getString("FoodType"), rs.getInt("DailyFoodAmount")));
            }

        return list;
    }

    private static List<Cat> fetchCats(Connection conn) throws SQLException {
        String query = "SELECT * FROM Cat";
        List<Cat> list = new ArrayList<>();
        PreparedStatement stmt = conn.prepareStatement(query); ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                list.add(new Cat(rs.getInt("AnimalID"), rs.getString("Name"), rs.getInt("Age"),
                        rs.getBoolean("Vaccinated"), rs.getInt("ShelterID"), rs.getString("Breed"),
                        rs.getBoolean("Neutered"), rs.getString("LitterType"), rs.getInt("DailyLitterAmount")));

        }
        return list;
    }

    private static List<Bird> fetchBirds(Connection conn) throws SQLException {
        String query = "SELECT * FROM Bird";
        List<Bird> list = new ArrayList<>();
        PreparedStatement stmt = conn.prepareStatement(query); ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                list.add(new Bird(rs.getInt("AnimalID"), rs.getString("Name"), rs.getInt("Age"),
                        rs.getBoolean("Vaccinated"), rs.getInt("ShelterID"), rs.getString("Species"),
                        rs.getBoolean("CanFly"), rs.getString("CageSize")));
            }

        return list;
    }
}
