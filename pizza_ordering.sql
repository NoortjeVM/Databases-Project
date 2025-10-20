-- MySQL dump 10.13  Distrib 9.4.0, for macos14.7 (x86_64)
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
INSERT INTO `customer` VALUES (1,'Wessel','Heerschop','1990-09-12','Nadinering 154','6215PD','+31962 895422',2),(2,'Elise','Bouwhuisen','1965-01-19','Milansingel 200','6221AX','(086)-9819895',0),(3,'Janne','Veltman','1990-09-22','Brittring 27','6215PD','+31(0)92-5378664',0),(4,'Yasmin','van Poppel','1965-11-12','Tristanlaan 121','6221AX','0425 084721',1),(5,'Dylano','Zuijdveld','2001-03-26','Jennifersingel 116','6215PD','073-1721189',2),(6,'Zakaria','Perrono','2004-10-01','Joeylaan 21','6221AX','+31948 413649',1),(7,'Juliette','Scheer','2007-10-17','Saraweg 90','6211RZ','+31(0)043 054062',1),(8,'Wessel','Guit','1980-10-22','Ashleyring 63','6221AX','+31602-387825',2),(9,'Maud','Verschuere','1996-11-22','Annelaan 159','6211RZ','(0106)-816564',1),(10,'Lenn','Kuiper','1983-11-11','Tirzaring 3','6215PD','+31(0)235 423625',0);
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
INSERT INTO `delivery_person` VALUES (1,'Amélie','van Rijnsbergen','6221AX','2025-10-20 17:24:40'),(2,'Lucas','Moensendijk','6211RZ','2025-10-20 17:24:40'),(3,'Rowan','Arens','6215PD','2025-10-20 17:24:40');
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
  PRIMARY KEY (`dessert_id`),
  CONSTRAINT `check_dessert_price_positive` CHECK ((`price` > 0))
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
  PRIMARY KEY (`drink_id`),
  CONSTRAINT `check_drink_price_positive` CHECK ((`price` > 0))
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
  UNIQUE KEY `ingredient_name` (`ingredient_name`),
  CONSTRAINT `check_ingredient_price_positive` CHECK ((`price` > 0))
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
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`delivery_person_id`) REFERENCES `delivery_person` (`delivery_person_id`),
  CONSTRAINT `check_order_total_price_positive` CHECK ((`total_price` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,4,NULL,1,'2025-10-13 07:37:41','Jentehof 43','6221AX','2025-10-13 08:06:41',19.52),(2,5,NULL,2,'2025-09-27 14:48:41','Pepijnboulevard 658','6215PD','2025-09-27 14:59:41',63.01),(3,8,NULL,3,'2025-10-04 16:34:41','Martstraat 2','6221AX','2025-10-04 17:00:41',95.78),(4,2,NULL,2,'2025-10-07 13:27:41','Brittsteeg 506','6221AX','2025-10-07 14:21:41',75.16),(5,5,NULL,2,'2025-10-16 08:02:41','Fatimalaan 59','6215PD','2025-10-16 08:59:41',70.00),(6,2,NULL,3,'2025-09-29 13:24:41','Isastraat 2','6221AX','2025-09-29 13:47:41',53.41),(7,4,NULL,3,'2025-09-29 11:46:41','Helenaring 1','6221AX','2025-09-29 12:16:41',42.77),(8,8,NULL,3,'2025-09-25 16:12:41','Elifbaan 3','6221AX','2025-09-25 16:13:41',57.79),(9,6,NULL,2,'2025-10-11 14:37:41','Annestraat 217','6221AX','2025-10-11 15:02:41',105.29),(10,10,NULL,3,'2025-10-13 14:32:41','Elifsingel 290','6215PD','2025-10-13 14:50:41',28.78),(11,9,NULL,1,'2025-10-11 12:54:41','Pienpad 116','6211RZ','2025-10-11 13:16:41',74.53),(12,3,NULL,3,'2025-10-08 14:46:41','Koensteeg 47','6215PD','2025-10-08 15:17:41',17.00),(13,7,NULL,1,'2025-09-24 07:23:41','Sebastiaanlaan 849','6211RZ','2025-09-24 07:47:41',78.48),(14,8,NULL,3,'2025-09-27 06:27:41','Jordyweg 0','6221AX','2025-09-27 07:03:41',16.02),(15,7,NULL,2,'2025-09-20 15:23:41','Yaralaan 69','6211RZ','2025-09-20 16:02:41',65.19),(16,10,NULL,3,'2025-09-20 07:36:41','Esmeestraat 954','6215PD','2025-09-20 07:53:41',103.95),(17,9,NULL,1,'2025-09-27 10:46:41','Wesselstraat 41','6211RZ','2025-09-27 11:09:41',51.19),(18,5,NULL,3,'2025-10-06 14:43:41','Tygobaan 85','6215PD','2025-10-06 15:09:41',28.03),(19,7,NULL,3,'2025-10-17 16:15:41','Sanderpad 710','6211RZ','2025-10-17 16:30:41',42.44),(20,3,NULL,1,'2025-09-26 09:28:41','Ceylinlaan 648','6215PD','2025-09-26 10:22:41',80.59);
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
INSERT INTO `order_item` VALUES (1,2,2),(1,16,1),(2,4,1),(2,5,3),(2,14,1),(3,2,1),(3,6,2),(3,7,1),(3,9,3),(3,13,2),(3,17,1),(4,1,3),(4,7,1),(4,9,3),(5,2,3),(5,3,3),(5,9,1),(5,15,1),(6,7,2),(6,9,2),(7,4,1),(7,10,3),(7,13,2),(8,4,1),(8,8,3),(8,12,2),(9,3,3),(9,4,1),(9,8,3),(9,10,3),(10,6,1),(10,9,1),(10,12,1),(11,2,2),(11,4,2),(11,10,3),(11,14,2),(12,9,1),(12,13,1),(13,5,3),(13,8,2),(13,14,1),(13,17,1),(14,2,2),(15,3,1),(15,4,2),(15,6,2),(15,11,2),(16,4,2),(16,5,3),(16,8,2),(16,12,2),(17,2,1),(17,4,2),(17,7,1),(17,14,1),(18,2,3),(18,12,2),(19,4,1),(19,8,2),(19,12,1),(20,2,3),(20,3,2),(20,7,1),(20,10,3),(20,12,1);
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

-- Dump completed on 2025-10-20 17:41:47
