USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishByUser`;

/* 페이지네이션을 위한 버킷리스트 항목 조회 프로시저 */
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishByUser` (
	IN p_user_id bigint,
	IN p_limit int,
    IN p_offset int
)
BEGIN
	SET @t1 = CONCAT('select * from tbl_wish where wish_user_id = ', p_user_id, ' order by wish_date desc limit ', p_limit, ' offset ', p_offset);
    PREPARE stmt FROM @t1;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$
DELIMITER ;


USE `BucketList`;
DROP procedure IF EXISTS `sp_GetWishByUser`;

/* 동적으로 페이지네이션을 하기 위한 프로시저 */
DELIMITER $$
USE `BucketList`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishByUser` (
	IN p_user_id bigint,
    IN p_limit int,
    IN p_offset int,
    out p_total bigint
)
BEGIN
	select count(*) into p_total from tbl_wish where wish_user_id = p_user_id;
    SET @t1 = CONCAT('select * from tbl_wish where wish_user_id = ', p_user_id, ' order by wish_date desc limit ', p_limit, ' offset ', p_offset);
    PREPARE stmt FROM @t1;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$
DELIMITER ;
