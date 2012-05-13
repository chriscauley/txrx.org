-- MySQL dump 10.13  Distrib 5.1.54, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: TXRX_DB
-- ------------------------------------------------------
-- Server version    5.1.54-1ubuntu4-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `billingplan`
--

DROP TABLE IF EXISTS `billingplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `billingplan` (
  `billingplanid` int(11) NOT NULL AUTO_INCREMENT,
  `createdon` date NOT NULL,
  `effectiveasof` date NOT NULL,
  `endedon` date DEFAULT NULL,
  `cost` float NOT NULL,
  `period` int(11) NOT NULL,
  `memberid` int(11) NOT NULL,
  `description` varchar(150) DEFAULT NULL,
  `descrip` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`billingplanid`),
  KEY `memberid_billingplan_fk` (`memberid`),
  CONSTRAINT `memberid_billingplan_fk` FOREIGN KEY (`memberid`) REFERENCES `txrxmember` (`memberid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `financialentry`
--

DROP TABLE IF EXISTS `financialentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `financialentry` (
  `financialentryid` int(11) NOT NULL AUTO_INCREMENT,
  `amount` double NOT NULL,
  `createdby` int(11) NOT NULL,
  `memberid` int(11) NOT NULL,
  `paymentform` varchar(45) DEFAULT NULL,
  `entrydate` date NOT NULL,
  `valid` tinyint(1) NOT NULL,
  `entrytype` varchar(45) NOT NULL,
  `item_name` varchar(45) DEFAULT NULL,
  `payer_email` varchar(70) DEFAULT NULL,
  `payer_id` varchar(45) DEFAULT NULL,
  `payment_fee` double DEFAULT NULL,
  `txn_id` varchar(45) DEFAULT NULL,
  `txn_type` varchar(45) DEFAULT NULL,
  `postentryid` int(11) DEFAULT NULL,
  `descrip` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`financialentryid`),
  KEY `createdby_financialentry_fk` (`createdby`),
  KEY `memberid_financialentry_fk` (`memberid`),
  KEY `postentryid_financialentry_fk` (`postentryid`),
  CONSTRAINT `createdby_financialentry_fk` FOREIGN KEY (`createdby`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `memberid_financialentry_fk` FOREIGN KEY (`memberid`) REFERENCES `txrxmember` (`memberid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `postentryid_financialentry_fk` FOREIGN KEY (`postentryid`) REFERENCES `postentry` (`postentryid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3410 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_level`
--

DROP TABLE IF EXISTS `member_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_level` (
  `member_levelid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `createdby` int(11) NOT NULL,
  PRIMARY KEY (`member_levelid`),
  KEY `createdby_member_level_fk` (`createdby`),
  CONSTRAINT `createdby_member_level_fk` FOREIGN KEY (`createdby`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `memberbalance`
--

DROP TABLE IF EXISTS `memberbalance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `memberbalance` (
  `memberbalanceid` int(11) NOT NULL AUTO_INCREMENT,
  `memberid` int(11) NOT NULL,
  `updatedate` date NOT NULL,
  `amount` double NOT NULL,
  PRIMARY KEY (`memberbalanceid`),
  KEY `memberid_memberbalance_fk` (`memberid`),
  CONSTRAINT `memberid_memberbalance_fk` FOREIGN KEY (`memberid`) REFERENCES `txrxmember` (`memberid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `paymentid` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `date` date NOT NULL,
  `createdby` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `memberid` int(11) NOT NULL,
  `method` int(11) NOT NULL,
  PRIMARY KEY (`paymentid`),
  KEY `memberid_payment_fk` (`memberid`),
  KEY `createdby_payment_fk` (`createdby`),
  CONSTRAINT `createdby_payment_fk` FOREIGN KEY (`createdby`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `memberid_payment_fk` FOREIGN KEY (`memberid`) REFERENCES `txrxmember` (`memberid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment_application`
--

DROP TABLE IF EXISTS `payment_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_application` (
  `payment_applicationid` int(11) NOT NULL AUTO_INCREMENT,
  `paymentid` int(11) NOT NULL,
  `invoiceid` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `datestamp` date NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `createdby` int(11) NOT NULL,
  PRIMARY KEY (`payment_applicationid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paypalIPN`
--

DROP TABLE IF EXISTS `paypalIPN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypalIPN` (
  `paypalipnid` int(11) NOT NULL AUTO_INCREMENT,
  `txnType` varchar(45) NOT NULL,
  `txnId` varchar(45) NOT NULL,
  `payerEmail` varchar(100) NOT NULL,
  `payerId` varchar(75) NOT NULL,
  `firstName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) DEFAULT NULL,
  `paymentFee` double NOT NULL,
  `paymentGross` double NOT NULL,
  `createdon` datetime NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `memberid` int(11) DEFAULT NULL,
  PRIMARY KEY (`paypalipnid`),
  KEY `memberid_paypalIPN_fk` (`memberid`),
  CONSTRAINT `memberid_paypalIPN_fk` FOREIGN KEY (`memberid`) REFERENCES `txrxmember` (`memberid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=600 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `postentry`
--

DROP TABLE IF EXISTS `postentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `postentry` (
  `postentryid` int(11) NOT NULL AUTO_INCREMENT,
  `postdate` date NOT NULL,
  `createdby` int(11) NOT NULL,
  `processedon` date NOT NULL,
  PRIMARY KEY (`postentryid`),
  KEY `createdby_postentry_fk` (`createdby`),
  CONSTRAINT `createdby_postentry_fk` FOREIGN KEY (`createdby`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rfid`
--

DROP TABLE IF EXISTS `rfid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rfid` (
  `rfidid` int(11) NOT NULL AUTO_INCREMENT,
  `facid` varchar(3) DEFAULT NULL,
  `cardid` varchar(5) NOT NULL,
  `issuedate` date NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `memberid` int(11) NOT NULL,
  PRIMARY KEY (`rfidid`),
  KEY `memberid_rfid_fk` (`memberid`),
  CONSTRAINT `memberid_rfid_fk` FOREIGN KEY (`memberid`) REFERENCES `txrxmember` (`memberid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rfidpermissions`
--

DROP TABLE IF EXISTS `rfidpermissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rfidpermissions` (
  `rfidpermissionid` int(11) NOT NULL AUTO_INCREMENT,
  `rfidid` int(11) NOT NULL,
  `rfidpermissiontemplateid` int(11) NOT NULL,
  PRIMARY KEY (`rfidpermissionid`),
  KEY `rfidid_rfidpermissions_fk` (`rfidid`),
  KEY `rfidpermissiontemplateid_rfidpermissions_fk` (`rfidpermissiontemplateid`),
  CONSTRAINT `rfidid_rfidpermissions_fk` FOREIGN KEY (`rfidid`) REFERENCES `rfid` (`rfidid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `rfidpermissiontemplateid_rfidpermissions_fk` FOREIGN KEY (`rfidpermissiontemplateid`) REFERENCES `rfidpermissiontemplate` (`rfidpermissiontemplateid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rfidpermissiontemplate`
--

DROP TABLE IF EXISTS `rfidpermissiontemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rfidpermissiontemplate` (
  `rfidpermissiontemplateid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  PRIMARY KEY (`rfidpermissiontemplateid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `roleid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `roledefid` int(11) NOT NULL,
  PRIMARY KEY (`roleid`),
  KEY `roledefid_role_fk` (`roledefid`),
  KEY `userid_role_fk` (`userid`),
  CONSTRAINT `roledefid_role_fk` FOREIGN KEY (`roledefid`) REFERENCES `roledef` (`rolddefid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `userid_role_fk` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `roledef`
--

DROP TABLE IF EXISTS `roledef`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roledef` (
  `rolddefid` int(11) NOT NULL AUTO_INCREMENT,
  `rolename` varchar(45) NOT NULL,
  PRIMARY KEY (`rolddefid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `txrxmember`
--

DROP TABLE IF EXISTS `txrxmember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `txrxmember` (
  `memberid` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) NOT NULL,
  `mi` varchar(1) DEFAULT NULL,
  `lastname` varchar(45) NOT NULL,
  `address1` varchar(45) NOT NULL,
  `address2` varchar(45) DEFAULT NULL,
  `address3` varchar(45) DEFAULT NULL,
  `city` varchar(45) NOT NULL,
  `state` varchar(2) NOT NULL,
  `country` varchar(2) NOT NULL,
  `zip` varchar(5) NOT NULL,
  `primaryphone` varchar(7) NOT NULL,
  `primaryarea` varchar(3) NOT NULL,
  `email` varchar(45) NOT NULL,
  `joindate` date NOT NULL,
  `member_level` int(11) NOT NULL,
  `createdby` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `paypalemail` varchar(100) DEFAULT NULL,
  `deletedon` date DEFAULT NULL,
  PRIMARY KEY (`memberid`),
  KEY `memberl_level_fk` (`member_level`),
  KEY `createdby_txrxmember_fk` (`createdby`),
  CONSTRAINT `createdby_txrxmember_fk` FOREIGN KEY (`createdby`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `memberl_level_fk` FOREIGN KEY (`member_level`) REFERENCES `member_level` (`member_levelid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(64) NOT NULL,
  `createdon` date NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `mi` varchar(1) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-05-12 22:28:48