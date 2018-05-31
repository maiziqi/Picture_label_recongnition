package com.plr.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Date;

@Service
public class PlrServiceImpl implements IPlrService{		//����Ӧ�øĳɾ�̬�ؽ���socket���ӣ�Ȼ������һֱ��close����һ������ͷ�һ
	private final String photo_path="D:/tmp/Plr_UploadPhoto/";
	private final String server_ip="127.0.0.1";
	private final short server_port=6666;
	@Override
	public String Plr_Uploadphoto(MultipartFile photofile) {
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
	public String Plr_Getlabel(String photo_path) {
		//����Ӧ�õ���Tensorflow����ȡ������
		String result_labelname = null;
		try {
			Socket server_sock=new Socket(server_ip,server_port);
			PrintWriter printwriter=new PrintWriter(server_sock.getOutputStream());
			printwriter.write(photo_path);
			printwriter.flush();
			//printwriter.close();						�Ҳ� �����������һ�к�ͻ��������
			server_sock.shutdownOutput();    			//�ر������		
			
			InputStream inputstream=server_sock.getInputStream();
			BufferedReader bufferedreader=new BufferedReader(new InputStreamReader(inputstream));
			result_labelname=bufferedreader.readLine();
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
		System.out.println(result_labelname);
		return result_labelname;
	}

}
