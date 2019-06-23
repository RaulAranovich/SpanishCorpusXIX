using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            DirectoryInfo d = new DirectoryInfo(@"C:\Users\Daniel\Desktop\Research\la_iberia\iberia_results_final\undone");
            FileInfo[] files = d.GetFiles("*", SearchOption.AllDirectories);
            var prog = @"C:\Users\Daniel\AppData\Local\Programs\Python\Python35-32\python.exe";
            //var outDir = @"C:\Users\Daniel\Desktop\Research\el_ancora\ancora_results\cSharpResultsTest";
            Parallel.ForEach(files, (file)=>
            {
                //var newName = outDir + " " + file.Name;
                var progArgs = @" cleanNewlines.py " + file.Name; //With full filepath
                var progArgs2 = file.Name; //without filepath
                ProcessStartInfo progInfo = new ProcessStartInfo();
                progInfo.WindowStyle = ProcessWindowStyle.Hidden;
                progInfo.Arguments = progArgs;
                progInfo.FileName = prog;

                //Console.WriteLine("Program to be run = " + prog);
                //Console.WriteLine("Program arguments = " + progArgs);
                //Console.WriteLine("Full console command? = " + progInfo.FileName + progInfo.Arguments);
                Console.WriteLine(file.FullName);
                Process.Start(progInfo).WaitForExit();
            });
        }
    }
}