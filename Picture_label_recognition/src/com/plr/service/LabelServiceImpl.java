package com.plr.service;

import com.plr.entity.Label;
import com.plr.dao.ILabelDAO;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LabelServiceImpl implements ILabelService{
	@Autowired
	private ILabelDAO labeldao;
	
	@Override
	public int insertLabel(Label label) throws Exception{
		return labeldao.insertLabel(label);
	}
	
	@Override
	public boolean isexist(String label_name) throws Exception{
		return labeldao.isexist(label_name)!=0;
	}
	
	@Override
	public int createlabel_table(String table_name) throws Exception{
		return labeldao.createlabel_table(table_name);
	}

	@Override
	public Label select_by_labelname(String label_name) throws Exception {
		return labeldao.select_by_labelname(label_name);
	}

	@Override
	public List<Label> select_all_label() throws Exception {
		return labeldao.select_all_label();
	}
}
