package com.plr.service;

import java.util.List;
import java.util.ArrayList;

//import com.plr.entity.PhotoName;
import com.plr.dao.IPhotonameDAO;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PhotonameServiceImpl implements IPhotonameService {
	@Autowired
	private IPhotonameDAO photonamedao;

	@Override
	public int insertPhotoname(String table_name, String photoname) throws Exception {
		return photonamedao.insertPhotoname(table_name, photoname);
	}

	@Override
	public List<String> search_photoname(String table_name, int photo_num) throws Exception {
		List<String> photo_list=new ArrayList<String>();
		for(int i=0;i<photo_num;i++) {
			photo_list.add(photonamedao.search_photo(table_name));
		}
		return photo_list;
	}
}