using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Text.RegularExpressions;
using System.Diagnostics;

namespace Proyecto_Compiladores_I
{
    public partial class Form1 : Form
    {
        String NombreArch = "";
        public Form1()
        {
            InitializeComponent();
        }
        String[] keywords = { "program", "if", "else", "fi", "do",
                                    "do","until","while", "read", "write",
                                    "float","int","bool", "not", "and","or"};
        String[] symbols = {"+","-","*","/","^","<","<=",">=","==","!=",
                                       "=",";",",","(",")","{","}" };
        private void Form1_Load(object sender, EventArgs e)
        {
            richTextBox1.Multiline = true;
            richTextBox1.WordWrap = false;
            richTextBox1.AcceptsTab = true;
            richTextBox1.ScrollBars = RichTextBoxScrollBars.ForcedBoth;
            //richTextBox1.Dock = DockStyle.Fill;
            richTextBox1.SelectionFont = new Font("Courier New", 10, FontStyle.Regular);
            richTextBox1.SelectionColor = Color.Black;
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void abrirToolStripMenuItem_Click(object sender, EventArgs e)
        {
           
            if (openFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK && openFileDialog1.FileName.Contains(".txt")) //Checks if it's all ok and if the file name contains .txt  
            {
                string open = File.ReadAllText(openFileDialog1.FileName);
                NombreArch = openFileDialog1.FileName;
                richTextBox1.Text = open;
               // MessageBox.Show("Abrir: "+NombreArch);
            }
            else
            {
                MessageBox.Show("The file you've chosen is not a text file");
            }
        }

        private void guardarComoToolStripMenuItem_Click(object sender, EventArgs e)
        {
           
            if (saveFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK) //Check if it's all ok  
            {
                string name = saveFileDialog1.FileName + ".txt"; //Just to make sure the extension is .txt  
                File.WriteAllText(name, richTextBox1.Text); //Writes the text to the file and saves it       
                NombreArch = saveFileDialog1.FileName + ".txt";
            }
        }

        private void guardarToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (NombreArch != "")
            {
                string name = NombreArch;
                File.WriteAllText(name, richTextBox1.Text); //Writes the text to the file and saves it       
            }
            else
            {
                if (saveFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK) //Check if it's all ok  
                {
                    string name = saveFileDialog1.FileName + ".txt"; //Just to make sure the extension is .txt  
                    File.WriteAllText(name, richTextBox1.Text); //Writes the text to the file and saves it       
                    NombreArch = saveFileDialog1.FileName;
                }
            }
            
           
           
        }

        private void cerrarToolStripMenuItem_Click(object sender, EventArgs e)
        {
            NombreArch = "";
            richTextBox1.Text = "";
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

            if (bandCheckGlob == true)
            {
                int indice = richTextBox1.SelectionStart;
                Regex r = new Regex(@"(\r|\n|\r\n)", RegexOptions.Multiline);

                //String[] lines = richTextBox1.Text.Split('\n','\r');
                String[] lines = r.Split(richTextBox1.Text);
                //Console.WriteLine(lines.Length);
                //Console.WriteLine(lines[0]);
                //Console.WriteLine(richTextBox1.Text);
                //Aux = new RichTextBox();
                richTextBox1.Text = "";
                foreach (string l in lines)
                {

                    ParseLine(l);

                }
                richTextBox1.SelectionStart = indice;
            }
            else
            {
                bandCheckGlob = true;
            }
           // Console.WriteLine(e.ToString());
        
           

        }
        //
        RichTextBox Aux = new RichTextBox();
        void ParseLine(string line)
        {
            Regex r = new Regex("([ \\t{}():;])");
            String[] tokens = r.Split(line);
           
            foreach (string token in tokens)
            {
                // Set the tokens default color and font.  
                richTextBox1.SelectionColor = Color.Black;
                richTextBox1.SelectionFont = new Font("Courier New", 10, FontStyle.Regular);
                // Check whether the token is a keyword.   

                if (token == "//" || token.StartsWith("//"))
                {
                    // Find the start of the comment and then extract the whole comment.
                    int index = line.IndexOf("//");
                    string comment = line.Substring(index, line.Length - index);
                    richTextBox1.SelectionColor = Color.LightGreen;
                    richTextBox1.SelectionFont = new Font("Courier New", 10, FontStyle.Regular);
                    richTextBox1.SelectedText = comment;
                    break;
                }

                
                for (int i = 0; i < keywords.Length; i++)
                {
                    if (keywords[i] == token)
                    {
                        // Apply alternative color and font to highlight keyword.  
                        richTextBox1.SelectionColor = Color.Blue;
                        richTextBox1.SelectionFont = new Font("Courier New", 10, FontStyle.Bold);
                        break;
                    }
                }

                richTextBox1.SelectedText = token;
                //richTextBox1.Text += token;
            }
          //richTextBox1.AppendText("\n");
            
           
        }
        bool bandCheckGlob = false;
        private void richTextBox1_KeyPress(object sender, KeyPressEventArgs e)
        {
            /*int indice = richTextBox1.SelectionStart;
            if (richTextBox1.Text.Length > 0)
            {
                int C = richTextBox1.GetLineFromCharIndex(richTextBox1.GetFirstCharIndexOfCurrentLine());
                int firstchar = richTextBox1.GetFirstCharIndexOfCurrentLine();
                if (richTextBox1.Text.Length > 1)
                {
                    richTextBox1.SelectedText = "";
                    int count = richTextBox1.Lines[C].Length;

                    // Eat new line chars
                   /* if (firstchar < richTextBox1.Lines.Length - 1)
                    {
                        count += richTextBox1.GetFirstCharIndexFromLine(C + 1) -
                            ((firstchar + count - 1) + 1);
                    }*/
            /*
                    richTextBox1.Text = richTextBox1.Text.Remove(firstchar, count);
                    if(richTextBox1.Lines.Length>0)
                    ParseLine(richTextBox1.Lines[C]);
                }
              
            }
            richTextBox1.SelectionStart = indice;
            bandCheckGlob = false;
            */
        }

        private void richTextBox1_KeyUp(object sender, KeyEventArgs e)
        {
           
        }

        private void richTextBox1_KeyDown(object sender, KeyEventArgs e)
        {
            
          
        }

        private void Compilar(object sender, EventArgs e)
        {
            string strCmdText;
            if (!(NombreArch != ""))
            {
                guardarComoToolStripMenuItem_Click(null, null);
            }
           
            //strCmdText = "/C analizador.py " + NombreArch;
            var p = new Process();
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.FileName = "python.exe";
            p.StartInfo.Arguments = "example.py " + "\""+NombreArch +"\"";
            // p = System.Diagnostics.Process.Start("CMD.exe", strCmdText);
            p.Start();
            //resLex.Text = "";
            resLex.Text = p.StandardOutput.ReadToEnd();
            p.WaitForExit();


            var p1 = new Process();
            p1.StartInfo.UseShellExecute = false;
            p1.StartInfo.RedirectStandardOutput = true;
            p1.StartInfo.FileName = "python.exe";
            p1.StartInfo.Arguments = "AnSintac.py " + "\"" + NombreArch + "\"";
            // p = System.Diagnostics.Process.Start("CMD.exe", strCmdText);
            p1.Start();
            //resLex.Text = "";
            resSin.Text = p1.StandardOutput.ReadToEnd();
            p1.WaitForExit();


        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
