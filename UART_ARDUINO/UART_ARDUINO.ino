
#define PIN_LED 13
String inString;
int rl1 = 52, rl2 = 50, rl3 = 48, rl4 = 46, rl5 = 44, rl6 = 42, rl7 = 40, rl8 = 38;
// Настройка
void setup_rl()
{
  for (int i = 52; i >= 38; i--)
  {
    if (i % 2 == 0)
    {
      pinMode(i, OUTPUT);
      digitalWrite(i, 0);
    }
  }
}
void run_rl(int rl,char a){
     a = digitalRead(rl);
     if(a ==0){
      digitalWrite(rl,1);
     }
     else if (a==1){
      digitalWrite(rl,0);
     }
}
void setup()
{
  Serial.begin(9600);
  Serial3.begin(9600);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  setup_rl();
}

// Выполнение
void loop()
{
}

void serialEvent3()
{
  while (Serial3.available())
  {
    char inChar = Serial3.read();
    inString += inChar;
    if (inChar == ']')
    {
      //Serial.write(inString[3]);
      char a = inString[3]; 
      if(a=='1'){
        run_rl(rl1,a);
      }
      else if (a=='2')
      {
        run_rl(rl2,a);
      }
      else if (a=='3')
      {
        run_rl(rl3,a);
      }
      else if (a=='4')
      {
        run_rl(rl4,a);
      }
       else if (a=='5')
      {
        run_rl(rl5,a);
      }
     else  if (a=='6') 
      {
        run_rl(rl6,a);
      }
      else if (a=='7')
      {
        run_rl(rl7,a);
      }
      else if (a=='8')
      {
        run_rl(rl8,a);
      }
      else
      {
        Serial.println("--FALSE--");
      }
      inString="";
    }
    else{
      Serial.print(inChar);
     }
  }
}
