package com.plr.entity;

public class PhotoName {
	int photo_id;
	String photo_name;
	public PhotoName(String photo_name) {
		this.photo_name=photo_name;
	}
	public int getPhoto_id() {
		return photo_id;
	}
	public void setPhoto_id(int photo_id) {
		this.photo_id = photo_id;
	}
	public String getPhoto_name() {
		return photo_name;
	}
	public void setPhoto_name(String photo_name) {
		this.photo_name = photo_name;
	}
}
