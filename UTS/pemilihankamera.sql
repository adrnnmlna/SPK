-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 31, 2023 at 04:51 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_pemilihankamera`
--

-- --------------------------------------------------------

--
-- Table structure for table `pemilihankamera`
--

CREATE TABLE `pemilihankamera` (
  `Nama_Kamera` varchar(30) NOT NULL,
  `Penyimpanan_Memori` varchar(10) NOT NULL,
  `Kapasitas_Baterai` varchar(10) NOT NULL,
  `Harga` varchar(30) NOT NULL,
  `Berat` varchar(10) NOT NULL,
  `Kualitas_Hasil` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pemilihankamera`
--

INSERT INTO `pemilihankamera` (`Nama_Kamera`, `Penyimpanan_Memori`, `Kapasitas_Baterai`, `Harga`, `Berat`, `Kualitas_Hasil`) VALUES
('Canon EOS 80D', '120 GB', '2130mAh', 'Rp6.500.000', '650gram', '7 per 10'),
('Canon EOS RP', '100 GB', ' 1080mAh ', ' Rp11.900.000 ', '880 gram', '9 per 10'),
('Canon EOS M6 Mark II', '60 GB', ' 1040mAh ', ' Rp8.900.000 ', '408 gram', '8 per 10'),
('Canon EOS 70D', '100 GB', ' 1800mAh ', ' Rp5.755.000 ', '755 gram', '8 per 10'),
('Sony Alpha A1', '80 GB', ' 2280mAh ', ' Rp20.000.000 ', '737 gram', '9 per 10'),
('Sony Alpha 7 II', '50 GB', ' 1080mAh ', ' Rp8.300.000 ', '371 gram', '7 per 10'),
('Sony Alpha A6400', '200 GB', ' 1020mAh ', ' Rp10.000.000 ', '403 gram', '7 per 10'),
('Nikon Coolpix P1000', '90 GB', ' 1100mAh ', ' Rp11.000.000 ', '1415 gram', '8 per 10'),
('Nikon Z50', '120 GB', ' 1120mAh ', ' Rp12.000.000 ', '395 gram', '9 per 10'),
('Nikon 1 J5', '70 GB', ' 1020mAh ', ' Rp4.760.000 ', '265 gram', '8 per 10');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
