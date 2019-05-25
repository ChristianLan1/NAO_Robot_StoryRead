/**
 * Author:LIUYI CHAI

 * Purpose:This class is a UI for users to upload their books
 */
import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Rectangle;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTable;
import javax.swing.JList;
import javax.swing.JButton;
import javax.swing.SwingConstants;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.util.ArrayList;
import java.util.List;
import java.awt.SystemColor;
import java.awt.Color;

import javax.swing.JEditorPane;

import java.awt.Font;

import javax.swing.UIManager;

import java.awt.event.MouseMotionAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JTextPane;


public class UploadUI<ClientUI> extends JFrame {
	private JPanel uploadPanel;
	private JTextField booknameField;
    private MainUI mainframe;
    private String path = "C:\\Users\\Zoe Chai\\Desktop\\nao\\nao_story_read\\NAO CODE\\books";//Chai
//    private String path = "C:\\Users\\Christian Lan\\OneDrive\\NAO CODE\\books";//Lan
    public static String bookTitle = "test";
	/**
	 * Launch the application.
	 */
	

	/**
	 * Create the frame.
	 */
	

	public UploadUI() {
		System.out.println("test");
		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				UploadUI uploadframe = new UploadUI();
				uploadframe.dispose();
			    	  
			}
		});
		
		
	
		setSize(518, 499);
		setLocationRelativeTo(null);
		uploadPanel = new JPanel();
		uploadPanel.setBackground(Color.WHITE);
		uploadPanel.setForeground(new Color(0, 0, 0));
		setContentPane(uploadPanel);
		uploadPanel.setLayout(null);
		
		
		JLabel lblBookTitle = new JLabel("Book Title:");
		lblBookTitle.setFont(new Font("Tahoma", Font.PLAIN, 18));
		lblBookTitle.setBounds(16, 150, 91, 35);
		uploadPanel.add(lblBookTitle);
		
		booknameField = new JTextField();
		booknameField.setFont(new Font("Tahoma", Font.PLAIN, 18));
		booknameField.setBounds(105, 150, 347, 35);
		uploadPanel.add(booknameField);
		booknameField.setColumns(10);
		
		
		JButton btnConfirm = new JButton("Confirm");
		btnConfirm.setFont(new Font("Tahoma", Font.PLAIN, 18));
		btnConfirm.setBounds(122, 395, 262, 35);
		uploadPanel.add(btnConfirm);
		
		JTextPane tipsPane = new JTextPane();
		tipsPane.setFont(new Font("Dialog", Font.PLAIN, 18));
		tipsPane.setForeground(Color.RED);
		tipsPane.setBounds(16, 201, 441, 132);
		uploadPanel.add(tipsPane);
		
		//set the upload button
		JButton btnuploadfile = new JButton("Choose file...");
		btnuploadfile.setFont(new Font("Tahoma", Font.PLAIN, 18));
		btnuploadfile.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.out.println("is this run?");
				JFileChooser c = new JFileChooser();
			      
				int rVal = c.showOpenDialog(UploadUI.this);
				if (rVal == JFileChooser.APPROVE_OPTION) {
			    	  
			    	  String fileName = c.getSelectedFile().getName();
			    	  String[] fileExtension = fileName.split("\\.");
			    	  
			    	  if (fileExtension[fileExtension.length - 1].equals("pdf")){
			    		  tipsPane.setText(null);
			    	      booknameField.setText(fileName);
			    	      //set the confirm button
			    	      btnConfirm.addActionListener(new ActionListener() {
			    				public void actionPerformed(ActionEvent e) {
			    					//copy the file to the the dictionary with the python files
			    					File bookfile = c.getSelectedFile();
			    					File copyfile = new File(path + "\\" +booknameField.getText());//test path
			    					
			    						if(copyfile.exists()){
			    							System.out.println("what's wrong");
			    							JOptionPane.showMessageDialog(null, "Oops! This book already exists.");
			    						}
			    						
			    						else{
			    							try {
												copyfile.createNewFile();
											
			    							    copyFile(bookfile, copyfile);//call the copyfile function
			    							    //show popup
			    							    JOptionPane.showConfirmDialog(null, "Book successfully uploaded! You can choose it from the book menu.");
			    		                        
					    					    //add the book tile to the booktitles array
					    					    System.out.println(mainframe.bookList);
					    					    bookTitle= getBookTitle(fileName);
					    					    mainframe.listModel.addElement(booknameField.getText());
					    					    
					    					    
			    							    
			    							} catch (IOException e1) {
												    // TODO Auto-generated catch block
												    e1.printStackTrace();
											}
			    						}
									
									
			    					
									
			    				}
			    			});
			    	  }
			    	  else{
			    		  tipsPane.setText("*The file you uploaded shoud be a pdf file.");
			    	  }
			        
			      }
				
			     if (rVal == JFileChooser.CANCEL_OPTION) {
			    	 tipsPane.setText("*Please choose a pdf file to upload.");
			    	 
			      }
			}
		});
		btnuploadfile.setBounds(6, 29, 475, 41);
		uploadPanel.add(btnuploadfile);
		
		}
	
	
	private void copyFile(File source, File dest) throws IOException {    
        FileChannel inputChannel = null;    
        FileChannel outputChannel = null;    
    try {
        inputChannel = new FileInputStream(source).getChannel();
        outputChannel = new FileOutputStream(dest).getChannel();
        outputChannel.transferFrom(inputChannel, 0, inputChannel.size());
    } finally {
        inputChannel.close();
        outputChannel.close();
    }
}
	
	public String getBookTitle(String fileName){
		bookTitle= fileName.substring(0, fileName.length()-4);
		return bookTitle;
		
	}



}

//:~