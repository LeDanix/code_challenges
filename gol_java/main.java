////////////////////////////////////////////
// Game of Life
// Author: Daniel Saiz Azor
// Powered by JDK 20
////////////////////////////////////////////

import src.graphics_;
import java.util.concurrent.TimeUnit;
import java.awt.Graphics;
import javax.swing.*;

import src.Matrix;


class GameOfLife{
    private static byte ROWS = 100;
    private static byte COLUMNS = 50;
    private static byte MAX_ITERATIONS = 100;
    private static boolean ACTIVE = true;

    public static void main(String[] args){
        byte iter = 0;
        Matrix matrix = new Matrix(ROWS, COLUMNS);
        graphics_ ghaphics = new graphics_(matrix);
        ghaphics.setVisible(true);
        while (iter++ < MAX_ITERATIONS){
            matrix.update();
            ghaphics = new graphics_(matrix);
        }









    }
}