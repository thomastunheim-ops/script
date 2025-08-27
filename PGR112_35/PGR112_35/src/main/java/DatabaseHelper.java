import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseHelper {
    private static  String uri = "jdbc:mysql://localhost:3306/ShelterDB";
    private static  String userName = "root";
    private static  String pswrd = "1234";

    public static Connection getConnection() throws SQLException {
        Connection dbConnection= DriverManager.getConnection(uri,userName,pswrd);
        return dbConnection;
    }
}
