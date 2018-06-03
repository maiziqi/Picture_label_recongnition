package com.plr.service;

import java.util.List;

import com.plr.entity.PhotoName;

public interface IPhotonameService {
	public int insertPhotoname(String table_name,String photoname,String photo_character) throws Exception;
	public List<String> search_photoname(String table_name,int photo_num) throws Exception;
	public List<PhotoName> select_all_photo(String table_name)throws Exception;
}
