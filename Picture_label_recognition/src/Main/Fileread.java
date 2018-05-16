package Main;
//实现了图片路径的全自动读入数据库
import java.io.IOException;
import java.io.File;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.plr.service.LabelServiceImpl;
import com.plr.service.PhotonameServiceImpl;
import com.plr.entity.Label;
import com.plr.entity.PhotoName;

public class Fileread {
	public Fileread() {}
	public static void file_list(String filepath) throws IOException{
		ApplicationContext ctx = new ClassPathXmlApplicationContext("classpath:config/Application.xml");
		LabelServiceImpl labelserviceimpl = ctx.getBean(LabelServiceImpl.class);
		PhotonameServiceImpl photonameserviceimpl=ctx.getBean(PhotonameServiceImpl.class);
		File file=new File(filepath);
		for(String label:file.list()) {
			String table_name=label+"_table";
			try {
				if(!labelserviceimpl.isexist(label)) {
					Label new_label=new Label(label,filepath+"/"+label,table_name);
					labelserviceimpl.insertLabel(new_label);
					labelserviceimpl.createlabel_table(table_name);
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			File labelfile=new File(filepath+"/"+label+"/full");
			for(String photo_name:labelfile.list()) {
				
				try {
					photonameserviceimpl.insertPhotoname(table_name, photo_name);
				} catch (Exception e) {
					e.printStackTrace();
				}
				
				File photo_path=new File(labelfile+"/"+photo_name);
				System.out.println(photo_path.toString());
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
