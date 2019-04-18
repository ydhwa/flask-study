/* 버킷 리스트 수정 등의 작업을 위한 특정한 버킷 리스트 하나를 조회하는 프로시저 */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getWishById` (
	IN p_wish_id bigint,
    IN p_user_id bigint
)
BEGIN
select * from tbl_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END

/* 버킷 리스트 아이템 수정하는 프로시저 */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateWish` (
	IN p_title varchar(45),
    IN p_description varchar(1000),
    IN p_wish_id bigint,
    IN p_user_id bigint
)
BEGIN
update tbl_wish set wish_title = p_title, wish_description = p_description
	where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$
DELIMITER ;

/* 버킷 리스트 아이템 삭제하는 프로시저 */
DELIMITER $$
USE `BucketList` $$
CREATE PROCEDURE `sp_deleteWish` (
	IN p_wish_id bigint,
    IN p_user_id bigint
)
BEGIN
delete from tbl_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$
DELIMITER ;

