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
import java.awt.FlowLayout;
import java.awt.GridBagLayout;
import java.awt.Image;

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

import java.awt.Font;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.Color;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.SystemColor;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JList;

public class PDF_Server{
	private PDF_Display display;
	private JFrame mainframe;
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
		mainframe.setSize(550, 400);
		mainframe.setLocationRelativeTo(null);
		mainframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		mainframe.getContentPane().setLayout(null);
		
	
		
		
		
		JLabel totalFrame = new JLabel("");
		totalFrame.setBounds(6, 6, 538, 366);
		mainframe.getContentPane().add(totalFrame);
		
		JLabel lblNewLabel = new JLabel("Waiting for the robot to connect......");
		lblNewLabel.setFont(new Font("Lucida Grande", Font.PLAIN, 16));
		lblNewLabel.setBounds(87, 146, 402, 55);
		mainframe.getContentPane().add(lblNewLabel);
	
		
	}
	
	
	
		public void requests(Socket socket){
			try {
				//shift the windows
				mainframe.dispose();
				display = new PDF_Display();
				display.setVisible(true);
				
				BufferedReader reader;
				String line;
				String clientMsg = null;
				
				reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));

				while((clientMsg = reader.readLine()) != null) {
					
						
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

}




