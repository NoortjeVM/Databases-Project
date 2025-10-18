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
INSERT INTO `customer` VALUES (1,'Inaya','Volcke','1982-07-29','Esméeboulevard 89\n7872 AJ\nKollumerpomp','6211RZ','+31281 930252',0),(2,'Aaliyah','Remmers','1987-07-24','Timodreef 4\n3495 QU\nKoudekerke','6215PD','+31(0)40 2118023',2),(3,'Kyano','Lips','1974-12-28','Jorndreef 887\n5497UH\nAlphen aan den Rijn','6215PD','(044) 6550461',1),(4,'Sylvie','van \'t Wel','1983-05-10','Casring 415\n9098BY\nReutum','6221AX','+31995-346164',1),(5,'Jet','VI','1967-09-06','Isedreef 10\n6209JC\nUden','6221AX','+31(0)97-5183843',0),(6,'Kyan','van Laarhoven','1997-07-13','Sarahring 230\n4680 SI\nGoënga','6215PD','(0344) 394096',1),(7,'Jim','van Baalen','1967-01-26','Benjaminbaan 0\n7463 DI\nSlappeterp','6211RZ','+31(0)24 1397270',1),(8,'Mare','Verhoeven','1986-06-07','Thijnboulevard 80\n5570PC\nOud Annerveen','6211RZ','(039) 5058246',0),(9,'Isabel','Lelijveld','1976-05-01','Corneliaring 51\n7546AF\nDe Kiel','6215PD','063-9537684',1),(10,'Zoë','van den Wittenboer','1987-06-24','Selinalaan 566\n7119 LA\nYerseke','6211RZ','(0728) 184730',2);
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
INSERT INTO `delivery_person` VALUES (1,'Mathijs','Gemen','6221AX','2025-10-18 20:57:01'),(2,'Hailey','van Munster','6211RZ','2025-10-18 20:57:01'),(3,'Yinthe','Melet','6215PD','2025-10-18 20:57:01');
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
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`delivery_person_id`) REFERENCES `delivery_person` (`delivery_person_id`),
  CONSTRAINT `check_order_total_price_positive` CHECK ((`total_price` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,4,NULL,3,'2025-10-05 16:03:01','Jamiedreef 660','6221AX','2025-10-05 16:44:01',39.90),(2,3,NULL,1,'2025-10-14 12:52:01','Rafweg 59','6215PD','2025-10-14 13:30:01',11.55),(3,8,NULL,1,'2025-10-16 16:00:01','Lucdreef 501','6211RZ','2025-10-16 16:35:01',52.25),(4,1,NULL,3,'2025-10-08 17:59:01','Kayleeweg 456','6211RZ','2025-10-08 18:08:01',38.25),(5,5,NULL,2,'2025-10-06 13:43:01','Laurenpad 64','6221AX','2025-10-06 13:50:01',28.10),(6,7,NULL,3,'2025-10-07 11:17:01','Ayoubsteeg 03','6211RZ','2025-10-07 11:55:01',51.75),(7,9,NULL,3,'2025-09-23 12:28:01','Meikedreef 4','6215PD','2025-09-23 12:34:01',21.50),(8,9,NULL,1,'2025-09-24 15:44:01','Josephinehof 0','6215PD','2025-09-24 16:04:01',39.25),(9,6,NULL,2,'2025-09-22 20:28:01','Valeriesteeg 9','6215PD','2025-09-22 21:17:01',18.00),(10,3,NULL,3,'2025-10-13 16:21:01','Pimpad 084','6215PD','2025-10-13 16:45:01',18.00),(11,7,NULL,3,'2025-10-01 10:29:01','Bilalbaan 6','6211RZ','2025-10-01 11:20:01',71.75),(12,2,NULL,3,'2025-10-13 13:23:01','Eliassteeg 079','6215PD','2025-10-13 14:17:01',72.85),(13,10,NULL,1,'2025-10-07 15:44:01','Dinaweg 647','6211RZ','2025-10-07 16:07:01',44.25),(14,6,NULL,1,'2025-09-30 13:47:01','Tijmenpad 8','6215PD','2025-09-30 14:34:01',16.10),(15,3,NULL,3,'2025-10-01 15:27:01','Sethdreef 08','6215PD','2025-10-01 16:12:01',9.25),(16,2,NULL,1,'2025-09-29 15:05:01','Amelialaan 763','6215PD','2025-09-29 15:32:01',34.50),(17,6,NULL,2,'2025-09-27 11:51:01','Mayastraat 4','6215PD','2025-09-27 12:34:01',21.05),(18,10,NULL,1,'2025-10-14 18:25:01','Imkebaan 080','6211RZ','2025-10-14 19:04:01',28.75),(19,6,NULL,2,'2025-10-13 11:48:01','Riklaan 2','6215PD','2025-10-13 12:39:01',37.50),(20,6,NULL,3,'2025-10-10 17:20:01','Rowanpad 34','6215PD','2025-10-10 17:30:01',31.30);
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
INSERT INTO `order_item` VALUES (1,4,3),(1,8,3),(2,4,1),(2,12,1),(3,5,3),(3,7,2),(3,8,1),(3,13,1),(4,1,3),(4,5,2),(4,7,1),(5,2,2),(5,4,2),(6,1,1),(6,2,1),(6,3,3),(6,8,2),(6,10,2),(7,6,2),(7,10,2),(8,1,3),(8,3,1),(8,6,2),(9,2,3),(10,3,2),(11,2,3),(11,3,2),(11,6,3),(11,7,1),(12,3,3),(12,4,2),(12,6,3),(12,14,1),(13,3,2),(13,5,2),(13,8,1),(13,11,2),(14,4,2),(15,1,1),(15,11,2),(16,2,1),(16,3,2),(16,8,2),(17,4,1),(17,8,2),(17,11,1),(18,2,1),(18,6,2),(18,8,1),(19,6,2),(19,7,1),(19,8,2),(20,4,1),(20,6,1),(20,8,2),(20,9,2);
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

-- Dump completed on 2025-10-18 21:08:23
