package com.plr.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;



import com.plr.entity.PhotoName;

//import com.plr.entity.PhotoName;

public interface IPhotonameDAO {
	public int insertPhotoname(@Param("table_name")String table_name,@Param("photoname")String photoname,@Param("photo_character")String photo_character) throws Exception;
	public List<String> search_photo(@Param("table_name")String table_name,@Param("photo_num")int num) throws Exception;
	public List<PhotoName> select_all_photo(@Param("table_name")String table_name)throws Exception;
}
