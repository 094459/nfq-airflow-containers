// Simple Java class to query MySQL and export output in CSV to an S3 bucket
// requires a creation of an AWS Secret to store the MySQL credentials

package co.uk.beachgeek;

import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.secretsmanager.SecretsManagerClient;
import software.amazon.awssdk.services.secretsmanager.model.GetSecretValueRequest;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.FileWriter;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;

import org.json.JSONObject; // To parse JSON secret

public class DatabaseToS3Exporter {

    public static void main(String[] args) throws Exception {
        if (args.length != 7) {
            System.out.println("Usage: java DatabaseToS3Exporter <db-server> <db-name> <sql-query> <s3-bucket-name> <aws-region> <secret-arn> <filename>");
            return;
        }

        String dbServer = args[0];
        String dbName = args[1];
        String sqlQuery = args[2];
        String s3BucketName = args[3];
        String awsRegion = args[4];
        String secretArn = args[5];
        String fileName = args[6];

        // Retrieve MySQL credentials from AWS Secrets Manager
        SecretsManagerClient secretsManagerClient = SecretsManagerClient.builder()
                .region(Region.of(awsRegion))
                .build();

        GetSecretValueRequest getSecretValueRequest = GetSecretValueRequest.builder()
                .secretId(secretArn)
                .build();

        String secretString = secretsManagerClient.getSecretValue(getSecretValueRequest).secretString();
        JSONObject secretJson = new JSONObject(secretString);
        String username = secretJson.getString("username");
        String password = secretJson.getString("password");

        // Connect to the database
        String jdbcUrl = "jdbc:mysql://" + dbServer + ":3306/" + dbName;
        Connection connection = DriverManager.getConnection(jdbcUrl, username, password);
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

        // Add a conditional statement here that uses fileName as the .key value if it exists
        // Otherwise, use "uploaded-output.csv"

        String key = fileName;
        if (fileName == null) {
            key = "uploaded-output.csv";
        }
        System.out.println("Key: " + key);
        System.out.println("CSV File: " + csvFile);
        System.out.println("S3 Bucket: " + s3BucketName);
        System.out.println("AWS Region: " + awsRegion);

        PutObjectRequest putObjectRequest = PutObjectRequest.builder()
        .bucket(s3BucketName)
        .key(key)
        .build();

        s3Client.putObject(putObjectRequest, RequestBody.fromFile(Paths.get(csvFile)));

        connection.close();
    }
}
