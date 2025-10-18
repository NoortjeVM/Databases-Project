-- MySQL dump 10.13  Distrib 9.4.0, for macos14.7 (arm64)
--
-- Host: localhost    Database: pizza_ordering
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `birthdate` date NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `postal_code` varchar(6) NOT NULL,
  `phone_number` varchar(32) NOT NULL,
  `gender` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Elif','Oosterhek','1983-09-14','Isaring 5\n7295 RH\nBiezenmortel','6215PD','0058 884558',2),(2,'Amira','Ulrich','1985-11-29','Yarastraat 21\n9333FU\nCasteren','6215PD','+31(0)429 432644',0),(3,'Ceylin','Postma','1974-12-28','Alexanderhof 7\n4946FQ\nHall','6221AX','0627-811920',1),(4,'Samuel','Maaswinkel','2001-08-31','Sophiesingel 261\n9945FA\nTiendeveen','6221AX','+31(0)40 0272714',1),(5,'Elise','Kortman','1967-01-15','Collinring 1\n6581 IO\nSchelluinen','6215PD','(034) 9910505',1),(6,'Mick','Merkx','1994-11-16','Lukesingel 4\n7932 VT\nHedel','6211RZ','+3102 8749773',1),(7,'Jennifer','van de Berg','1986-06-05','Stefpad 63\n1873NG\nKampen','6211RZ','064 1230322',0),(8,'Lynn','Muller','1974-11-05','Fienweg 9\n3674UP\nGeertruidenberg','6215PD','(089) 5049214',0),(9,'Rayan','Labado','1973-06-02','Fabiënnestraat 47\n9013TW\nHolthees','6211RZ','0841-885802',1),(10,'Anne','Rutten','1969-02-25','Arieweg 118\n5330CE\nHengelo','6221AX','0155-259308',2);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_person`
--

DROP TABLE IF EXISTS `delivery_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_person` (
  `delivery_person_id` int NOT NULL AUTO_INCREMENT,
  `delivery_person_first_name` varchar(32) NOT NULL,
  `delivery_person_last_name` varchar(32) NOT NULL,
  `postal_code` varchar(6) NOT NULL,
  `next_available_time` datetime NOT NULL,
  PRIMARY KEY (`delivery_person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_person`
--

LOCK TABLES `delivery_person` WRITE;
/*!40000 ALTER TABLE `delivery_person` DISABLE KEYS */;
INSERT INTO `delivery_person` VALUES (1,'Maarten','Haselaar','6221AX','2025-10-18 20:31:02'),(2,'Giovanni','van Hoevel en van Zwindrecht','6211RZ','2025-10-18 20:31:02'),(3,'Niek','Broeshart','6215PD','2025-10-18 20:31:02');
/*!40000 ALTER TABLE `delivery_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dessert`
--

DROP TABLE IF EXISTS `dessert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dessert` (
  `dessert_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` decimal(8,2) NOT NULL,
  PRIMARY KEY (`dessert_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dessert`
--

LOCK TABLES `dessert` WRITE;
/*!40000 ALTER TABLE `dessert` DISABLE KEYS */;
INSERT INTO `dessert` VALUES (1,'Tiramisu',4.00),(2,'Panna Cotta',3.50),(3,'Brownie',2.50);
/*!40000 ALTER TABLE `dessert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discount_code`
--

DROP TABLE IF EXISTS `discount_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discount_code` (
  `discount_id` int NOT NULL AUTO_INCREMENT,
  `percentage` int NOT NULL,
  `discount_code` varchar(32) NOT NULL,
  PRIMARY KEY (`discount_id`),
  UNIQUE KEY `discount_code` (`discount_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount_code`
--

LOCK TABLES `discount_code` WRITE;
/*!40000 ALTER TABLE `discount_code` DISABLE KEYS */;
INSERT INTO `discount_code` VALUES (1,10,'WELCOME10'),(2,15,'STUDENT15'),(3,20,'VIP20');
/*!40000 ALTER TABLE `discount_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drink`
--

DROP TABLE IF EXISTS `drink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drink` (
  `drink_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` decimal(8,2) NOT NULL,
  PRIMARY KEY (`drink_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drink`
--

LOCK TABLES `drink` WRITE;
/*!40000 ALTER TABLE `drink` DISABLE KEYS */;
INSERT INTO `drink` VALUES (1,'Coca Cola',2.00),(2,'Sprite',2.00),(3,'Ice Tea',2.50),(4,'Beer',3.50);
/*!40000 ALTER TABLE `drink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `ingredient_name` varchar(32) NOT NULL,
  `price` decimal(8,2) NOT NULL,
  `vegetarian` tinyint(1) NOT NULL,
  `vegan` tinyint(1) NOT NULL,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE KEY `ingredient_name` (`ingredient_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Tomato Sauce',1.50,1,1),(2,'Mozzarella',2.00,1,0),(3,'Vegan Mozzarella',3.00,1,1),(4,'Pepperoni',2.50,0,0),(5,'Mushrooms',1.75,1,1),(6,'Bell Peppers',1.25,1,1),(7,'Onions',1.00,1,1),(8,'Olives',1.50,1,1),(9,'Ham',2.75,0,0),(10,'Pineapple',1.80,1,1),(11,'Basil',0.75,1,1),(12,'Parmesan',2.20,1,0),(13,'Gorgonzola',2.30,1,0);
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item`
--

DROP TABLE IF EXISTS `menu_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `item_type` varchar(20) NOT NULL,
  `item_ref_id` int NOT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item`
--

LOCK TABLES `menu_item` WRITE;
/*!40000 ALTER TABLE `menu_item` DISABLE KEYS */;
INSERT INTO `menu_item` VALUES (1,'pizza',1),(2,'pizza',2),(3,'pizza',3),(4,'pizza',4),(5,'pizza',5),(6,'pizza',6),(7,'pizza',7),(8,'pizza',8),(9,'pizza',9),(10,'pizza',10),(11,'drink',1),(12,'drink',2),(13,'drink',3),(14,'drink',4),(15,'dessert',1),(16,'dessert',2),(17,'dessert',3);
/*!40000 ALTER TABLE `menu_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `discount_id` int DEFAULT NULL,
  `delivery_person_id` int NOT NULL,
  `order_time` datetime NOT NULL,
  `delivery_address` varchar(255) NOT NULL,
  `postal_code` varchar(6) NOT NULL,
  `pickup_time` datetime NOT NULL,
  `total_price` decimal(8,2) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `discount_id` (`discount_id`),
  KEY `delivery_person_id` (`delivery_person_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`discount_id`) REFERENCES `discount_code` (`discount_id`),
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`delivery_person_id`) REFERENCES `delivery_person` (`delivery_person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,1,NULL,3,'2025-10-11 16:51:02','Rafaelring 403','6215PD','2025-10-11 17:01:02',34.25),(2,1,NULL,1,'2025-10-11 19:39:02','Liviadreef 250','6215PD','2025-10-11 19:39:02',20.75),(3,3,NULL,1,'2025-09-22 10:33:02','Hendriksteeg 8','6221AX','2025-09-22 10:59:02',67.40),(4,9,NULL,1,'2025-10-08 18:46:02','Dylanosteeg 09','6211RZ','2025-10-08 18:59:02',22.50),(5,3,NULL,1,'2025-10-16 18:14:02','Suusboulevard 2','6221AX','2025-10-16 18:45:02',73.65),(6,6,NULL,2,'2025-09-19 14:56:02','Sanderdreef 0','6211RZ','2025-09-19 15:48:02',48.05),(7,2,NULL,1,'2025-10-07 12:04:02','Hugodreef 203','6215PD','2025-10-07 12:21:02',30.00),(8,2,NULL,2,'2025-10-13 11:46:02','Giovannisingel 55','6215PD','2025-10-13 12:20:02',31.05),(9,6,NULL,2,'2025-10-10 12:01:02','Thomaspad 034','6211RZ','2025-10-10 12:04:02',43.10),(10,4,NULL,3,'2025-09-27 14:37:02','Faasbaan 5','6221AX','2025-09-27 14:57:02',17.75),(11,5,NULL,3,'2025-09-26 15:53:02','Fatimasteeg 90','6215PD','2025-09-26 15:57:02',90.90),(12,1,NULL,2,'2025-10-05 17:43:02','Eviebaan 861','6215PD','2025-10-05 17:52:02',32.25),(13,10,NULL,3,'2025-10-01 16:51:02','Merijnring 8','6221AX','2025-10-01 17:37:02',68.25),(14,9,NULL,2,'2025-09-26 09:33:02','Samlaan 2','6211RZ','2025-09-26 10:23:02',38.05),(15,9,NULL,3,'2025-09-25 15:32:02','Kyarabaan 1','6211RZ','2025-09-25 16:22:02',52.00),(16,9,NULL,3,'2025-09-18 14:56:02','Mohammedsingel 68','6211RZ','2025-09-18 15:21:02',34.75),(17,7,NULL,3,'2025-09-24 11:01:02','Joshuaboulevard 0','6211RZ','2025-09-24 11:22:02',18.50),(18,10,NULL,1,'2025-10-11 19:58:02','Adamdreef 6','6221AX','2025-10-11 20:48:02',12.75),(19,5,NULL,1,'2025-10-01 19:12:02','Isalaan 64','6215PD','2025-10-01 20:05:02',80.85),(20,2,NULL,3,'2025-09-24 11:57:02','Lisehof 22','6215PD','2025-09-24 12:00:02',47.00);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_item` (
  `order_id` int NOT NULL,
  `item_id` int NOT NULL,
  `amount` int NOT NULL,
  PRIMARY KEY (`order_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`),
  CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `menu_item` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_item`
--

LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS */;
INSERT INTO `order_item` VALUES (1,4,1),(1,8,2),(1,10,1),(1,13,1),(2,7,1),(2,8,1),(2,15,1),(3,2,2),(3,6,3),(3,7,3),(3,8,1),(4,4,2),(4,11,1),(4,17,1),(5,4,3),(5,5,1),(5,6,3),(5,10,2),(5,11,1),(6,3,2),(6,4,1),(6,6,1),(6,9,2),(7,4,2),(7,5,1),(7,12,1),(8,6,1),(8,9,2),(8,12,2),(9,4,3),(9,6,2),(10,10,3),(10,12,1),(11,1,1),(11,5,3),(11,6,3),(11,9,3),(11,12,2),(12,2,2),(12,10,3),(12,11,1),(12,15,1),(13,1,2),(13,5,3),(13,8,3),(13,14,1),(14,5,3),(14,6,1),(15,1,3),(15,2,1),(15,4,2),(15,7,2),(16,1,2),(16,2,2),(16,10,3),(17,4,1),(17,9,1),(18,1,3),(19,2,2),(19,5,3),(19,6,2),(19,10,3),(19,13,2),(19,16,1),(20,1,3),(20,4,2),(20,8,1),(20,11,2),(20,16,1);
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza`
--

DROP TABLE IF EXISTS `pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza` (
  `pizza_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`pizza_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (1,'Margherita'),(2,'Vegan Margherita'),(3,'Pepperoni'),(4,'Veggie Deluxe'),(5,'Vegan Deluxe'),(6,'Hawaiian'),(7,'Four Cheese'),(8,'Meat Feast'),(9,'Capricciosa'),(10,'Funghi');
/*!40000 ALTER TABLE `pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza_ingredient`
--

DROP TABLE IF EXISTS `pizza_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pizza_ingredient` (
  `pizza_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  PRIMARY KEY (`pizza_id`,`ingredient_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `pizza_ingredient_ibfk_1` FOREIGN KEY (`pizza_id`) REFERENCES `pizza` (`pizza_id`),
  CONSTRAINT `pizza_ingredient_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza_ingredient`
--

LOCK TABLES `pizza_ingredient` WRITE;
/*!40000 ALTER TABLE `pizza_ingredient` DISABLE KEYS */;
INSERT INTO `pizza_ingredient` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(3,2),(4,2),(6,2),(7,2),(8,2),(9,2),(10,2),(2,3),(5,3),(3,4),(8,4),(4,5),(5,5),(9,5),(10,5),(4,6),(5,6),(4,7),(5,7),(4,8),(5,8),(9,8),(6,9),(8,9),(9,9),(6,10),(1,11),(2,11),(7,12),(7,13);
/*!40000 ALTER TABLE `pizza_ingredient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-18 20:31:44
