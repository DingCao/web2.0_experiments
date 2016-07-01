-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- Host: w.rdc.sae.sina.com.cn:3307
-- Generation Time: Mar 08, 2016 at 10:48 AM
-- Server version: 5.6.23
-- PHP Version: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `app_secretfriends`
--

-- --------------------------------------------------------

--
-- Table structure for table `Questions`
--

CREATE TABLE IF NOT EXISTS `Questions` (
  `ques_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `ques_name` tinytext,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `upper` char(11) NOT NULL,
  `ques_context` text,
  PRIMARY KEY (`ques_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `Questions`
--

INSERT INTO `Questions` (`ques_id`, `ques_name`, `time`, `upper`, `ques_context`) VALUES
(00000000001, '【数据】重置', '2015-01-07 00:00:00', 'Admin', '重置所有的数据'),
(00000000002, '【版本】密友公众版开放！', '2015-01-07 00:00:00', 'Admin', '经过团队近两个星期的努力，密友(secretfriends)对公众开放~');

-- --------------------------------------------------------

--
-- Table structure for table `Replies`
--

CREATE TABLE IF NOT EXISTS `Replies` (
  `reply_id` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `ques_id` int(10) unsigned zerofill NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `reply_context` tinytext NOT NULL,
  PRIMARY KEY (`reply_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `Replies`
--

INSERT INTO `Replies` (`reply_id`, `ques_id`, `uid`, `time`, `reply_context`) VALUES
(0000000001, 0000000001, 2, '2016-03-06 12:16:22', '-..-/../.-/---/-..-/../.-/---/-.-././.../..../..'),
(0000000002, 0000000002, 2, '2016-03-06 12:16:22', '增加密码类型之后的测试');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `uname` char(20) NOT NULL,
  `password` char(20) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `uname` (`uname`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `uname`, `password`) VALUES
(0000000001, 'admin123', 'Admin123'),
(0000000002, 'DingCao', 'DingCao'),
(0000000003, 'Nobody', 'Nobody'),
(0000000004, 'ShaoLing', 'ShaoLing'),
(0000000005, 'TingTing', 'TingTing');


-- Self adds
ALTER TABLE questions
ADD uid INT unsigned zerofill NOT NULL
AFTER upper;

UPDATE questions Q
SET uid = (
  SELECT uid FROM users U
  WHERE Q.upper = U.uname
);
