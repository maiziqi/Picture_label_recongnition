package com.plr.service;

import org.springframework.stereotype.Service;

@Service
public class PlrServiceImpl implements IPlrService{

	@Override
	public String Plr_Getlabel(String photo_path) {
		//这里应该调用Tensorflow，获取分类结果
		return "Tiger";
	}

}
