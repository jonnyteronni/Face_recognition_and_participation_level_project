CREATE TABLE project9.timeseries (
`id` int NOT NULL AUTO_INCREMENT,
`frame_id` int,
`name` varchar(100)NOT NULL,
`time` float,
`record_source` varchar(100)NOT NULL,
`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`id`)
);