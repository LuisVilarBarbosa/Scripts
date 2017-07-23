import java.io.File;
import java.io.FileInputStream;

public class FilesComparator {
    private static int BUFFER_SIZE = 1048576;	// 1 MB

    private static long fileSize(String filename) throws Exception {
        File f = new File(filename);
        if (!f.exists())
            throw new Exception("The file does not exist: " + filename);
        return f.length();
    }

    private static boolean areFilesEqual(String filename1, String filename2) throws Exception {
        long f1Size = fileSize(filename1);
        long f2Size = fileSize(filename2);
        if (f1Size != f2Size)
            return false;

        FileInputStream f1 = new FileInputStream(filename1);
        FileInputStream f2 = new FileInputStream(filename2);

        byte data1[] = new byte[BUFFER_SIZE];
        byte data2[] = new byte[BUFFER_SIZE];
        boolean equal = true;
        boolean readError = false;

        for (long i = 0; i < f1Size && equal; i += BUFFER_SIZE) {
            int read1 = f1.read(data1);
            int read2 = f2.read(data2);

            if (read1 != read2) {
                readError = true;
                break;
            }

            for (int j = 0; j < read1; j++) {
                if (data1[j] != data2[j]) {
                    equal = false;
                    break;
                }
            }
        }

        f1.close();
        f2.close();

        if (readError)
            throw new Exception("An error occurred reading the data from the files.");

        return equal;
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Usage: java FilesComparator <filename1> <filename2>");
            return;
        }

        String filename1 = args[0], filename2 = args[1];

        try {
            if (areFilesEqual(filename1, filename2))
                System.out.println("The files are equal.");
            else
                System.out.println("The files are not equal.");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
