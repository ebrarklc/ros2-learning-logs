#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose # Bu sefer Pose (Konum) mesajını kullanıyoruz

class KonumDinleyen(Node):
    def __init__(self):
        super().__init__("konum_dinleyen_node")
        
        # SUBSCRIBER OLUŞTURMA:
        # 1. Mesaj tipi (Pose)
        # 2. Dinlenecek Topic (/turtle1/pose)
        # 3. Callback Fonksiyonu (Veri gelince ne yapayım?)
        self.pose_subscriber = self.create_subscription(
            Pose, 
            "/turtle1/pose", 
            self.pose_callback, 
            10
        )
        self.get_logger().info("Konum Dinleyicisi Başladı! 🕵️")

    # Bu fonksiyon, HER YENİ VERİ GELDİĞİNDE otomatik çalışır
    def pose_callback(self, msg: Pose):
        # msg değişkeni X, Y, Theta (Açı) verilerini taşır
        self.get_logger().info(f"Kaplumbağa Konumu -> X: {str(round(msg.x, 2))}, Y: {str(round(msg.y, 2))}")

def main(args=None):
    rclpy.init(args=args)
    node = KonumDinleyen()
    rclpy.spin(node) # Veri gelmesini bekle
    rclpy.shutdown()

if __name__ == '__main__':
    main()
