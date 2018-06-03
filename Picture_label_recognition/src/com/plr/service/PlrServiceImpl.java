package com.plr.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import net.sf.json.JSONArray;									//����������ͨѶ��Ҫ�õ�json
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
	public String Plr_Uploadphoto(MultipartFile photofile) {								//�ͻ����ϴ�һ��MultipartFile��Ƭ�����ظ���Ƭ��������·��
		Date date=new Date();
		String photoFullpath=photo_path+date.getTime()+"_"+photofile.getOriginalFilename();			//ͼƬ��ǰ����ʱ��ǰ׺����ֹͼƬ���ظ�
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
	public photo_Label_and_Character Plr_Getlabel(String photo_path) {					//����ͼƬ·�������ظ���Ƭ��Ԥ��������������
		//����Ӧ�õ���Tensorflow����ȡ������
		photo_Label_and_Character photo_result = null;
		try {
			Socket server_sock=new Socket(server_ip,server_port);
			PrintWriter printwriter=new PrintWriter(new OutputStreamWriter(server_sock.getOutputStream(),"utf-8"));
			printwriter.write(photo_path);
			printwriter.flush();
			//printwriter.close();						�Ҳ� �����������һ�к�ͻ��������
			server_sock.shutdownOutput();    			//�ر������		
			
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
	public String[] Similar_Picture_Recognition(List<photoname_and_characterArray> all_photo, String character_str) {		//����ͼƬʶ��
		Similar_photo[] similar_photo=new Similar_photo[similar_num];
		double[] target_photo_characterArray=photoname_and_characterArray.trunStr_toArray(character_str);
		int num=all_photo.size();
		for(int i=0;i<num;i++) {
			photoname_and_characterArray curr_photo=all_photo.get(i);
			double curr_degree=compare_photo(curr_photo.getCharacterArray(),target_photo_characterArray);
			Similar_photo new_similar_photo=new Similar_photo(curr_photo.getPhotoname(),curr_degree);
			int j=0,end=Math.min(similar_num-1, i);
			for(;j<end&&curr_degree>similar_photo[j].degree;j++);	//j�ҵ�����curr_photoӦ�ò����λ��
			if(j==similar_num) continue;						//�ȵ�������������
			similar_photo[end]=new_similar_photo;
			for(int z=end;z>j;z--) myswitch(similar_photo,z,z-1);		//curr_photo�����ǰ�ƣ�ֱ���Լ���λ��
		}
		String[] result=new String[similar_num];
		for(int i=0;i<similar_num;i++) result[i]=similar_photo[i].photo_name;		//��ǰ��������¼��result
		return result;
	}
	private static final int similar_num=4;									//ֻ�ҳ�ͼƬ�������ƶ�ǰ  4  ����ͼƬ
	private class Similar_photo{							//����������Ϊ���������һ�㣨������һ�����ݽṹ��
		public String photo_name;
		public double degree;			//degree��¼���Ƴ̶ȣ�ԽСԽ���ƣ�
		public Similar_photo(String photo_name,double degree) {
			this.photo_name=photo_name;
			this.degree=degree;
		}
	}
	private double compare_photo(double[] curr_character,double[]target_character) {		//�Ƚ�ͼƬ������ֵ��������ֵ��
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
