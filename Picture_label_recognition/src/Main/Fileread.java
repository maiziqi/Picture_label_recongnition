package Main;
//实现了图片路径的全自动读入数据库
import java.io.IOException;
import java.io.File;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.plr.service.LabelServiceImpl;
import com.plr.service.PhotonameServiceImpl;
import com.plr.service.PlrServiceImpl;
import com.plr.entity.Label;
import com.plr.entity.PhotoName;
import com.plr.general_class.photo_Label_and_Character;

public class Fileread {
	public Fileread() {}
	public static void file_list(String filepath) throws IOException{
		ApplicationContext ctx = new ClassPathXmlApplicationContext("classpath:config/Application.xml");
		LabelServiceImpl labelserviceimpl = ctx.getBean(LabelServiceImpl.class);
		PhotonameServiceImpl photonameserviceimpl=ctx.getBean(PhotonameServiceImpl.class);
		PlrServiceImpl plrserviceimpl=ctx.getBean(PlrServiceImpl.class);
		File file=new File(filepath);
		for(String label:file.list()) {
			String table_name=label+"_table";								//规定一个label的图片表名为：label名+"_table"
			try {
				if(!labelserviceimpl.isexist(label)) {								//查询label是否已存在，不存在则创建
					Label new_label=new Label(label,filepath+"/"+label,table_name);		//标签名，路径，表名
					labelserviceimpl.insertLabel(new_label);
					labelserviceimpl.createlabel_table(table_name);					//同时还要创建该label的图片表
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			File labelfile=new File(filepath+"/"+label);
			for(String photo_name:labelfile.list()) {
				String photo_path=labelfile.getAbsolutePath()+"/"+photo_name;			//图片的绝对路径
				photo_Label_and_Character plac=plrserviceimpl.Plr_Getlabel(photo_path);
				String photo_character=plac.getPhoto_character();
				try {
					photonameserviceimpl.insertPhotoname(table_name, photo_name,photo_character);
				} catch (Exception e) {
					e.printStackTrace();
				}
				
				/*File photo_path=new File(labelfile+"/"+photo_name);
				System.out.println(photo_path.toString());*/
			}
		}
	}
	
	public static void main(String[] args) {
		String filepath="D:/tmp/mycifar10_data/Train";
		try{
			Fileread.file_list(filepath);
		}catch(IOException e) {
			System.out.println(e);
		}
	}
}
