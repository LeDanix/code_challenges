////////////////////////////////////////////
// Game of Life
// Author: Daniel Saiz Azor
// Powered by JDK 20
////////////////////////////////////////////
import src.graphics_;

import javax.swing.SwingUtilities;

import src.Matrix;
import src.utils;


class GameOfLife{
    private static byte ROWS = 127;
    private static byte COLUMNS = 127;
    // private static int MAX_ITERATIONS = 500;

    public static void main(String[] args){
        Matrix matrix = new Matrix(ROWS, COLUMNS);
        graphics_ graphics = new graphics_(matrix);
        
        while (true){
            matrix.update();
            graphics.repaint();
            utils.wait(50);
        }
    }
}