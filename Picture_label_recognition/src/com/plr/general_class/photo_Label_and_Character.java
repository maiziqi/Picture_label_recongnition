package com.plr.general_class;

public class photo_Label_and_Character {						//��������������LabelServiceImpl��Controller����ʱ��ͬʱ����label��character
	private String photo_label;
	private String photo_character;
	
	public photo_Label_and_Character(String photo_label,String photo_character) {
		this.photo_label=photo_label;
		this.photo_character=photo_character.substring(1, photo_character.length()-1);					//ȥ���ַ���ǰ���"["��"]"
	}
	public String getPhoto_label() {
		return photo_label;
	}
	public String getPhoto_character() {
		return photo_character;
	}
}
