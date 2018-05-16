package com.plr.entity;

public class Label {
	int label_id;
	String label_name;
	String label_path;
	String table_name;
//	public Label(int label_id,String label_name,String label_path,String table_name) {
//		this.label_id=label_id;
//		this.label_name=label_name;
//		this.label_path=label_path;
//		this.table_name=table_name;
//	}
	public Label(String label_name,String label_path,String table_name) {
		this.label_name=label_name;
		this.label_path=label_path;
		this.table_name=table_name;
	}
	public int getLabel_id() {
		return label_id;
	}
	public void setLabel_id(int label_id) {
		this.label_id = label_id;
	}
	public String getLabel_name() {
		return label_name;
	}
	public void setLabel_name(String label_name) {
		this.label_name = label_name;
	}
	
	public String getLabel_path() {
		return label_path;
	}
	public void setLabel_path(String label_path) {
		this.label_path = label_path;
	}
	public String getTable_name() {
		return table_name;
	}
	public void setTable_name(String table_name) {
		this.table_name = table_name;
	}
	
}
