package com.plr.dao;

import org.apache.ibatis.annotations.Param;

//import com.plr.entity.PhotoName;

public interface IPhotonameDAO {
	public int insertPhotoname(@Param("table_name")String table_name,@Param("photoname")String photoname) throws Exception;
	public String search_photo(@Param("table_name")String table_name) throws Exception;
}
