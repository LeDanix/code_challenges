package src;

public class Coord {
    private byte x = 0;
    private byte y = 0;

    public Coord(byte x, byte y){
        this.x = x;
        this.y = y;
    }

    public byte _x(){
        return this.x;
    }
    
    public byte _y(){
        return this.y;
    }
}
