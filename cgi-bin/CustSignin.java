import java.sql.*;
import oracle.jdbc.pool.OracleDataSource;

public class CustSignin {
    public static void main(String[] args) throws SQLException {
        String username = args[0];

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
        int id = -1;
        try {
            // Create and compose statement
            Statement stmt = conn.createStatement();

            ResultSet rset;

            // See if username exists in database
            String query = String.format("SELECT id FROM customers WHERE username = '%s'", username);

            rset = stmt.executeQuery(query);

            boolean exists = rset.next();

            if (exists) {
                // Customer exists, so we get their ID
                id = rset.getInt(1);
            } else {
                // Customer does not exist, so we insert them into the database
                query = String.format("INSERT INTO customers (username) VALUES ('%s')", username);
                stmt.executeUpdate(query);

                // Now retrieve the newly added customer's ID
                query = String.format("SELECT id FROM customers WHERE username = '%s'", username);
                rset = stmt.executeQuery(query);

                if (rset.next())
                    id = rset.getInt("id");

                rset.close();
            }

            rset.close();
            stmt.close();

            status = "success";
        } catch (SQLException e) {
            System.err.println(e);
            status = "error";
        } finally {
            System.out.printf("{\"status\": \"%s\", \"id\": %d, \"username\": \"%s\"}", status, id, username);

            // Commit and close the connection
            conn.close();
        }
    }
}
