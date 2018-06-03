package com.plr.service;

import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import com.plr.entity.PhotoName;
import com.plr.general_class.photoname_and_characterArray;
import com.plr.general_class.photo_Label_and_Character;

public interface IPlrService {
	public String Plr_Uploadphoto(MultipartFile photofile);
	public photo_Label_and_Character Plr_Getlabel(String photo_path);
	public String[] Similar_Picture_Recognition(List<photoname_and_characterArray> all_photo,String character_str);
}
