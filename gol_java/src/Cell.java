package src;
import src.CellState;

public class Cell {
    private byte c_state;

    public Cell(){
        this.c_state = (Math.random() > 0.5) ? CellState.ALIVE : CellState.DEAD;;
    }
    public byte _state(){
        return this.c_state;
    }
    public void set_state(byte cell_state){
        this.c_state = cell_state;
    }
}
