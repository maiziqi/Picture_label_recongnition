package com.plr.dao;

import org.apache.ibatis.annotations.Param;

import com.plr.entity.Label;

public interface ILabelDAO {
	public int insertLabel(Label label) throws Exception;
	public int isexist(String label_name) throws Exception;
	public int createlabel_table(@Param("table_name")String table_name) throws Exception;
	public Label select_by_labelname(String label_name) throws Exception;
}
