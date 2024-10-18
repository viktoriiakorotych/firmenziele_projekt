/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.5.2-MariaDB, for osx10.19 (arm64)
--
-- Host: localhost    Database: firmenziele_db
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Abteilung`
--

DROP TABLE IF EXISTS `Abteilung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Abteilung` (
  `id_department` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id_department`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Benutzer`
--

DROP TABLE IF EXISTS `Benutzer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Benutzer` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `id_department` int DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  KEY `id_department` (`id_department`),
  CONSTRAINT `benutzer_ibfk_1` FOREIGN KEY (`id_department`) REFERENCES `Abteilung` (`id_department`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Zielbewertungen`
--

DROP TABLE IF EXISTS `Zielbewertungen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Zielbewertungen` (
  `id_goal_score` int NOT NULL AUTO_INCREMENT,
  `goals_id` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  `comment` text,
  `modified_by` varchar(255) DEFAULT NULL,
  `last_modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id_goal_score`),
  KEY `goals_id` (`goals_id`),
  CONSTRAINT `zielbewertungen_ibfk_1` FOREIGN KEY (`goals_id`) REFERENCES `Ziele` (`id_goals`),
  CONSTRAINT `zielbewertungen_chk_1` CHECK ((`score` between 1 and 10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Ziele`
--

DROP TABLE IF EXISTS `Ziele`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ziele` (
  `id_goals` int NOT NULL AUTO_INCREMENT,
  `statement` text NOT NULL,
  `criteria` text,
  `status_from` varchar(255) DEFAULT NULL,
  `measure_success` varchar(255) DEFAULT NULL,
  `id_department` int DEFAULT NULL,
  `last_modified_date` datetime DEFAULT NULL,
  `modified_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_goals`),
  KEY `id_department` (`id_department`),
  CONSTRAINT `ziele_ibfk_1` FOREIGN KEY (`id_department`) REFERENCES `Abteilung` (`id_department`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Zielhistorie`
--

DROP TABLE IF EXISTS `Zielhistorie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Zielhistorie` (
  `id_goals_history` int NOT NULL AUTO_INCREMENT,
  `id_goals` int DEFAULT NULL,
  `previous_score` int DEFAULT NULL,
  `new_score` int DEFAULT NULL,
  `change_description` text,
  `last_modified_date` datetime DEFAULT NULL,
  `modified_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_goals_history`),
  KEY `id_goals` (`id_goals`),
  CONSTRAINT `zielhistorie_ibfk_1` FOREIGN KEY (`id_goals`) REFERENCES `Ziele` (`id_goals`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-10-18 12:14:50
