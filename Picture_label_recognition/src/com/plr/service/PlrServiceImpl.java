package com.plr.service;

import org.springframework.stereotype.Service;

@Service
public class PlrServiceImpl implements IPlrService{

	@Override
	public String Plr_Getlabel(String photo_path) {
		//����Ӧ�õ���Tensorflow����ȡ������
		return "Tiger";
	}

}
