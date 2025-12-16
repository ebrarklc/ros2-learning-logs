#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient # Action kutuphanesi
from turtlesim.action import RotateAbsolute # Mesaj turu

class DondurBeni(Node):
    def __init__(self):
        super().__init__("dondur_beni_node")
        
        # 1. MÜŞTERİ (CLIENT) OLUŞTUR
        # Yapı: ActionClient(node, MesajTipi, 'action_ismi')
        self._action_client = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')

    def hedef_gonder(self, aci):
        # Hedef mesajını hazırla (theta)
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = aci
        
        # Server'ı bekle
        self.get_logger().info('Action Server aranıyor...')
        self._action_client.wait_for_server()
        
        # Hedefi gönder ve geri bildirimleri (feedback) dinle
        self.get_logger().info('Hedef gönderiliyor...')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.geri_bildirim_geldi) # Feedback gelince buraya git
        
        # Hedef sunucuya ulaştı mı? Cevabı bekle
        self._send_goal_future.add_done_callback(self.hedef_kabul_edildi_mi)

    def hedef_kabul_edildi_mi(self, future):
        # Sunucu "Tamam yaparım" dedi mi?
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Hedef REDDEDİLDİ :(')
            return

        self.get_logger().info('Hedef KABUL EDİLDİ, dönmeye başlıyorum...')
        
        # Sonucu bekle (İş bitince ne olacak?)
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.sonuc_geldi)

    def geri_bildirim_geldi(self, feedback_msg):
        # SÜREKLİ ÇAĞRILIR (Feedback)
        kalan_yol = feedback_msg.feedback.remaining
        self.get_logger().info(f'Dönüyorum... Kalan mesafe: {kalan_yol:.2f}')

    def sonuc_geldi(self, future):
        # TEK SEFER ÇAĞRILIR (Result)
        result = future.result().result
        self.get_logger().info(f'İŞLEM TAMAMLANDI! Toplam dönülen açı: {result.delta}')
        rclpy.shutdown() # İş bitince programı kapat

def main(args=None):
    rclpy.init(args=args)
    node = DondurBeni()
    
    # Koda "3.14 (Batı)" açısına dönmesini söyleyelim
    node.hedef_gonder(3.14) 
    
    rclpy.spin(node)

if __name__ == '__main__':
    main()
