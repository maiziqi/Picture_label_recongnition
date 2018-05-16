package com.plr.controller;

import java.util.List;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import javax.annotation.Resource;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.plr.entity.Label;
import com.plr.entity.PhotoName;
import com.plr.service.LabelServiceImpl;
import com.plr.service.PhotonameServiceImpl;
import com.plr.service.PlrServiceImpl;


@Controller 
public class LabelController {
	@Resource
	private LabelServiceImpl labelserviceimpl;
	@Resource
	private PhotonameServiceImpl photonameserviceimpl;
	@Resource
	private PlrServiceImpl plrserviceimpl;
	
	@RequestMapping("/plr_getlabel")
	@ResponseBody//此注解不能省略 否则ajax无法接受返回值(不加时，return就是跳转页面了) 
	public String plr_getlabel(@RequestParam(value="photopath")String photopath) {
//		System.out.println("?w"+photopath);
//		List<String> label_list=new ArrayList<String>();
//		label_list.add("D:/abc");
//		label_list.add("C:/qwer");
//		JSONArray jsonarray = JSONArray.fromObject(label_list);
//		JSONObject json=new JSONObject();
//		json.put("label_list", jsonarray);
//		return json.toString();
		JSONObject result_json=new JSONObject();
		String labelname=plrserviceimpl.Plr_Getlabel(photopath);
		result_json.put("labelname", labelname);
//		try {
//			Label label=labelserviceimpl.select_by_labelname(labelname);
//			result_json.put("labelpath", label.getLabel_path());
//			String table_name=label.getTable_name();
//			System.out.println(table_name);
//			//获取所有图片名字
//		}catch(Exception e) {
//			System.out.println(e);
//		}
		return result_json.toString();
	}
	
	@RequestMapping("/plr_getphoto")
	@ResponseBody
	public String plr_getphoto(@RequestParam(value="labelname")String labelname,@RequestParam(value="photonum")int photonum) {
		JSONObject result_json=new JSONObject();
		try{
			if(!labelserviceimpl.isexist(labelname)) {
				result_json.put("isexist", 0);						//0代表不存在
				throw new Exception("Exception:Label not exist label");
			}
			Label label=labelserviceimpl.select_by_labelname(labelname);
			result_json.put("labelpath", label.getLabel_path());
			String table_name=label.getTable_name();
			List<String> photo_list=photonameserviceimpl.search_photoname(table_name, photonum);
			JSONArray json_photo_list=JSONArray.fromObject(photo_list);
			result_json.put("photolist", json_photo_list);
		}catch(Exception e) {
			System.out.println(e);
		}
		finally{
			return result_json.toString();
		}
	}
	
}
