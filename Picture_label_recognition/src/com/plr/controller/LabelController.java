package com.plr.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;

import com.plr.entity.Label;
import com.plr.entity.PhotoName;
import com.plr.general_class.photo_Label_and_Character;
import com.plr.general_class.photoname_and_characterArray;
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
							
	public static HashMap<String,List<photoname_and_characterArray>> photo_list_hash=new HashMap<String,List<photoname_and_characterArray>>();
	
	static{								//这里将数据库中所有图片读好，目的是提前将字符串形式的图片特征值处理并存储为double数组，以空间换时间
		ApplicationContext ctx = new ClassPathXmlApplicationContext("classpath:config/Application.xml");			//静态方法里暂时只能这样获取到bean了
		LabelServiceImpl static_labelserviceimpl = ctx.getBean(LabelServiceImpl.class);
		PhotonameServiceImpl static_photonameserviceimpl=ctx.getBean(PhotonameServiceImpl.class);
		try {
			List<Label> label_list=static_labelserviceimpl.select_all_label();
			for(Label label:label_list) {
				String table_name=label.getTable_name();
				List<PhotoName> all_photo=static_photonameserviceimpl.select_all_photo(table_name);
				List<photoname_and_characterArray> pac_list=new ArrayList<photoname_and_characterArray>();
				for(PhotoName photo:all_photo) {
					photoname_and_characterArray pac=new photoname_and_characterArray(photo.getPhoto_name(),photo.getPhoto_character());
					pac_list.add(pac);
				}
				photo_list_hash.put(label.getLabel_name(), pac_list);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@RequestMapping(value="/plr_getphoto",produces="application/json;charset=utf-8")
	@ResponseBody
	public String plr_getphoto(@RequestParam(value="labelname")String labelname,@RequestParam(value="photonum")int photonum) {		//给出标签名label和图片数量N，随机返回N张label标签的图片
		JSONObject result_json=new JSONObject();
		try{
			if(!labelserviceimpl.isexist(labelname)) {
				result_json.put("isexist", 0);						//0代表不存在
				throw new Exception("Exception:Label not exist");
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
	
	@RequestMapping(value="/plr_getlabel",method=RequestMethod.POST,produces="application/json;charset=utf-8")
	@ResponseBody
	public String plr_getlabel(@RequestParam(value="photo")MultipartFile photofile) {			//仅仅获得上传图片的标签
		JSONObject result_json=new JSONObject();
		if(photofile==null||photofile.isEmpty()) {
			result_json.put("upload_success",false);
			return result_json.toString();
		}
		String photoFullpath=plrserviceimpl.Plr_Uploadphoto(photofile);
		if(photoFullpath==null) {
			result_json.put("upload_success",false);
			return result_json.toString();
		}
		result_json.put("upload_success", true);
		photo_Label_and_Character plac=plrserviceimpl.Plr_Getlabel(photoFullpath);
		result_json.put("labelname", plac.getPhoto_label());
		return result_json.toString();
	}
	
	@RequestMapping(value="/plr_getsimilarphoto",method=RequestMethod.POST, produces = "application/json; charset=utf-8")
	@ResponseBody
	public String plr_getsimilarphoto(@RequestParam(value="photo")MultipartFile photofile) {		//客户端上传一张图片，下载该图片，并将该图片丢入Tensorflow测试，返回预测的label
		//System.out.println("666");
		JSONObject result_json=new JSONObject();
		if(photofile==null||photofile.isEmpty()) {
			result_json.put("upload_success",false);
			return result_json.toString();
		}
		String photoFullpath=plrserviceimpl.Plr_Uploadphoto(photofile);
		if(photoFullpath==null) {
			result_json.put("upload_success",false);
			return result_json.toString();
		}
		result_json.put("upload_success", true);
		photo_Label_and_Character plac=plrserviceimpl.Plr_Getlabel(photoFullpath);			//获得图片标签和特征值
		String label_name=plac.getPhoto_label();
		String label_character=plac.getPhoto_character();
		result_json.put("labelname", label_name);
		
		try {
			Label label=labelserviceimpl.select_by_labelname(label_name);
			result_json.put("labelpath", label.getLabel_path());						//放入该标签路径
			List<photoname_and_characterArray> photo_list=photo_list_hash.get(label_name);
			String similar_photo_name_list[]=plrserviceimpl.Similar_Picture_Recognition(photo_list, label_character);
			JSONArray similar_photo_name_jsonarray=JSONArray.fromObject(similar_photo_name_list);
			result_json.put("similar_photo_list", similar_photo_name_jsonarray);				//放入相似图片名字数组
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return result_json.toString();
	}
}
