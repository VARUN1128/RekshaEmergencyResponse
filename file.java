
import java.io.*;
import java.util.Scanner;
class WriteFile{
	public static void main(String args[]){
		String flname = args[0];
		
		FileOutputStream fout;
		
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter Input :");
		String input = sc.nextLine();
		char charArray[] = input.toCharArray();
		try {
			fout =  new FileOutputStream(flname);
		}catch(IOException e){
			System.out.println("Cannot Create The file");
			return;
		}
		
		try{
			for(int i=0;i<input.length();i++){
				fout.write(charArray[i]);
			}
			fout.write('\n');
		}
		catch(IOException e){
			System.out.println("Error: Cannot write to file");
			System.out.println(e);
		}
		finally{
			try{
				fout.close();
			}catch(IOException e){
				System.out.println("Error: Cannot Close file");
				System.out.println(e);	
			}
		}
	}
}