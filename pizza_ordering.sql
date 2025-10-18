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
INSERT INTO `customer` VALUES (1,'Lenn','Jaceps','1995-04-24','Floorlaan 534\n6248 PN\nZwammerdam','6211RZ','0915-495935',1),(2,'Hendrik','Melet','2000-07-13','Eviering 0\n3726 KQ\nMechelen','6221AX','0407-965701',2),(3,'Ize','Höning','1965-01-15','Yaradreef 54\n3868KB\nKornhorn','6215PD','(0440)-167060',0),(4,'Rosalie','Brandt','1990-08-10','Livbaan 71\n7992 FF\nZeeland','6215PD','(0565) 904923',0),(5,'Maryam','Hemma van Allemanië','2001-09-11','Aiméesteeg 293\n9290 ID\nIdaerd','6215PD','074-2208708',0),(6,'Seth','de Bont','1992-03-26','Rikhof 294\n7862UQ\nHeerlen','6221AX','(0115) 391636',2),(7,'Senna','Heijmans','1989-11-24','Jorislaan 49\n5021YT\nEexterzandvoort','6215PD','(061) 2305668',0),(8,'Youssef','van Bovenen','1991-12-12','Elinring 35\n8850OX\nPurmer','6215PD','+31(0)414-410806',2),(9,'Thijs','Wouters','1985-11-03','Rubenlaan 1\n2717 ON\nBeesd','6215PD','+31(0)72-8642372',1),(10,'Jesper','Postma','1992-03-20','Faasstraat 3\n3718 CF\nGraauw','6221AX','(0145)-585731',0);
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
INSERT INTO `delivery_person` VALUES (1,'Rayan','Claesner','6221AX','2025-10-18 19:53:01'),(2,'Lauren','Adriaense','6211RZ','2025-10-18 19:53:01'),(3,'Jacob','Willemsen','6215PD','2025-10-18 20:23:21');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dessert`
--

LOCK TABLES `dessert` WRITE;
/*!40000 ALTER TABLE `dessert` DISABLE KEYS */;
INSERT INTO `dessert` VALUES (1,'Tiramisu',4.00),(2,'Panna Cotta',3.50);
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Tomato Sauce',1.50,1,1),(2,'Mozzarella',2.00,1,0),(3,'Pepperoni',2.50,0,0),(4,'Mushrooms',1.75,1,1),(5,'Bell Peppers',1.25,1,1),(6,'Onions',1.00,1,1),(7,'Olives',1.50,1,1),(8,'Ham',2.75,0,0),(9,'Pineapple',1.80,1,1),(10,'Basil',0.75,1,1),(11,'Parmesan',2.20,1,0),(12,'Gorgonzola',2.30,1,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item`
--

LOCK TABLES `menu_item` WRITE;
/*!40000 ALTER TABLE `menu_item` DISABLE KEYS */;
INSERT INTO `menu_item` VALUES (1,'pizza',1),(2,'pizza',2),(3,'pizza',3),(4,'pizza',4),(5,'pizza',5),(6,'pizza',6),(7,'pizza',7),(8,'pizza',8),(9,'drink',1),(10,'drink',2),(11,'drink',3),(12,'drink',4),(13,'dessert',1),(14,'dessert',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,2,NULL,1,'2025-09-19 09:27:02','Mirteboulevard 538','6221AX','2025-09-19 09:50:02',40.50),(2,9,NULL,1,'2025-10-11 14:01:02','Nathanstraat 13','6215PD','2025-10-11 15:01:02',37.65),(3,10,NULL,2,'2025-10-14 10:58:02','Liseboulevard 481','6221AX','2025-10-14 11:31:02',51.75),(4,9,NULL,1,'2025-09-26 18:32:02','Mirteweg 2','6215PD','2025-09-26 19:16:02',25.30),(5,3,NULL,1,'2025-10-06 10:53:02','Lucasboulevard 203','6215PD','2025-10-06 11:43:02',26.25),(6,10,NULL,1,'2025-09-29 12:48:02','Lauraring 91','6221AX','2025-09-29 13:40:02',50.75),(7,7,NULL,1,'2025-09-21 16:06:02','Liamdreef 53','6215PD','2025-09-21 17:03:02',35.75),(8,8,NULL,1,'2025-09-20 09:05:02','Yfkeweg 2','6215PD','2025-09-20 09:23:02',8.05),(9,3,NULL,2,'2025-10-03 11:41:02','Evydreef 61','6215PD','2025-10-03 12:32:02',29.55),(10,1,NULL,2,'2025-09-24 15:14:02','Aminastraat 95','6211RZ','2025-09-24 16:08:02',23.25),(11,10,NULL,3,'2025-09-24 18:32:02','Jesperpad 4','6221AX','2025-09-24 19:25:02',30.75),(12,8,NULL,2,'2025-10-09 12:30:02','Evysingel 3','6215PD','2025-10-09 12:47:02',52.60),(13,6,NULL,3,'2025-09-22 18:48:02','Jobdreef 4','6221AX','2025-09-22 19:13:02',12.25),(14,3,NULL,1,'2025-09-26 09:37:02','Demipad 64','6215PD','2025-09-26 10:08:02',23.50),(15,4,NULL,3,'2025-10-08 13:03:02','Colinpad 11','6215PD','2025-10-08 13:34:02',8.00),(16,6,NULL,3,'2025-10-04 18:36:02','Jennasteeg 70','6221AX','2025-10-04 19:23:02',20.00),(17,9,NULL,1,'2025-09-19 14:05:02','Sebastiaanstraat 805','6215PD','2025-09-19 14:18:02',21.75),(18,8,NULL,3,'2025-10-08 15:14:02','Wesleyring 537','6215PD','2025-10-08 15:52:02',33.00),(19,5,NULL,3,'2025-10-13 16:25:02','Siemlaan 95','6215PD','2025-10-13 16:33:02',80.10),(20,4,NULL,1,'2025-10-04 13:23:02','Louiseweg 67','6215PD','2025-10-04 13:42:02',40.50),(21,4,NULL,3,'2025-10-18 19:53:21','','6215PD','2025-10-18 19:53:21',8.50);
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
INSERT INTO `order_item` VALUES (1,3,3),(1,7,1),(1,13,1),(2,4,3),(2,7,1),(2,9,2),(3,2,2),(3,3,3),(3,6,1),(3,13,1),(4,1,2),(4,4,1),(4,6,1),(5,6,3),(6,3,2),(6,6,1),(6,7,2),(6,11,2),(7,7,3),(7,8,1),(7,9,1),(8,4,1),(9,2,3),(9,4,1),(9,12,1),(10,8,3),(10,9,2),(10,14,1),(11,1,1),(11,5,2),(11,12,2),(11,14,1),(12,4,2),(12,6,3),(12,8,1),(12,11,2),(13,1,1),(13,10,2),(13,13,1),(14,6,2),(14,11,1),(14,14,1),(15,5,1),(16,2,2),(16,5,1),(17,1,3),(17,3,1),(18,3,3),(18,11,1),(18,14,1),(19,3,3),(19,4,2),(19,7,2),(19,8,2),(19,10,2),(19,14,1),(20,1,3),(20,3,1),(20,5,1),(20,6,1),(20,10,1),(21,1,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (1,'Margherita'),(2,'Pepperoni'),(3,'Veggie Deluxe'),(4,'Hawaiian'),(5,'Four Cheese'),(6,'Meat Feast'),(7,'Capricciosa'),(8,'Funghi');
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
INSERT INTO `pizza_ingredient` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(2,3),(6,3),(3,4),(7,4),(8,4),(3,5),(3,6),(3,7),(7,7),(4,8),(6,8),(7,8),(4,9),(1,10),(5,11),(5,12);
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

-- Dump completed on 2025-10-18 20:08:37
