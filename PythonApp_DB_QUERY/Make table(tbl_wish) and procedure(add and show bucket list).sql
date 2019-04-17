USE `BucketList`;

/* 버킷 리스트 테이블 생성 */
CREATE TABLE `tbl_wish` (
	`wish_id` int(11) NOT NULL AUTO_INCREMENT,
    `wish_title` varchar(45) DEFAULT NULL,
    `wish_description` varchar(5000) DEFAULT NULL,
    `wish_user_id` int(11) DEFAULT NULL,
    `wish_date` datetime DEFAULT NULL,
    PRIMARY KEY (`wish_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/* 버킷 리스트 저장 프로시저 */
USE `BucketList`;
DROP procedure IF EXISTS `BucketList`.`sp_addWish`;
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addWish` (
	IN p_title varchar(45),
    IN p_description varchar(1000),
    IN p_user_id bigint
)
BEGIN
	insert into tbl_wish (
		wish_title,
        wish_description,
        wish_user_id,
        wish_date
	)
    values (
		p_title,
        p_description,
        p_user_id,
        NOW()
	);
END$$
DELIMITER ;;

/* 버킷리스트를 조회하는 프로시저 */
USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishByUser`;
DELIMITER $$
USE `BucketList`$$
CREATE PROCEDURE `sp_GetWishByUser` (
	IN p_user_id bigint
)
BEGIN
	select * from tbl_wish where wish_user_id = p_user_id;
END $$
DELIMITER ;

