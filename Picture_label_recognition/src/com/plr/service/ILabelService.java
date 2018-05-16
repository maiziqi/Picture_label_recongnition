package com.plr.service;

import com.plr.entity.Label;

public interface ILabelService {
	public int insertLabel(Label label) throws Exception;
	public boolean isexist(String label_name) throws Exception;
	public int createlabel_table(String table_name) throws Exception;
	public Label select_by_labelname(String label_name) throws Exception;
}
