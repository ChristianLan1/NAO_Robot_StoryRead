import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;

public class PDF_Server {
	private ServerSocket listeningSocket;
	private static final int PORT = 5555;
	private int numOfClients;
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
	PDF_Server server= new PDF_Server();
	server.start();

	}
	public PDF_Server() throws IOException{
		System.out.println("initializing the server...");
		listeningSocket = new ServerSocket(8088);
		
		
	}
	
	
		public void requests(Socket socket){
			try {
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
