package src;
import src.Matrix;
import javax.swing.*;
import java.awt.*;

public class graphics_ extends JFrame{
    Matrix matrix;
    private final int squareSize = 10;

    public graphics_(Matrix matrix){
        this.matrix = matrix;
        setTitle("Game of Life");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(matrix._rows() * squareSize, matrix._columns() * squareSize);
        setLocationRelativeTo(null);
        setResizable(true);
        repaint();   
    }
    
    @Override
    public void paint(Graphics g){
        super.paint(g);
        for (byte i = 0; i < this.matrix._rows(); i++) {
            for (byte j = 0; j < this.matrix._columns(); j++) {
                Coord coord = new Coord(i, j);
                g.setColor(Color.BLACK);
                g.drawRect(i * squareSize, j * squareSize, squareSize, squareSize);
                g.setColor(this.matrix.get_cell(coord)._state() == 1 ? Color.BLACK : Color.WHITE);
                g.fillRect(i * squareSize, j * squareSize, squareSize, squareSize);
            }
        }
    }
}
