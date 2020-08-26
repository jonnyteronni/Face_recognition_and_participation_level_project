CREATE TABLE project9.timeseries (
`frame_id` int NOT NULL AUTO_INCREMENT,
`name` varchar(50)NOT NULL,
`time` float,
`record_source` varchar(50)NOT NULL,
`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (frame_id)
);