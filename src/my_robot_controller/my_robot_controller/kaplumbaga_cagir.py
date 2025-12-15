#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn # Spawn servisi mesaj yapısını çağırıyoruz
from functools import partial

class KaplumbagaCagirici(Node):
    def __init__(self):
        super().__init__("kaplumbaga_cagirici_node")
        
        # 1. MÜŞTERİ (CLIENT) OLUŞTUR:
        # Hangi servis tipi? (Spawn)
        # Hangi servise bağlanacak? (/spawn)
        self.client = self.create_client(Spawn, "/spawn")
        
        # 2. SERVİS AÇIK MI DİYE KONTROL ET:
        # Servis bulunana kadar bekle (her 1 saniyede bir kontrol et)
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Spawn servisi bekleniyor... Kaplumbağa simülasyonu açık mı?")
        
        # 3. İSTEĞİ GÖNDER:
        self.istek_gonder(5.0, 5.0, 0.0, "yavru_tosbaga")

    def istek_gonder(self, x, y, theta, isim):
        # İstek mesajını oluştur
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = isim
        
        # Asenkron (bloklamadan) çağrı yap
        future = self.client.call_async(request)
        
        # Cevap gelince 'cevap_geldi' fonksiyonunu çalıştır
        future.add_done_callback(partial(self.cevap_geldi))

    def cevap_geldi(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Başarılı! Yeni kaplumbağa yaratıldı: {response.name}")
        except Exception as e:
            self.get_logger().error(f"Servis çağrısı başarısız oldu: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = KaplumbagaCagirici()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
