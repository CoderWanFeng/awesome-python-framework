-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: 192.168.1.88    Database: zw
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `account_view`
--

DROP TABLE IF EXISTS `account_view`;
/*!50001 DROP VIEW IF EXISTS `account_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `account_view` AS SELECT 
 1 AS `sysid`,
 1 AS `type`,
 1 AS `tableid`,
 1 AS `project_name_id`,
 1 AS `cause`,
 1 AS `money`,
 1 AS `account_date`,
 1 AS `finish_flag`,
 1 AS `expense_name_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `api_account_normal`
--

DROP TABLE IF EXISTS `api_account_normal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_account_normal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `account_date` datetime(6) DEFAULT NULL,
  `money` decimal(10,2) NOT NULL,
  `cause` varchar(64) NOT NULL,
  `finish_flag` varchar(64) NOT NULL,
  `expense_name_id` int NOT NULL,
  `project_name_id` int DEFAULT NULL,
  `approve_id` int DEFAULT NULL,
  `approvetime` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_account_normal_expense_name_id_49705d34_fk_api_userinfo_id` (`expense_name_id`),
  KEY `api_account_normal_project_name_id_5751ba35_fk_api_proje` (`project_name_id`),
  KEY `api_account_normal_approve_id_26aec184_fk_api_userinfo_id` (`approve_id`),
  CONSTRAINT `api_account_normal_approve_id_26aec184_fk_api_userinfo_id` FOREIGN KEY (`approve_id`) REFERENCES `api_userinfo` (`id`),
  CONSTRAINT `api_account_normal_expense_name_id_49705d34_fk_api_userinfo_id` FOREIGN KEY (`expense_name_id`) REFERENCES `api_userinfo` (`id`),
  CONSTRAINT `api_account_normal_project_name_id_5751ba35_fk_api_proje` FOREIGN KEY (`project_name_id`) REFERENCES `api_project_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_account_project`
--

DROP TABLE IF EXISTS `api_account_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_account_project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `zhushu` decimal(10,2) NOT NULL,
  `money_traffic` decimal(10,2) NOT NULL,
  `sumDate` int NOT NULL,
  `sumButie` decimal(10,2) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `account_date` datetime(6) DEFAULT NULL,
  `explain` varchar(64) NOT NULL,
  `finish_flag` varchar(64) NOT NULL,
  `Type_traffic_id` int NOT NULL,
  `expense_name_id` int NOT NULL,
  `project_name_id` int DEFAULT NULL,
  `approve_id` int DEFAULT NULL,
  `approvetime` datetime(6) DEFAULT NULL,
  `end_addr` varchar(64) NOT NULL,
  `start_addr` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_account_project_Type_traffic_id_eb115fe7_fk_api_traff` (`Type_traffic_id`),
  KEY `api_account_project_expense_name_id_4713ca03_fk_api_userinfo_id` (`expense_name_id`),
  KEY `api_account_project_project_name_id_239ae86a_fk_api_proje` (`project_name_id`),
  KEY `api_account_project_approve_id_bcc8c683_fk_api_userinfo_id` (`approve_id`),
  CONSTRAINT `api_account_project_approve_id_bcc8c683_fk_api_userinfo_id` FOREIGN KEY (`approve_id`) REFERENCES `api_userinfo` (`id`),
  CONSTRAINT `api_account_project_expense_name_id_4713ca03_fk_api_userinfo_id` FOREIGN KEY (`expense_name_id`) REFERENCES `api_userinfo` (`id`),
  CONSTRAINT `api_account_project_project_name_id_239ae86a_fk_api_proje` FOREIGN KEY (`project_name_id`) REFERENCES `api_project_info` (`id`),
  CONSTRAINT `api_account_project_Type_traffic_id_eb115fe7_fk_api_traff` FOREIGN KEY (`Type_traffic_id`) REFERENCES `api_traffic_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_attachment`
--

DROP TABLE IF EXISTS `api_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_attachment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `hetong_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_attachment_hetong_id_21fedf9b_fk_api_contract_info_id` (`hetong_id`),
  CONSTRAINT `api_attachment_hetong_id_21fedf9b_fk_api_contract_info_id` FOREIGN KEY (`hetong_id`) REFERENCES `api_contract_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_contract_info`
--

DROP TABLE IF EXISTS `api_contract_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_contract_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contract_name` varchar(64) NOT NULL,
  `contract_type` varchar(64) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `Date_start` date NOT NULL,
  `Date_end` date DEFAULT NULL,
  `taxes` decimal(10,2) DEFAULT NULL,
  `explain` varchar(64) DEFAULT NULL,
  `body_id` int NOT NULL,
  `project_id` int NOT NULL,
  `target_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_contract_info_body_id_c55d999f_fk_api_entity_info_id` (`body_id`),
  KEY `api_contract_info_project_id_639fe0b2_fk_api_project_info_id` (`project_id`),
  KEY `api_contract_info_target_id_161f2f75_fk_api_entity_info_id` (`target_id`),
  CONSTRAINT `api_contract_info_body_id_c55d999f_fk_api_entity_info_id` FOREIGN KEY (`body_id`) REFERENCES `api_entity_info` (`id`),
  CONSTRAINT `api_contract_info_project_id_639fe0b2_fk_api_project_info_id` FOREIGN KEY (`project_id`) REFERENCES `api_project_info` (`id`),
  CONSTRAINT `api_contract_info_target_id_161f2f75_fk_api_entity_info_id` FOREIGN KEY (`target_id`) REFERENCES `api_entity_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_contract_info_attachment`
--

DROP TABLE IF EXISTS `api_contract_info_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_contract_info_attachment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contract_info_id` int NOT NULL,
  `attachment_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_contract_info_attach_contract_info_id_attachm_c80da761_uniq` (`contract_info_id`,`attachment_id`),
  KEY `api_contract_info_at_attachment_id_649c1829_fk_api_attac` (`attachment_id`),
  CONSTRAINT `api_contract_info_at_attachment_id_649c1829_fk_api_attac` FOREIGN KEY (`attachment_id`) REFERENCES `api_attachment` (`id`),
  CONSTRAINT `api_contract_info_at_contract_info_id_58ff24d9_fk_api_contr` FOREIGN KEY (`contract_info_id`) REFERENCES `api_contract_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_contract_plan`
--

DROP TABLE IF EXISTS `api_contract_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_contract_plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_plan` date NOT NULL,
  `money_plan` decimal(10,2) NOT NULL,
  `contractinfo_id` int NOT NULL,
  `contract_type` varchar(64) NOT NULL,
  `finish_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_contract_plan_contractinfo_id_b5a147be_fk_api_contr` (`contractinfo_id`),
  CONSTRAINT `api_contract_plan_contractinfo_id_b5a147be_fk_api_contr` FOREIGN KEY (`contractinfo_id`) REFERENCES `api_contract_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_department`
--

DROP TABLE IF EXISTS `api_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_department` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(64) NOT NULL,
  `dept_manager_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dept_name` (`dept_name`),
  KEY `api_department_dept_manager_id_5200f69a_fk_api_userinfo_id` (`dept_manager_id`),
  CONSTRAINT `api_department_dept_manager_id_5200f69a_fk_api_userinfo_id` FOREIGN KEY (`dept_manager_id`) REFERENCES `api_userinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_entity_info`
--

DROP TABLE IF EXISTS `api_entity_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_entity_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `entity_name` varchar(128) NOT NULL,
  `entity_addr` varchar(128) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `bank_addr` varchar(64) DEFAULT NULL,
  `bank_number` varchar(64) DEFAULT NULL,
  `shuiHao` varchar(64) DEFAULT NULL,
  `explain` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `entity_name` (`entity_name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_project_info`
--

DROP TABLE IF EXISTS `api_project_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_project_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(64) NOT NULL,
  `customer_id` int NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_name` (`project_name`),
  KEY `api_project_info_customer_id_25507cdf_fk_api_entity_info_id` (`customer_id`),
  KEY `api_project_info_owner_id_a66e32d6_fk_api_entity_info_id` (`owner_id`),
  CONSTRAINT `api_project_info_customer_id_25507cdf_fk_api_entity_info_id` FOREIGN KEY (`customer_id`) REFERENCES `api_entity_info` (`id`),
  CONSTRAINT `api_project_info_owner_id_a66e32d6_fk_api_entity_info_id` FOREIGN KEY (`owner_id`) REFERENCES `api_entity_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_subsidize_info`
--

DROP TABLE IF EXISTS `api_subsidize_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_subsidize_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `money` decimal(5,2) NOT NULL,
  `Department_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_subsidize_info_Department_id_649bb846_fk_api_department_id` (`Department_id`),
  CONSTRAINT `api_subsidize_info_Department_id_649bb846_fk_api_department_id` FOREIGN KEY (`Department_id`) REFERENCES `api_department` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_test`
--

DROP TABLE IF EXISTS `api_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_traffic_type`
--

DROP TABLE IF EXISTS `api_traffic_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_traffic_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_name` (`project_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_userinfo`
--

DROP TABLE IF EXISTS `api_userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_userinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_type` int NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `name` varchar(32) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `department_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `name` (`name`),
  KEY `api_userinfo_department_id_8f2ce9d9_fk_api_department_id` (`department_id`),
  CONSTRAINT `api_userinfo_department_id_8f2ce9d9_fk_api_department_id` FOREIGN KEY (`department_id`) REFERENCES `api_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_usertoken`
--

DROP TABLE IF EXISTS `api_usertoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `api_usertoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` varchar(64) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_usertoken_user_id_5984b1b0_fk_api_userinfo_id` FOREIGN KEY (`user_id`) REFERENCES `api_userinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'zw'
--

--
-- Final view structure for view `account_view`
--

/*!50001 DROP VIEW IF EXISTS `account_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`zw`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `account_view` AS select concat('a',`api_account_project`.`id`) AS `sysid`,'a' AS `type`,`api_account_project`.`id` AS `tableid`,`api_account_project`.`project_name_id` AS `project_name_id`,`api_account_project`.`explain` AS `cause`,((`api_account_project`.`sumButie` + `api_account_project`.`zhushu`) + `api_account_project`.`money_traffic`) AS `money`,`api_account_project`.`account_date` AS `account_date`,`api_account_project`.`finish_flag` AS `finish_flag`,`api_account_project`.`expense_name_id` AS `expense_name_id` from `api_account_project` union all select concat('b',`api_account_normal`.`id`) AS `sysid`,'b' AS `b`,`api_account_normal`.`id` AS `tableid`,`api_account_normal`.`project_name_id` AS `project_name_id`,`api_account_normal`.`cause` AS `cause`,`api_account_normal`.`money` AS `money`,`api_account_normal`.`account_date` AS `account_date`,`api_account_normal`.`finish_flag` AS `finish_flag`,`api_account_normal`.`expense_name_id` AS `expense_name_id` from `api_account_normal` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-10 14:14:39
