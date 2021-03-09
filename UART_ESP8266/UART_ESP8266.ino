#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include<SoftwareSerial.h> 
SoftwareSerial s(3, 1);
const char *ssid = "Gia Khiem";        // Nhập tên WiFi
const char *password = "15012007";         // Nhập Mật khẩu WiFi
const char *mqttServer = "broker.emqx.io"; // Nhập địa chỉ của server MQTT
unsigned long b_time;
String clientId = "ClientESP8266";    // Client ID của mạch
const char *m_topic = "BCI"; // Topic mình đã tạo ở trên
String mss = "";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
void setup()
{
    s.begin(9600);
    s.println("hahaha");
    setup_wifi();
    /* Hàm start - read Callback client */
    client.setServer(mqttServer, 1883);
    client.setCallback(callback);
    pinMode(2, OUTPUT);
}
void setup_wifi()
{
    delay(10);
    s.println();
    s.print("Connecting to ");
    s.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        s.print(".");
    }
    s.println("");
    s.println("WiFi connected");
    s.println("IP address: ");
    s.println(WiFi.localIP());
}
/* Ham call back nhan lai du lieu */
void callback(char *topic, byte *payload, unsigned int length)
{
    //s.print(topic);
    for (int i = 0; i < length; i++)
    {
        mss += (char)payload[i];
    }
    s.print(mss);
    mss = "";
    s.println();
    xulidulieu(payload);
}
void xulidulieu(byte *data)
{
    //s.println(*data);
    /* Xử lí dữ liệu đọc về tại đây */
}
void reconnect()
{
    while (!client.connected())
    {
        s.print("Attempting MQTT connection...");
        if (client.connect(clientId.c_str()))
        {
            s.println("connected");
            client.publish(m_topic, "Reconnect"); // Gửi dữ liệu
            client.subscribe(m_topic);            // Theo dõi dữ liệu
        }
        else
        {
            s.print("failed, rc=");
            s.print(client.state());
            // Doi 1s
            delay(1000);
        }
    }
}
void loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();
    /* Mỗi 1s gửi dữ liệu thời gian lên topic server*/
    long now = millis();
    if (now - lastMsg > 1000)
    {
        lastMsg = now;
        //s.print("Message send: ");
        //client.publish(m_topic, msg);
    }
}
