import java.sql.*;
import java.io.*;
import oracle.jdbc.*;
import oracle.jdbc.pool.OracleDataSource;

public class AddDeveloper {
    public static void main(String[] args) throws SQLException {
        System.out.printf("Content-type: application/json\n\n");

        String name = args[0];

        String user = "kkarboviak";
        String password = "ModernWarfare3";
        String database = "oracle1.aero.und.edu:1521/cs513.aero.und.edu";

        // Open an OracleDataSource and get a connection
        OracleDataSource ods = new OracleDataSource();
        ods.setURL("jdbc:oracle:thin:@" + database);
        ods.setUser(user);
        ods.setPassword(password);
        Connection conn = ods.getConnection();

        try {
            // Create and compose statement
            Statement stmt = conn.createStatement();
            String query = String.format("INSERT INTO developers (name) VALUES ('%s')", name);

            // Insert the data into the developers table
            stmt.executeUpdate(query);
            stmt.close();

            System.out.println("{\"status\": \"success\"}");
        } catch (SQLException e) {
            System.err.println(e);
            System.out.println("{\"status\": \"error\"}");
        } finally {
            // Commit and close the connection
            conn.close();
        }
    }
}
