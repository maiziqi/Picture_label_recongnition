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
public class PlrServiceImpl implements IPlrService{
	private final static String photo_path="D:/tmp/Plr_UploadPhoto/";
	private final static String server_ip="127.0.0.1";
	private final static short server_port=6666;
	private static Socket socket;
	private static PrintWriter pw;
	private static BufferedReader br;
	static {										//将socket连接改为静态连接，并一直不断开，减少socket连接时间
		try {
			socket=new Socket(server_ip,server_port);
			pw=new PrintWriter(socket.getOutputStream());
			InputStream inputstream=socket.getInputStream();
			br=new BufferedReader(new InputStreamReader(inputstream,"utf-8"));
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
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
			pw.write(photo_path);
			pw.flush();
			//printwriter.close();						我曹 在这里加上这一行后就会出错？？？	

			result_labelname=br.readLine();
			System.out.println(result_labelname);
			return result_labelname;
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}

}
