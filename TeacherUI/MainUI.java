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

public class MainUI {
	private UploadUI uploadframe;
	private JFrame mainframe;
	private ChoosePageUI choosepageframe;
	private JTextField searchField;
	public static List<String> bookList = new ArrayList<>();
	public static JList<String> list = new JList<String>(new DefaultListModel<String>());
	public static File bookText;
	
	

	public MainUI() {
	
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
		
		searchField = new JTextField();
		searchField.setBounds(37, 6, 408, 26);
		mainframe.getContentPane().add(searchField);
		searchField.setColumns(10);
		
		JButton btnSearch = new JButton("Search");
		btnSearch.setBounds(442, 6, 80, 29);
		mainframe.getContentPane().add(btnSearch);
		
		//close the main window and open the upload window when clicking "upload my books"
		JButton btnChooseYourBooks = new JButton("Upload my books");
		btnChooseYourBooks.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				uploadframe = new UploadUI();
				uploadframe.setVisible(true);
			}
		});
		btnChooseYourBooks.setBounds(329, 37, 169, 29);
		mainframe.getContentPane().add(btnChooseYourBooks);
		
		JLabel lblNewLabel_1 = new JLabel("Choose a book");
		lblNewLabel_1.setBounds(37, 42, 109, 16);
		mainframe.getContentPane().add(lblNewLabel_1);
		
	
		
		
		
		JLabel totalFrame = new JLabel("");
		totalFrame.setBounds(37, 44, 476, 297);
		mainframe.getContentPane().add(totalFrame);
	
		
	}
	public static void main(String[] args) throws IOException {
		
		File folder = new File("/Users/rose/Desktop/books");
		folder.mkdir();
		if(folder.exists()==false){
			folder.createNewFile();
		}
		File[] fileLists = folder.listFiles();
		if(fileLists!= null){
		    
		}
		

		MainUI mainWindow = new MainUI();
		mainWindow.mainframe.setVisible(true);
		
		list.setBounds(37, 71, 461, 243);
		mainWindow.mainframe.getContentPane().add(list);
		list.setBorder(BorderFactory.createLineBorder(Color.BLACK));
		if(fileLists.length != 0){
			for (int i = 0; i < fileLists.length; i++) {
			    if(fileLists[i].isFile()) {
			    	((DefaultListModel)list.getModel()).addElement(fileLists[i].getName().substring(0, fileLists[i].getName().length()-4));
			    }
		    }
		}
		
		
		JButton btnComfirm = new JButton("Comfirm");
		btnComfirm.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			    if(list.getSelectedValue() == null){
			    	JOptionPane.showConfirmDialog(null, "You didn't choose any book.");
			    }
			    else{
			    	ChoosePageUI choosepageframe = new ChoosePageUI();
					choosepageframe.setVisible(true);
			    }
				
			}
		});
		btnComfirm.setBounds(381, 312, 117, 29);
		mainWindow.mainframe.getContentPane().add(btnComfirm);
		
		
		
		
				}
}


