package src;
import src.Cell;
import src.CellState;
import src.Coord;
import java.lang.Math;

public class Matrix {
    private Cell [][] matrix;
    private byte rows;
    private byte colums;
    
    public Matrix(byte rows, byte columns){
        this.rows = rows;
        this.colums = columns;
        // Generate an empty matrix
        this.matrix = new Cell[rows][columns];
        // Initialize Matrix with random values
        for (int i = 0; i < this.matrix.length; i++){
            for (int j = 0; j < this.matrix[i].length; j++){
                Cell cell = new Cell();
                this.matrix[i][j] = cell;
            }
        }
    }

    private Cell[][] _matrix(){
        return this.matrix;
    }
    public byte _rows(){
        return this.rows;
    }
    public byte _columns(){
        return this.colums;
    }
    
    public Cell get_cell(Coord coord){
        return this.matrix[coord._x()][coord._y()];
    }
    
    private void set_cell(Coord coord, Cell cell){
        this.matrix[coord._x()][coord._y()] = cell;
    }

    private byte n_alives(Coord coord){
        byte[][] aux_array = {{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}};
        byte count = 0;
        byte x = coord._x();
        byte y = coord._y(); 
        for(int i = 0; i < aux_array.length; i++){
            if ((x + aux_array[i][0]) >= 0 && 
                (y + aux_array[i][1]) >= 0 && 
                (x + aux_array[i][0]) < this._rows() && 
                (y + aux_array[i][1]) < this._columns()){
                Cell aux_cell = this._matrix()[x + aux_array[i][0]][y + aux_array[i][1]];
                count = (byte) ((aux_cell._state() == CellState.ALIVE) ? count + 1 : count);
            }
        }
        return count;
    }

    private byte gol_logic(Coord coord){
        byte c_state;
        byte n_alives = n_alives(coord);
        if (this.get_cell(coord)._state() == CellState.DEAD){
            c_state = (n_alives == 3) ? CellState.ALIVE : CellState.DEAD;
        }
        else{
            c_state = (n_alives > 3 || n_alives < 2) ? CellState.DEAD : CellState.ALIVE;
        }
        return c_state;
    }

    public void update(){
        Matrix aux_matrix = new Matrix(this._rows(), this._columns());
        // Game Of Life logic matrix fill
        for(byte i = 0; i < this._rows(); i++){
            for(byte j = 0; j < this._columns(); j++){
                Coord coord = new Coord(i, j);
                Cell cell = new Cell();
                cell.set_state(this.gol_logic(coord));
                aux_matrix.set_cell(coord, cell);
            }
        }
        // Dumping aux_matrix results into origin matrix (class object)
        for(byte i = 0; i < this._rows(); i++){
            for(byte j = 0; j < this._columns(); j++){
                Coord coord = new Coord(i, j);
                this.set_cell(coord, aux_matrix.get_cell(coord));
            }
        }
    }

    
}
