-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: inventory_management_1_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int NOT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (6,'Wireless Mouse','Computer Accessories',25.00,55,'Logitech','C:/Users/dev/Downloads/mouse.jpeg'),(7,'USB Flash Drive 64GB','Storage Devices',13.00,80,'Sandisk','C:/Users/dev/Downloads/sandisk.jpeg'),(18,'aa','aa',65.00,2,'aa','C:/Users/dev/OneDrive/Pictures/Screenshots/Screenshot 2026-05-23 171732.png'),(19,'ii','ii',5.00,2,'ii','C:/Users/dev/OneDrive/Pictures/20260601_OHR.OlivaPalermo_EN-IN8542997213_UHD_bing.jpg');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_name` varchar(100) NOT NULL,
  `supplier_name` varchar(100) DEFAULT NULL,
  `cost_price` decimal(10,2) NOT NULL,
  `quantity` int NOT NULL,
  `purchase_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
INSERT INTO `purchases` VALUES (1,'almond oild','sfa',2.00,20,'2026-07-21 20:42:56'),(2,'almond oil','egdsf',2.00,20,'2026-07-21 20:43:49'),(3,'as','fdcgvb',2.00,20,'2026-07-22 04:48:46'),(4,'ds','uhh',3.00,30,'2026-07-22 16:02:00'),(5,'uhb','jijbjnm',20.00,10,'2026-07-22 16:02:34'),(6,'wireless mouse','global tech supplies',25.00,20,'2026-07-25 15:59:00'),(7,'ds','sd',3.00,4,'2026-07-25 16:16:29'),(8,'milk','nhu',5.00,2,'2026-07-27 06:57:30'),(9,'milk','njk',2.00,10,'2026-07-27 06:58:04'),(10,'mlk','km',2.00,2,'2026-07-27 06:58:31'),(11,'mlk','nik',2.00,10,'2026-07-27 06:58:53'),(12,'iii','iiii',2.00,10,'2026-07-27 07:11:27'),(13,'oooo','oooo',5.00,2,'2026-07-27 07:14:02'),(14,'oooo','oooo',5.00,10,'2026-07-27 07:15:01'),(15,'nn','nn',2.00,4,'2026-07-27 07:15:33'),(16,'nn','nn',2.00,10,'2026-07-27 07:15:51'),(17,'yy','yy',2.00,10,'2026-07-27 07:19:05'),(18,'kk','njn',2.00,2,'2026-07-27 07:19:54'),(19,'hh','hh',2.00,2,'2026-07-27 07:22:52'),(20,'jj','jjj',5.00,2,'2026-07-27 07:25:07'),(21,'pp','pp',2.00,2,'2026-07-27 07:29:06'),(22,'kkk','kk',2.00,1,'2026-07-27 07:34:26'),(23,'ee','ee',2.00,2,'2026-07-27 07:36:08'),(24,'milk','kk',2.00,10,'2026-07-27 08:07:30'),(25,'ff','ff',2.00,3,'2026-07-27 08:08:56'),(26,'kk','kk',9.00,2,'2026-07-27 08:09:32'),(27,'ii','ii',6.00,5,'2026-07-27 08:12:42'),(28,'ooii','oo',10.00,10,'2026-07-27 08:15:57');
/*!40000 ALTER TABLE `purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_name` varchar(100) NOT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `quantity_sold` int NOT NULL,
  `total_revenue` decimal(10,2) NOT NULL,
  `sale_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,'almond oil',2.00,20,40.00,'2026-07-21 20:44:30'),(2,'ee',10.00,2,20.00,'2026-07-27 07:40:17'),(3,'nn',5.00,14,70.00,'2026-07-27 07:44:23'),(4,'oooo',5.00,6,30.00,'2026-07-27 07:44:59'),(5,'iii',5.00,10,50.00,'2026-07-27 07:49:19'),(6,'oooo',6.00,6,36.00,'2026-07-27 07:52:56'),(7,'mlk',5.00,12,60.00,'2026-07-27 07:55:29'),(8,'milk',10.00,12,120.00,'2026-07-27 08:01:43'),(9,'wireless keyboard',100.00,10,1000.00,'2026-07-27 08:03:30'),(10,'wireless keyboard',100.00,10,1000.00,'2026-07-27 08:03:46');
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (2,'Tech Source Electronics Pvt.Ltd','9876543210','sales@techsourceelectronics.com','Sector 62,Noida ,UP,India'),(3,'Global Office Supplies','9123456789','support@globalofficesupplies.com','MG Road, Bengaluru, Karnataka,India'),(4,'Prime IT Distributors','9988777665','contact@primeitdistributiors.com','Andheri East, Mumbai, Maharashtra,India'),(5,'fffd','574665','4wetrgfh','tryhj');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `sms_notifications_viewed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','1245789',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-30  0:38:13
