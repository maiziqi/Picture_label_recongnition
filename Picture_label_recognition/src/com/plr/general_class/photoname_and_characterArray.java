package com.plr.general_class;

public class photoname_and_characterArray {
	private String photoname;
	private double[] characterArray;
	public photoname_and_characterArray(String photoname,String character_str) {
		this.photoname=photoname;
		this.characterArray=trunStr_toArray(character_str);
	}
	public String getPhotoname() {
		return photoname;
	}
	public double[] getCharacterArray() {
		return characterArray;
	}
	public static double[] trunStr_toArray(String str) {					//将字符串的character转化为一个double数组
		double[] array;
		String str_list[]=str.split(",");
		array=new double[str_list.length];
		for(int i=0;i<str_list.length;i++) array[i]=Double.parseDouble(str_list[i]);
		return array;
	}
}
