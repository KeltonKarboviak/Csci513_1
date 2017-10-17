import java.sql.*;
import oracle.jdbc.pool.OracleDataSource;

public class AddDeveloper {
    public static void main(String[] args) throws SQLException {
        String name = args[0];

        String database = System.getenv("ORACLE_HOST");
        String user = System.getenv("ORACLE_USER");
        String password = System.getenv("ORACLE_PASSWORD");

        // Open an OracleDataSource and get a connection
        OracleDataSource ods = new OracleDataSource();
        ods.setURL("jdbc:oracle:thin:@" + database);
        ods.setUser(user);
        ods.setPassword(password);
        Connection conn = ods.getConnection();

        String status = "";
        try {
            // Create and compose statement
            Statement stmt = conn.createStatement();
            String query = String.format("INSERT INTO developers (name) VALUES ('%s')", name);

            // Insert the data into the developers table
            stmt.executeUpdate(query);
            stmt.close();

            status = "success";
        } catch (SQLException e) {
            System.err.println(e);
            status = "error";
        } finally {
            System.out.printf("{\"status\": \"%s\", \"name\": \"%s\"}", status, name);

            // Commit and close the connection
            conn.close();
        }
    }
}
