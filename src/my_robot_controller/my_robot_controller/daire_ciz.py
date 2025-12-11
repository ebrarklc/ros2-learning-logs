#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # Hız mesajı tipi

class DaireCizen(Node): # Node sınıfından miras alıyoruz
    def __init__(self):
        super().__init__("daire_cizen_node") # Node ismini verdik
        
        # PUBLISHER OLUŞTURMA:
        # 1. Hangi mesaj tipini kullanacak? (Twist)
        # 2. Hangi Topic'e yazacak? (/turtle1/cmd_vel)
        # 3. Kuyruk boyutu ne kadar? (10)
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        
        # ZAMANLAYICI (TIMER):
        # Her 0.5 saniyede bir 'hareket_et' fonksiyonunu çalıştır
        self.timer = self.create_timer(0.5, self.hareket_et)
        self.get_logger().info("Daire Çizen Node Başlatıldı! 🐢")

    def hareket_et(self):
        msg = Twist()
        msg.linear.x = 2.0  # Doğrusal Hız (İleri)
        msg.angular.z = 1.0 # Açısal Hız (Dönme)
        
        # Mesajı yayınla (Publish)
        self.cmd_vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args) # ROS iletişimini başlat
    node = DaireCizen()   # Node'u oluştur
    rclpy.spin(node)      # Node'u açık tut (sürekli döngü)
    rclpy.shutdown()      # Kapanırken temizlik yap

if __name__ == '__main__':
    main()
