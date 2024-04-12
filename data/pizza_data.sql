-- Generate sample pizza order data

-- Create table
CREATE TABLE pizza_orders (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  address VARCHAR(255),
  pizza VARCHAR(50),
  cost DECIMAL(10,2)
);

-- Insert rows
INSERT INTO pizza_orders (address, pizza, cost) VALUES
('789 Đường Nguyễn Thị Minh Khai, Quận 1, Thành phố Hồ Chí Minh', 'Cheese', 10.99),
('123 Đường Lê Lợi, Quận 1, Thành phố Hồ Chí Minh', 'Chicken Alfredo', 12.99),
('456 Đường Trần Phú, Quận 2, Thành phố Hồ Chí Minh', 'Pepperoni', 14.99),
('789 Đường Nguyễn Thị Minh Khai, Quận 1, Thành phố Hồ Chí Minh', 'Hawaiian', 16.99),
('123 Đường Lê Lợi, Quận 1, Thành phố Hồ Chí Minh', 'Cheese', 10.99),
('456 Đường Trần Phú, Quận 2, Thành phố Hồ Chí Minh', 'Chicken Alfredo', 12.99),
('789 Đường Nguyễn Thị Minh Khai, Quận 1, Thành phố Hồ Chí Minh', 'Pepperoni', 14.99),
('123 Đường Lê Lợi, Quận 1, Thành phố Hồ Chí Minh', 'Hawaiian', 16.99),
('789 Đường Nguyễn Thị Minh Khai, Quận 1, Thành phố Hồ Chí Minh', 'Cheese', 10.99),
('123 Đường Lê Lợi, Quận 1, Thành phố Hồ Chí Minh', 'Chicken Alfredo', 12.99),
('456 Đường Trần Phú, Quận 2, Thành phố Hồ Chí Minh', 'Pepperoni', 14.99),
('789 Đường Nguyễn Thị Minh Khai, Quận 1, Thành phố Hồ Chí Minh', 'Hawaiian', 16.99),
('123 Đường Lê Lợi, Quận 1, Thành phố Hồ Chí Minh', 'Cheese', 10.99),
('456 Đường Trần Phú, Quận 2, Thành phố Hồ Chí Minh', 'Chicken Alfredo', 12.99)


-- Verify row count
SELECT COUNT(*) FROM pizza_orders;
SELECT * from pizza_orders WHERE pizza = "Margherita";
SELECT * from pizza_orders; -- should return 100
