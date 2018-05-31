package com.plr.service;

import org.springframework.web.multipart.MultipartFile;

public interface IPlrService {
	public String Plr_Uploadphoto(MultipartFile photofile);
	public String Plr_Getlabel(String photo_path);
}
