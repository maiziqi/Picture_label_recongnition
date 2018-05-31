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
public class PlrServiceImpl implements IPlrService{		//这里应该改成静态地进行socket连接，然后连接一直不close，有一次请求就发一
	private final String photo_path="D:/tmp/Plr_UploadPhoto/";
	private final String server_ip="127.0.0.1";
	private final short server_port=6666;
	@Override
	public String Plr_Uploadphoto(MultipartFile photofile) {
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
	public String Plr_Getlabel(String photo_path) {
		//这里应该调用Tensorflow，获取分类结果
		String result_labelname = null;
		try {
			Socket server_sock=new Socket(server_ip,server_port);
			PrintWriter printwriter=new PrintWriter(server_sock.getOutputStream());
			printwriter.write(photo_path);
			printwriter.flush();
			//printwriter.close();						我曹 在这里加上这一行后就会出错？？？
			server_sock.shutdownOutput();    			//关闭输出流		
			
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
