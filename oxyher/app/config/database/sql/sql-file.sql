DROP DATABASE oxyher;
CREATE DATABASE oxyher;
use oxyher;
CREATE TABLE `user_auth` (
  `id` bigint AUTO_INCREMENT UNIQUE,
  `username` varchar(255) PRIMARY KEY,
  `password` varchar(255),
  `google_email_auth` varchar(255) DEFAULT 'NOT_GIVEN',
  `account_verified` int DEFAULT 0,
  `rem_log_in` int DEFAULT 0,
  `who_is` varchar(255) NOT NULL
);

CREATE TABLE `user_details` (
  `username` varchar(255) ,
  `full_name` varchar(255) DEFAULT 'NOT_GIVEN' ,
  `email` varchar(255) DEFAULT 'NOT_GIVEN'  ,
  `phone_no` bigint  ,
  `address` varchar(255) DEFAULT 'NOT_GIVEN' ,
  `gender` enum('MALE', 'FEMALE','NOT_GIVEN','NOT_PREFER_TO_SAY') DEFAULT 'NOT_GIVEN'
);

CREATE TABLE `user_session` (
  `username` varchar(255),
  `session_id` varchar(255),
  `last_login_time` timestamp,
  `last_login_ip` varchar(255)
);

CREATE TABLE `products` (
  `product_name` varchar(255),
  `brand_name` varchar(255),
  `description` varchar(255),
  `product_price` int,
  `product_img_url` varchar(255),
  `ratings` float
);

CREATE TABLE user_cart (
    username varchar(255),
    items text,  
    quantity INT DEFAULT 1,
    updated_at TIMESTAMP 
);


ALTER TABLE `user_details` ADD FOREIGN KEY (`username`) REFERENCES `user_auth` (`username`);

ALTER TABLE `user_session` ADD FOREIGN KEY (`username`) REFERENCES `user_auth` (`username`);

ALTER TABLE `user_cart` ADD FOREIGN KEY (`username`) REFERENCES `user_auth` (`username`);



