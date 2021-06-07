-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 07, 2021 at 06:49 AM
-- Server version: 8.0.17
-- PHP Version: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `posttest`
--

CREATE TABLE `posttest` (
  `postID` int(11) NOT NULL,
  `address` varchar(45) NOT NULL,
  `contents` varchar(60000) NOT NULL,
  `title` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Owner` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posttest`
--

INSERT INTO `posttest` (`postID`, `address`, `contents`, `title`, `type`, `date`, `Owner`) VALUES
(1, '14', 'contents', 'test', 'find', '2021-04-15 23:29:54', 'admin'),
(2, '14', 'test', 'test', 'find', '2021-04-05 17:45:21', 'admin'),
(3, '14', 'test', 'test', 'find', '2021-04-05 17:46:29', 'admin'),
(4, '14', 'test', 'test', 'find', '2021-04-05 17:47:36', 'admin'),
(5, 'St.Lucia', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'INFS3208_Assignment', 'find', '2018-10-07 04:08:08', 's4405278'),
(6, 'St.Lucia', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'INFS3208_Assignment 2', 'find', '2018-10-07 04:08:49', 's4405278'),
(7, 'St.Lucia', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'INFS3208_Assignment 3', 'find', '2018-10-07 04:08:55', 's4405278'),
(10, 'St.Lucia', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'INFS3208_Assignment 4', 'employ', '2018-10-07 04:20:22', 's4405278'),
(14, 'St.Lucia', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'INFS3208_Assignment 5', 'employ', '2018-10-07 04:25:24', 's4405278'),
(16, '14', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'wa diu!', 'find', '2021-02-22 21:58:08', 'admin'),
(447, '14', 'sqlteet', 'sqltest\' and 1=1 -- -', 'find', '2021-04-03 20:44:28', 'admin'),
(512, '14', 'contents', 'test', 'find', '2021-04-15 23:30:02', 'admin'),
(513, '14', 'contents', 'test', 'find', '2021-04-15 23:38:23', 'admin'),
(514, '14', 'contents', 'test', 'find', '2021-04-15 23:39:30', 'admin'),
(515, '14', 'contents', 'test', 'find', '2021-04-15 23:42:47', 'admin'),
(516, '14', 'contents', 'test', 'find', '2021-04-15 23:43:42', 'admin'),
(517, '14', 'contents', 'test', 'find', '2021-04-15 23:48:48', 'admin'),
(518, '14', 'contents', 'test', 'find', '2021-04-15 23:49:47', 'admin'),
(519, '14', 'contents', 'test', 'find', '2021-04-15 23:50:49', 'admin'),
(520, '14', 'contents', 'test', 'find', '2021-04-15 23:51:44', 'admin'),
(521, '14', 'contents', 'test', 'find', '2021-04-15 23:52:09', 'admin'),
(522, '14', 'test', 'test', 'find', '2021-04-16 11:36:13', 'admin'),
(523, '14', 'test', 'test', 'find', '2021-04-16 13:00:36', 'admin'),
(524, '14', '1', '1', '1', '2021-04-23 11:13:29', 'admin'),
(525, '14', '1', '1', '1', '2021-04-25 17:26:40', 'admin'),
(526, '14', '1', '1', '1', '2021-04-25 17:32:41', 'admin'),
(527, '14', '1', '1', '1', '2021-04-25 18:19:54', 'admin'),
(528, '14', '1', '1', '1', '2021-04-25 18:25:12', 'admin'),
(529, '14', '1', '1', '1', '2021-04-25 18:26:12', 'admin'),
(530, '14', '1', '1', '1', '2021-04-25 18:34:54', 'admin'),
(531, '14', '1', '1', '1', '2021-04-25 18:45:03', 'admin'),
(532, '14', '1', '1', '1', '2021-04-25 18:46:21', 'admin'),
(533, '14', '1', '1', '1', '2021-04-25 19:58:55', 'admin'),
(534, '14', '1', '1', '', '2021-04-30 21:55:44', 'admin'),
(535, '14', '1', '1', '', '2021-05-03 12:28:36', 'admin'),
(536, '14', '1', '1', '', '2021-05-03 20:41:08', 'admin'),
(537, '14', '1', '1', '1', '2021-05-03 20:47:18', 'admin'),
(538, '14', '1', '1', '1', '2021-05-03 20:48:48', 'admin'),
(539, '14', '1', '1', '1', '2021-05-03 20:56:08', 'admin'),
(540, '14', '1', '1', '1', '2021-05-03 21:01:45', 'admin'),
(541, '14', '1', '1', '1', '2021-05-03 21:03:20', 'admin'),
(542, '14', '1', '1', '1', '2021-05-03 21:05:11', 'admin'),
(543, '14', '1', '1', '1', '2021-05-06 23:07:47', 'admin'),
(544, '14', '1', '1', '1', '2021-05-07 00:04:16', 'admin'),
(545, '14', '1', '1', '1', '2021-05-20 18:03:46', 'admin'),
(546, '14', '1', '1', '1', '2021-05-20 18:08:43', 'admin'),
(547, '14', '1', '1', '1', '2021-05-20 18:20:07', 'admin'),
(548, '14', '1', '1', '1', '2021-05-20 18:26:35', 'admin'),
(549, '14', '1', '1', '1', '2021-05-20 21:16:24', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `usertest`
--

CREATE TABLE `usertest` (
  `ID` int(100) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Email` varchar(60) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `Icon` varchar(20) NOT NULL DEFAULT 'img/default.jpg',
  `Gender` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Country` varchar(45) NOT NULL,
  `Phone` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `usertest`
--

INSERT INTO `usertest` (`ID`, `Username`, `Email`, `Password`, `Icon`, `Gender`, `Address`, `Country`, `Phone`) VALUES
(1, 's4405272', 'ligushijila@gmail.com', '$2b$12$YaH6BYCGNPN7RwXepo0iDuu0.XmKZV.kOMdVU4DyiOKPy5h13ZMZ2', 'baa7da208ecf84b6.png', '', '', '', 0),
(7, 's4405278', 'ligusjila@gmail.com', '$2y$10$Uet3sY2u/4Frrs45Y6uWgO6oQDEBXMsNNDWAHvOLujDtPHOBDXfvC', 'default.jpg', 'Male', 'St.Lucia', 'Austraila', 451871234),
(8, 'admin', 'ligushijila2@gmail.com', '$2y$10$HRo1qEdo.vx3jIipki3JN.8rM3C/NIqTN17LCZbbo/xOCwflCPlVK', 'default.jpg', 'Male', '14', 'Australia', 451870270),
(9, 'admin2', '123@123.com', '$2y$10$yeuwPaZD1LbCRW12Sp0MduewLenzOoxtMwT5N.bbYkxf8XAL8derW', 'img/default.jpg', 'Male', '14', 'au', 451870270),
(10, 'admin3', '123@ga.com', '$2y$10$maor4zKQ6uVua5o7CjO.F.WhjNHvsATp9Wecza6u9BCGK7pHZ3s5i', 'img/default.jpg', 'Male', 'auu', 'au', 1234);

-- --------------------------------------------------------

--
-- Table structure for table `user_post_relationship`
--

CREATE TABLE `user_post_relationship` (
  `U_id` int(11) NOT NULL,
  `P_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_post_relationship`
--

INSERT INTO `user_post_relationship` (`U_id`, `P_id`) VALUES
(8, 1),
(8, 2),
(8, 3),
(8, 4),
(7, 14),
(8, 16),
(8, 447),
(8, 512),
(8, 513),
(8, 514),
(8, 515),
(8, 516),
(8, 517),
(8, 518),
(8, 519),
(8, 520),
(8, 521),
(8, 522),
(8, 523),
(8, 524),
(8, 525),
(8, 526),
(8, 527),
(8, 528),
(8, 529),
(8, 530),
(8, 531),
(8, 532),
(8, 533),
(8, 534),
(8, 535),
(8, 536),
(8, 537),
(8, 538),
(8, 539),
(8, 540),
(8, 541),
(8, 542),
(8, 543),
(8, 544),
(8, 545),
(8, 546),
(8, 547),
(8, 548),
(8, 549);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posttest`
--
ALTER TABLE `posttest`
  ADD PRIMARY KEY (`postID`);

--
-- Indexes for table `usertest`
--
ALTER TABLE `usertest`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Username_UNIQUE` (`Username`),
  ADD UNIQUE KEY `Email_UNIQUE` (`Email`);

--
-- Indexes for table `user_post_relationship`
--
ALTER TABLE `user_post_relationship`
  ADD PRIMARY KEY (`U_id`,`P_id`),
  ADD KEY `FK_Pid_idx` (`P_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `posttest`
--
ALTER TABLE `posttest`
  MODIFY `postID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=550;

--
-- AUTO_INCREMENT for table `usertest`
--
ALTER TABLE `usertest`
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_post_relationship`
--
ALTER TABLE `user_post_relationship`
  ADD CONSTRAINT `FK_Pid` FOREIGN KEY (`P_id`) REFERENCES `posttest` (`postID`),
  ADD CONSTRAINT `FK_Uid` FOREIGN KEY (`U_id`) REFERENCES `usertest` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
