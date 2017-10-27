import java.sql.*;
import oracle.jdbc.pool.OracleDataSource;

public class GetUsernameFromId {
    public static void main(String[] args) throws SQLException {
        String userId = args[0];

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
        String username = "";
        try {
            // Create and compose statement
            Statement stmt = conn.createStatement();

            ResultSet rset;

            String query = String.format("SELECT username FROM customers WHERE id = %s", userId);

            // Retrieve the customer's username from the customers table
            rset = stmt.executeQuery(query);

            if (rset.next())
                username = rset.getString(1);

            stmt.close();
            rset.close();

            status = "success";
        } catch (SQLException e) {
            System.err.println(e);
            status = "error";
        } finally {
            System.out.printf("{\"status\": \"%s\", \"username\": \"%s\"}", status, username);

            // Commit and close the connection
            conn.close();
        }
    }
}
