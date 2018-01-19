-- Procedure to insert if userid exists
PROCEDURE `spAddItems` (IN `p_userId` INT, IN `p_item` VARCHAR(25))  
BEGIN
	if p_userId = (select UserId 
        from tbluser
        where userid = p_userid)
    then
        insert into tblItem(
            UserId,
            ItemName
        )
        values(
            p_userId,
            p_item
        );
	end if;
END$$

-- Procedure to authenticate user
PROCEDURE `spAuthenticateUser` (IN `p_username` VARCHAR(20))  
BEGIN
     select * from tblUser where UserName = p_username;
END$$

-- Procedure to create user if not exists
PROCEDURE `spCreateUser` (IN `p_Username` VARCHAR(50), IN `p_Password` VARCHAR(50))  
BEGIN
    if ( select exists (select 1 from tblUser where UserName = p_username) ) THEN
        select 'Username Exists !!';
    ELSE
    insert into tblUser
    (
        UserName,
        Password
    )
    values
    (
        p_Username,
        p_Password
    );
    END IF;
END$$

-- Procedure to delete item
PROCEDURE `spDeleteItem` (IN `p_itemId` INT)  
BEGIN
    DELETE FROM `tblitem` WHERE Id = p_itemId;
END$$

-- Procedure to get list of items
PROCEDURE `spGetAllItems` (IN `p_userId` INT)  
BEGIN
    select Id, ItemName from tblItem where UserId = p_userId; 
END$$

-- Procedure to get one item
PROCEDURE `spGetOneItem` (IN `p_id` INT(11))  
BEGIN
     select * from tblItem where Id = p_id;
END$$

-- Procedure to update item
PROCEDURE `spUpdateItem` (IN `p_itemId` INT, IN `p_itemName` VARCHAR(45))  
BEGIN    
    UPDATE `tblitem`
    SET `ItemName` = p_itemName
    WHERE `Id` = p_itemId;
END$$