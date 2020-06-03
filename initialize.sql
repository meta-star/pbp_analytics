-- Phishing Blocker Project - Analytics
--
-- This OSS is licensed under the Mozilla Public License, v. 2.0.
-- https://github.com/star-inc/pbp-analytics
-- Copyright (c) 2020 Star Inc.(https://starinc.xyz)

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE TABLE `blacklist` (
  `uuid` varchar(36) NOT NULL,
  `url` text NOT NULL,
  `date` datetime NOT NULL,
  `url_hash` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `result_cache` (
  `url_hash` varchar(64) NOT NULL,
  `score` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `trustlist` (
  `uuid` varchar(36) NOT NULL,
  `url` text NOT NULL,
  `target_view_narray` mediumblob DEFAULT NULL,
  `target_view_signature` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `trust_domain` (
  `uuid` varchar(36) NOT NULL,
  `foreign_key` varchar(36) NOT NULL,
  `domain` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `warnlist` (
  `uuid` varchar(36) NOT NULL,
  `url` text NOT NULL,
  `origin` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `blacklist`
  ADD PRIMARY KEY (`uuid`),
  ADD UNIQUE KEY `url_hash` (`url_hash`);

ALTER TABLE `result_cache`
  ADD PRIMARY KEY (`url_hash`);

ALTER TABLE `trustlist`
  ADD PRIMARY KEY (`uuid`);

ALTER TABLE `trust_domain`
  ADD PRIMARY KEY (`uuid`),
  ADD KEY `foreign_key` (`foreign_key`),
  ADD CONSTRAINT `trust_domain_ibfk_1` FOREIGN KEY (`foreign_key`) REFERENCES `trustlist` (`uuid`) ON DELETE CASCADE;

ALTER TABLE `warnlist`
  ADD PRIMARY KEY (`uuid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
