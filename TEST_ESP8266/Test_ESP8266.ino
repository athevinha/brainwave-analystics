#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include<SoftwareSerial.h> 
SoftwareSerial s(3, 1);
const char *ssid = "Duc Vinh";        // Nhập tên WiFi
const char *password = "0977290586";         // Nhập Mật khẩu WiFi
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
    Serial.begin(115200);
    Serial.println("hahaha");
    setup_wifi();
    /* Hàm start - read Callback client */
    client.setServer(mqttServer, 1883);
    client.setCallback(callback);
    pinMode(2, OUTPUT);
}
void setup_wifi()
{
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
/* Ham call back nhan lai du lieu */
void callback(char *topic, byte *payload, unsigned int length)
{
    //Serial.print(topic);
    for (int i = 0; i < length; i++)
    {
        mss += (char)payload[i];
    }
    Serial.print(mss);
    mss = "";
    Serial.println();
    xulidulieu(payload);
}
void xulidulieu(byte *data)
{
    //Serial.println(*data);
    /* Xử lí dữ liệu đọc về tại đây */
}
void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        if (client.connect(clientId.c_str()))
        {
            Serial.println("connected");
            client.publish(m_topic, "Reconnect"); // Gửi dữ liệu
            client.subscribe(m_topic);            // Theo dõi dữ liệu
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
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
        //Serial.print("Message send: ");
        //client.publish(m_topic, msg);
    }
}
