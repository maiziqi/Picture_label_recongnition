package com.plr.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import net.sf.json.JSONArray;									//与服务器间的通讯需要用到json
import net.sf.json.JSONObject;	

import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Date;
import java.util.List;

import com.plr.entity.PhotoName;
import com.plr.general_class.photo_Label_and_Character;
import com.plr.general_class.photoname_and_characterArray;

@Service
public class PlrServiceImpl implements IPlrService{
	private final String photo_path="D:/tmp/Plr_UploadPhoto/";
	private final String server_ip="127.0.0.1";
	private final short server_port=6666;
	@Override
	public String Plr_Uploadphoto(MultipartFile photofile) {								//客户端上传一张MultipartFile照片，下载该照片，并返回路径
		Date date=new Date();
		String photoFullpath=photo_path+date.getTime()+"_"+photofile.getOriginalFilename();			//图片名前加上时间前缀，防止图片名重复
		FileOutputStream fos=null;
		try {
			fos=new FileOutputStream(photoFullpath);
			fos.write(photofile.getBytes());
			return photoFullpath;
		}
		catch(Exception e) {
			e.printStackTrace();
			return null;
		}
		finally {
			try {
				fos.close();
			}catch(IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	@Override
	public photo_Label_and_Character Plr_Getlabel(String photo_path) {					//输入图片路径，返回该照片的预测结果和特征向量
		//这里应该调用Tensorflow，获取分类结果
		photo_Label_and_Character photo_result = null;
		try {
			Socket server_sock=new Socket(server_ip,server_port);
			PrintWriter printwriter=new PrintWriter(new OutputStreamWriter(server_sock.getOutputStream(),"utf-8"));
			printwriter.write(photo_path);
			printwriter.flush();
			//printwriter.close();						我曹 在这里加上这一行后就会出错？？？
			server_sock.shutdownOutput();    			//关闭输出流		
			
			InputStream inputstream=server_sock.getInputStream();
			BufferedReader bufferedreader=new BufferedReader(new InputStreamReader(inputstream,"utf-8"));
			String result=bufferedreader.readLine();
			JSONObject jsonobject=JSONObject.fromObject(result);
			photo_result=new photo_Label_and_Character(jsonobject.get("label").toString(),jsonobject.get("character").toString());
			printwriter.close();	
			bufferedreader.close();
			
			server_sock.close();
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
//		System.out.println(result_labelname);
		return photo_result;
	}

	@Override
	public String[] Similar_Picture_Recognition(List<photoname_and_characterArray> all_photo, String character_str) {		//相似图片识别
		Similar_photo[] similar_photo=new Similar_photo[similar_num];
		double[] target_photo_characterArray=photoname_and_characterArray.trunStr_toArray(character_str);
		int num=all_photo.size();
		for(int i=0;i<num;i++) {
			photoname_and_characterArray curr_photo=all_photo.get(i);
			double curr_degree=compare_photo(curr_photo.getCharacterArray(),target_photo_characterArray);
			Similar_photo new_similar_photo=new Similar_photo(curr_photo.getPhotoname(),curr_degree);
			int j=0,end=Math.min(similar_num-1, i);
			for(;j<end&&curr_degree>similar_photo[j].degree;j++);	//j找到的是curr_photo应该插入的位置
			if(j==similar_num) continue;						//比第五名还大，跳过
			similar_photo[end]=new_similar_photo;
			for(int z=end;z>j;z--) myswitch(similar_photo,z,z-1);		//curr_photo逐个往前移，直至自己的位置
		}
		String[] result=new String[similar_num];
		for(int i=0;i<similar_num;i++) result[i]=similar_photo[i].photo_name;		//将前五名名字录入result
		return result;
	}
	private static final int similar_num=4;									//只找出图片库中相似度前  4  名的图片
	private class Similar_photo{							//这个类仅仅是为了排序好排一点（即定义一种数据结构）
		public String photo_name;
		public double degree;			//degree记录相似程度（越小越相似）
		public Similar_photo(String photo_name,double degree) {
			this.photo_name=photo_name;
			this.degree=degree;
		}
	}
	private double compare_photo(double[] curr_character,double[]target_character) {		//比较图片的特征值，获得其差值和
		double result=0.0;
		for(int i=0;i<curr_character.length;i++) {
			result+=Math.abs(curr_character[i]-target_character[i]);
		}
		return result;
	}
	private void myswitch(Similar_photo[] array,int i,int j) {
		Similar_photo t=array[i];
		array[i]=array[j];
		array[j]=t;
	}
}
