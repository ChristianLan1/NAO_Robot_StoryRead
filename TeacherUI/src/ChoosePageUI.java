/**
 * Author:LIUYI CHAI

 * Purpose:This class is a UI for users to choose book pages
 */
import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.Image;

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
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JTextPane;

public class ChoosePageUI<ClientUI> extends JFrame {
	private JPanel uploadPanel;
	private List<JLabel> playerIconList = new ArrayList<JLabel>();
	private int optionInt = 0;
	private JTextField beginNum;
	private JTextField endNum;
	private MainUI mainframe;
	
	/**
	 * Launch the application.
	 */
	

	/**
	 * Create the frame.
	 */
	
	//关闭窗口时弹窗
	public ChoosePageUI() {
		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				ChoosePageUI choosepageframe = new ChoosePageUI();
				choosepageframe.dispose();
			    
			}
		});
		
		setSize(300, 450);
		setLocationRelativeTo(null);
		uploadPanel = new JPanel();
		uploadPanel.setForeground(new Color(0, 0, 0));
		setContentPane(uploadPanel);
		uploadPanel.setLayout(null);
		
		
		JLabel lblBookTitle = new JLabel("");
		lblBookTitle.setBounds(16, 18, 262, 26);
		uploadPanel.add(lblBookTitle);
		lblBookTitle.setText(mainframe.list.getSelectedValue());
		
		JTextPane txtpnChoosePages = new JTextPane();
		txtpnChoosePages.setText("Choose the pages that you want the robot to read:");
		txtpnChoosePages.setBounds(16, 83, 278, 38);
		uploadPanel.add(txtpnChoosePages);
		
		JLabel lblFrom = new JLabel("From");
		lblFrom.setBounds(16, 133, 43, 16);
		uploadPanel.add(lblFrom);
		
		beginNum = new JTextField();
		beginNum.setBounds(48, 128, 52, 26);
		uploadPanel.add(beginNum);
		beginNum.setColumns(10);
		
		JLabel To = new JLabel(" -");
		To.setBounds(96, 133, 18, 16);
		uploadPanel.add(To);
		
		endNum = new JTextField();
		endNum.setBounds(106, 128, 53, 26);
		uploadPanel.add(endNum);
		endNum.setColumns(10);
		
		JTextPane Note = new JTextPane();
		Note.setForeground(Color.GRAY);
		Note.setFont(new Font("Times", Font.PLAIN, 13));
		Note.setText(" NOTE : \n * The pages are counted from 0. Usually the  first page (page 0) is the book cover. \n * You'd better choose the pages from the  beginning of the story.");
		Note.setBounds(16, 180, 262, 79);
		Note.setBorder(BorderFactory.createLineBorder(Color.GRAY));
		uploadPanel.add(Note);
		
		JTextPane tipsPane = new JTextPane();
		tipsPane.setFont(new Font("Times", Font.PLAIN, 13));
		tipsPane.setForeground(Color.RED);
		tipsPane.setBounds(16, 83, 262, 38);
		uploadPanel.add(tipsPane);
		
		JTextPane Tips = new JTextPane();
		Tips.setFont(new Font("Times", Font.PLAIN, 13));
		Tips.setForeground(Color.RED);
		Tips.setBounds(16, 300, 262, 50);
		uploadPanel.add(Tips);
		
		JButton btnConfirm = new JButton("Confirm");
		btnConfirm.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String begin = beginNum.getText().trim();
				String end = endNum.getText().trim();
				int beginInt = Integer.parseInt(begin);
				int endInt = Integer.parseInt(end);
				
				if(beginInt>=0 && endInt>=0 && endInt >= beginInt){
					JOptionPane.showConfirmDialog(null, "You have successfully set the pages!");
					List<Integer> pageList = new ArrayList<>();
					System.out.println(Integer.parseInt(begin));
					for(int i=beginInt;i<=endInt;i++){
						pageList.add(i);
					}
					
					PrintWriter writer;
					try {
						File pageText = new File("/C:/Users/Christian Lan/OneDrive/NAO CODE/"+ mainframe.list.getSelectedValue()+"_pages.txt");
						if(pageText.exists()==false){
							pageText.createNewFile();
						}
						writer = new PrintWriter(pageText, "UTF-8");
					    writer.println(mainframe.list.getSelectedValue()+".pdf");
					    writer.println(pageList);
				    	writer.close();
					} catch (FileNotFoundException
							| UnsupportedEncodingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
				}
				else{
					Tips.setText("*The pages you selected must be a number >= 0, and the end number must be bigger than the begin number.");
				}
			}
		});
		btnConfirm.setBounds(89, 393, 117, 29);
		uploadPanel.add(btnConfirm);
		
		
		
		}




}

//:~