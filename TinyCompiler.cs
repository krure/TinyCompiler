using System;
namespace Proyecto_Compiladores_I
public class TinyCompiler
{
    String[] keywords = { "program", "if", "else", "fi", "do",
                                    "do","until","while", "read", "write",
                                    "float","int","bool", "not", "and","or"};
    String[] symbols = {"+","-","*","/","^","<","<=",">=","==","!=",
                                       "=",";",",","(",")","{","}" };
    public TinyCompiler()
	{
	}

    static void main(String args)
    {
        String NombreArch = "";
        if (args!=null) //Checks if it's all ok and if the file name contains .txt  
        {
            string open = File.ReadAllText(args);
            //NombreArch = ;
            Console.WriteLine("Open: " + open);
        }
        else
        {
            Console.WriteLine("Necesita especificar nombre de archivo a compilar");
        }
    }
}
