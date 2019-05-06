/**
 * Author:LIUYI CHAI

 * Purpose:This class is a UI for users to choose books
 */

import java.awt.EventQueue;

import javax.swing.JFrame;

import java.awt.GridLayout;

import javax.swing.JPanel;

import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridBagLayout;
import java.awt.Image;
import java.awt.Toolkit;

import javax.swing.JTextField;

import java.awt.GridBagConstraints;

import javax.swing.JButton;

import java.awt.Insets;

import javax.swing.JTextArea;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.net.*;
import java.nio.Buffer;
import java.util.*;

import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JLabel;
import javax.swing.GroupLayout.Alignment;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.SwingConstants;

import java.awt.Font;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.Color;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.SystemColor;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;

import javax.swing.JList;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.util.ImageIOUtil;

public class PDF_Server{
	private JFrame mainframe;
	private JLabel imgLabel;
	private String pathChai = "C:\\Users\\Zoe Chai\\Desktop";
	private String pathLan = "C:\\Users\\Christian Lan\\OneDrive\\NAO CODE";
	public static List<String> bookList = new ArrayList<>();
	public static JList<String> list = new JList<String>(new DefaultListModel<String>());
	public static File bookText;
	
	private ServerSocket listeningSocket;
	private static final int PORT = 5555;
	private int numOfClients;
	
	public static void main(String[] args) throws IOException {
		
		PDF_Server server= new PDF_Server();
		
		server.mainframe.setVisible(true);
		server.start();
		
		

	}

	public PDF_Server() throws IOException {
		    System.out.println("initializing the server...");
		    listeningSocket = new ServerSocket(8088);
			
		    initialize();
			
		
	}
	
	/**
	 * Initialize the contents of the frame.
	 */
	public void initialize() {
		mainframe = new JFrame();
		mainframe.getContentPane().setBackground(Color.WHITE);
		mainframe.getContentPane().setFont(new Font("Cooper Black", Font.BOLD, 19));
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		int width = (int)screenSize.getWidth();
		int height = (int)screenSize.getHeight();
		
		mainframe.setSize(width,height);
		mainframe.setLocationRelativeTo(null);
		mainframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		mainframe.getContentPane().setLayout(null);
		
		imgLabel = new JLabel("Waiting for the robot to connect......",SwingConstants.CENTER);
		imgLabel.setFont(new Font("Lucida Grande", Font.PLAIN, 20));
		imgLabel.setBounds(mainframe.getBounds());
		mainframe.getContentPane().add(imgLabel);
		
	}
	
	
	
	public void requests(Socket socket){
			try {
	
				
				System.out.println("1");//test 1
				
				BufferedReader reader;
				String line;
				String clientMsg = null;
				
				reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));
                
				//get the pages and book title
				String[] pages = getBookPages();
				List<String> pageArray = new ArrayList<>(); 
				for(int i=1;i<pages.length;i++){
					pageArray.add(pages[i]);
					System.out.println("pageArray:"+pageArray.get(i-1));
				}
				
				String bookTitle = getBookTitle();
				
				imgLabel.setText("Connection established. Preparing the book file......");
				convert(bookTitle);//parse the pdf file
				
				System.out.println("2");//test 2
				
				
				//set the book cover as the first page
				imgLabel.setText("");
				Image pageImg = new ImageIcon(pathChai + "\\imgs\\0.png").getImage();
				Image scaledImage = pageImg.getScaledInstance(imgLabel.getWidth(),imgLabel.getHeight(),Image.SCALE_SMOOTH);
				ImageIcon icon = new ImageIcon(scaledImage);
				imgLabel.setIcon(icon);
				
				System.out.println("3");//test3
				
				
		        //turn page when receiving the "turn" message
		        while((clientMsg = reader.readLine()) != null) {
		        	   System.out.println("get0:"+pageArray.get(0));
					   int pagenum = Integer.parseInt(pageArray.get(0));
					   
					   //check if the first chosen page is the book cover
					   if(pagenum==0){
						   pageArray.remove(pageArray.get(0));
						   pagenum = Integer.parseInt(pageArray.get(0));
					   }
					   turnPage(pagenum);
					   pageArray.remove(pageArray.get(0));
					   System.out.println(clientMsg);
				} 
			
				// TODO Auto-generated catch block
				
			
				
			}catch (UnsupportedEncodingException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			
			//Do turn page logic here when get msg from robot
		}
	
	public void start(){
		try {
			//Create a server socket listening on port 8080
			listeningSocket = new ServerSocket(PORT);
			Socket clientSocket = null;
			
			numOfClients = 0; //counter to keep track of the number of clients
			
			//Listen for incoming connections for ever 
			while (true) {
				System.out.println("port: "+ PORT);
				System.out.println("Server listening on port "+PORT+" for a connection"+"\n");
				//System.out.println("Server listening on port "+port+" for a connection");
				//Accept an incoming client connection request 
				clientSocket = listeningSocket.accept(); //This method will block until a connection request is received
				
				System.out.println("Connection Established");
				
				numOfClients++;
				
				requests(clientSocket);
				
				
				
				
				
				//clientSocket.close();
			}
		} catch (SocketException ex) {
			ex.printStackTrace();
		}catch (IOException e) {
			e.printStackTrace();
		} 
		finally {
			if(listeningSocket != null) {
				try {
					listeningSocket.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
	
//read the book_pages.txt file to get the pages
private String[] getBookPages() throws IOException{
	String[] pages = null;
	File book_pages = new File(pathChai + "\\books\\book_pages.txt");
	if(!book_pages.exists()){
		System.out.println("There is no chosen book.");
	}else{
        String lines = null;
        FileReader fileReader = new FileReader(pathChai + "\\books\\book_pages.txt");
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        int count = 0;
        while((lines=bufferedReader.readLine()) != null) {
        	if(count == 1){
        		String bookPagesStr = "["+lines.trim();
            	String regex = "\\D+";
            	pages = bookPagesStr.split(regex);//get a string array of the page numbers
            	
            	System.out.println(pages[0]);
            	
        	}
        	count++;
        }   

        bufferedReader.close();         
    }
	return pages;
}

//read the book_pages.txt file to get the books
private String getBookTitle() throws IOException{
		String bookTitle = null;
		File book_pages = new File(pathChai + "\\books\\book_pages.txt");
		if(!book_pages.exists()){
			System.out.println("There is no chosen book.");
		}else{
          String line = null;
          FileReader fileReader = new FileReader(pathChai + "\\books\\book_pages.txt");
          BufferedReader bufferedReader = new BufferedReader(fileReader);
          int count = 0;
          while((line=bufferedReader.readLine()) != null) {
          	if(count == 0){
          		bookTitle = line.trim();
          	}
          	count++;
          	
          	
          }   

          bufferedReader.close();         
      }return bookTitle;
}

//convert the pdf pages to images using pdfbox
private void convert(String bookTitle){
		try {
			
			File pdfFile = new File(pathChai + "\\books\\"+ bookTitle);
			if(!pdfFile.exists()){
				System.out.println("Book not found.");
			}else{
				PDDocument document = PDDocument.loadNonSeq(pdfFile, null);
				List<PDPage> pdPages = document.getDocumentCatalog().getAllPages();
				int page = 0;
				
				File folder = new File(pathChai + "\\imgs");
				folder.mkdir();
				if(folder.exists()==false){
					folder.createNewFile();
				}
				
				for (PDPage pdPage : pdPages)
				{ 
				    
				    BufferedImage bim = pdPage.convertToImage(BufferedImage.TYPE_INT_RGB, 300);
				    ImageIOUtil.writeImage(bim,"png", pathChai + "\\imgs\\" + page,BufferedImage.TYPE_INT_RGB, 300);
				    ++page;
				}
				document.close();
			}
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			///e1.printStackTrace();
		}
		}
//set the pane with images
private void turnPage(int pagenum){
	Image pageImg = new ImageIcon(pathChai + "\\imgs\\" + pagenum + ".png").getImage();
	Image scaledImage = pageImg.getScaledInstance(imgLabel.getWidth(),imgLabel.getHeight(),Image.SCALE_SMOOTH);
	ImageIcon icon = new ImageIcon(scaledImage);
	imgLabel.setIcon(icon);
}
	
}




