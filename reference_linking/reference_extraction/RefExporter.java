import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
//import java.io.InputStreamReader;
//import java.util.Collection;

import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.text.AnnotationFS;
import org.apache.uima.fit.factory.AnalysisEngineFactory;
import org.apache.uima.fit.util.CasUtil;


public class RefExporter {

	
	public static final String GESETZ_TYPE = "Main.Gesetz";
	public static final String RICHTLINIE_TYPE = "Main.Richtlinie";
	public static final String VERORDNUNG_TYPE = "Main.Verordnung";
	public static final String GERICHT_TYPE = "Main.Gericht";
	public static final String REF1_TYPE = "Main.REF1";
	//public static final String TOC_TYPE = "Main.toc";
	//public static int start = 0;

	
	
    
    /**     MAIN FUNCTION HERE */
    public static void main(String[] args) throws Exception {
    	
        final AnalysisEngine engine =
                AnalysisEngineFactory.createEngine("MainEngine");
        
        final CAS cas = engine.newCAS();
        
        Path currentRelativePath = Paths.get("");
		String s = currentRelativePath.toAbsolutePath().toString();

		File inputDir = new File(s + "/input");
		
		// get a listing of all files in the directory
	    String[] filesInDir = inputDir.list();

	    // sort the list of files (optional)
	    // Arrays.sort(filesInDir);

	    // have everything i need, just print it now
	    for ( int i=0; i<filesInDir.length; i++ )
	    {
	    	  int counter = 0;
		      System.out.println( "file: " + filesInDir[i] );
		      File fInput = new File(s + "/input/" + filesInDir[i]);
		      BufferedReader br_file = new BufferedReader(new FileReader(fInput));
				
		      //read the data from the file to a string
		      String st;
		      String text = "";
		      while ((st = br_file.readLine()) != null) {
		    	  text += st;
		      }
		      cas.setDocumentText(text); // read from file - Still unable to set cas.setDocument to directly pass the file
		      engine.process(cas);
	        
		      // Writing to output file 
		      String fileName = "output/ref_" + filesInDir[i];
		      FileWriter fileWriter = new FileWriter(fileName);
			
		      BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
		   
//		    for (AnnotationFS toc : CasUtil.select(cas, cas.getTypeSystem().getType(TOC_TYPE))) 
//		        {
//		        
//		        	start=toc.getEnd();
//		  
//				}
//		      
	       
	        for (AnnotationFS Gesetz : CasUtil.select(cas, cas.getTypeSystem().getType(GESETZ_TYPE))) 
	        {
//	        	if(Gesetz.getBegin()>start) {
	        	bufferedWriter.write("Gesetz,");
	        	bufferedWriter.write(String.valueOf(Gesetz.getBegin()));
	        	bufferedWriter.write(",");
	        	bufferedWriter.write(String.valueOf(Gesetz.getEnd()));
	        	bufferedWriter.write(",");
				bufferedWriter.write("\"");
				bufferedWriter.write(Gesetz.getCoveredText());
				bufferedWriter.write("\",");
				bufferedWriter.write("\"");
				bufferedWriter.write(String.valueOf(counter)+ "_"+ String.valueOf(filesInDir[i]) );
				bufferedWriter.write("\"");
				bufferedWriter.write("\r\n");
				counter++;
//				}
	        }
	      
	        for (AnnotationFS Richtlinie : CasUtil.select(cas, cas.getTypeSystem().getType(RICHTLINIE_TYPE))) 
	        {	
//	        	if(Richtlinie.getBegin()>start) {
	        	bufferedWriter.write("Richtlinie,");
	        	bufferedWriter.write(String.valueOf(Richtlinie.getBegin()));
	        	bufferedWriter.write(",");
	        	bufferedWriter.write(String.valueOf(Richtlinie.getEnd()));
	        	bufferedWriter.write(",");
				bufferedWriter.write("\"");
				bufferedWriter.write(Richtlinie.getCoveredText());
				bufferedWriter.write("\",");
				bufferedWriter.write("\"");
				bufferedWriter.write(String.valueOf(counter)+ "_"+ String.valueOf(filesInDir[i]) );
				bufferedWriter.write("\"");
				bufferedWriter.write("\r\n");
				counter++;
//			}
	        }
	        for (AnnotationFS Verordnung : CasUtil.select(cas, cas.getTypeSystem().getType(VERORDNUNG_TYPE))) 
		        {
//	        	if(Verordnung.getBegin()>start) {
		        	bufferedWriter.write("Verordnung,");
		        	bufferedWriter.write(String.valueOf(Verordnung.getBegin()));
		        	bufferedWriter.write(",");
		        	bufferedWriter.write(String.valueOf(Verordnung.getEnd()));
		        	bufferedWriter.write(",");
					bufferedWriter.write("\"");
					bufferedWriter.write(Verordnung.getCoveredText());
					bufferedWriter.write("\",");
					bufferedWriter.write("\"");
					bufferedWriter.write(String.valueOf(counter)+ "_"+ String.valueOf(filesInDir[i]) );
					bufferedWriter.write("\"");
					bufferedWriter.write("\r\n");
					counter++;
//		        }
	        }
	        
	        for (AnnotationFS Gericht : CasUtil.select(cas, cas.getTypeSystem().getType(GERICHT_TYPE))) 
	        {
//	        	if(Gericht.getBegin()>start) {
	        	bufferedWriter.write("Gericht,");
	        	bufferedWriter.write(String.valueOf(Gericht.getBegin()));
	        	bufferedWriter.write(",");
	        	bufferedWriter.write(String.valueOf(Gericht.getEnd()));
	        	bufferedWriter.write(",");
				bufferedWriter.write("\"");
				bufferedWriter.write(Gericht.getCoveredText());
				bufferedWriter.write("\",");
				bufferedWriter.write("\"");
				bufferedWriter.write(String.valueOf(counter)+ "_"+ String.valueOf(filesInDir[i]) );
				bufferedWriter.write("\"");
				bufferedWriter.write("\r\n");
				counter++;
//			}
	        }
	        for (AnnotationFS REF1 : CasUtil.select(cas, cas.getTypeSystem().getType(REF1_TYPE))) 
	        {
//	        	if(REF1.getBegin()>start) {
	        	bufferedWriter.write("REF,");
	        	bufferedWriter.write(String.valueOf(REF1.getBegin()));
	        	bufferedWriter.write(",");
	        	bufferedWriter.write(String.valueOf(REF1.getEnd()));
	        	bufferedWriter.write(",");
				bufferedWriter.write("\"");
				bufferedWriter.write(REF1.getCoveredText());
				bufferedWriter.write("\",");
				bufferedWriter.write("\"");
				bufferedWriter.write(String.valueOf(counter)+ "_"+String.valueOf( filesInDir[i]) );
				bufferedWriter.write("\"");
				bufferedWriter.write("\r\n");
				counter++;
//			}
	        }
	        bufferedWriter.close(); // close the output file writer
	        br_file.close(); // close the input file reader as well
	        cas.reset(); // reset the cas for next file
	        counter=0;
	    }  
  // String command = "python /c start python mergeOutput.py";
//Process p = Runtime.getRuntime().exec(command); 
//BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
//String ret = in.readLine();
//System.out.println(ret);
}



}
// To convert all pdf files in a folder to txt files. Open Gitbash or powershell and 
// for file in *.pdf; do pdftotext "$file" "$file.txt"; done
