package co.uk.beachgeek;

import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.FileWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.nio.file.Paths;

public class DatabaseToS3ExporterRegion {

    public static void main(String[] args) throws Exception {
        if (args.length != 5) {
            System.out.println("Usage: java DatabaseToS3Exporter <db-server> <db-name> <sql-query> <s3-bucket-name> <aws-region>");
            return;
        }

        String dbServer = args[0];
        String dbName = args[1];
        String sqlQuery = args[2];
        String s3BucketName = args[3];
        String awsRegion = args[4];

        // Connect to the database
        String jdbcUrl = "jdbc:mysql://" + dbServer + ":3306/" + dbName;
        Connection connection = DriverManager.getConnection(jdbcUrl, "root", "password");  // Assuming default credentials, modify if different
        var statement = connection.createStatement();
        var resultSet = statement.executeQuery(sqlQuery);

        // Export result to CSV
        String csvFile = "output.csv";
        try (var writer = new FileWriter(csvFile)) {
            int columnCount = resultSet.getMetaData().getColumnCount();
            while (resultSet.next()) {
                for (int i = 1; i <= columnCount; i++) {
                    writer.write(resultSet.getString(i));
                    if (i < columnCount) {
                        writer.write(",");
                    }
                }
                writer.write("\n");
            }
        }

        // Upload CSV to S3
        S3Client s3Client = S3Client.builder()
                .region(Region.of(awsRegion))
                .build();

        PutObjectRequest putObjectRequest = PutObjectRequest.builder()
                .bucket(s3BucketName)
                .key("uploaded-output.csv")
                .build();

        s3Client.putObject(putObjectRequest, RequestBody.fromFile(Paths.get(csvFile)));

        connection.close();
    }
}
