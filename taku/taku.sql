-- phpMyAdmin SQL Dump
-- version 4.2.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2014-09-24 12:19:07
-- 服务器版本： 5.6.19
-- PHP Version: 5.4.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `taku`
--

-- --------------------------------------------------------

--
-- 表的结构 `ofUser`
--

CREATE TABLE IF NOT EXISTS `ofUser` (
`id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(20) NOT NULL,
  `nickname` varchar(20) DEFAULT NULL,
  `gender` varchar(4) DEFAULT '男',
  `age` int(3) DEFAULT '18',
  `height` varchar(10) DEFAULT NULL,
  `weight` varchar(10) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `ofUser`
--

INSERT INTO `ofUser` (`id`, `username`, `password`, `nickname`, `gender`, `age`, `height`, `weight`, `avatar`) VALUES
(2, '313832830@qq.com', 'shisong', '大侠', '女', 18, '168cm', '90kg', 'avatars/1411546353.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ofUser`
--
ALTER TABLE `ofUser`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ofUser`
--
ALTER TABLE `ofUser`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
