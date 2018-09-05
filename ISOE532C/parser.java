/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.awt.List;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author dedsec
 */

public class parser {

    public static String getCode(String file) throws IOException{
        String code = "";
        try (FileInputStream in = new FileInputStream(file)) {
           int c;
           while ((c = in.read()) != -1) {
               code += (char)c;
           }
        }
        return code;
    }
    
    public static int getDataTypes(String code) {
        String dataTypes[] = {"int", "float", "double", "char"};
        int count = 0;
        for(String dataType: dataTypes) {
            // String regex = "[\\s+|;|^]" + dataType + "\\s+";
            String regex = "[\\s+|;]"+dataType+"\\s+([\\**_]?[a-zA-Z0-9\\[\\]]*(\\s*=\\s*[a-zA-Z0-9_\"]*)?)((\\s*,\\s*)([\\**_]?[a-zA-Z0-9\\[\\]]*(\\s*=\\s*[a-zA-Z0-9_\"]*)?))*;";
            regex = "[\\s|;]"+ dataType +"\\s.*(,.*)*;"; // simpler regex, but still not perfect
            // System.out.println(regex);
            Pattern pattern = Pattern.compile(regex);
            Matcher m = pattern.matcher(code);
            if (m.find()) {
                count += 1;
            }
        }
        return count;
    }
    public static int getCount(String code, String dataType) {
        String regex = "[\\s+|;]"+dataType+"\\s+([\\**_]?[a-zA-Z0-9\\[\\]]*(\\s*=\\s*[a-zA-Z0-9_\"]*)?)((\\s*,\\s*)([\\**_]?[a-zA-Z0-9\\[\\]]*(\\s*=\\s*[a-zA-Z0-9_\"]*)?))*;";
        regex = "[\\s|;]"+ dataType +"\\s.*(,.*)*;"; // simpler regex, but still not perfect
        String declaration;
        int count;
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        count = 0;
        while(m.find()) {
            // System.out.println(code.substring(m.start(), m.end()));
            declaration = code.substring(m.start(), m.end());
            // System.out.println(declaration);
            count += 1;
            for(int i = 0; i < declaration.length(); i++) {
                if(declaration.charAt(i) == ',') {
                    count += 1;
                }
            }
        }
        return count;
    }
    
    public static int getInitialized(String code, String dataType) {
        String regex = "[\\s+|;]"+dataType+"\\s+([\\**_]?[a-zA-Z0-9\\[\\]]*(\\s*=\\s*[a-zA-Z0-9_\"]*)?)((\\s*,\\s*)([\\**_]?[a-zA-Z0-9\\[\\]]*(\\s*=\\s*[a-zA-Z0-9_\"]*)?))*;";        String declaration;
        regex = "[\\s|;]"+ dataType +"\\s.*(,.*)*;"; // simpler regex, but still not perfect
        int initialized;
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        initialized = 0;
        while(m.find()) {
            // System.out.println(code.substring(m.start(), m.end()));
            declaration = code.substring(m.start(), m.end());
            // System.out.println(declaration);
            for(int i = 0; i < declaration.length(); i++) {
                if(declaration.charAt(i) == '=') {
                    initialized += 1;
                }
            }
        }
        return initialized;
    }
    
    public static int getForLoops(String code) {
        String regex = "for\\s*\\(.*;.*;.*\\)";
        int count = 0;
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        while(m.find()) {
            // System.out.println(code.substring(m.start(), m.end()));
            count += 1;
        }
        return count;
    }
 
    public static int getWhileLoops(String code) {
        String regex = "while\\s*\\(.*\\)";
        int count = 0;
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        while(m.find()) {
            //System.out.println(code.substring(m.start(), m.end()));
            count += 1;
        }
        return count;
    }
    
    public static int getUnitialized(String code, String dataType) {
        return getCount(code, dataType) - getInitialized(code, dataType);
    }
    
    public static int getConditionals(String code) {
        String regex = "if\\s*\\(.*\\)";
        int count = 0;
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        while(m.find()) {
            // System.out.println(code.substring(m.start(), m.end()));
            count += 1;
        }
        return count;
    }
    
    public static String getFunctionsCount(String code) {
        String regex = "((int)|(void)|(float)|(char)|(double))\\s+\\w+\\(.*\\)";
        int count = 0;
        String out = "";
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        while(m.find()) {
            // System.out.println(code.substring(m.start(), m.end()));
            out += code.substring(m.start(), m.end()) + "\n";
            count += 1;
        }
        return out;
    }
    
    public static ArrayList getFunctions(String code) {
        ArrayList<String> functions = new ArrayList<>();
        String regex = "((int)|(void)|(float)|(char)|(double))\\s+\\w+\\(.*\\)\\s*\\{";
        int c = 0;
        String out = "";
        // System.out.println(regex);
        Pattern pattern = Pattern.compile(regex);
        Matcher m = pattern.matcher(code);
        while(m.find()){
            String fBegin = code.substring(m.end());
            int bCount = 1;
            String function = code.substring(m.start(), m.end());
            for(int i = 0; i < fBegin.length(); i++) {
                if(fBegin.charAt(i) == '{') {
                    bCount += 1;
                } else if(fBegin.charAt(i) == '}') {
                    bCount -= 1;
                }
                function += fBegin.charAt(i);
                if(bCount == 0) {
                    functions.add(function);
                    break;
                }
            }
            c += 1;
        }
        return functions;
    }
    
    
    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String args[]) throws IOException {

        String code = getCode("/home/iiita/Desktop/dedsec/soe/input.c");
        FileOutputStream out = new FileOutputStream("/home/iiita/Desktop/dedsec/soe/ouput.txt");
        // System.out.println(code);
        
        int n, intCount, floatCount, doubleCount, charCount, forLoops, whileLoops, conditionals;
        n = getDataTypes(code);
        intCount = getCount(code, "int");
        floatCount = getCount(code, "float");
        doubleCount = getCount(code, "double");
        charCount = getCount(code, "char");
        forLoops = getForLoops(code);
        whileLoops = getWhileLoops(code);
        conditionals = getConditionals(code);
        
        String fn = getFunctionsCount(code);
        ArrayList<String> functions = getFunctions(code);
        int tc = 0;
        
        for(String func: functions){
            String name = func.substring(func.indexOf(" "),func.indexOf("("));
            int cnt = getConditionals(func) + getForLoops(func) + getWhileLoops(func);
            tc += cnt+1;
            System.out.println("Function " + name + "(): " + cnt + " + " + "1 = " + (cnt+1));
        }
        System.out.println("TC = " + tc);
        
        String output = "";        
        output += ("DataTypes: " + n) + "\n";
        output += ("intCount: " + intCount + " " + getInitialized(code, "int")) + "\n";
        output += ("floatCount: " + floatCount + " " + getInitialized(code, "float")) + "\n";
        output += ("doubleCount: " + doubleCount + " " + getInitialized(code, "double")) + "\n";
        output += ("charCount: " + charCount + " " + getInitialized(code, "char")) + "\n";
        output += ("forLoops: " + forLoops) + "\n";
        output += ("whileLoops: " + whileLoops) + "\n";
        output += ("conditionals: " + conditionals) + "\n";
        output += ("\nFunctions:\n" + fn);
        output += ("\nCyclomatic Complexity:\n" + tc);
        
        for(int i = 0; i < output.length(); i++) {
            out.write(output.charAt(i));
        }
        
//        System.out.println("DataTypes: " + n);
//        System.out.println("intCount: " + intCount + " " + getInitialized(code, "int"));
//        System.out.println("floatCount: " + floatCount);
//        System.out.println("doubleCount: " + doubleCount);
//        System.out.println("charCount: " + charCount);
//        System.out.println("forLoops: " + forLoops);
//        System.out.println("whileLoops: " + whileLoops);
    }      
}
